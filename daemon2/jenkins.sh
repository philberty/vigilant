#!/usr/bin/env bash
set -e

./getdeps.sh
mkdir _build
BUILD_DIR=`pwd`/_build
./config/autogen.sh
./configure --prefix=$BUILD_DIR
make
make install

