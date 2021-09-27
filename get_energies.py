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
    da = utils.randomInDistrib(lambda x: numpy.exp(-x/la) / la)
    if verbose:
        print("da = ", da)

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
        print("Distance traveled in grain ", round(da,3), "angstrom")
        print("Point of impact ", hit_pos)
        print("Absorbed at column ", x)

    # Emit electron with probability Y=0.5*(1+Th[(E-E0)/2])
    if photonAbsorbed:
        E0 = 8
        electron_emitted = utils.randomInDistrib(lambda x: 0.5*(1+numpy.tanh[(energy-E0)/2]))

if __name__ == "__main__":
    grain = getGrainFromFile("grains/Grain_N100_S1p0_B3p0.txt")
    throwPhoton(grain, True)