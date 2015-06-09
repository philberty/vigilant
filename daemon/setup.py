#!/usr/bin/env python3

from distutils.core import setup

setup(name='vigilant-daemon',
      version='0.4',
      description='Data aggregation daemon',
      author='Philip Herron',
      author_email='herron.philip@googlemail.com',
      packages=['Daemon'],
      scripts=['daemon.py']
)
