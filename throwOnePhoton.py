import matplotlib.pyplot as plt
import grain as G
import os
import distrib
from photon import *
from isAbsorbed import *

import numpy as np # do not remove even if seems to be unused
from numpy import pi, cos, sin, tan, exp, log, arcsin, arccos, arctan, sinh, cosh, tanh, arcsinh, arccosh, arctanh, sqrt, round # do not remove even if seems to be unused
from numpy.random.mtrand import rand # do not remove even if seems to be unused



def throwOnePhoton(grain, angle = ["rand()*2*pi","rand()*pi"], target = ["rand()","rand()","rand()"], verbose = False, name="grain", minimalVerbose = False):

    if verbose:
        plt.figure(num=name)

    if not os.path.isdir("results"):
        os.makedirs("results")
    result = open("results/" + name + ".dat","a")
    
    dim = grain.ndim
    E = getPhotonEnergy(verbose)
    Ei = G.getIonisationEnergy(grain)

    if type(angle) == str: angle = [angle]
    if dim == 2:
        phi = eval(angle[0])
        theta = pi
        (sizeX,sizeY) = grain.shape
        size = sqrt(sizeX*sizeX+sizeY*sizeY)
    
    if dim == 3:
        phi = eval(angle[0])
        phi = eval(angle[1])
        (sizeX,sizeY,sizeZ) = grain.shape
        size = sqrt(sizeX*sizeX+sizeY*sizeY+sizeZ*sizeZ)

    # Deplacment vector
    Dx = cos(phi)*sin(theta);     Dy = sin(phi)*sin(theta);     Dz = cos(theta)

    # Origin
    Ox = 0 if Dx > 0 else sizeX - 1;     Oy = 0 if Dy > 0 else sizeY - 1; 
    if dim ==3: Oz = 0 if Dz > 0 else sizeZ - 1

    # Targeted point (the photon trajectory touch this point)
    Tx = eval(target[0])*sizeX;     Ty = eval(target[1])*sizeY
    if dim == 3: Tz = eval(target[2])*sizeZ

    if Dx == 0 and Dy == 0 and Dz == 0: Dx = 1.0

    if Dx == 0: A = (Ty - Oy)/Dy
    elif Dy == 0: A = (Tx - Ox)/Dx
    else: A = min((Tx - Ox)/Dx, (Ty - Oy)/Dy)

    # Coordinates of the photon when it appear on the matrix
    Rx = Tx - Dx * A;     Ry = Ty - Dy * A

    if verbose:
        print(f"\n  - A photon appeared at Rx={round(Rx,3)} Ry={round(Ry,3)}")
        print(f"  - The photon's direction is: Dx={round(Dx,3)}, Dy={round(Dy,3)} (angle={round(phi/pi,3)}pi rad)")
        print(f"  - It has an energy of {round(E,3)} eV")
        print(f"  - And the ionisation energy of the grain is {round(Ei,3)} eV")
    
    # Getting random distance using the probability P=exp(-da/la) / la
    la = 100 # 10^-6 cm = 100 angstrom -> 100 pixels
    da = distrib.random(lambda x: exp(-x/la) / la,0,100)

    # Getting absorbtion position
    absorbed, Rx, Ry, hitPos = isAbsorbed(grain, da, Rx, Ry, Dx, Dy)

    """
    If the photon didn't hit the grain
    """

    if hitPos == []:
        if verbose: print("X - But... it missed the grain")
        if minimalVerbose: print("0",end="")
        result.write(str(-1) + '\n')
        return -1

    """
    If the photon entered in the grain
    """

    if verbose:
        print("0 - It hit the grain!")
        print("  - In these conditions, the photon will travel ", round(da,3), "angstroms through the grain")
        xaxis, fx = distrib.plot(lambda x: exp(-x/la) / la, 0, int(size+1), int(size+1)/1000)
        plt.subplot(222); plt.plot(xaxis,fx,'r--',da,exp(-da/la) / la,'bs'); plt.title("Distance traveled by photon in the grain"); plt.xlabel("Distance (da)"); plt.ylabel("Probability amplitude distribution (P)"); plt.legend(["P=exp(-da/la) / la","Random da"])

    """
    If the photon passed through the grain
    """

    if not absorbed: 
        if verbose:
            print("X - And... this distance was too high, it passed trhough the grain :/")
            plt.show()
        if minimalVerbose: print("1",end="")
        result.write(str(-2) + '\n')
        return -2
    
    """
    If the photon is absorbed
    """

    if verbose: print("0 - Oh, it was absorbed at Rx=", Rx, " Ry=", Ry)
    E0 = 8
    electron_emitted = rand() < 0.5*(1+tanh((E-E0)/2)) # Emit electron with probability Y=0.5*(1+Th[(E-E0)/2])
    
    if verbose:
        print("  - In these conditions, the probability of emitting an electron is ", round(0.5*(1+tanh((E-E0)/2)),3))

        # Plot electron emission probability
        xaxis, fx = distrib.plot(lambda x: 0.5*(1+tanh((x-E0)/2)), 0, max(15,E), max(15,E)/100)
        plt.subplot(223); plt.plot(xaxis,fx,'r--',E,0.5*(1+tanh((E-E0)/2)),'bs'); plt.title("Electron emission"); plt.xlabel("Energy of the photon (E)"); plt.ylabel("Probability (Y)"); plt.legend(["Y=0.5*(1+Th[(E-E0)/2])","Current situation"])

    """
    If no electron emitted
    """

    if not electron_emitted:
        if verbose:
            print("X - No electron was emitted :/")
            plt.show()
        if minimalVerbose: print("2",end="")
        result.write(str(-3) + '\n')
        return -3
            
    """
    If an electron is emitted
    """

    # Direction of the electron
    Dx = -1 + rand()*2; Dy = -1 + rand()*2
    normalisationFactor = 1 / (sqrt(Dx*Dx+Dy*Dy))
    Dx = Dx*normalisationFactor; Dy = Dy*normalisationFactor 

    if verbose:
        print("0 - An electron has been emitted at Rx=", Rx+0.5, " , Ry=", Ry+0.5)
        print("  - The electron's direction is: Dx=", round(Dx,3), " , Dy=", round(Dy,3))

    # Getting random distance traveled by the electron using the probability P=exp(-de/le) / le
    le = 10 # 10^-6 cm = 100 angstrom -> 100 pixels
    de = distrib.random(lambda x: exp(-x/le) / le,0,100)
    if verbose:
        print("  - In these conditions, the electron will travel ", round(de,3), "angstroms through the grain")

        # Plot travel distance probability
        xaxis, fx = distrib.plot(lambda x: exp(-x/le) / le, 0, int(size+1), int(size+1)/1000)
        plt.subplot(224); plt.plot(xaxis,fx,'r--',de,exp(-de/le) / le,'bs'); plt.title("Distance traveled by electron in the grain"); plt.xlabel("Distance (de)"); plt.ylabel("Probability amplitude distribution (P)"); plt.legend(["P=exp(-de/le)/le","Random de"])

    # Getting absorbtion position
    absorbed, Rx, Ry, hitPos = isAbsorbed(grain, de, Rx, Ry, Dx, Dy)

    """
    If the electron was re-absorbed
    """

    if absorbed:
        if verbose:
            print("X - The electron was re-absorbed at position: Rx=", round(Rx,3), ", Ry=", round(Ry,3))
            plt.show()
        if minimalVerbose: print("3",end="")
        result.write(str(-4) + '\n')
        return -4
    
    """
    If the electron get ou the grain
    """

    if verbose:
        print("0 - The electron was ejected with a kinetic energy of ", E - Ei, "eV")
        plt.show()
    if minimalVerbose: print("\nElectron excaped with " + str(round(E-Ei,3)) + " eV\n",end="")
    result.write(str(E - Ei) + '\n')
    return  E - Ei

if __name__ == "__main__":

    import run
    run.simulation("example.txt",1,"rand()*2*pi",["rand()","rand()"],True)
    