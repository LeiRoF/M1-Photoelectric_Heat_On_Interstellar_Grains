import distrib
import matplotlib.pyplot as plt
import numpy as np

T = 5*5_778 # 5 times our sun temperature
h = 6.626e-34 # Planck constant
c = 3e+8 # speed of light
k = 1.38e-23 # Boltzmann constant

def radiation(wav):
    global T
    global h
    global c
    global k
    a = 2.0*h*c**2
    b = h*c/(wav*k*T)
    intensity = a/ ( (wav**5) * (np.exp(b) - 1.0) )
    return intensity

def getPhotonEnergy(verbose = False):
    wavelenght_min = 1 # in nanometer
    wavelenght_max = 1000 # in nanometer
    l = distrib.random(radiation,wavelenght_min*10**-9,wavelenght_max*10**-9,10**-9) # Real star radiation in nanometer
    global h
    global c
    E = h * c / l * 6.242e+18
    
    if verbose:
        plt.subplot(221)
        x = np.arange(wavelenght_min,l*10**9*5)
        f = radiation
        plt.plot(x,f(x*10**-9),'r--',l*10**9,f(l),'bs')
        plt.title("Black-body radiation at T = " + str(T) + " K")
        plt.xlabel("Wavelenght (um)")
        plt.ylabel("Spectral radiance (W m−2 sr−1 Hz−1")
        plt.legend(["Planck's law","Photon with E = " + str(round(E,2)) + " eV"])

    return E