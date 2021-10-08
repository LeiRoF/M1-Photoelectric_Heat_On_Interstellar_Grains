from genericpath import isfile
from sys import argv
from sys import exit
from time import time
from os.path import isfile, splitext
from os import listdir
from utils import endProgram, CPUcount, CPUinfo

import grain
import throwManyPhotons
import ask


#--------------------------------------------------
# Start simulation
#--------------------------------------------------



def simulation(file = None, count = None, angle = None, target = [], verbose = None, name = None, temperature = None):

    if name is None : name = ask.name()

    # If no file(s) given in parameter of the function, get it/them from the user
    if file is None:
        grains, names = ask.grains()

    # Else, get the grain from give file(s)
    else:
        if type(file) == str : file = [file]
        if "example.txt" in file:
            grain.checkExampleGrain()
        grains = []
        names = []
        for i in file:
            grains.append(grain.getFromFile("grains/" + i))
            names.append(splitext(i)[0].split("/")[-1].split("\\")[-1])
    if len(grains) == 0: endProgram(reason="noGrain")
    
    # Asking each parameter to the user if they was not given in parameter of this function
    if temperature is None : temperature = ask.temperature()
    if count is None : count = ask.count()
    if angle is None : angle = ask.angle()
    if target == [] : target = ask.target()
    if verbose is None : verbose = ask.verbose()

    # Writing timeStats header
    if not isfile("timeStats.dat"):
        with open("timeStats.dat","a") as stats:
            stats.write("program_version number_of_photon grain_size number_of_threads time_ellapsed cpu_info\n")

    if not verbose:
        cpu = CPUinfo()
        stats = open("timeStats.dat","a")

    # Run simulation for each grain (1 grain = 1 file given in parameter)
    for i in range(len(grains)):
        if len(grains) > 1: name = name + names[i]
        print("\nRunning simulation n°",i+1,"/",len(grains),":",names[i])
        simuTime = time()
        throwManyPhotons.throwManyPhotons(grains[i], count, angle = angle, target=target, verbose = verbose, name=name)
        simuTime = time() - simuTime

        # Adding data to timeStats if verbose is disabled (verbose mode can affect the simulation time)
        if not verbose:
            print("\nSimulation time: ", simuTime)
            stats.write(str(count) + " " + str(len(grains[i])) + " " + str(min(count,CPUcount())) + " " + str(round(simuTime,3)) + " " + cpu + "\n")

    if not verbose: stats.close()


#--------------------------------------------------
# Start simulation from this file
#--------------------------------------------------



if __name__ == "__main__":
    simulation()