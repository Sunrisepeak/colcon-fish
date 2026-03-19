# Design

## Why a separate plugin?

Fish shell is not POSIX-compatible. Existing shell extensions (bash, zsh) depend on `sh` as a "primary shell" — they source `.sh` scripts via `eval "$(python3 ... sh bash)"`. Fish cannot execute `sh` syntax, so it needs its own primary shell implementation.

## Architecture

colcon-core discovers shell extensions via the `colcon_core.shell` entry point. Each extension generates setup scripts for its shell. Extensions with `PRIORITY > 100` are "primary shells" that operate independently.

```
colcon_core.shell entry points:
  sh    (priority=200, primary)  — generates .sh scripts
  fish  (priority=200, primary)  — generates .fish scripts (this plugin)
  bash  (priority=100)           — extends sh with bash-specific features
  zsh   (priority=100)           — extends sh with zsh-specific features
```

## FishShell class

`colcon_fish/shell/fish.py` implements `ShellExtensionPoint` with:

**Format strings** — define how generated Python utilities output fish commands:

```python
FORMAT_STR_COMMENT_LINE = '# {comment}'
FORMAT_STR_SET_ENV_VAR  = 'set -gx {name} "{value}"'
FORMAT_STR_USE_ENV_VAR  = '${name}'
FORMAT_STR_INVOKE_SCRIPT = 'begin; set -lx COLCON_CURRENT_PREFIX "{prefix}"; ...; end'
```

**Methods implemented:**

| Method | Output |
|--------|--------|
| `create_prefix_script` | `local_setup.fish` + `_local_setup_util_fish.py` + `setup.fish` |
| `create_package_script` | `share/<pkg>/package.fish` |
| `create_hook_set_value` | `set -gx NAME "value"` |
| `create_hook_append_value` | fish list append or colon append |
| `create_hook_prepend_value` | fish list prepend or colon prepend |
| `generate_command_environment` | Raises `SkipExtensionException` (falls back to sh) |

## Fish list variables

Fish natively treats `PATH`, `MANPATH`, and `CDPATH` as list variables (space-separated internally), not colon-separated strings. The plugin handles this:

```fish
# For PATH, MANPATH, CDPATH — fish list syntax:
contains -- "/new/path" $PATH; or set -gx PATH "/new/path" $PATH

# For all other variables — colon-separated (same as sh):
set -gx CMAKE_PREFIX_PATH "/new/path:$CMAKE_PREFIX_PATH"
```

This matches the behavior of [ament_package's fish support](https://github.com/ament/ament_package).

## Custom prefix_util.py.em

colcon-core's `prefix_util.py.em` template generates a Python utility that reads `.dsv` files and outputs shell commands. The default template doesn't handle fish list variables, so this plugin overrides `_get_prefix_util_template_path()` to use its own version with `_FISH_LIST_VARS` support.

## generate_command_environment

This method provides the build-time environment for `colcon build` subprocesses. Since fish may not be available on all systems and the build itself doesn't need fish-specific features, this plugin raises `SkipExtensionException`, letting colcon fall back to the `sh` extension. This matches how non-primary shells (bash, zsh) behave.

## Relationship with ament_package

colcon-fish and ament_package's fish support are independent but complementary:

- **ament_package** generates per-package environment hooks and `local_setup.fish` during CMake install
- **colcon-fish** generates workspace-level entry points (`setup.fish`, `local_setup.fish`) and the Python utility that orchestrates package sourcing

colcon-fish does **not** depend on ament_package's fish support. However, when both are installed, the full environment chain works: `setup.fish` → `_local_setup_util_fish.py` → reads `.dsv` files → sources ament's `local_setup.fish` and hook scripts.

## File generation flow

```
colcon build
  │
  ├─ For each package (cmake --install):
  │    ament_cmake generates:
  │      share/<pkg>/package.dsv        (lists all hooks)
  │      share/<pkg>/local_setup.fish   (ament's per-package setup)
  │      share/<pkg>/environment/*.dsv  (AMENT_PREFIX_PATH, PATH, etc.)
  │
  └─ Post-build (colcon shell extensions):
       FishShell.create_prefix_script() generates:
         setup.fish                     (chains prefixes)
         local_setup.fish               (sources packages via Python)
         _local_setup_util_fish.py      (reads .dsv, outputs fish commands)
       FishShell.create_package_script() generates:
         share/<pkg>/package.fish       (sources .fish hooks)
       FishShell.create_hook_*() generates:
         share/<pkg>/hook/*.fish        (environment variable hooks)
```
