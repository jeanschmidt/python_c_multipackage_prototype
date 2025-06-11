from setuptools import setup
import os
import subprocess
from setuptools.command.install import install
from setuptools.command.develop import develop

class CompileC(install):
    def run(self):
        # Navigate to the python_load_poc_c_extension directory and run make
        c_ext_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'python_load_poc_c_extension')
        subprocess.check_call(['make', '-C', c_ext_dir])
        
        # Continue with the regular installation
        super().run()

class CompileCDev(develop):
    def run(self):
        # Navigate to the python_load_poc_c_extension directory and run make
        c_ext_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'python_load_poc_c_extension')
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