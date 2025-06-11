#!/bin/bash

TEST_FOLDER=test_env

set -e

# Setup the environment
virtualenv .venv
source .venv/bin/activate

# Build and install the python_load_poc package
pushd python_load_poc
pip3 install -r requirements.txt
python3 setup.py build
python3 setup.py install
popd

# Do the testing (from another directory so it wont load the local python_load_poc)
mkdir -p $TEST_FOLDER
pushd $TEST_FOLDER
echo ""
echo "########################################################################################"
python3 -c "import python_load_poc; python_load_poc.print_message()"
echo "########################################################################################"
echo ""
popd

# Install the alternative package
pushd python_load_poc_alt
pip3 install -r requirements.txt
python3 setup.py build
python3 setup.py install
popd

# Do the testing for the alternative package
mkdir -p $TEST_FOLDER
pushd $TEST_FOLDER
echo ""
echo "########################################################################################"
python3 -c "import python_load_poc; python_load_poc.print_message()"
echo "########################################################################################"
echo ""
popd

# Cleanup
deactivate
. ./cleanup_linux.sh
