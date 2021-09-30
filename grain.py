import numpy as np
import matplotlib.pyplot as plt

# Convert a grain stored in a txt file in an numpy.array
def getFromFile(file):
    with open(file, "r") as file:
        array = []
        for line in file:
            array.append(line.split(" "))
    return np.array(array)

def getMin(grain):
    cpt = 0
    for row in grain:
        for pixel in row:
            if pixel == "1":
                return cpt   
        cpt += 1
    return None

def getMax(grain):
    cpt = len(grain)
    for row in reversed(grain):
        for pixel in row:
            if pixel == "1":
                return cpt
        cpt -= 1
    return None

def getSize(grain):
    min = getMin(grain); max = getMax(grain)
    return (max - min) if type(min) == type(max) == int else None

def getNbCarbon(grain):
    return 0.5*((getSize(grain)/(10**(-10)))**3)

def getIonisationEnergy(grain):
    Z = -1 # for electrons, cf. Bakes & Tielens paper page 828
    return 4.4 + (Z + 1/2) * 25.1 / np.sqrt(getNbCarbon(grain))


if __name__ == "__main__":
    grain = getFromFile("grains/Grain_N100_S1p0_B3p0.txt")
    
    size = getSize(grain)

    Nc = getNbCarbon(grain)

    Ei = getIonisationEnergy(grain)

    #print(25.1/np.sqrt(getNbCarbon(grain)))

    print("Size = ", size, " Angstroms")
    print("Number of carbons = ", Nc)
    print("Ionisation energy = ", Ei, " eV")

    #plt.plot(grain)
    #plt.show()