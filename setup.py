#!/usr/bin/env python
from setuptools import setup

package_name = 'itsense'

import imp
ver_file, ver_pathname, ver_description = imp.find_module(
            '_version', [package_name])
try:
    _version = imp.load_module('version', ver_file, ver_pathname,
            ver_description)
finally:
    ver_file.close()

version = _version.version

DISTNAME = 'iterative-sense'
DESCRIPTION = 'A Python implementation of the iterative SENSE solver'
LONG_DESCRIPTION = open('README.md').read()
MAINTAINER = 'Ghislain Vaillant'
MAINTAINER_EMAIL = 'ghisvail@gmail.com'
LICENSE = 'GPL'
URL = 'https://github.com/ghisvail/iterative-sense'

classifiers = [
    'Programming Language :: Python',
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Operating System :: POSIX :: Linux',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Mathematics',
    'Topic :: Multimedia :: Sound/Audio :: Analysis',
]

def setup_package():
    metadata = dict(
        name=DISTNAME,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        description=DESCRIPTION,
        install_requires=[
            "pykrylov >= 0.1.1",
            "pynfft > 1.0",],
        license=LICENSE,
        long_description=LONG_DESCRIPTION,
        url=URL,
        classifiers=classifiers,
        packages=[package_name],
        version=version,)
    setup(**metadata)

if __name__ == "__main__":
    setup_package()
