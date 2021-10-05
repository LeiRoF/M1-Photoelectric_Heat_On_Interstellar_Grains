import run
import matplotlib.pyplot as plt
import time
import numpy as np
import sys
from sys import argv
import os
import grain as G


def askFile(file = None):
    grains = []
    names = []
    try:
        if file is None:
            file = argv[1]
            if file[0] == file[-1] in ["'",'"']: file = file[1:-2]

    except FileNotFoundError:
        print('\n[ERROR] File "', argv[1] ,'" not found.\n   Correct syntax: python grain.py [filename (string)] [count (int)] [angle (float or lambda)] [verbose (bool)]\nMore information on https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/throwManyPhotons.html')
        sys.exit()
    except IndexError:
        lock = True
        while lock:
            try:
                file = ""
                file = input("\nSelect result file (must be present in the 'results' folder and not contain space or comma).\n\nYour file [example.dat]: ")
                if file == "":
                    print("example.dat")
                    file = "results/example.dat"
                    lock = False
                else:
                    if file[-4:] != ".dat":
                        file = "results/" + file + ".dat"
                    lock = False
                open(file)
            except KeyboardInterrupt:
                run.endProgram()
            except:
                print("\n[Error] Cannot open or interprete your data file '" + file + "'")
    return file

def plotEnergy(file):
    y = []
    events = [0,0,0,0,0]
    start = time.time()
    
    with open(file,"r") as res:
        for energy in res:
            energy = energy.strip()
            if energy == '':
                continue
            if energy not in ["-1", "-2", "-3","-4"]:
                try:
                    if float(energy) < 12:
                        y.append(float(energy))
                        events[4] += 1
                except ValueError:
                    pass
            else: events[-int(energy)-1] += 1
    end = time.time()
    print("Elapsed time to read data: ", end - start)

    
    plt.figure(num=os.path.splitext(file)[0].split("/")[-1].split("\\")[-1])

    plt.subplot(121)
    plt.hist(y,bins=min(50,int(len(y)/10)))
    plt.title("Energy of emitted photons"); plt.xlabel("Energie (eV)"); plt.ylabel("Nb electrons emitted")

    plt.subplot(122)
    plt.bar(0,events[0],label="photon missed the grain"); plt.bar(1,events[1],label="photon passed through the grain"); plt.bar(2,events[2],label="photon was absorbed but no electon was emitted"); plt.bar(3,events[3],label="an electron was emitted but was re-absorbed in the grain"); plt.bar(4,events[4],label="the electron escaped from the grain")
    plt.title("Event proportion"); plt.xlabel("Event type"); plt.ylabel("Number of events"); plt.legend()


if __name__ == "__main__":
    file = askFile()
    plotEnergy(file)
    plt.show()