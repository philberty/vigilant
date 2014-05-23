import sys
import pkgconfig
from distutils.core import setup
from Cython.Build import cythonize

if pkgconfig.exists ('watchy') is False:
    print >> sys.stderr, "Make sure pkg-config watchy --cflags --libs works."
    sys.exit (1)
watchy = pkgconfig.parse ('watchy')

setup (
    name = "Watchy",
    version = "0.1",
    url = 'https://github.com/redbrain/watchy',
    author = 'Philip Herron',
    author_email = 'redbrain@gcc.gnu.org',
    license = "MIT",
    description = 'A stats agregation daemon over UDP',
    ext_modules = cythonize ('pywatchy', ['bindings/python/watchy.pyx'],
                             include_dirs = watchy ['include_dirs'],
                             libraries = watchy ['libraries'],
                             library_dirs = watchy ['library_dirs'])
    packages = ['WatchyServer'],
    scripts = ['watchy.py'],
    package_dir = {'WatchyServer': 'WatchyServer'},
    package_data = {'WatchyServer': ['templates/*',
                                     'static/css/*',
                                     'static/js/*']},
    data_files=[('/etc/watchy/', ['etc/watchy/example-watchy.cfg',
                                  'etc/watchy/watchy.cfg.tmpl'])],
)
