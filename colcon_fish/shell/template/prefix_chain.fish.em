# generated from colcon_fish/shell/template/prefix_chain.fish.em

# This script extends the environment with the environment of other prefix
# paths which were sourced when this file was generated as well as all packages
# contained in this prefix path.
@[if chained_prefix_path]@

# source chained prefixes
@[  for prefix in reversed(chained_prefix_path)]@
set -gx COLCON_CURRENT_PREFIX "@(prefix)"
if test -f "$COLCON_CURRENT_PREFIX/@(prefix_script_no_ext).fish"
    source "$COLCON_CURRENT_PREFIX/@(prefix_script_no_ext).fish"
end

@[  end for]@
@[end if]@

# source this prefix
set -gx COLCON_CURRENT_PREFIX (builtin realpath (dirname (status -f)))
if test -f "$COLCON_CURRENT_PREFIX/@(prefix_script_no_ext).fish"
    source "$COLCON_CURRENT_PREFIX/@(prefix_script_no_ext).fish"
end

set -e COLCON_CURRENT_PREFIX
