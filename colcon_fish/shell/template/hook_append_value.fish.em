# generated from colcon_fish/shell/template/hook_append_value.fish.em

@{
import os
if os.path.isabs(subdirectory):
    value = subdirectory
else:
    value = '$COLCON_CURRENT_PREFIX'
    if subdirectory:
        value += '/' + subdirectory
}@
if not contains -- "@(value)" $@(name)
    set -gx @(name) $@(name) "@(value)"
end
