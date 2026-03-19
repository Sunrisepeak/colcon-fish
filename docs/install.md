# Installation

## Prerequisites

- Python 3.6+
- [colcon-core](https://github.com/colcon/colcon-core) (installed with ROS 2)
- [fish shell](https://fishshell.com) 3.0+

## Install from source

```bash
git clone https://github.com/colcon/colcon-fish.git
cd colcon-fish
pip install -e .
```

On Ubuntu with system Python, add `--break-system-packages`:

```bash
pip install -e . --break-system-packages
```

## Verify installation

```fish
python3 -c "from colcon_fish.shell.fish import FishShell; print('OK')"
```

Check that `fish` appears in the registered shell extensions:

```fish
python3 -c "
from colcon_core.shell import get_shell_extensions
for p, exts in get_shell_extensions().items():
    for name in exts:
        print(f'  {name} (priority={p})')
"
```

Expected output includes:

```
  fish (priority=200)
  sh (priority=200)
```

## Uninstall

```bash
pip uninstall colcon-fish
```
