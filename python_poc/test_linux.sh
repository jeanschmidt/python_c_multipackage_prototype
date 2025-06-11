#!/bin/bash

TEST_FOLDER=test_env

set -e

# Do the build and install in a virtual environment
virtualenv .venv
source .venv/bin/activate

pushd python_load_poc
pip3 install -r requirements.txt
python3 setup.py build
python3 setup.py install
popd

# Do the testing (from another directory so it wont load the local python_load_poc)
mkdir -p $TEST_FOLDER
pushd $TEST_FOLDER
python3 -c "import python_load_poc; python_load_poc.print_message()"
popd

# Cleanup
deactivate
. ./cleanup_linux.sh
