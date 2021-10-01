import numpy as np
import matplotlib.pyplot as plt
from throwOnePhoton import throwOnePhoton

def throwManyPhotons(count, file, verbose = False):

    #precision = 1

    #step = 30*10**precision

    #x = np.linspace(-15, 15, step)
    #y = np.zeros(len(x))
    y = []
    events = np.zeros(4)

    #for i in range(step): y.append(0)
    for i in range(count):
        energy = throwOnePhoton(file)
        if energy not in [None, -1, -2, -3]:
            y.append(energy)
            print("[", i, "] ", energy, " eV")
            #index = int((15+np.round(energy,precision)) * 10**precision)
            #print("[", i,"] energy: ", energy, "index", index)
            #y[index] += 1
            events[3] += 1
        elif energy is not None: events[-energy-1] += 1



    #plt.plot(x, y, 'b-')
    #plt.hist(x,weights=y,bins=50)
    plt.subplot(121);   plt.hist(y,bins=50);    plt.title("Energy of emitted photons"); plt.xlabel("Energie (eV)"); plt.ylabel("Nb electrons emitted")
    
    plt.subplot(122); plt.title("Event proportion"); plt.xlabel("Event type"); plt.ylabel("Number of events")
    plt.bar(0,events[0],label="photon passed through the grain")
    plt.bar(1,events[1],label="photon was absorbed but no electon was emitted")
    plt.bar(2,events[2],label="an electron was emitted but was re-absorbed in the grain")
    plt.bar(3,events[3],label="the electron escaped from the grain")
    plt.legend()
    
    
    
    plt.show()

if __name__ == "__main__":
    throwManyPhotons(100000, "grains/Grain_N100_S1p0_B3p0.txt", verbose = True)