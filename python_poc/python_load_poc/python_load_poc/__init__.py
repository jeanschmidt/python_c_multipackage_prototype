"""
Python package that loads a C function dynamically using ctypes.
"""
import os
import ctypes
import sys
import importlib.util
import importlib.metadata

def _find_library_path(package_name, relative_path):
    """Attempt to find a library in an installed package"""
    try:
        # Check if the package is installed
        if importlib.util.find_spec(package_name) is not None:
            package_path = os.path.dirname(importlib.util.find_spec(package_name).origin)
            lib_path = os.path.join(os.path.dirname(package_path), relative_path)
            if os.path.exists(lib_path):
                return lib_path
    except (ImportError, AttributeError):
        pass
    return None

# Find the library
_current_dir = os.path.dirname(os.path.abspath(__file__))

# First check if the alternative implementation is available
_alt_internal_lib_path = _find_library_path(
    "python_load_poc_alt", 
    "python_load_poc_alt_c_extension/build/libmessage-internal.so"
)

# Define paths for our default libraries
# First try to find the library relative to the package install location
_build_path = os.path.join(_current_dir, '..', 'python_load_poc_c_extension', 'build')

# If that doesn't work, fall back to the development location
if not os.path.exists(_build_path):
    _project_root = os.path.dirname(os.path.dirname(_current_dir))
    _build_path = os.path.join(_project_root, 'python_poc', 'python_load_poc', 'python_load_poc_c_extension', 'build')

if not os.path.exists(_build_path) and _alt_internal_lib_path is None:
    raise FileNotFoundError(f"Could not find build directory at {_build_path}")

# Define the library paths
_default_internal_lib_path = os.path.join(_build_path, 'libmessage-internal.so')
_main_lib_path = os.path.join(_build_path, 'libmessage.so')

# Load the libraries
try:
    # First load the internal library with RTLD_GLOBAL flag to make its symbols available
    # Prefer the alternative implementation if available
    if _alt_internal_lib_path is not None and os.path.exists(_alt_internal_lib_path):
        internal_lib_path = _alt_internal_lib_path
        print(f"Using alternative implementation")
    else:
        internal_lib_path = _default_internal_lib_path
        print(f"Using default implementation")
        
    ctypes.CDLL(internal_lib_path, mode=ctypes.RTLD_GLOBAL)
    print(f"Loaded internal library from: {internal_lib_path}")

    # Now load the main library - it will find symbols in the globally loaded internal library
    _lib = ctypes.CDLL(_main_lib_path)
    print(f"Loaded main library from: {_main_lib_path}")
except Exception as e:
    print(f"Failed to load C library: {e}", file=sys.stderr)
    raise

print_message = _lib.print_message

# Export the function
__all__ = ['print_message']
