import matplotlib.pyplot as plt
import grain as G
import os
import distrib

import numpy as np # do not remove even if seems to be unused
from numpy import pi, cos, sin, tan, exp, log, arcsin, arccos, arctan, sinh, cosh, tanh, arcsinh, arccosh, arctanh, sqrt, round # do not remove even if seems to be unused
from numpy.random.mtrand import rand # do not remove even if seems to be unused


def isAbsorbed(grain, dist, Rx, Ry, Dx, Dy, step= 0.1):
    hitPos = []

    (sizeX,sizeY) = grain.shape
    
    while 0 <= Rx and Rx < sizeX and 0 <= Ry and Ry < sizeY and dist > 0:
        if grain[int(Rx)][int(Ry)]:
            if hitPos == []:
                hitPos = [Rx,Ry]
            dist -= step
        Rx += step*Dx
        Ry += step*Dy
    if dist <= 0:
        return True, Rx, Ry, hitPos
    else:
        return False, Rx, Ry, hitPos

def throwOnePhoton(grain, angle = 0, target = ["rand()","rand()"], verbose = False, name="grain", minimalVerbose = False):

    result = open("results/" + name + ".dat","a")
    E = 3+rand()*12 # Photon energy 3 < E < 15 eV
    Ei = G.getIonisationEnergy(grain)
    angle = eval(angle)
    (sizeX,sizeY) = grain.shape
    

    # Deplacment vector
    Dx = cos(angle)
    Dy = sin(angle)

    # Origin
    Ox = 0 if Dx > 0 else sizeX - 1
    Oy = 0 if Dy > 0 else sizeY - 1

    # Targeted point (the photon trajectory touch this point)
    Tx = eval(target[0])*sizeX
    Ty = eval(target[1])*sizeY

    if Dx == 0 and Dy == 0: 
        Dx = 1.0

    if Dx == 0: A = (Ty - Oy)/Dy
    elif Dy == 0: A = (Tx - Ox)/Dx
    else: A = min((Tx - Ox)/Dx, (Ty - Oy)/Dy)

    # Coordinates of the photon when it appear on the matrix
    Rx = Tx - Dx * A
    Ry = Ty - Dy * A

    if not os.path.isdir("results"):
        os.makedirs("results")

    if verbose:
        print("\n  - A photon appeared at Rx=", round(Rx,3), ", Ry=", round(Ry,3))
        print("  - The photon's direction is: Dx=", round(Dx,3), ", Dy=", round(Dy,3), " (angle = ", round(angle/pi,3), "pi rad)")
        print("  - It has an energy of ", round(E,3), " eV")
    
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
        print("0 - It hit the grain at Rx=", hitPos[0], ", Ry=", hitPos[0])
        print("  - In these conditions, the photon will travel ", round(da,3), "angstroms through the grain")
        xaxis, fx = distrib.plot(lambda x: exp(-x/la) / la, 0, 100, 1)
        plt.figure(num=name)
        plt.subplot(131)
        plt.plot(xaxis,fx,'r--',da,exp(-da/la) / la,'bs')
        plt.title("Distance traveled by photon in the grain")
        plt.xlabel("Distance (da)")
        plt.ylabel("Probability amplitude distribution (P)")
        plt.legend(["P=exp(-da/la) / la","Random da"])

    """
    If the photon passed through the grain
    """

    if not absorbed: 
        if verbose: print("X - And... this distance was too high, it passed trhough the grain :/")
        result.write(str(-2) + '\n')
        plt.show()
        if minimalVerbose: print("1",end="")
        return -2
    
    """
    If the photon is absorbed
    """

    if verbose: print("0 - Oh, it was absorbed at Rx=", Rx, " Ry=", Ry)
    E0 = 8
    electron_emitted = rand() < 0.5*(1+tanh((E-E0)/2)) # Emit electron with probability Y=0.5*(1+Th[(E-E0)/2])
    if verbose:
        print("  - In these conditions, the probability of emitting an electron is ", round(0.5*(1+tanh((E-E0)/2)),3))
        xaxis, fx = distrib.plot(lambda x: 0.5*(1+tanh((x-E0)/2)), 3, 15, 0.1)
        plt.subplot(132)
        plt.plot(xaxis,fx,'r--',E,0.5*(1+tanh((E-E0)/2)),'bs')
        plt.title("Electron emission")
        plt.xlabel("Energy of the photon (E)")
        plt.ylabel("Probability (Y)")
        plt.legend(["Y=0.5*(1+Th[(E-E0)/2])","Current situation"])

    """
    If no electron emitted
    """

    if not electron_emitted:
        if verbose: print("X - No electron was emitted :/")
        result.write(str(-3) + '\n')
        plt.show()
        if minimalVerbose: print("2",end="")
        return -3
            
    """
    If an electron is emitted
    """

    # Direction of the electron
    Dx = -1 + rand()*2
    Dy = -1 + rand()*2
    normalisationFactor = 1 / (sqrt(Dx*Dx+Dy*Dy))
    Dx = Dx*normalisationFactor
    Dy = Dy*normalisationFactor 

    if verbose:
        print("0 - An electron has been emitted at Rx=", Rx+0.5, " , Ry=", Ry+0.5)
        print("  - The electron's direction is: Dx=", round(Dx,3), " , Dy=", round(Dy,3))

    # Getting random distance traveld by the electron using the probability P=exp(-de/le) / le
    le = 10 # 10^-6 cm = 100 angstrom -> 100 pixels
    de = distrib.random(lambda x: exp(-x/le) / le,0,100)
    if verbose:
        print("  - In these conditions, the electron will travel ", round(de,3), "angstroms through the grain")

        xaxis, fx = distrib.plot(lambda x: exp(-x/le) / le, 0, 100, 0.1)
        plt.subplot(133)
        plt.plot(xaxis,fx,'r--',de,exp(-de/le) / le,'bs')
        plt.title("Distance traveled by electron in the grain")
        plt.xlabel("Distance (de)")
        plt.ylabel("Probability amplitude distribution (P)")
        plt.legend(["P=exp(-de/le)/le","Random de"])

    # Getting absorbtion position
    absorbed, Rx, Ry, hitPos = isAbsorbed(grain, de, Rx, Ry, Dx, Dy)

    """
    If the electron was re-absorbed
    """

    if absorbed:
        if verbose: print("X - The electron was re-absorbed at position: Rx=", round(Rx,3), ", Ry=", round(Ry,3))
        result.write(str(-4) + '\n')
        plt.show()
        if minimalVerbose: print("3",end="")
        return -4
    
    """
    If the electron get ou the grain
    """

    if verbose: print("0 - The electron was ejected with a kinetic energy of ", E - Ei, "eV")
    result.write(str(E - Ei) + '\n')
    plt.show()
    if minimalVerbose: print("\nElectron excaped with " + str(round(E-Ei,3)) + " eV\n",end="")
    return  E - Ei

if __name__ == "__main__":

    import run
    run.simulation("example.txt",1,"rand()*2*pi",["rand()","rand()"],True)
    