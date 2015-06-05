#!/usr/bin/env bash
set -e

rm -rf _deps
mkdir _deps
pushd _deps

rm -rf _builds
mkdir _builds

pushd _builds
BUILD_DIR=`pwd`
popd

wget https://github.com/HardySimpson/zlog/archive/latest-stable.tar.gz
tar zxvf latest-stable.tar.gz
pushd zlog-latest-stable
make PREFIX=$BUILD_DIR
make install PREFIX=$BUILD_DIR
popd

wget ftp://ftp.mirrorservice.org/pub/i-scream/libstatgrab/libstatgrab-0.91.tar.gz
tar zxvf libstatgrab-0.91.tar.gz
pushd libstatgrab-0.91
./configure --prefix=$BUILD_DIR
make
make install
popd

wget https://github.com/google/protobuf/releases/download/v2.6.1/protobuf-2.6.1.tar.gz
tar zxvf protobuf-2.6.1.tar.gz
pushd protobuf-2.6.1
./configure --prefix=$BUILD_DIR
make
make install
popd

wget https://sourceforge.net/projects/levent/files/libevent/libevent-2.0/libevent-2.0.22-stable.tar.gz
tar zxvf libevent-2.0.22-stable.tar.gz
pushd libevent-2.0.22-stable
./configure --prefix=$BUILD_DIR
make
make install
popd

wget http://www.digip.org/jansson/releases/jansson-2.7.tar.gz
tar zxvf jansson-2.7.tar.gz
pushd jansson-2.7
./configure --prefix=$BUILD_DIR
make
make install
popd

popd
