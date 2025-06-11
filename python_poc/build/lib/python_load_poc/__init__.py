"""
Python package that loads a C function dynamically using ctypes.
"""
import os
import ctypes
import sys

# Find the library
_current_dir = os.path.dirname(os.path.abspath(__file__))

# First try to find the library relative to the package install location
_lib_path = os.path.join(_current_dir, '..', 'python_load_poc_c_extension', 'build', 'libmessage.so')

# If that doesn't work, fall back to the development location
if not os.path.exists(_lib_path):
    _project_root = os.path.dirname(os.path.dirname(_current_dir))
    _lib_path = os.path.join(_project_root, 'python_poc', 'python_load_poc_c_extension', 'build', 'libmessage.so')

# Load the library
try:
    _lib = ctypes.CDLL(_lib_path)
    print_message = _lib.print_message
    print(f"Loaded library from: {_lib_path}")
except Exception as e:
    print(f"Failed to load C library from {_lib_path}: {e}", file=sys.stderr)
    raise

# Export the function
__all__ = ['print_message']
