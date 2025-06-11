## 1. CPU-specific flags

- -DCPU_INTEL, -DCPU_AARCH64, -DCPU_POWER flags based on system processor
- Native architecture optimization: -march=native when USE_NATIVE_ARCH=ON
- OpenMP flags (when USE_OPENMP=ON): -fopenmp or MSVC equivalent
- SIMD/Vector capabilities:
- ARM: -D__NEON__ when NEON is found
- For certain ARM architectures: -mcpu=cortex-a8, -mcpu=cortex-a9
- When on Apple Silicon: -DAT_BUILD_ARM_VEC256_WITH_SLEEF
- S390X: ZVECTOR extension flags

## 2. CUDA-specific flags

- Main feature flag: -DUSE_CUDA
- Half-precision flags:
- -DCUDA_HAS_FP16=1
- -D__CUDA_NO_HALF_OPERATORS__
- -D__CUDA_NO_HALF_CONVERSIONS__
- -D__CUDA_NO_HALF2_OPERATORS__
- -D__CUDA_NO_BFLOAT16_CONVERSIONS__
- CUDA architectures set through TORCH_CUDA_ARCH_LIST environment variable
- cuDNN flags (when USE_CUDNN=ON):
- Linking against cuDNN libraries
- NVCC compiler flags:
- --expt-relaxed-constexpr
- --expt-extended-lambda
- -DCUB_WRAPPED_NAMESPACE=at_cuda_detail
- -Xfatbin -compress-all
- -Wno-deprecated-gpu-targets
- Debug flags (when DEBUG_CUDA=ON):
- -lineinfo
- -g -G (for device code debugging)
- Flash attention flags (when USE_FLASH_ATTENTION=ON)
- Memory-efficient attention flags (when USE_MEM_EFF_ATTENTION=ON)
- NCCL flags (when USE_NCCL=ON)
- NVRTC flags (when USE_NVRTC=ON)
- MAGMA flags (when USE_MAGMA=ON)
- LIBCUDACXX flags: -DLIBCUDACXX_ENABLE_SIMPLIFIED_COMPLEX_OPERATIONS

## 3. ROCm/HIP-specific flags

- Main feature flag: -DUSE_ROCM
- Architecture flags from PYTORCH_ROCM_ARCH environment variable
- HIP compiler flags:
- -D__HIP_PLATFORM_AMD__=1
- -DCUDA_HAS_FP16=1
- -DUSE_ROCM
- -D__HIP_NO_HALF_OPERATORS__=1
- -D__HIP_NO_HALF_CONVERSIONS__=1
- -DTORCH_HIP_VERSION=${TORCH_HIP_VERSION}
- -Wno-shift-count-negative
- -Wno-shift-count-overflow
- -Wno-duplicate-decl-specifier
- -DCAFFE2_USE_MIOPEN
- -DTHRUST_DEVICE_SYSTEM=THRUST_DEVICE_SYSTEM_HIP
- --offload-compress (for HIPCC)
- Windows-specific ROCm flags:
- -DROCM_ON_WINDOWS
- -fms-extensions
- ROCm version flags: -DROCM_VERSION=${ROCM_VERSION_DEV_INT}
- MIOpen flags: -DCAFFE2_USE_MIOPEN
- RCCL flags (when USE_NCCL=ON && USE_ROCM=ON)
- HIPBLASLT flags (when hipBLASLT is found): -DHIPBLASLT_VEC_EXT
- Debug flags in debug build:
- -g2
- -O0
- -fdebug-info-for-profiling
- Kernel assert flags (when USE_ROCM_KERNEL_ASSERT=ON)

## 4. XPU (Intel SYCL)-specific flags

- Main feature flag: -DUSE_XPU
- SYCL compiler version flag: -DSYCL_COMPILER_VERSION=${SYCL_COMPILER_VERSION}
- Architecture flags via XPU_ARCH_FLAGS setting
- XCCL flags (when USE_XCCL=ON)
- KINETO flags (when XPU_ENABLE_KINETO=ON)

## 5. Common backend selection flags

- Use of MKL: -DUSE_MKL=ON for Intel MKL math libraries
- Use of MKLDNN: -DUSE_MKLDNN=ON for Intel MKL-DNN
- Use of FBGEMM: -DUSE_FBGEMM for Facebook GEMM library
- Use of QNNPACK/XNNPACK: -DUSE_PYTORCH_QNNPACK, -DUSE_XNNPACK
- Vulkan support: -DUSE_VULKAN, -DUSE_VULKAN_API

## 6. Mobile-specific flags

- Mobile platform flags: -DC10_MOBILE
- iOS/Android specific options

## 7. Multi-platform optimization flags

- Flag for SLEEF VEC256 support: -DAT_BUILD_ARM_VEC256_WITH_SLEEF
- KINETO profiler flags based on backends
