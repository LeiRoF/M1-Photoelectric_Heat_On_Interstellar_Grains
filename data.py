
import matplotlib.pyplot as plt
import time
import numpy as np
import sys
from sys import argv


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
                list = ""
                list = input("\nSelect grain file (must be present in the 'grains' folder and not contain space or comma) or a file list separeted with a comma. Write 'all' to run simulation on every file in the 'grains' folder. You can generate one using: python grain.py\n\nYour file [example.txt]: ")
                if list == "":
                    print("example.txt")
                    if not os.path.isfile("grains/example.txt"):
                        print("Generating example grain...")
                        G.generate(N = 100, sigma_dens = 1.0, beta = 3.0, path = "./grains/", doplot = 0, writeFile = True, verbose = False, id3D = 0, name="example")
                    grains.append(G.getFromFile("grains/example.txt"))
                    names.append("example") # Getting file name
                    print("\nSelected file(s):")
                    print(" - example.txt")
                    lock = False

                elif list.lower() in ["a", "all"]:
                    print("\nSelected file(s):")
                    for file in os.listdir("./grains/"):
                        print(" - " + file)
                        grains.append(G.getFromFile("grains/" + file))
                        names.append(os.path.splitext(file)[0]) # Getting file name
                    lock = False
                else:
                    list.replace(" ","").split(",")
                    if type(list) is str: list = [list]
                    print("\nSelected file(s):")
                    for file in list:
                        if file[-4:] != ".txt":
                            file += ".txt"
                        print(" - " + file)
                        grains.append(G.getFromFile("grains/" + file))
                        names.append(os.path.splitext(file)[0])
                    lock = False
            except KeyboardInterrupt:
                endProgram()
            except:
                print("\n[Error] Cannot open or interprete your file '" + file + "' as a grain")
                #raise

    return grains, names

def plotEnergy(file):
    y = []
    events = [0,0,0,0]
    start = time.time()
    
    with open(file,"r") as res:
        for energy in res:
            energy = energy.strip()
            if energy == '':
                continue
            if energy not in ["None", "-1", "-2", "-3"]:
                try:
                    if float(energy) < 12:
                        y.append(float(energy))
                        events[3] += 1
                except ValueError:
                    pass
            elif energy != "None": events[-int(energy)-1] += 1
    end = time.time()
    print("Elapsed time to read data: ", end - start)

    plt.subplot(121)
    plt.hist(y,bins=50)
    plt.title("Energy of emitted photons"); plt.xlabel("Energie (eV)"); plt.ylabel("Nb electrons emitted")

    plt.subplot(122)
    plt.bar(0,events[0],label="photon passed through the grain"); plt.bar(1,events[1],label="photon was absorbed but no electon was emitted"); plt.bar(2,events[2],label="an electron was emitted but was re-absorbed in the grain"); plt.bar(3,events[3],label="the electron escaped from the grain")
    plt.title("Event proportion"); plt.xlabel("Event type"); plt.ylabel("Number of events"); plt.legend()

    plt.show()

if __name__ == "__main__":
    plotEnergy("results/Grain_N100_S1p0_B3p0.dat")