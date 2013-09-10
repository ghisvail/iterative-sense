"""
itsense: a Python implementation of the iterative SENSE solver
"""

__version__ = '0.1.0'

try:
    # This variable is injected in the __builtins__ by the build
    # process.
    __PACKAGE_SETUP__
except NameError:
    __PACKAGE_SETUP__ = False

if not __PACKAGE_SETUP__:
    from .itsense import IterativeSenseSolver
    __all__ = ['IterativeSenseSolver',]
