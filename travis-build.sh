#!/bin/bash
set -e -x
_INSTALL=`pwd`/_binstall
autoreconf --force --install
./configure CC=$CC CFLAGS="-g -O2 -Wall -Werror" --prefix=$_INSTALL
make
make install
export PKG_CONFIG_PATH=$_INSTALL/lib/pkgconfig
python setup.py build
