#!/bin/bash

rm -rf .venv
rm -rf test_env

pushd python_load_poc
rm -rf *.egg-info
rm -rf build
pushd python_load_poc_c_extension
make clean
popd
popd

pushd python_load_poc_alt
rm -rf *.egg-info
rm -rf build
pushd python_load_poc_alt_c_extension
make clean
popd
popd
