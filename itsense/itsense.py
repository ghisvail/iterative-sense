# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np
from pykrylov.linop import (BlockLinearOperator, BlockDiagonalLinearOperator,
                            DiagonalOperator, IdentityOperator, LinearOperator)
from pykrylov.cg import CG
from pynfft import NFFT


__all__ = ['IterativeSenseSolver',]


class NfftOperator(object):
    """
    Wrapper class for the pynfft.NFFT object used by the iterative SENSE \
    solver.
    """
    def __init__(self, plan):
        self.plan = plan
        self.nargin = self.plan.N_total
        self.nargout = self.plan.M_total
        self.dtype = np.complex128
    def direct(self, f_hat):
        self.plan.f_hat = f_hat
        self.plan.trafo()
        return self.plan.f
    def adjoint(self, f):
        self.plan.f = f
        self.plan.adjoint()
        return self.plan.f_hat


class IterativeSenseSolver(object):
    def __init__(self, k, s, d=None, niter=10, nc=None, nk=None, N=None,
                 **kwargs):
        """
        TODO: empty docsting
        """
        self.nk = nk or np.prod(k.shape[:-1])
        self.nc = nc or s.shape[0]
        self.N = N or s.shape[1:]
        self.k = k
        self.s = s
        self.d = d
        self.niter = niter

        # precompute shared plan for each FT operations
        self._plan = NFFT(N=self.N, M=self.nk)
        self._plan.x = k

        # define linear operators for iterative SENSE algo
        nk = self.nk
        nc = self.nc        
        d = self.d.ravel() if self.d is not None else None
        s = self.s.reshape([nc, -1])
        
        if d is not None:
            D_diag = DiagonalOperator(diag=d)
        else:
            D_diag = IdentityOperator(nargin=nk)            
        blocks = [D_diag] * nc
        self._D = BlockDiagonalLinearOperator(blocks)

        diag = 1.0 / np.sqrt((s ** 2).sum(axis=0))
        diag = diag.ravel()        
        self._I = DiagonalOperator(diag=diag)

        Nfft = NfftOperator(self._plan)
        F = LinearOperator(nargin=Nfft.nargin, nargout=Nfft.nargout,
                           matvec=Nfft.direct, matvec_transp=Nfft.adjoint,
                           dtype=Nfft.dtype)
        blocks = [[F * DiagonalOperator(_s)] for _s in s]
        self._E = BlockLinearOperator(blocks)

        # solver is initialized separately, avoid long object creation time
        self.solver = None

    def __call__(self, m):
        """
        TODO: empty docstring
        """
        self.solve(m)
        return self.solution

    def initialize(self):
        """
        TODO: empty docsting
        """
        # precompute NFFT plan
        self._plan.precompute()
        # initialize CG solver
        D, E, I = (self._D, self._E, self._I)
        A = I * E.T * D * E * I
        #matvec = lambda x: A * x
        self.solver = CG(op=A, matvec_max=self.niter)        

    def solve(self, m):
        """
        TODO: empty docsting
        """
        if self.solver is None:
            raise RuntimeError("Attempted to use non-initialized solver")
        D, E, I = (self._D, self._E, self._I)        
        b = I * E.T * D * m
        self.rhs = b
        self.solver.solve(b)
        b_approx = self.solver.bestSolution
        v_approx = I * b_approx
        self.solution = v_approx
