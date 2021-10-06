from genericpath import isfile
from throwManyPhotons import throwManyPhotons
from sys import argv
from sys import exit
from time import time
from grain import getFromFile, generate
from os.path import isfile, splitext
from os import listdir, cpu_count
import matplotlib.pyplot as plt
from cpuinfo import get_cpu_info

import numpy as np # do not remove even if seems to be unused
from numpy import pi, cos, sin, tan, exp, log, arcsin, arccos, arctan, sinh, cosh, tanh, arcsinh, arccosh, arctanh, sqrt, round # do not remove even if seems to be unused
from numpy.random.mtrand import rand # do not remove even if seems to be unused


#--------------------------------------------------
# End program messages
#--------------------------------------------------



def endProgram(reason="interrupted"):
    if reason == "noGrain": print("\n[Error] No grain found. You can generate a grain by running the following command: python grain.py")
    else:print("\nProgram interrupted.")
    exit()


#--------------------------------------------------
# Get CPU infos
#--------------------------------------------------



def getCPU():
    print("\nGetting CPU info...")
    cpuInfo = get_cpu_info()["brand_raw"]
    print("-> ",cpuInfo)
    return cpuInfo.replace(" ","_")



#--------------------------------------------------
# Generate example grain if it doesn't exist
#--------------------------------------------------



def checkExampleGrain():
    if not isfile("grains/example.txt"):
        print("Generating example grain...")
        generate(N = 100, sigma_dens = 0.5, beta = 0.5, path = "./grains/", doplot = 0, writeFile = True, verbose = False, id3D = 0, name="example")



#--------------------------------------------------
# Ask grain to user
#--------------------------------------------------



def askGrains():
    grains = []
    names = []
    # Look at parameters given in argument in the python command
    try:
        file = argv[1]
        # Removing list delimiter
        if (file[0:1] == "'[" and file[-2:-1] == "]'") or (file[0:1] == '"[' and file[-2:-1] == ']"'): file = file[2:-3]
        
        list = file.split(",")
        for file in list:
            # Removing files delimiters
            if file[0] == file[-1] in ["'",'"']: file = file[1:-2]
            grains.append(getFromFile("grains/" + file))
            names.append(splitext(file)[0])
        return grains,names

    # Possible errors
    except FileNotFoundError:
        print('\n[ERROR] File "', argv[1] ,'" not found.\n   Correct syntax: python throwManyPhotons.py [filename (string)] [count (int)] [angle (float or lambda)] [verbose (bool)]\nMore information on https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/throwManyPhotons.html')
        exit()
    except IndexError:
        pass

    # No argument, so the program will directly ask the user
    while True:
        try:
            list = ""
            list = input("\nSelect grain file (must be present in the 'grains' folder and not contain space or comma) or a file list separeted with a comma. Write 'all' to run simulation on every file in the 'grains' folder. You can generate one using: python grain.py\n\nYour file [example.txt]: ")
            
            # If user want to use the example grain
            if list == "":
                print("example.txt")
                checkExampleGrain()
                grains.append(getFromFile("grains/example.txt"))
                names.append("example") # Getting file name
                print("\nSelected file(s):")
                print(" - example.txt")
                return grains, names

            # If the user want to use all grains
            elif list.lower() in ["a", "all"]:
                print("\nSelected file(s):")
                for file in listdir("./grains/"):
                    print(" - " + file)
                    grains.append(getFromFile("grains/" + file))
                    names.append(splitext(file)[0]) # Getting file name
                return grains, names

            # If the user specify each files
            else:
                list.replace(" ","").split(",")
                if type(list) is str: list = [list]
                print("\nSelected file(s):")
                for file in list:
                    if file[-4:] != ".txt":
                        file += ".txt"
                    print(" - " + file)
                    grains.append(getFromFile("grains/" + file))
                    names.append(splitext(file)[0])
                return grains, names

        # Possible errors
        except KeyboardInterrupt:
            endProgram()
        except:
            print("\n[Error] Cannot open or interprete your file '" + file + "' as a grain")
            #raise



#--------------------------------------------------
# Ask count to user
#--------------------------------------------------



def askCount():

    # Look at parameters given in argument in the python command
    try:
        count = int(argv[2])
        return count

    # Possible errors
    except ValueError:
        print('\n[ERROR] "count" parameter must be an integer.\n   Correct syntax: python throwManyPhotons.py [filename (string)] [count (int)] [angle (float or lambda)] [verbose (bool)]\nMore information on https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/throwManyPhotons.html')
        exit(1)
    except IndexError:
        pass

    # No argument, so the program will directly ask the user
    while True:
        try:
            count = input("\nNumber of photon [1000]: ")
            if count == "": count = 1000; print("1000")
            count = int(count)
            if count < 0 :
                raise
            else:
                return count
    
        # Possible errors
        except KeyboardInterrupt:
            endProgram()
        except:
            print("\n[Error] Incorrect value. You must enter a positive integer.")



#--------------------------------------------------
# Ask angle to user
#--------------------------------------------------



def askAngle():

    # Look at parameters given in argument in the python command
    try:
        angle = argv[3]
        if angle[0] == angle[-1] in ["'",'"']: angle = angle[1:-2]
        eval(angle)
        return angle
    
    

    # Possible errors
    except IndexError:
        pass
    except:
        print('\n[ERROR] "angle" parameter not correct. It must be a number or an expression that can be evaluated by python (ex: rand() * 2 * pi)\n   Correct syntax: python throwManyPhotons.py [filename (string)] [count (int)] [angle (float or lambda)] [verbose (bool)]\nMore information on https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/throwManyPhotons.html')
        raise
 
    # No argument, so the program will directly ask the user
    while True:
        try:
            angle = input("\nAngle [rand()*2*pi]: ")
            if angle == "": angle = "rand()*2*pi"; print("rand()*2*pi")
            float(eval(angle))
            return angle

        # Possible errors
        except KeyboardInterrupt:
            endProgram()
        except:
            print("\n[Error] Incorrect value. You must enter a float value that represent your angle in radian. You can also enter an expression that will be evaluated to get the angle. Ex: rand()*2*pi")
            raise



#--------------------------------------------------
# Ask target to user
#--------------------------------------------------



def askTarget():
    
    # Look at parameters given in argument in the python command
    try:
        Tx = argv[4]
        if Tx[0] == Tx[-1] in ["'",'"']: Tx = Tx[1:-2]
        eval(Tx)
        Ty = argv[5]
        if Ty[0] == Tx[-1] in ["'",'"']: Ty = Ty[1:-2]
        eval(Ty)

        return [Tx,Ty]

    # Possible errors
    except IndexError:
        pass
    except:
        print('\n[ERROR] "Tx" parameter not correct. It must be a number or an expression that can be evaluated by python (ex: rand() * 2 * pi)\n   Correct syntax: python throwManyPhotons.py [filename (string)] [count (int)] [angle (float or lambda)] [verbose (bool)]\nMore information on https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/throwManyPhotons.html')
        raise

    # No argument for Tx, so the program will directly ask the user
    lock = True
    while lock:
        try:
            Tx = input("\nTarget position X [rand()]: ")
            if Tx == "": Tx = "rand()"; print("rand()")
            float(eval(Tx))
            lock = False
        
        # Possible errors
        except KeyboardInterrupt:
            endProgram()
        except:
            print("\n[Error] Incorrect value. You must enter a float value that represent the X coordinate of the photon's target point (must be included beetween 0 and 1). You can also enter an expression that will be evaluated to get this coordinate. Ex: rand()")
    
    # No argument for Ty, so the program will directly ask the user
    lock = True
    while lock:
        try:
            Ty = input("\nTarget position Y [rand()]: ")
            if Ty == "": Ty = "rand()"; print("rand()")
            float(eval(Ty))
            lock = False

        # Possible errors
        except KeyboardInterrupt:
            endProgram()
        except:
            print("\n[Error] Incorrect value. You must enter a float value that represent the Y coordinate of the photon's target point (must be included beetween 0 and 1). You can also enter an expression that will be evaluated to get this coordinate. Ex: rand()")
    
    return [Tx,Ty]



#--------------------------------------------------
# Ask verbose to user
#--------------------------------------------------



def askVerbose():
    
    # Look at parameters given in argument in the python command
    try:
        verbose = argv[6].lower() in ["true","1"]
        return verbose

    # Possible errors
    except ValueError:
        print('\n[ERROR] "verbose" parameter must be set to "True" or "False".\n   Correct syntax: python throwManyPhotons.py [filename (string)] [count (int)] [angle (float or lambda)] [verbose (bool)]\nMore information on https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/throwManyPhotons.html')
        exit(1)
    except IndexError:
        pass

    # No argument, so the program will directly ask the user
    while True:
        try:
            verbose = input("\nVerbose? [no]: ")
            if verbose == "": verbose = "no"; print("no")
            if verbose.lower() in ["1", "true", "t","y","yes"]: return True
            elif verbose.lower() in ["0", "false", "f","n","no"]: return False
            else: print("\n[Error] Incorrect value. Just answer by 'yes' or 'no'\n")

        # Possible errors
        except KeyboardInterrupt:
            endProgram()



#--------------------------------------------------
# Start simulation
#--------------------------------------------------



def simulation(file = None, count = None, angle = None, target = [], verbose = None):

    # If no file(s) given in parameter of the function, get it/them from the user
    if file is None:
        grains, names = askGrains()

    # Else, get the grain from give file(s)
    else:
        if type(file) == str : file = [file]
        if "example.txt" in file:
            checkExampleGrain()
        grains = []
        names = []
        for i in file:
            grains.append(getFromFile("grains/" + i))
            names.append(splitext(i)[0].split("/")[-1].split("\\")[-1])
    if len(grains) == 0: endProgram(reason="noGrain")
    
    # Asking each parameter to the user if they was not given in parameter of this function
    if count is None : count = askCount()
    if angle is None : angle = askAngle()
    if target == [] : target = askTarget()
    if verbose is None : verbose = askVerbose()

    # Writing timeStats header
    if not isfile("timeStats.dat"):
        with open("timeStats.dat","a") as stats:
            stats.write("program_version number_of_photon grain_size number_of_threads time_ellapsed cpu_info\n")

    if not verbose:
        cpu = getCPU()
        stats = open("timeStats.dat","a")

    # Run simulation for each grain (1 grain = 1 file given in parameter)
    for i in range(len(grains)):
        print("\nRunning simulation n°",i+1,"/",len(grains),":",names[i])
        simuTime = time()
        throwManyPhotons(grains[i], count, angle = angle, target=target, verbose = verbose, name=names[i])
        simuTime = time() - simuTime

        # Adding data to timeStats if verbose is disabled (verbose mode can affect the simulation time)
        if not verbose:
            print("\nSimulation time: ", simuTime)
            stats.write("1.0 " + str(count) + " " + str(len(grains[i])) + " " + str(min(count,cpu_count())) + " " + str(round(simuTime,3)) + " " + cpu + "\n")

    if not verbose: stats.close()


#--------------------------------------------------
# Start simulation from this file
#--------------------------------------------------



if __name__ == "__main__":
    simulation()