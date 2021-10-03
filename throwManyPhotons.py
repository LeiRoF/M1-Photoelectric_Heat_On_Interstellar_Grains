import numpy as np
import matplotlib.pyplot as plt
from throwOnePhoton import throwOnePhoton
from sys import argv
import sys
import time
from multiprocessing import Pool
import os
import data

from numpy import pi # do not remove even if seems to be unused
from numpy.random.mtrand import rand # do not remove even if seems to be unused

def throwManyPhotons(file, count, angle = 0, target = ["rand()","rand()"], verbose = False):

    y = []
    events = np.zeros(4)

    # Verbose -> simulation sequential on 1 thread
    if verbose:
        for i in range(count):
            energy = throwOnePhoton(file,angle,target)
            if energy not in [None, -1, -2, -3]:
                y.append(energy)
                if verbose: print("[", i, "] ", round(energy,3), " eV")
                events[3] += 1
            elif energy is not None: events[-energy-1] += 1

    # Not Vetbose -> Simulation parrallelized
    else:
        list = [(file,angle,target)]*count
        cores = max(os.cpu_count()-1,1)
        print("Executing simulation on ", cores , " threads")
        with Pool(cores) as p:
            p.starmap(throwOnePhoton,list)

    if verbose:
        plt.subplot(121)
        plt.hist(y,bins=50)
        plt.title("Energy of emitted photons"); plt.xlabel("Energie (eV)"); plt.ylabel("Nb electrons emitted")
        
        plt.subplot(122)
        plt.bar(0,events[0],label="photon passed through the grain"); plt.bar(1,events[1],label="photon was absorbed but no electon was emitted"); plt.bar(2,events[2],label="an electron was emitted but was re-absorbed in the grain"); plt.bar(3,events[3],label="the electron escaped from the grain")
        plt.title("Event proportion"); plt.xlabel("Event type"); plt.ylabel("Number of events"); plt.legend()
        
        plt.show()

if __name__ == "__main__":

    try:
        file = argv[1]
        if file[0] == file[-1] in ["'",'"']: file = file[1:-2]
        with open(file): pass
    except IndexError:
        file = "grains/Grain_N100_S1p0_B3p0.txt"
    except FileNotFoundError:
        print('\n[ERROR] File "', argv[1] ,'" not found.\n   Correct syntax: python throwManyPhotons.py [filename (string)] [count (int)] [angle (float or lambda)] [verbose (bool)]\nMore information on https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/throwManyPhotons.html\n')
        sys.exit(1)
    
    try:
        count = int(argv[2])
    except ValueError:
        print('\n[ERROR] "count" parameter must be an integer.\n   Correct syntax: python throwManyPhotons.py [filename (string)] [count (int)] [angle (float or lambda)] [verbose (bool)]\nMore information on https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/throwManyPhotons.html\n')
        sys.exit(1)
    except IndexError:
        count = 1000

    try:
        angle = argv[3]
        if angle[0] == angle[-1] in ["'",'"']: angle = angle[1:-2]
        eval(angle)
    except IndexError:
        angle = 0
    except:
        print('\n[ERROR] "angle" parameter not correct. It must be a number or an expression that can be evaluated by python (ex: rand() * 2 * pi)\n   Correct syntax: python throwManyPhotons.py [filename (string)] [count (int)] [angle (float or lambda)] [verbose (bool)]\nMore information on https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/throwManyPhotons.html\n')
        raise

    try:
        Tx = argv[4]
        if Tx[0] == Tx[-1] in ["'",'"']: Tx = Tx[1:-2]
        from numpy import pi
        from numpy.random.mtrand import rand
        eval(Tx)
    except IndexError:
        Tx = 0
    except:
        print('\n[ERROR] "Tx" parameter not correct. It must be a number or an expression that can be evaluated by python (ex: rand() * 2 * pi)\n   Correct syntax: python throwManyPhotons.py [filename (string)] [count (int)] [angle (float or lambda)] [verbose (bool)]\nMore information on https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/throwManyPhotons.html\n')
        raise

    try:
        Ty = argv[5]
        if Ty[0] == Tx[-1] in ["'",'"']: Ty = Ty[1:-2]
        from numpy import pi
        from numpy.random.mtrand import rand
        eval(Ty)
    except IndexError:
        Ty = 0
    except:
        print('\n[ERROR] "Ty" parameter not correct. It must be a number or an expression that can be evaluated by python (ex: rand() * 2 * pi)\n   Correct syntax: python throwManyPhotons.py [filename (string)] [count (int)] [angle (float or lambda)] [verbose (bool)]\nMore information on https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/throwManyPhotons.html\n')
        raise

    try:
        verbose = argv[6].lower() in ["true","1"]
    except ValueError:
        print('\n[ERROR] "verbose" parameter must be set to "True" or "False".\n   Correct syntax: python throwManyPhotons.py [filename (string)] [count (int)] [angle (float or lambda)] [verbose (bool)]\nMore information on https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/throwManyPhotons.html\n')
        sys.exit(1)
    except IndexError:
        verbose = True

    start = time.time()

    throwManyPhotons(file, count, angle = angle, target=[Tx,Ty], verbose = verbose)
    
    end = time.time()
    print("Simulation time: ", end - start)
    
    
    