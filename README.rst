colcon-fish
===========

An extension for `colcon-core <https://github.com/colcon/colcon-core>`_ that adds `fish shell <https://fishshell.com>`_ support.

After installation, ``colcon build`` automatically generates ``.fish`` setup scripts alongside the existing ``.sh`` / ``.bash`` / ``.zsh`` scripts.

Quick start
-----------

.. code-block:: fish

   # Install
   pip install -e /path/to/colcon-fish

   # Build your workspace
   cd ~/ros2_ws
   colcon build

   # Source in fish
   source install/setup.fish

   # Use
   ros2 run my_package my_node

See ``docs/`` for full documentation.
