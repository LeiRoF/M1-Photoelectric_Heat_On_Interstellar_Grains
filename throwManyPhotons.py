import numpy as np
import matplotlib.pyplot as plt
from throwOnePhoton import throwOnePhoton

def throwManyPhotons(count, file, verbose = False):

    precision = 1

    step = 30*10**precision

    x = np.linspace(-15, 15, step)
    y = []
    for i in range(step): y.append(0)
    for i in range(count):
        energy = throwOnePhoton(file)
        if energy not in [None, -1, -2, -3]:
            index = int((15+np.round(energy,precision)) * 10**precision)
            print("[", i,"] energy: ", energy, "index", index)
            y[index] += 1

    plt.plot(x, y, 'b-')
    plt.show()

if __name__ == "__main__":
    throwManyPhotons(10000, "grains/Grain_N100_S1p0_B3p0.txt", verbose = True)