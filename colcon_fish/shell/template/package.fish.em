# generated from colcon_fish/shell/template/package.fish.em

# This script extends the environment for this package.

set -l _colcon_package_fish_COLCON_CURRENT_PREFIX
if test -n "$COLCON_CURRENT_PREFIX"
    set _colcon_package_fish_COLCON_CURRENT_PREFIX "$COLCON_CURRENT_PREFIX"
else
    set _colcon_package_fish_COLCON_CURRENT_PREFIX \
        (builtin realpath (dirname (status -f))/../..)
end
@[if hooks]@

set -gx COLCON_CURRENT_PREFIX "$_colcon_package_fish_COLCON_CURRENT_PREFIX"

# source fish hooks
@[  for hook in hooks]@
if test -f "$COLCON_CURRENT_PREFIX/@(hook[0])"
    if test -n "$COLCON_TRACE"
        echo "# source \"$COLCON_CURRENT_PREFIX/@(hook[0])\""
    end
    source "$COLCON_CURRENT_PREFIX/@(hook[0])"@
@[    for hook_arg in hook[1]]@
 @(hook_arg)@
@[    end for]

end
@[  end for]@

set -e COLCON_CURRENT_PREFIX
@[end if]@
