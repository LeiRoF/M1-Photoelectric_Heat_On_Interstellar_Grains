from sys import argv
import sys
import numpy as np
import matplotlib.pyplot as plt
import grain as G
import os
import distrib
from numpy.random.mtrand import randint

from numpy import pi # do not remove even if seems to be unused
from numpy.random.mtrand import rand # do not remove even if seems to be unused


def isAbsorbed(grain, dist, Rx, Ry, Dx, Dy, step= 0.001):
    hitPos = []
    while 0 <= Rx < len(grain) and 0 <= Ry < len(grain) and dist > 0:
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

def throwOnePhoton(file, angle = 0, target = ["rand()","rand()"], verbose = False):

    name = os.path.splitext(file)[0].split("/")[-1].split("\\")[-1] # Getting file name
    grain = G.getFromFile(file)
    start_pos = randint(len(grain))
    E = 3+rand()*12 # Photon energy 3 < E < 15 eV
    Ei = G.getIonisationEnergy(grain)
    grain1D = grain[start_pos] # We consider only the dimension corresponding to the direction of the photon

    angle = eval(angle)

    # Deplacment vector
    Dx = np.cos(angle)
    Dy = np.sin(angle)

    # Origin
    Ox = 0 if Dx > 0 else len(grain)
    Oy = 0 if Dy > 0 else len(grain)

    # Targeted point (the photon trajectory touch this point)
    Tx = eval(target[0])*len(grain)
    Ty = eval(target[1])*len(grain)

    A = min((Tx - Ox)/Dx, (Ty - Oy)/Dy)

    # Coordinates of the photon when it appear on the matrix
    Rx = Tx - Dx * A
    Ry = Ty - Dy * A

    if not os.path.isdir("results"):
        os.makedirs("results")

    if verbose:
        print("  - A photon appeared at Rx=", round(Rx,3), ", Ry=", round(Ry,3))
        print("  - The photon's direction is: Dx=", round(Dx,3), ", Dy=", round(Dy,3), " (angle = ", round(angle/pi,3), "pi rad)")
        print("  - It has an energy of ", round(E,3), " eV")
    
    # Getting random distance using the probability P=exp(-da/la) / la
    la = 100 # 10^-6 cm = 100 angstrom -> 100 pixels
    da = distrib.random(lambda x: np.exp(-x/la) / la,0,100)

    # Getting absorbtion position
    absorbed, Rx, Ry, hitPos = isAbsorbed(grain, da, Rx, Ry, Dx, Dy)

    """
    If the photon didn't hit the grain
    """

    if hitPos == []:
        if verbose: print("X - But... it missed the grain")
        return None

    """
    If the photon entered in the grain
    """

    if verbose:
        print("0 - It hit the grain at Rx=", hitPos[0], ", Ry=", hitPos[0])
        print("  - In these conditions, the photon will travel ", round(da,3), "angstroms through the grain")
        xaxis, fx = distrib.plot(lambda x: np.exp(-x/la) / la, 0, 100, 1)
        plt.subplot(131)
        plt.plot(xaxis,fx,'r--',da,np.exp(-da/la) / la,'bs')
        plt.title("Distance traveled by photon in the grain")
        plt.xlabel("Distance (da)")
        plt.ylabel("Probability amplitude distribution (P)")
        plt.legend(["P=exp(-da/la) / la","Random da"])

    """
    If the photon passed through the grain
    """

    if not absorbed: 
        if verbose: print("X - And... this distance was too high, it passed trhough the grain :/")
        with open("results/" + name + ".dat","a") as result:
            result.write(str(-1) + '\n')
        return -1
    
    """
    If the photon is absorbed
    """

    if verbose: print("0 - Oh, it was absorbed at Rx=", Rx, " Ry=", Ry)
    E0 = 8
    electron_emitted = rand() < 0.5*(1+np.tanh((E-E0)/2)) # Emit electron with probability Y=0.5*(1+Th[(E-E0)/2])
    if verbose:
        print("  - In these conditions, the probability of emitting an electron is ", round(0.5*(1+np.tanh((E-E0)/2)),3))
        xaxis, fx = distrib.plot(lambda x: 0.5*(1+np.tanh((x-E0)/2)), 3, 15, 0.1)
        plt.subplot(132)
        plt.plot(xaxis,fx,'r--',E,0.5*(1+np.tanh((E-E0)/2)),'bs')
        plt.title("Electron emission")
        plt.xlabel("Energy of the photon (E)")
        plt.ylabel("Probability (Y)")
        plt.legend(["Y=0.5*(1+Th[(E-E0)/2])","Current situation"])

    """
    If no electron emitted
    """

    if not electron_emitted:
        if verbose: print("X - No electron was emitted :/")
        with open("results/" + name + ".dat","a") as result:
            result.write(str(-2) + '\n')
        return -2
            
    """
    If an electron is emitted
    """

    # Direction of the electron
    Dx = -1 + rand()*2
    Dy = -1 + rand()*2
    normalisationFactor = 1 / (np.sqrt(Dx*Dx+Dy*Dy))
    Dx = Dx*normalisationFactor
    Dy = Dy*normalisationFactor 

    if verbose:
        print("0 - An electron has been emitted at Rx=", Rx+0.5, " , Ry=", Ry+0.5)
        print("  - The electron's direction is: Dx=", np.round(Dx,3), " , Dy=", np.round(Dy,3))

    # Getting random distance traveld by the electron using the probability P=exp(-de/le) / le
    le = 10 # 10^-6 cm = 100 angstrom -> 100 pixels
    de = distrib.random(lambda x: np.exp(-x/le) / le,0,100)
    if verbose:
        print("  - In these conditions, the electron will travel ", np.round(de,3), "angstroms through the grain")

        xaxis, fx = distrib.plot(lambda x: np.exp(-x/le) / le, 0, 100, 0.1)
        plt.subplot(133)
        plt.plot(xaxis,fx,'r--',de,np.exp(-de/le) / le,'bs')
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
        if verbose: print("X - The electron was re-absorbed at position: Rx=", np.round(Rx,3), ", Ry=", np.round(Ry,3))
        with open("results/" + name + ".dat","a") as result:
            result.write(str(-3) + '\n')
        return -3
    
    """
    If the electron get ou the grain
    """

    if verbose: print("0 - The electron was ejected with a kinetic energy of ", E - Ei, "eV")
    with open("results/" + name + ".dat","a") as result:
            result.write(str(E - Ei) + '\n')
    return  E - Ei
    

    

if __name__ == "__main__":

    try:
        file = argv[1]
        if file[0] == file[-1] in ["'",'"']: file = file[1:-2]
        with open(file): pass
    except IndexError:
        file = "grains/Grain_N100_S1p0_B3p0.txt"
    except FileNotFoundError:
        print('\n[ERROR] File "', argv[1] ,'" not found. Correct syntax: python throwManyPhotons.py [filename (string)] [count (int)]\nMore information on https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/throwOnePhoton.html\n')
        sys.exit(1)

    try:
        angle = argv[2]
        if angle[0] == angle[-1] in ["'",'"']: angle = angle[1:-2]
        eval(angle)
    except IndexError:
        angle = 0
    except:
        print('\n[ERROR] "angle" parameter not correct. It must be a number or an expression that can be evaluated by python (ex: rand() * 2 * pi)\n   Correct syntax: python throwOnePhoton.py [filename (string)] [angle (lambda)] [target X (lambda)] [target Y (lambda)] [verbose (bool)]\nMore information on https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/throwOnePhoton.html\n')
        raise

    try:
        Tx = argv[3]
        if Tx[0] == Tx[-1] in ["'",'"']: Tx = Tx[1:-2]
        from numpy import pi
        from numpy.random.mtrand import rand
        eval(Tx)
    except IndexError:
        Tx = 0
    except:
        print('\n[ERROR] "Tx" parameter not correct. It must be a number or an expression that can be evaluated by python (ex: rand() * 2 * pi)\n   Correct syntax: python throwOnePhoton.py [filename (string)] [angle (lambda)] [target X (lambda)] [target Y (lambda)] [verbose (bool)]\nMore information on https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/throwOnePhoton.html\n')
        raise

    try:
        Ty = argv[4]
        if Ty[0] == Tx[-1] in ["'",'"']: Ty = Ty[1:-2]
        from numpy import pi
        from numpy.random.mtrand import rand
        eval(Ty)
    except IndexError:
        Ty = 0
    except:
        print('\n[ERROR] "Ty" parameter not correct. It must be a number or an expression that can be evaluated by python (ex: rand() * 2 * pi)\n   Correct syntax: python throwOnePhoton.py [filename (string)] [angle (lambda)] [target X (lambda)] [target Y (lambda)] [verbose (bool)]\nMore information on https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/throwOnePhoton.html\n')
        raise

    throwOnePhoton(file, angle = angle, target = [Tx,Ty], verbose = True)
    plt.show()
    