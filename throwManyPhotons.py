import numpy as np
import matplotlib.pyplot as plt
import throwOnePhoton
from sys import argv
import sys
import time
from multiprocessing import Pool
import os
from numpy import pi # do not remove even if seems to be unused
from numpy.random.mtrand import rand # do not remove even if seems to be unused


def run(grain, count, angle = 0, target = ["rand()","rand()"], verbose = False, name = "grain"):

    y = []
    events = np.zeros(4)
    # Verbose -> simulation sequential on 1 thread
    if verbose:
        for i in range(count):
            if count == 1: energy = throwOnePhoton.run(grain,angle,target,True,name)
            else: energy = throwOnePhoton.run(grain,angle,target,False,name)
            if energy not in [None, -1, -2, -3]:
                y.append(energy)
                if verbose and count > 1: print("[", i, "] ", round(energy,3), " eV")
                events[3] += 1
            elif energy is not None: events[-energy-1] += 1

    # Not Vetbose -> Simulation parrallelized
    else:
        list = [(grain,angle,target,False,name)]*count
        cores = max(os.cpu_count()-1,1)
        print("Executing simulation on ", cores , " threads")
        with Pool(cores) as p:
            p.starmap(throwOnePhoton.run,list)

    if verbose & count > 1:
        
        plt.figure(num=name)
        plt.subplot(121)
        plt.hist(y,bins=min(50,int(len(y)/10)))
        plt.title("Energy of emitted photons"); plt.xlabel("Energie (eV)"); plt.ylabel("Nb electrons emitted")
        
        plt.subplot(122)
        plt.bar(0,events[0],label="photon passed through the grain"); plt.bar(1,events[1],label="photon was absorbed but no electon was emitted"); plt.bar(2,events[2],label="an electron was emitted but was re-absorbed in the grain"); plt.bar(3,events[3],label="the electron escaped from the grain")
        plt.title("Event proportion"); plt.xlabel("Event type"); plt.ylabel("Number of events"); plt.legend()
        

if __name__ == "__main__":
    import run
    run.simulation("example.txt",1000,"rand()*2*pi",["rand()","rand()"],True)
    plt.show()
    
    
    