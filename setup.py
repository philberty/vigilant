#!/usr/bin/env python
from distutils.core import setup

setup (
    name = "Watchy",
    version = "0.1",
    url = 'https://github.com/redbrain/watchy',
    author = 'Philip Herron',
    author_email = 'redbrain@gcc.gnu.org',
    description = 'A stats agregation daemon over UDP',
    license = "MIT",
    packages = ['pywatchyd'],
    scripts = ['watchyd.py'],
)
