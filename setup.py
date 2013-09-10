#!/usr/bin/env python
import sys
from setuptools import setup

if sys.version_info[0] < 3:
    import __builtin__ as builtins
else:
    import builtins

builtins.__PACKAGE_SETUP__ = True

import itsense 
VERSION = itsense.__version__

DISTNAME = 'iterative-sense'
DESCRIPTION = 'A Python implementation of the iterative SENSE solver'
LONG_DESCRIPTION = open('README.md').read()
MAINTAINER = 'Ghislain Vaillant'
MAINTAINER_EMAIL = 'ghisvail@gmail.com'
LICENSE = 'GPL'

def setup_package():
    metadata = dict(
        name=DISTNAME,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        description=DESCRIPTION,
        install_requires=['pykrylov', 'pynfft'],
        license=LICENSE,
        long_description=LONG_DESCRIPTION,
        packages=['itsense',],
        version=VERSION,)
    setup(**metadata)

if __name__ == "__main__":
    setup_package()
