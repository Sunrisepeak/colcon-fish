# Usage

## Basic workflow

```fish
# 1. Source the ROS 2 base environment (if not already in fish config)
source /opt/ros/jazzy/setup.fish

# 2. Build your workspace
cd ~/ros2_ws
colcon build

# 3. Source the workspace
source install/setup.fish

# 4. Run nodes
ros2 run my_package my_node
```

## What `colcon build` generates

After `colcon build`, the following fish files appear in the install directory:

```
install/
├── setup.fish                    # Entry point — sources chained prefixes + local_setup.fish
├── local_setup.fish              # Sources all packages in this prefix (via Python utility)
├── _local_setup_util_fish.py     # Python script that reads .dsv files and outputs fish commands
└── <pkg_name>/
    └── share/<pkg_name>/
        ├── package.fish          # Per-package script — sources all hooks for this package
        └── hook/
            ├── cmake_prefix_path.fish
            ├── ros_package_path.fish
            └── pkg_config_path.fish
```

## Sourcing order

`setup.fish` does the following in order:

1. Sources chained prefix paths (e.g., `/opt/ros/jazzy/local_setup.fish`)
2. Sources `local_setup.fish` for the current workspace

`local_setup.fish` does:

1. Prepends the workspace to `COLCON_PREFIX_PATH`
2. Runs `_local_setup_util_fish.py` which reads each package's `.dsv` file
3. Evaluates the output — setting environment variables and sourcing hook scripts

## Environment variables set

| Variable | Description |
|----------|-------------|
| `COLCON_PREFIX_PATH` | List of sourced workspace prefixes |
| `AMENT_PREFIX_PATH` | Package discovery for `ros2 run` / `ros2 pkg list` |
| `CMAKE_PREFIX_PATH` | CMake `find_package()` search paths |
| `PATH` | Executable search path (if the package installs to `bin/`) |
| `PYTHONPATH` | Python module search path |
| `LD_LIBRARY_PATH` | Shared library search path |
| `PKG_CONFIG_PATH` | pkg-config search path |
| `ROS_PACKAGE_PATH` | ROS package search path |

The exact set depends on what each package's `ament_package()` registers.

## Debug with COLCON_TRACE

```fish
set -gx COLCON_TRACE 1
source install/setup.fish
```

This prints every command the setup scripts execute, useful for diagnosing environment issues.

## Add to fish config

To auto-source on every fish session, add to `~/.config/fish/config.fish`:

```fish
# ROS 2 base
if test -f /opt/ros/jazzy/setup.fish
    source /opt/ros/jazzy/setup.fish
end

# Your workspace (optional)
if test -f ~/ros2_ws/install/setup.fish
    source ~/ros2_ws/install/setup.fish
end
```

## Duplicate source protection

Sourcing `setup.fish` multiple times is safe. Environment variables are deduplicated — paths are not added twice.
