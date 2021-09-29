import numpy as np
from numpy.random.mtrand import rand, randint
import matplotlib.pyplot as plt
import utils
import os
import distributionTools

def throwOnePhoton(file, verbose = False):
    name = os.path.splitext(file)[0].split("/")[-1]
    grain = utils.getGrainFromFile(file)
    start_pos = randint(len(grain))
    E = 3+rand()*12 # Photon energy 3 < E < 15 eV
    Ei = 11.26 # Ionisation energy for graphite sphere (carbon)
    grain1D = grain[start_pos] # We consider only the dimension corresponding to the direction of the photon

    if not os.path.isdir("results"):
        os.makedirs("results")

    if verbose:
        print("   - A photon appeared at Rx=0.0, Ry=", start_pos+0.5)
        print("   - The photon's direction is: Dx=1.0 , Dy=0.0")
        print("   - It has an energy of ", round(E,3), " eV")
    
    # Getting point of impact between photon and drain
    cpt = 0
    hit_pos = -1
    for occuped_space in grain1D:
        if int(occuped_space):
            if hit_pos == -1:
                hit_pos = cpt
        cpt += 1

    # Getting random distance using the probability P=exp(-da/la) / la
    la = 100 # 10^-6 cm = 100 angstrom -> 100 pixels
    da = distributionTools.randomInDistrib(lambda x: np.exp(-x/la) / la,0,100)

    # Getting absorbtion position
    x = 0
    distBeforeAbsorbtion = int(da) + 1
    while x < len(grain) and distBeforeAbsorbtion > 0:
        if int(grain1D[x]):
            distBeforeAbsorbtion -= 1
        x += 1

    """
    If the photon didn't hit the grain
    """

    if not(0 <= hit_pos < len(grain)):
        if verbose: print("❌ - But... it missed the grain")
        return None

    """
    If the photon entered in the grain
    """

    if verbose:
        print("✅ - It hit the grain at Rx=", hit_pos+0.5, ", Ry+0.5", start_pos+0.5)
        print("   - In these conditions, the photon will travel ", round(da,3), "angstroms through the grain")
        xaxis, fx = distributionTools.plotDistrib(lambda x: np.exp(-x/la) / la, 0, 100, 1)
        plt.subplot(231)
        plt.plot(xaxis,fx,'r--',da,np.exp(-da/la) / la,'bs')
        plt.title("Distance traveled by photon in the grain")
        plt.xlabel("Distance (da)")
        plt.ylabel("Probability amplitude distribution (P)")
        plt.legend(["P=exp(-da/la) / la","Random da"])

    """
    If the photon passed through the grain
    """

    if not (0 <= x < len(grain)): 
        if verbose: print("❌ - And... this distance was too high, it passed trhough the grain :/")
        with open("results/" + name + ".dat","a") as result:
            result.write(str(-1) + '\n')
        return -1
    
    """
    If the photon is absorbed
    """

    if verbose: print("✅ - Oh, it was absorbed at Rx=", x+0.5, " Ry=", start_pos+0.5)
    E0 = 8
    electron_emitted = rand() < 0.5*(1+np.tanh((E-E0)/2)) # Emit electron with probability Y=0.5*(1+Th[(E-E0)/2])
    if verbose:
        print("   - In these conditions, the probability of emitting an electron is ", round(0.5*(1+np.tanh((E-E0)/2)),3))
        xaxis, fx = distributionTools.plotDistrib(lambda x: 0.5*(1+np.tanh(x-E0)/2), 3, 15, 0.1)
        plt.subplot(232)
        plt.plot(xaxis,fx,'r--',E,0.5*(1+np.tanh((E-E0)/2)),'bs')
        plt.title("Electron emition")
        plt.xlabel("Energy of the photon (E)")
        plt.ylabel("Probability (Y)")
        plt.legend(["Y=0.5*(1+Th[(E-E0)/2])","Current situation"])

    """
    If no electron emitted
    """

    if not electron_emitted:
        if verbose: print("❌ - No electron was emitted :/")
        with open("results/" + name + ".dat","a") as result:
            result.write(str(-2) + '\n')
        return -2
            
    """
    If an electron is emitted
    """

    # Position of the electron
    Rx = x
    Ry = start_pos

    # Direction of the electron
    Dx = -1 + rand()*2
    Dy = -1 + rand()*2
    normalisationFactor = 1 / (np.sqrt(Dx*Dx+Dy*Dy))
    Dx = Dx*normalisationFactor
    Dy = Dy*normalisationFactor 

    if verbose:
        print("✅ - An electron has been emitted at Rx=", Rx+0.5, " , Ry=", Ry+0.5)
        print("   - The electron's direction is: Dx=", np.round(Dx,3), " , Dy=", np.round(Dy,3))

    # Getting random distance traveld by the electron using the probability P=exp(-de/le) / le
    le = 10 # 10^-6 cm = 100 angstrom -> 100 pixels
    de = distributionTools.randomInDistrib(lambda x: np.exp(-x/le) / le,0,100)
    if verbose:
        print("   - In these conditions, the electron will travel ", np.round(de,3), "angstroms through the grain")

        xaxis, fx = distributionTools.plotDistrib(lambda x: np.exp(-x/le) / le, 0, 100, 0.1)
        plt.subplot(233)
        plt.plot(xaxis,fx,'r--',de,np.exp(-de/le) / le,'bs')
        plt.title("Distance traveled by electron in the grain")
        plt.xlabel("Distance (de)")
        plt.ylabel("Probability amplitude distribution (P)")
        plt.legend(["P=exp(-de/le)/le","Random de"])
        plt.show()

    # Getting absorbtion position
    step = 0.001
    distBeforeAbsorbtion = int(de) + 1
    while 0 <= Rx < len(grain) and 0 <= Ry < len(grain) and distBeforeAbsorbtion > 0:
        if int(grain[int(Rx)][int(Ry)]):
            distBeforeAbsorbtion -= step
        Rx += step*Dx
        Ry += step*Dy

    """
    If the electron was re-absorbed
    """

    if 0 <= Rx < len(grain) and 0 <= Ry < len(grain):
        if verbose: print("❌ - The electron was re-absorbed at position: Rx=", np.round(Rx,3), ", Ry=", np.round(Ry,3))
        with open("results/" + name + ".dat","a") as result:
            result.write(str(-3) + '\n')
        return -3
    
    """
    If the electron get ou the grain
    """

    x = -1
    electronAbsorbed = False
    if verbose: print("✅ - The electron was ejected with a kinetic energy of ", E - Ei, "eV")
    with open("results/" + name + ".dat","a") as result:
            result.write(str(E - Ei) + '\n')
    return E - Ei

    

if __name__ == "__main__":
    throwOnePhoton("grains/Grain_N100_S1p0_B3p0.txt", verbose = True)
    