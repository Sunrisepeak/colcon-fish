# generated from colcon_fish/shell/template/prefix.fish.em

# This script extends the environment with all packages contained in this
# prefix path.

# Determine prefix from this script's location
# Note: set -l must be declared before the if block for proper fish scoping
set -l _colcon_prefix_fish_COLCON_CURRENT_PREFIX
if test -n "$COLCON_CURRENT_PREFIX"
    set _colcon_prefix_fish_COLCON_CURRENT_PREFIX "$COLCON_CURRENT_PREFIX"
else
    set _colcon_prefix_fish_COLCON_CURRENT_PREFIX (builtin realpath (dirname (status -f)))
end

# prepend COLCON_PREFIX_PATH (dedup)
if not contains -- "$_colcon_prefix_fish_COLCON_CURRENT_PREFIX" $COLCON_PREFIX_PATH
    set -gx COLCON_PREFIX_PATH "$_colcon_prefix_fish_COLCON_CURRENT_PREFIX" $COLCON_PREFIX_PATH
end

# check environment variable for custom Python executable
set -l _colcon_python_executable "@(python_executable)"
if test -n "$COLCON_PYTHON_EXECUTABLE"
    if not test -f "$COLCON_PYTHON_EXECUTABLE"
        echo "error: COLCON_PYTHON_EXECUTABLE '$COLCON_PYTHON_EXECUTABLE' doesn't exist"
        return 1
    end
    set _colcon_python_executable "$COLCON_PYTHON_EXECUTABLE"
else
    # if it doesn't exist try a fall back
    if not test -f "$_colcon_python_executable"
        if not command -v python3 > /dev/null 2>&1
            echo "error: unable to find python3 executable"
            return 1
        end
        set _colcon_python_executable (python3 -c "import sys; print(sys.executable)")
    end
end

# get all commands in topological order and source them
set -l _colcon_ordered_commands (command "$_colcon_python_executable" \
    "$_colcon_prefix_fish_COLCON_CURRENT_PREFIX/_local_setup_util_fish.py" fish@
@[if merge_install]@
 --merged-install@
@[end if]@
)

if test -n "$COLCON_TRACE"
    echo "# Execute generated script:"
    echo "# <<<"
    for _line in $_colcon_ordered_commands
        echo "$_line"
    end
    echo "# >>>"
end

for _line in $_colcon_ordered_commands
    eval "$_line"
end
