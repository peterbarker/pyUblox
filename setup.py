from __future__ import absolute_import, print_function
#from setuptools.command.build_py import build_py
# Work around mbcs bug in distutils.
# http://bugs.python.org/issue10945
#import codecs
#try:
#    codecs.lookup('mbcs')
#except LookupError:
#    ascii = codecs.lookup('ascii')
#    func = lambda name, enc=ascii: {True: enc}.get(name=='mbcs')
#    codecs.register(func)

import setuptools
#from setuptools import setup, Extension
#import glob, os, shutil, fnmatch, platform, sys

version = '0.1.0'


setuptools.setup(
    name = 'pyublox',
    version = version,
    description = 'Python UBlox tools',
    long_description = ('Libraries and utilities for working with uBlox GPS units'),
    url = 'https://github.com/tridge/pyUblox/',
    classifiers=['Development Status :: 4 - Beta',
                 'Environment :: Console',
                 'Intended Audience :: Science/Research',
                 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)', # TBC with tridge!  No license exists at
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.5',
                 'Topic :: Scientific/Engineering'
    ],
    license='GPLv3',
    packages = [ 'ublox',
                 'ublox.mga',
    ],
    install_requires=[
        'future',
    ],
    entry_points = {
        "console_scripts": [
        ],
    },
)
