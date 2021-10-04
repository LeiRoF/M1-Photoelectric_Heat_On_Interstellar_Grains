import throwManyPhotons
from sys import argv
import sys
import time
from multiprocessing import Pool
import grain as G
import os

from numpy import pi # do not remove even if seems to be unused
from numpy.random.mtrand import rand # do not remove even if seems to be unused

def programInterrupted():
    print("\nProgram interrupted.")
    sys.exit()

def simulation(file = None, count = None, angle = None, target = [], verbose = None):
    grains = []
    names = []
    try:
        if file is not None:
            grains.append(G.getFromFile("grains/" + file))
            name = os.path.splitext(file)[0].split("/")[-1].split("\\")[-1] # Getting file name
        else:
            file = argv[1]
            if file[0] == file[-1] in ["'",'"']: file = file[1:-2]
            grains.append(G.getFromFile("grains/" + file))
            names.append(os.path.splitext(file)[0])
    except FileNotFoundError:
        print('\n[ERROR] File "', argv[1] ,'" not found.\n   Correct syntax: python throwManyPhotons.py [filename (string)] [count (int)] [angle (float or lambda)] [verbose (bool)]\nMore information on https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/throwManyPhotons.html')
        sys.exit(1)
    
    except IndexError:
        lock = True
        while lock:
            try:
                list = ""
                list = input("\nSelect grain file (must be present in the 'grains' folder and not contain space or comma) or a file list separeted with a comma. Wirte 'all' to run simulation on every file in the 'grains' folder. You can generate one using: python grain.py\n\nYour file: ")
                if list.lower() in ["a", "all"]:
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
                programInterrupted()
            except:
                print("\n[Error] Cannot open or interprete your file '" + file + "' as a grain")
                #raise
    
    try:
        count = int(argv[2])
    except ValueError:
        print('\n[ERROR] "count" parameter must be an integer.\n   Correct syntax: python throwManyPhotons.py [filename (string)] [count (int)] [angle (float or lambda)] [verbose (bool)]\nMore information on https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/throwManyPhotons.html')
        sys.exit(1)
    except IndexError:
        lock = True
        while lock:
            count = input("\nNumber of photon: ")
            try:
                count = int(count)
                if count < 0 :
                    raise
                else:
                    lock = False
            except KeyboardInterrupt:
                programInterrupted()
            except:
                print("\n[Error] Incorrect value. You must enter a positive integer.")


    try:
        angle = argv[3]
        if angle[0] == angle[-1] in ["'",'"']: angle = angle[1:-2]
        eval(angle)
    except IndexError:
        lock = True
        while lock:
            angle = input("\nAngle: ")
            try:
                float(eval(angle))
                lock = False
            except KeyboardInterrupt:
                programInterrupted()
            except:
                print("\n[Error] Incorrect value. You must enter a float value that represent your angle in radian. You can also enter an expression that will be evaluated to get the angle. Ex: rand()*2*pi")
                raise
    except KeyboardInterrupt:
        programInterrupted()
    except:
        print('\n[ERROR] "angle" parameter not correct. It must be a number or an expression that can be evaluated by python (ex: rand() * 2 * pi)\n   Correct syntax: python throwManyPhotons.py [filename (string)] [count (int)] [angle (float or lambda)] [verbose (bool)]\nMore information on https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/throwManyPhotons.html')
        raise

    if target == []:
        try:
            Tx = argv[4]
            if Tx[0] == Tx[-1] in ["'",'"']: Tx = Tx[1:-2]
            eval(Tx)
            Ty = argv[5]
            if Ty[0] == Tx[-1] in ["'",'"']: Ty = Ty[1:-2]
            eval(Ty)
        except IndexError:
            lock = True
            while lock:
                Tx = input("\nTarget position X: ")
                try:
                    float(eval(Tx))
                    lock = False
                except:
                    print("\n[Error] Incorrect value. You must enter a float value that represent the X coordinate of the photon's target point (must be included beetween 0 and 1). You can also enter an expression that will be evaluated to get this coordinate. Ex: rand()")
            
            lock = True
            while lock:
                Ty = input("\nTarget position Y: ")
                try:
                    float(eval(Ty))
                    lock = False
                except:
                    print("\n[Error] Incorrect value. You must enter a float value that represent the Y coordinate of the photon's target point (must be included beetween 0 and 1). You can also enter an expression that will be evaluated to get this coordinate. Ex: rand()")
        
        except KeyboardInterrupt:
            programInterrupted()
        except:
            print('\n[ERROR] "Tx" parameter not correct. It must be a number or an expression that can be evaluated by python (ex: rand() * 2 * pi)\n   Correct syntax: python throwManyPhotons.py [filename (string)] [count (int)] [angle (float or lambda)] [verbose (bool)]\nMore information on https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/throwManyPhotons.html')
            raise
        
        target == [Tx,Ty]

    try:
        verbose = argv[6].lower() in ["true","1"]
    except ValueError:
        print('\n[ERROR] "verbose" parameter must be set to "True" or "False".\n   Correct syntax: python throwManyPhotons.py [filename (string)] [count (int)] [angle (float or lambda)] [verbose (bool)]\nMore information on https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/throwManyPhotons.html')
        sys.exit(1)
    except IndexError:
        try:
            lock = True
            while lock:
                verbose = input("\nVerbose? ")
                if verbose.lower() in ["1", "true", "t","y","yes"]: verbose = True; lock = False
                elif verbose.lower() in ["0", "false", "f","n","no"]: verbose = True; lock = False
                else: print("\n[Error] Incorrect value. Just answer by 'yes' or 'no'\n")
        except KeyboardInterrupt:
            programInterrupted()

    start = time.time()

    for i in range(len(grains)):
        throwManyPhotons.run(grains[i], count, angle = angle, target=target, verbose = verbose, name=names[i])
    
    end = time.time()
    print("Simulation time: ", end - start)

if __name__ == "__main__":
    simulation()