import sys
import pkgconfig

from distutils.core import setup
from distutils.extension import Extension

from Cython.Build import cythonize
from pip.req import parse_requirements

if pkgconfig.exists ('watchy') is False:
    print >> sys.stderr, "Make sure pkg-config watchy --cflags --libs works."
    sys.exit (1)
watchy = pkgconfig.parse ('watchy')
extensions = [
    Extension ('pywatchy', ['bindings/python/pywatchy.pyx'],
               include_dirs = list (watchy ['include_dirs']),
               libraries = list (watchy ['libraries']),
               library_dirs = list (watchy ['library_dirs']),
               runtime_library_dirs = list (watchy ['library_dirs']))
]
install_reqs = parse_requirements ('./requirements.txt')
reqs = [str(ir.req) for ir in install_reqs]
setup (
    name = "Watchy",
    version = "0.2",
    url = 'https://github.com/redbrain/watchy',
    author = 'Philip Herron',
    author_email = 'redbrain@gcc.gnu.org',
    license = "MIT",
    description = 'A stats agregation daemon over UDP',
    platforms = ('Any',),
    #FIXME: requires = reqs,
    keywords = ('stats', 'web', 'monitoring', 'udp'),
    ext_modules = cythonize (extensions),
    packages = ['WatchyServer', 'WatchyServer.backends'],
    scripts = ['watchy.py'],
    package_data = {'WatchyServer': ['templates/*',
                                     'static/css/*',
                                     'static/js/*']},
    data_files=[('/etc/watchy/', ['etc/watchy/example-watchy.cfg'])],
)
