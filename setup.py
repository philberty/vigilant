#!/usr/bin/env python
from distutils.core import setup

setup (
    name = "Watchy",
    version = "0.1",
    url = 'https://github.com/redbrain/watchy',
    author = 'Philip Herron',
    author_email = 'redbrain@gcc.gnu.org',
    license = "MIT",
    description = 'A stats agregation daemon over UDP',
    packages = ['WatchyServer'],
    scripts = ['watchy.py'],
    package_dir = {'WatchyServer': 'WatchyServer'},
    package_data = {'WatchyServer': ['templates/*',
                                     'static/css/*',
                                     'static/js/*']},
    data_files=[('/etc/watchy/', ['etc/watchy/example-watchy.cfg',
                                  'etc/watchy/watchy.cfg.tmpl'])],
)
