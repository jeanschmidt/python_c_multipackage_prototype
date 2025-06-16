"""
Python package that loads a C function dynamically using ctypes.
"""
import os
import ctypes
import sys
import platform
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

# Determine file extensions based on platform
_is_windows = platform.system() == "Windows"
if _is_windows:
    _lib_prefix = ""
    _lib_suffix = ".dll"
else:
    _lib_prefix = "lib"
    _lib_suffix = ".so"

# First check if the alternative implementation is available
_alt_internal_lib_path = _find_library_path(
    "python_load_poc_alt", 
    f"python_load_poc_alt_c_extension/build/{_lib_prefix}message-internal{_lib_suffix}"
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
_default_internal_lib_path = os.path.join(_build_path, f'{_lib_prefix}message-internal{_lib_suffix}')
_main_lib_path = os.path.join(_build_path, f'{_lib_prefix}message{_lib_suffix}')

# Load the libraries
try:
    # Determine which implementation to use
    if _alt_internal_lib_path is not None and os.path.exists(_alt_internal_lib_path):
        internal_lib_path = _alt_internal_lib_path
        print(f"Using alternative implementation")
    else:
        internal_lib_path = _default_internal_lib_path
        print(f"Using default implementation")
    
    if _is_windows:
        # On Windows, first load the internal library to ensure it's in memory
        # This will be used by the delay-load mechanism in the main DLL
        internal_lib = ctypes.WinDLL(internal_lib_path)
        print(f"Loaded internal library from: {internal_lib_path}")
        
        # Now load the main library which will delay-load the internal library when needed
        _lib = ctypes.WinDLL(_main_lib_path)
        print(f"Loaded main library from: {_main_lib_path}")
        
        # Get the print_message function
        print_message = _lib.print_message
    else:
        # Linux/Mac use RTLD_GLOBAL to make symbols available
        ctypes.CDLL(internal_lib_path, mode=ctypes.RTLD_GLOBAL)
        print(f"Loaded internal library from: {internal_lib_path}")

        # Now load the main library - it will find symbols in the globally loaded internal library
        _lib = ctypes.CDLL(_main_lib_path)
        print(f"Loaded main library from: {_main_lib_path}")
        
        # Get the function from the library
        print_message = _lib.print_message
except Exception as e:
    print(f"Failed to load C library: {e}", file=sys.stderr)
    raise

# Export the function
__all__ = ['print_message']
