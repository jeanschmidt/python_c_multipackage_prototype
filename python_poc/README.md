# Python Dynamic library load prototype

The goal of this prototype is to prove that we can build a package that dinamicaly loads .so/.dll dependencies based on available packages installed in the system.

## Approach

Use `ctypes.CDLL` with flag `ctypes.RTLD_GLOBAL` to dynamically load dependencies.

## Status

Currently this approach is proven to Linux, next steps would be to validate them in Windows and MacOS systems.
