#!/bin/bash

rm -rf test_env
rm -rf .venv
rm -rf *.egg-info
rm -rf build
pushd python_load_poc_c_extension
make clean
popd
