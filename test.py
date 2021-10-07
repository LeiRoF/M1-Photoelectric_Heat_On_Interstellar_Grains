import matplotlib.pyplot as plt
from numpy import exp,pi
import distrib

def starLight(v):
    h = 6.63e-34 # Planck constant
    c = 299_792_458.0 # speed of light
    k = 1.38e-23 # Boltzmann constant
    T = 5_778 # temperature at the surface of the start (5000 for the sun)
    return (8*pi*v**3*h) / (c**3 * (exp((h*v)/(k*T)) - 1 ))

def starLight2(v):
    h = 6.63e-34 # Planck constant
    c = 299_792_458.0 # speed of light
    k = 1.38e-23 # Boltzmann constant
    T = 5_778 # temperature at the surface of the start (5000 for the sun)
    return (2 * h * v**3) / (c**2 * ( exp(h*v/(k*T)) - 1 ))

plt.subplot(121)
x, fx = distrib.plot(starLight,0,10000,1)
plt.plot(x,fx)
plt.subplot(122)
x, fx = distrib.plot(starLight2,0,10000,1)
plt.plot(x,fx)
plt.show()