#!/usr/bin/env bash
set -e

virtualenv env
. env/bin/activate
pip install -r requirements.txt
python setup.py build
python setup.py install
