import matplotlib.pyplot as plt
import time
from sys import argv
from os import listdir
from os.path import splitext
from multiprocessing import Pool
from utils import CPUcount, endProgram

def askFile():
    # Look at parameters given in argument in the python command
    try:
        file = argv[1]
        # Removing list delimiter
        if (file[0:1] == "'[" and file[-2:-1] == "]'") or (file[0:1] == '"[' and file[-2:-1] == ']"'): file = file[2:-3]
        list = file.split(",")
        # Trying to open file
        for i in range(len(list)):
            # Removing files delimiters
            if list[i][0] == list[i][-1] in ["'",'"']: list[i] = list[i][1:-2]
            open(list[i])
        return list

    # Possible errors
    except FileNotFoundError:
        print('\n[ERROR] File "', list[i] ,'" not found.\n   Correct syntax: python data.py [fileList (string)]\nMore information on https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/data.html')
        exit()
    except IndexError:
        pass

    # No argument, so the program will directly ask the user
    while True:
        try:
            list = ""
            list = input("\nSelect data file (must be present in the 'results' folder and not contain space or comma) or a file list separeted with a comma. Write 'all' to run analyse every file in the 'results' folder.\n\nYour file [example.dat]: ")
            
            # If user want to use the example grain
            if list == "":
                print("example.dat")
                list = ["results/example.dat"]
                print("\nSelected file(s):")
                print(" - example.dat")
                return list

            # If the user want to use all grains
            elif list.lower() in ["a", "all"]:
                print("\nSelected file(s):")
                for file in listdir("./grains/"):
                    print(" - " + file)
                    open(file)
                return list

            # If the user specify each files
            else:
                if (list[0:1] == "'[" and list[-2:-1] == "]'") or (list[0:1] == '"[' and list[-2:-1] == ']"'): list = list[2:-3]
                list = list.replace(" ","").split(",")
                if type(list) is str: list = [list]
                print("\nSelected file(s):")
                for file in list:
                    if file[-4:] != ".dat":
                        file += ".dat"
                    print(" - " + file)
                    open(file)
                return list

        # Possible errors
        except KeyboardInterrupt:
            endProgram()
        except:
            print("\n[Error] Cannot open or interprete your file '" + file + "' as a grain")
            #raise

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

def analyse(fileList):

    if fileList is None: fileList = askFile()

    cores = min(len(fileList),CPUcount())
    print("\nAnalysing data on ", cores , " threads")
    with Pool(cores) as p:
        p.map(plotEnergy,fileList)
    


if __name__ == "__main__":
    fileList = askFile()
    analyse(fileList)

    