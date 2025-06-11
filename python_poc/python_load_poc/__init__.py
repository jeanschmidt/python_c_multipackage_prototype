"""
Python package that loads a C function dynamically using ctypes.
"""
import os
import ctypes
import sys

# Find the library
_current_dir = os.path.dirname(os.path.abspath(__file__))

# Find the build directory path
# First try to find the library relative to the package install location
_build_path = os.path.join(_current_dir, '..', 'python_load_poc_c_extension', 'build')

# If that doesn't work, fall back to the development location
if not os.path.exists(_build_path):
    _project_root = os.path.dirname(os.path.dirname(_current_dir))
    _build_path = os.path.join(_project_root, 'python_poc', 'python_load_poc_c_extension', 'build')

if not os.path.exists(_build_path):
    raise FileNotFoundError(f"Could not find build directory at {_build_path}")

# Need to load libmessage.so which depends on libmessage-internal.so
_lib_path = os.path.join(_build_path, 'libmessage.so')

# Load the library
try:
    # Load the main library - it will automatically find the dependency in the same directory
    _lib = ctypes.CDLL(_lib_path)
    print(f"Loaded library from: {_lib_path}")
except Exception as e:
    print(f"Failed to load C library from {_lib_path}: {e}", file=sys.stderr)
    raise

print_message = _lib.print_message

# Export the function
__all__ = ['print_message']
