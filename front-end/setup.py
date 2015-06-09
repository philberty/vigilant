#!/usr/bin/env python3

from distutils.core import setup

setup(name='vigilant-www',
      version='0.4',
      description='Front-end webapp to vigilant',
      author='Philip Herron',
      author_email='herron.philip@googlemail.com',
      url='https://.github.com/vigilantlabs',
      packages=['Dashboard'],
      package_data={'Dashboard': ['www']},
      scripts=['dashboard.py']
)
