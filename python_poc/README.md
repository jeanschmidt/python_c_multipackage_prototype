# Python Dynamic library load prototype

The goal of this prototype is to prove that we can build a package that dinamicaly loads .so/.dll dependencies based on available packages installed in the system.

## Approach

Use `ctypes.CDLL` with flag `ctypes.RTLD_GLOBAL` to dynamically load dependencies on Linux/MacOS.

Use Delay-Load for Windows and just load libraries with LoadLibrary on Windows ahead of the dynamic loading. The side-effect is a small performance impact.

The goal is to have a main `torch` package with depends on `torch-cpu` package by default, so you can just run:

```
pip3 install torch
```

And have torch CPU available. But if you want to have now CUDA capability you should be able to install:

```
pip3 install torch-cuda
```

And the already-existing library in the system should now use the newer binaries provided in `torch-cuda`.

The goal is to leverage also the approach provided by Eli to use what he called (torchpick)[https://github.com/seemethere/torchpick]


## Status

Working on Linux, MacOS and Windows
