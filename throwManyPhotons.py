import numpy as np
import matplotlib.pyplot as plt
import throwOnePhoton
from multiprocessing import Pool
import os
from numpy import pi # do not remove even if seems to be unused
from numpy.random.mtrand import rand # do not remove even if seems to be unused


def runSimulation(grain, count, angle = 0, target = ["rand()","rand()"], verbose = False, name = "grain"):

    y = []
    events = np.zeros(4)

    makeVerbose = count == 1 and verbose == True
    list = [(grain,angle,target,makeVerbose,name)]*count
    cores = min(count,os.cpu_count())
    print("Executing simulation on ", cores , " threads")
    with Pool(cores) as p:
        res = p.starmap(throwOnePhoton.runSimulation,list)
    for energy in res:
        if energy not in [None, -1, -2, -3]:
            y.append(energy)
            events[3] += 1
        elif energy is not None: events[-energy-1] += 1

    if verbose and count > 1: #verbose allow to show results of this specific simulation (instead of showing results of all simulation stored in the same file)
        
        plt.figure(num=name)
        plt.subplot(121)
        plt.hist(y,bins=max(min(50,int(len(y)/10)),3))
        plt.title("Energy of emitted photons"); plt.xlabel("Energie (eV)"); plt.ylabel("Nb electrons emitted")
        
        plt.subplot(122)
        plt.bar(0,events[0],label="photon passed through the grain"); plt.bar(1,events[1],label="photon was absorbed but no electon was emitted"); plt.bar(2,events[2],label="an electron was emitted but was re-absorbed in the grain"); plt.bar(3,events[3],label="the electron escaped from the grain")
        plt.title("Event proportion"); plt.xlabel("Event type"); plt.ylabel("Number of events"); plt.legend()
        

if __name__ == "__main__":
    import run
    run.simulation("example.txt",1000,"rand()*2*pi",["rand()","rand()"],True)
    plt.show()
    
    
    