# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np
from pykrylov.linop import (BlockLinearOperator, BlockDiagonalLinearOperator,
                            DiagonalOperator, IdentityOperator, LinearOperator)
from pykrylov.cg import CG
from pynfft import NFFT


__all__ = ['IterativeSenseSolver',]


class IterativeSenseSolver(object):
    def __init__(self, k, s, w=None, niter=10, **kwargs):
        """
        TODO: empty docsting
        """
        # get geometry
        ncoils = len(s)
        ndims = s[0].ndim 
        ngrid = s[0].shape
        nknots = k.size / ndims
        k = k.reshape([nknots, ndims])
        
        # set shared plan for each ForFT and AdjFT operations
        self._plan = get_plan(nknots, ngrid)
        self._plan.precompute(k)

        # define linear operators for iterative SENSE algo
        if w is not None:
            D_block = DiagonalOperator(diag=w.ravel())
        else:
            D_block = IdentityOperator(nargin=nknots)
        blocks = [D_block] * ncoils
        D = BlockDiagonalLinearOperator(blocks=blocks)

        diag = np.sqrt(np.sum([_s ** 2 for _s in s], axis=0))       
        I = DiagonalOperator(diag=diag.ravel())

        F = LinearOperator(
                nargin=self._plan.N_total,
                nargout=self._plan.M,
                matvec=lambda u: self._plan.forward(f_hat=u),
                matvec_transp=lambda u: self._plan.adjoint(f=u).ravel(),
                dtype=np.complex128,)
        blocks = [[F * DiagonalOperator(diag=_s.ravel())] for _s in s]
        
        E = BlockLinearOperator(blocks=blocks)

        self.D = D
        self.E = E
        self.I = I
        self.m = None
        self.rhs = None
        self.shape = (ngrid, nknots*ncoils)
        self.solution = None
        self.solver = CG(op=I*E.T*D*E*I, matvec_max=niter)

    def __call__(self, m):
        """
        TODO: empty docstring
        """
        self.m = np.asarray(m).reshape(self.shape[1])
        self.execute()
        return self.solution
       
    def execute(self):
        """
        TODO: empty docsting
        """
        D, E, I, m = (self.D, self.E, self.I, self.m)
        b = I * E.T * D * m
        self.solver.solve(b)
        b_approx = self.solver.bestSolution
        v_approx = I * b_approx
        self.rhs = b.reshape(self.shape[0])
        self.solution = v_approx.reshape(self.shape[0])


def get_plan(M, N):
    f = np.empty(M, dtype=np.complex128)
    f_hat = np.empty(N, dtype=np.complex128)
    plan = NFFT(f, f_hat)
    return plan