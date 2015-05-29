#!/usr/bin/env bash
set -e

bower install

virtualenv env
. env/bin/activate
pip install -r requirements.txt
python setup.py build

# add karma
