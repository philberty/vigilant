#!/usr/bin/env bash
set -e

virtualenv env
. env/bin/activate
python setup.py build
python setup.py install
