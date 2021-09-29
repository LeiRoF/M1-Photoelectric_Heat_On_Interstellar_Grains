import numpy as np

# Convert a grain stored in a txt file in an numpy.array
def getGrainFromFile(file):
    with open(file, "r") as file:
        array = []
        for line in file:
            array.append(line.split(" "))
    return np.array(array)