import numpy as np
import matplotlib.pyplot as plt
from throwOnePhoton import throwOnePhoton
from sys import argv
import sys
import time

def throwManyPhotons(file, count, verbose = False):

    y = []
    events = np.zeros(4)

    for i in range(count):
        energy = throwOnePhoton(file)
        if energy not in [None, -1, -2, -3]:
            y.append(energy)
            if verbose: print("[", i, "] ", round(energy,3), " eV")
            events[3] += 1
        elif energy is not None: events[-energy-1] += 1


    if verbose:

        plt.subplot(121)
        plt.hist(y,bins=50);
        plt.title("Energy of emitted photons"); plt.xlabel("Energie (eV)"); plt.ylabel("Nb electrons emitted")
        
        plt.subplot(122)
        plt.bar(0,events[0],label="photon passed through the grain"); plt.bar(1,events[1],label="photon was absorbed but no electon was emitted"); plt.bar(2,events[2],label="an electron was emitted but was re-absorbed in the grain"); plt.bar(3,events[3],label="the electron escaped from the grain")
        plt.title("Event proportion"); plt.xlabel("Event type"); plt.ylabel("Number of events"); plt.legend()

if __name__ == "__main__":

    try:
        file = argv[1]
        if file[0] == file[-1] in ["'",'"']: file = file[1:-2]
        with open(file): pass
    except IndexError:
        file = "grains/Grain_N100_S1p0_B3p0.txt"
    except FileNotFoundError:
        print('\n[ERROR] File "', argv[1] ,'" not found. Correct syntax: python throwManyPhotons.py [filename (string)] [count (int)] [verbose (bool)]\nMore information on https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/throwManyPhotons.html\n')
        sys.exit(1)
    
    try:
        count = int(argv[2])
    except ValueError:
        print('\n[ERROR] "count" parameter must be an integer. Correct syntax: python throwManyPhotons.py [filename (string)] [count (int)] [verbose (bool)]\nMore information on https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/throwManyPhotons.html\n')
        sys.exit(1)
    except IndexError:
        count = 1000

    try:
        verbose = bool(argv[3])
    except ValueError:
        print('\n[ERROR] "verbose" parameter must be set to "True" or "False". Correct syntax: python throwManyPhotons.py [filename (string)] [count (int)] [verbose (bool)]\nMore information on https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/throwManyPhotons.html\n')
        sys.exit(1)
    except IndexError:
        verbose = False

    start = time.time()
    #asyncio.run(throwManyPhotons(file, count, verbose))
    throwManyPhotons(file, count, verbose)
    end = time.time()
    print("Elapsed time: ", end - start)