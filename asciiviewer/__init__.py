import os
import sys
import warnings

from ._version import __version__ as __version__

if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True
    # Disable deprecation warnings when frozen
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    if sys.platform.startswith('linux'):
        # The Linux binary is built inside a conda environment (see environment.yml), and the
        # bundled libxkbcommon has that environment's path baked in as its compile-time default
        # XKB config root. On a machine without that conda env, xkbcommon can't find the keyboard
        # layout data, fails to build a keymap, and GTK segfaults the moment a key is pressed.
        # Point it at the standard system location instead.
        _xkb_config_root = '/usr/share/X11/xkb'
        if os.path.isdir(_xkb_config_root):
            os.environ.setdefault('XKB_CONFIG_ROOT', _xkb_config_root)
