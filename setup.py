#!/usr/bin/env python3

from StatsCore import StatsDaemonState
from distutils.core import setup

setup(name='StatsCore',
      version=StatsDaemonState.STATS_DAEMON_VERSION,
      description='Observant Stats Daemon and Client',
      author='Philip Herron',
      author_email='herron.philip@googlemail.com',
      url='https://redbrain.github.com/observant',
      packages=['StatsCore', 'StatsBoard'],
      package_data={'StatsBoard': ['www']},
      scripts=['daemon.py', 'dashboard.py']
)
