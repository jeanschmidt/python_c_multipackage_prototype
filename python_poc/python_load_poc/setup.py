from setuptools import setup
import os
import subprocess
import sys
import platform
from setuptools.command.install import install
from setuptools.command.develop import develop

class CompileC(install):
    def run(self):
        # Navigate to the python_load_poc_c_extension directory
        c_ext_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'python_load_poc_c_extension')
        
        # Run the appropriate build command based on the platform
        if platform.system() == "Windows":
            # On Windows, use MSVC compiler
            # First check if Visual Studio tools are in the path
            try:
                # For Windows, we use nmake with the Windows-specific makefile
                subprocess.check_call(['nmake', '/f', 'Makefile.win'], cwd=c_ext_dir, shell=True)
            except (subprocess.SubprocessError, FileNotFoundError) as e:
                print(f"Warning: nmake command failed: {e}. Trying alternative approaches...")
                # Try with direct path to nmake if available
                try:
                    # Look for Visual Studio installation
                    vs_paths = [
                        r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.29.30133\bin\Hostx64\x64",
                        r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx64\x64",
                        # Add more potential paths as needed
                    ]
                    for vs_path in vs_paths:
                        nmake_path = os.path.join(vs_path, "nmake.exe")
                        if os.path.exists(nmake_path):
                            print(f"Found nmake at {nmake_path}")
                            subprocess.check_call([nmake_path, '/f', 'Makefile.win'], cwd=c_ext_dir, shell=True)
                            break
                    else:
                        # Fallback to make if nmake is not available (e.g., using MinGW)
                        print("Falling back to MinGW make if available...")
                        subprocess.check_call(['make', '-f', 'Makefile'], cwd=c_ext_dir, shell=True)
                except Exception as e:
                    print(f"Error: Failed to build C extension: {e}")
                    print("Please ensure you have Visual Studio Build Tools or MinGW installed.")
        else:
            # For Linux/macOS use standard make
            subprocess.check_call(['make', '-C', c_ext_dir])
        
        # Continue with the regular installation
        super().run()

class CompileCDev(develop):
    def run(self):
        # Navigate to the python_load_poc_c_extension directory
        c_ext_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'python_load_poc_c_extension')
        
        # Run the appropriate build command based on the platform
        if platform.system() == "Windows":
            # On Windows, use MSVC compiler
            # First check if Visual Studio tools are in the path
            try:
                # For Windows, we use nmake with the Windows-specific makefile
                subprocess.check_call(['nmake', '/f', 'Makefile.win'], cwd=c_ext_dir, shell=True)
            except (subprocess.SubprocessError, FileNotFoundError) as e:
                print(f"Warning: nmake command failed: {e}. Trying alternative approaches...")
                # Try with direct path to nmake if available
                try:
                    # Look for Visual Studio installation
                    vs_paths = [
                        r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.29.30133\bin\Hostx64\x64",
                        r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx64\x64",
                        # Add more potential paths as needed
                    ]
                    for vs_path in vs_paths:
                        nmake_path = os.path.join(vs_path, "nmake.exe")
                        if os.path.exists(nmake_path):
                            print(f"Found nmake at {nmake_path}")
                            subprocess.check_call([nmake_path, '/f', 'Makefile.win'], cwd=c_ext_dir, shell=True)
                            break
                    else:
                        # Fallback to make if nmake is not available (e.g., using MinGW)
                        print("Falling back to MinGW make if available...")
                        subprocess.check_call(['make', '-f', 'Makefile'], cwd=c_ext_dir, shell=True)
                except Exception as e:
                    print(f"Error: Failed to build C extension: {e}")
                    print("Please ensure you have Visual Studio Build Tools or MinGW installed.")
        else:
            # For Linux/macOS use standard make
            subprocess.check_call(['make', '-C', c_ext_dir])
        
        # Continue with the regular development installation
        super().run()

setup(
    name="python_load_poc",
    version="0.1",
    packages=["python_load_poc"],
    package_data={
        "python_load_poc": ["../python_load_poc_c_extension/build/*"],
    },
    include_package_data=True,
    cmdclass={
        'install': CompileC,
        'develop': CompileCDev,
    },
)