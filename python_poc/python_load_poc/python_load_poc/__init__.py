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

# Define the library paths
_internal_lib_path = os.path.join(_build_path, 'libmessage-internal.so')
_main_lib_path = os.path.join(_build_path, 'libmessage.so')

# Load the libraries
try:
    # First load the internal library with RTLD_GLOBAL flag to make its symbols available
    ctypes.CDLL(_internal_lib_path, mode=ctypes.RTLD_GLOBAL)
    print(f"Loaded internal library from: {_internal_lib_path}")

    # Now load the main library - it will find symbols in the globally loaded internal library
    _lib = ctypes.CDLL(_main_lib_path)
    print(f"Loaded main library from: {_main_lib_path}")
except Exception as e:
    print(f"Failed to load C library: {e}", file=sys.stderr)
    raise

print_message = _lib.print_message

# Export the function
__all__ = ['print_message']
