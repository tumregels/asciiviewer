import sys
import warnings

if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True
    # Disable deprecation warnings when frozen
    warnings.filterwarnings("ignore", category=DeprecationWarning)
