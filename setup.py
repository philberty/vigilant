#!/usr/bin/env python3

from distutils.core import setup

setup(name='StatsCore',
      version='0.1',
      description='Observant Stats Daemon and Client',
      author='Philip Herron',
      author_email='herron.philip@googlemail.com',
      url='https://redbrain.github.com/observant',
      packages=['StatsCore', 'StatsBoard'],
      package_data={'StatsBoard': ['www']},
      scripts=['daemon.py', 'dashboard.py']
)
