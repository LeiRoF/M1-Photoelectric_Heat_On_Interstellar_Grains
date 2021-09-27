#!/usr/bin/python

from numpy import *
from matplotlib.pylab import *
import numpy as np


def addGRF(cube, sigma_dens, Adens, beta, Npad=0, Kmin=0, beta_in=0, smooth=None, fixedseed=False):

   dims = shape(cube)
   nAxes = len(dims)   # number of axes
   Cubedims = zeros(nAxes, int32)
   for i in range(nAxes):
      Cubedims[i] = dims[i] + Npad

   centre = (Cubedims-1)/2.0
   Coords = indices(Cubedims, np.float64)#, complex)
   for i in range(nAxes): Coords[i] -= centre[i]
   Kradius2 =  sum(Coords**2,axis=0)

   FourierCube = np.random.seed()   # necessary to have different random number in parallel threads (if forked at the same time, they get the same seed unless np.random.seed() is called)
   if fixedseed: FourierCube = np.random.seed(1)
   FourierCube  = np.asarray(np.random.normal(size=(Cubedims),scale=1/Kradius2**(beta/2)), complex)

   if Kmin>0:
      m_in = nonzero(Kradius2<Kmin**2)
      FourierCube[m_in] = np.asarray( Kmin**(-beta*0.5) / Kmin**(beta_in*0.5) \
                           * np.random.normal(size=(np.shape(m_in[0])),scale=1/Kradius2[m_in]**(beta/2)), complex )

   FourierCube[nonzero(FourierCube!=FourierCube)] = 0.

   Phase = ones(Cubedims, complex)
   Phase = uniform(size=Cubedims)*2*pi*1j
   Phase *= exp(Phase)
   FourierCube *= Phase

   # Multiply by a smoothing Gaussian
   if (smooth):
      Ksmooth = float(dims[0])/smooth
      FourierCube *= exp(-(Kradius)**2/(2*Ksmooth**2))

   # Compute the density cube by inverse Fourier transform the Fourier cube
   RealCube = fftn(ifftshift(FourierCube))

   if Npad>0:
      Density = ones(dims, float32)
      Indices = []
      for i in range(nAxes):
         Indices.append(slice(Npad/2,Cubedims[i]-Npad/2-(Npad%2)))
      Indices = tuple(Indices)
      Density = exp( sigma_dens*abs(RealCube[Indices]) )
   else:
      Density = exp( sigma_dens*abs(RealCube) )

   Density /= mean(Density.flatten())

   return Density * Adens



