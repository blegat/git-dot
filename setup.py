#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from setuptools import setup
from __version__ import version

with open('README.rst') as file:
  long_description = file.read()

setup(name='smartcp',
  version=version,
  description='Convert Git History to a Dot File',
  author='Benoît Legat',
  author_email='benoit.legat@gmail.com',
  url='http://www.github.com/blegat/git-dot',
  long_description = long_description,
  license = 'GPLv3+',
  install_requires = [
    'PyYAML',
    ],
  py_modules=['git-dot', '__version__'],
  entry_points=dict(console_scripts=['git-dot=git-dot:main',
    'git-dot-%s=git-dot:main' % sys.version[:3]]),
  classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Topic :: Utilities',
    ],
)
