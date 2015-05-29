#!/usr/bin/env bash
set -e

bower install
virtualenv env
. env/bin/activate
python setup.py build

# add karma
