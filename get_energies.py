import numpy
from numpy.random.mtrand import rand, randint
import math
import utils

def getGrainFromFile(file):
    with open(file, "r") as file:
        array = []
        for line in file:
            array.append(line.split(" "))
    return numpy.array(array)

def throwPhoton(grain, verbose = False):
    start_pos = randint(len(grain))
    energy = 3+rand()*12
    grain1D = grain[start_pos] # We consider only the dimension corresponding to the direction of the photon
    
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
    da = utils.randomInDistrib(lambda x: numpy.exp(-x/la) / la,0,100)

    # Getting absorbtion position
    x = 0
    distBeforeAbsorbtion = int(da) + 1
    while x < len(grain) and distBeforeAbsorbtion > 0:
        if int(grain1D[x]):
            distBeforeAbsorbtion -= 1
        x += 1
    if x == 100:
        x = -1
        photonAbsorbed = False
    else:
        photonAbsorbed = True
    
    # Printing results
    if verbose:
        print("   - A photon appeared in column ", start_pos, "!")
        print("   - It have an energy of ", round(energy,3), " eV")
        if hit_pos == -1:
            print("❌ - But... it missed the grain")
        else:
            print("✅ - It hitted the grain at line ", start_pos, ", column ", hit_pos, "!")
            print("   - In this condition, the photon will travel ", round(da,3), "angstroms trhough the grain")
            if x == -1:
                print("❌ - And... this distance was to hight, it passed trhough the grain :/")
            else:
                print("✅ - Oh, it was absorbed at column ", x)

    # Emit electron with probability Y=0.5*(1+Th[(E-E0)/2])
    if photonAbsorbed:
        E0 = 8
        electron_emitted = rand() < 0.5*(1+numpy.tanh((energy-E0)/2))
        if verbose:
            print("   - In this conditions, the probability of emitting an electron is ", round(0.5*(1+numpy.tanh((energy-E0)/2)),3))
            if electron_emitted:
                print("✅ - An electron has been emitted!")
            else:
                print("❌ - No electron was emitted :/")

        if electron_emitted:
            # Getting random distance traveld by the electron using the probability P=exp(-de/le) / le
            le = 10 # 10^-6 cm = 100 angstrom -> 100 pixels
            de = utils.randomInDistrib(lambda x: numpy.exp(-x/le) / le,0,100)
            if verbose:
                print("   - In this condition, the electron will travel ", round(de,3), "angstroms trhough the grain")

            # Getting absorbtion position

            distBeforeAbsorbtion = int(de) + 1
            while x < len(grain) and distBeforeAbsorbtion > 0:
                if int(grain1D[x]):
                    distBeforeAbsorbtion -= 1
                x += 1
            if x == 100:
                x = -1
                electronAbsorbed = False
            else:
                electronAbsorbed = True
            if verbose:
                if electronAbsorbed:
                    print("❌ - The electron was re-absorbed at column ", x, "!")
                else:
                    print("✅ - The electron was ejected!")
    

if __name__ == "__main__":
    grain = getGrainFromFile("grains/Grain_N100_S1p0_B3p0.txt")
    throwPhoton(grain, True)