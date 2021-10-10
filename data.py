import matplotlib.pyplot as plt
import time
from sys import argv
from os import listdir
from os.path import splitext
from multiprocessing import Pool
from utils import CPUcount
import ask

def plotEnergy(file):
    y = []
    events = [0,0,0,0,0]
    
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

    
    plt.figure(num=splitext(file)[0].split("/")[-1].split("\\")[-1])

    plt.subplot(121)
    plt.hist(y,bins=min(50,int(len(y)/10)))
    plt.title("Energy of emitted photons"); plt.xlabel("Energie (eV)"); plt.ylabel("Nb electrons emitted")

    plt.subplot(122)
    plt.bar(0,events[0],label="photon missed the grain"); plt.bar(1,events[1],label="photon passed through the grain"); plt.bar(2,events[2],label="photon was absorbed but no electon was emitted"); plt.bar(3,events[3],label="an electron was emitted but was re-absorbed in the grain"); plt.bar(4,events[4],label="the electron escaped from the grain")
    plt.title("Event proportion"); plt.xlabel("Event type"); plt.ylabel("Number of events"); plt.legend()
    plt.show()



def analyse(fileList = []):

    if type(fileList) == str:
        fileList = [fileList]
    
        if fileList[0].lower() in ["a", "all"]:
            fileList = []
            for file in listdir("./results/"):
                fileList.append(file)

    if fileList ==[]: fileList = ask.dataFile()

    cores = min(len(fileList),CPUcount())
    print("\nAnalysing data on ", cores , " threads")
    with Pool(cores) as p:
        p.map(plotEnergy,fileList)
    


if __name__ == "__main__":
    analyse()

    