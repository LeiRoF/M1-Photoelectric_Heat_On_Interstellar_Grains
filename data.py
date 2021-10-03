
import matplotlib.pyplot as plt
import time

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