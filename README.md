# colcon-fish

[Fish shell](https://fishshell.com) support for [colcon](https://github.com/colcon/colcon-core).

## Quick Start

```fish
# Install
pip install colcon-fish

# Build your ROS 2 workspace
cd ~/ros2_ws && colcon build

# Source in fish
source install/setup.fish

# Run
ros2 run my_package my_node
```

## Documentation

- [Installation](https://github.com/Sunrisepeak/colcon-fish/blob/main/docs/install.md)
- [Usage](https://github.com/Sunrisepeak/colcon-fish/blob/main/docs/usage.md)
- [Design](https://github.com/Sunrisepeak/colcon-fish/blob/main/docs/design.md)

## Other

- [colcon-core](https://github.com/colcon/colcon-core) - core framework
- [colcon documentation](https://colcon.readthedocs.io) - official docs
- [colcon/colcon-core#710](https://github.com/colcon/colcon-core/issues/710) - fish support issue

## License

Apache-2.0
