# Copyright 2024 Speak
# Licensed under the Apache License, Version 2.0

from pathlib import Path
import sys

from colcon_core.plugin_system import satisfies_version
from colcon_core.plugin_system import SkipExtensionException
from colcon_core.prefix_path import get_chained_prefix_path
from colcon_core.shell import logger
from colcon_core.shell import ShellExtensionPoint
from colcon_core.shell.template import expand_template


class FishShell(ShellExtensionPoint):
    """Generate `.fish` scripts to extend the environment."""

    # primary shell - fish cannot reuse sh
    PRIORITY = 200

    FORMAT_STR_COMMENT_LINE = '# {comment}'
    FORMAT_STR_SET_ENV_VAR = 'set -gx {name} "{value}"'
    FORMAT_STR_USE_ENV_VAR = '${name}'
    FORMAT_STR_INVOKE_SCRIPT = \
        'begin; set -lx COLCON_CURRENT_PREFIX "{prefix}"; ' \
        'if test -f "{script_path}"; ' \
        'if test -n "$COLCON_TRACE"; ' \
        'echo "# source \\"{script_path}\\""; end; ' \
        'source "{script_path}"; ' \
        'else; echo "not found: \\"{script_path}\\"" 1>&2; end; end'
    FORMAT_STR_REMOVE_LEADING_SEPARATOR = \
        'set -gx {name} (string replace --regex "^:" "" -- "${name}")'
    FORMAT_STR_REMOVE_TRAILING_SEPARATOR = \
        'set -gx {name} (string replace --regex ":\\$" "" -- "${name}")'

    def __init__(self):  # noqa: D107
        super().__init__()
        satisfies_version(ShellExtensionPoint.EXTENSION_POINT_VERSION, '^2.2')
        if sys.platform == 'win32':
            raise SkipExtensionException('Not used on Windows systems')

    def create_prefix_script(self, prefix_path, merge_install):  # noqa: D102
        prefix_env_path = prefix_path / 'local_setup.fish'
        logger.info("Creating prefix script '%s'" % prefix_env_path)
        expand_template(
            Path(__file__).parent / 'template' / 'prefix.fish.em',
            prefix_env_path,
            {
                'prefix_path': prefix_path,
                'python_executable': sys.executable,
                'merge_install': merge_install,
            })

        prefix_util_path = prefix_path / '_local_setup_util_fish.py'
        logger.info("Creating prefix util module '%s'" % prefix_util_path)
        expand_template(
            self._get_prefix_util_template_path(),
            prefix_util_path, {'shell_extension': self})

        prefix_chain_env_path = prefix_path / 'setup.fish'
        logger.info(
            "Creating prefix chain script '%s'" % prefix_chain_env_path)
        expand_template(
            Path(__file__).parent / 'template' / 'prefix_chain.fish.em',
            prefix_chain_env_path,
            {
                'prefix_path': prefix_path,
                'chained_prefix_path': get_chained_prefix_path(
                    skip=prefix_path),
                'prefix_script_no_ext': 'local_setup',
            })

        return [
            prefix_env_path,
            prefix_util_path,
            prefix_chain_env_path,
        ]

    def _get_prefix_util_template_path(self):
        """Get the path of the fish-specific prefix_util.py.em template."""
        return Path(__file__).parent / 'template' / 'prefix_util.py.em'

    def create_package_script(  # noqa: D102
        self, prefix_path, pkg_name, hooks
    ):
        pkg_env_path = prefix_path / 'share' / pkg_name / 'package.fish'
        logger.info("Creating package script '%s'" % pkg_env_path)
        expand_template(
            Path(__file__).parent / 'template' / 'package.fish.em',
            pkg_env_path,
            {
                'prefix_path': prefix_path,
                'hooks': list(filter(
                    lambda hook: str(hook[0]).endswith('.fish'), hooks)),
            })
        return [pkg_env_path]

    def create_hook_set_value(  # noqa: D102
        self, env_hook_name, prefix_path, pkg_name, name, value,
    ):
        hook_path = prefix_path / 'share' / pkg_name / 'hook' / \
            ('%s.fish' % env_hook_name)
        logger.info("Creating environment hook '%s'" % hook_path)
        if value == '':
            value = '$COLCON_CURRENT_PREFIX'
        expand_template(
            Path(__file__).parent / 'template' / 'hook_set_value.fish.em',
            hook_path, {'name': name, 'value': value})
        return hook_path

    def create_hook_append_value(  # noqa: D102
        self, env_hook_name, prefix_path, pkg_name, name, subdirectory,
    ):
        hook_path = prefix_path / 'share' / pkg_name / 'hook' / \
            ('%s.fish' % env_hook_name)
        logger.info("Creating environment hook '%s'" % hook_path)
        expand_template(
            Path(__file__).parent / 'template' / 'hook_append_value.fish.em',
            hook_path,
            {
                'name': name,
                'subdirectory': subdirectory,
            })
        return hook_path

    def create_hook_prepend_value(  # noqa: D102
        self, env_hook_name, prefix_path, pkg_name, name, subdirectory,
    ):
        hook_path = prefix_path / 'share' / pkg_name / 'hook' / \
            ('%s.fish' % env_hook_name)
        logger.info("Creating environment hook '%s'" % hook_path)
        expand_template(
            Path(__file__).parent / 'template' / 'hook_prepend_value.fish.em',
            hook_path,
            {
                'name': name,
                'subdirectory': subdirectory,
            })
        return hook_path

    async def generate_command_environment(  # noqa: D102
        self, task_name, build_base, dependencies,
    ):
        raise SkipExtensionException(
            'fish shell does not support generating command environments')
