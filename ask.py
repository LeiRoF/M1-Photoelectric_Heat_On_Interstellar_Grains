from utils import endProgram
import grain
from os.path import splitext
from os import listdir
from sys import argv, exit

import numpy as np # do not remove even if seems to be unused
from numpy import pi, cos, sin, tan, exp, log, arcsin, arccos, arctan, sinh, cosh, tanh, arcsinh, arccosh, arctanh, sqrt, round # do not remove even if seems to be unused
from numpy.random.mtrand import rand # do not remove even if seems to be unused

n = 1 # argv index


#--------------------------------------------------
# Ask 3D to user
#--------------------------------------------------



def in3D():
    
    # Look at parameters given in argument in the python command
    try:
        global n
        in3D = argv[n].lower() in ["3","3d","1", "true", "t","y","yes"]
        n += 1
        return False #in3D

    # Possible errors
    except ValueError:
        print('\n[ERROR] "in3D" parameter must be set to "True" or "False".\n   Correct syntax: python grain.py [3D] [size] [sigma_dens] [beta]\nMore information on https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/grain.html')
        exit(1)
    except IndexError:
        pass

    # No argument, so the program will directly ask the user
    while True:
        try:
            print("\n3D [no]: no (coming soon)")
            in3D = "False"
            #in3D = input("\n3D [no]: ")
            if in3D == "": in3D = "no"; print("no")
            if in3D.lower() in ["3","3D","1", "true", "t","y","yes"]: return True
            elif in3D.lower() in ["2","2d","0", "false", "f","n","no"]: return False
            else: print("\n[Error] Incorrect value. Just answer by 'yes' or 'no'\n")

        # Possible errors
        except KeyboardInterrupt:
            endProgram()

    

#--------------------------------------------------
# Ask name to user
#--------------------------------------------------



def name():
    illegal_character = ["/","\\",":","*","?",'"',"<",">","|"]
    try:
        global n
        name = argv[n]
        if name[0] == name[-1] in ["'",'"']: name = name[1:-2]
        for i in illegal_character:
            if i in name:
                print("[Error] Illegal caracter in the name.")
                exit()
        n += 1
        return name.replace(" ","_")
    except IndexError:
        pass

    while True:
        name = input("\nEnter the name of your simulation [example]:")
        if name == "":
            return "example"
        if name[0] == name[-1] in ["'",'"']: name = name[1:-2]
        illegal = False
        for i in illegal_character:
            if i in name:
                print("[Error] Illegal caracter in the name.")
                illegal = True
                break
        if not illegal:
            return name.replace(" ","_")
        


#--------------------------------------------------
# Ask grain size to user
#--------------------------------------------------



def grainSize():
    # Look at parameters given in argument in the python command
    try:
        global n
        N = int(argv[n])
        n += 1
        return N

    # Possible errors
    except ValueError:
        print("\n[ERROR] 'Size' must be a positive integer.\n   Correct syntax: python grain.py [3D] [size] [sigma_dens] [beta]\nMore information on https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/grain.html")
        exit()
    except IndexError:
        pass

    # No argument, so the program will directly ask the user
    while True:
        try:
            N = input("\nSize of the grain (int>0) [100]: ")
            if N == "": N = 100; print(N)
            N = int(N)
            return N
        except ValueError:
            print("Invalid value.")
        except KeyboardInterrupt:
            endProgram()
    


#--------------------------------------------------
# Ask sigma density to user
#--------------------------------------------------



def sigmaDens():
    # Look at parameters given in argument in the python command
    try:
        global n
        sigma_dens = float(argv[n])
        n += 1
        return sigma_dens

    # Possible errors
    except ValueError:
        print("\n[ERROR] 'Beta_dens' must be a positive float.\n   Correct syntax: python grain.py [3D] [size] [sigma_dens] [beta]\nMore information on https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/grain.html")
        exit()
    except IndexError:
        pass

    # No argument, so the program will directly ask the user
    while True:
        try:
            sigma_dens = input("\nWidth of the density distribution (float>0) [1.0]: ")
            if sigma_dens == "": sigma_dens = 1.0; print(sigma_dens)
            sigma_dens = float(sigma_dens)
            return sigma_dens
        except ValueError:
            print("Invalid value")
        except KeyboardInterrupt:
            endProgram()
    


#--------------------------------------------------
# Ask beta parameter to user
#--------------------------------------------------



def beta():
    # Look at parameters given in argument in the python command
    try:
        global n
        beta = float(argv[n])
        n += 1
        return beta

    # Possible errors
    except ValueError:
        print("\n[ERROR] 'Beta' must be a positive float.\n   Correct syntax: python grain.py [3D] [size] [sigma_dens] [beta]\nMore information on https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/grain.html")
        exit()
    except IndexError:
        pass

    # No argument, so the program will directly ask the user
    while True:
        try:
            beta = input("\nSlope of the power spectrum (float>0) [default:3.0]: ")
            if beta == "": beta = 3.0; print(beta)
            beta = float(beta)
            return beta
        except ValueError:
            print("Invalid value")
        except KeyboardInterrupt:
            endProgram()
    


#--------------------------------------------------
# Ask data file to user
#--------------------------------------------------



def dataFile():
    # Look at parameters given in argument in the python command
    try:
        global n
        file = argv[n]
        n += 1
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
                for file in listdir("./results/"):
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
            print("\n[Error] Cannot open or interprete your file '" + file + "' as a data file")



#--------------------------------------------------
# Ask grain to user
#--------------------------------------------------



def grains():
    grains = []
    names = []
    # Look at parameters given in argument in the python command
    try:
        global n
        file = argv[n]
        n += 1
        # Removing list delimiter
        if (file[0:1] == "'[" and file[-2:-1] == "]'") or (file[0:1] == '"[' and file[-2:-1] == ']"'): file = file[2:-3]
        
        list = file.split(",")
        for file in list:
            # Removing files delimiters
            if file[0] == file[-1] in ["'",'"']: file = file[1:-2]
            grains.append(grain.getFromFile("grains/" + file))
            names.append(splitext(file)[0])
        return grains,names

    # Possible errors
    except FileNotFoundError:
        print('\n[ERROR] File "', argv[n] ,'" not found.\n   Correct syntax: python run.py [filename (string)] [count (int)] [angle (float or lambda)] [verbose (bool)]\nMore information on https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/run.html')
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
                grain.checkExampleGrain()
                grains.append(grain.getFromFile("grains/example.txt"))
                names.append("example") # Getting file name
                print("\nSelected file(s):")
                print(" - example.txt")
                return grains, names

            # If the user want to use all grains
            elif list.lower() in ["a", "all"]:
                print("\nSelected file(s):")
                for file in listdir("./grains/"):
                    print(" - " + file)
                    grains.append(grain.getFromFile("grains/" + file))
                    names.append(splitext(file)[0]) # Getting file name
                return grains, names

            # If the user specify each files
            else:
                if (list[0:1] == "'[" and list[-2:-1] == "]'") or (list[0:1] == '"[' and list[-2:-1] == ']"'): list = list[2:-3]
                list.replace(" ","").split(",")
                if type(list) is str: list = [list]
                print("\nSelected file(s):")
                for file in list:
                    if file[-4:] != ".txt":
                        file += ".txt"
                    print(" - " + file)
                    grains.append(grain.getFromFile("grains/" + file))
                    names.append(splitext(file)[0])
                return grains, names

        # Possible errors
        except KeyboardInterrupt:
            endProgram()
        except:
            print("\n[Error] Cannot open or interprete your file '" + file + "' as a grain")
            #raise



#--------------------------------------------------
# Ask star temperature to user
#--------------------------------------------------



def temperature():

    # Look at parameters given in argument in the python command
    try:
        global n
        temperature = float(argv[n])
        if temperature < 0: temperature = -temperature
        n += 1
        return temperature

    # Possible errors
    except ValueError:
        print('\n[ERROR] "temperature" parameter must be a positive float.\n   Correct syntax: python run.py [name (string)] [filename (string)] [temperature (float)] [count (int)] [angle phi (float or lambda)] [angle theta (float or lambda)] [target x (float)] [target y (float)] [target z (float)] [verbose (bool)]\nMore information on https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/run.html')
        exit(1)
    except IndexError:
        pass

    # No argument, so the program will directly ask the user
    while True:
        try:
            temperature = input("\nTemperature of the star in Kelvin [28 890]: ")
            if temperature == "": temperature = 28890; print("28890 (5 times the temperature of our sun)")
            temperature = float(temperature)
            if temperature < 0 :
                raise
            else:
                return temperature
    
        # Possible errors
        except KeyboardInterrupt:
            endProgram()
        except:
            print("\n[Error] Incorrect value. You must enter a positive integer.")



#--------------------------------------------------
# Ask count to user
#--------------------------------------------------



def count():

    # Look at parameters given in argument in the python command
    try:
        global n
        count = int(argv[n])
        n += 1
        return count

    # Possible errors
    except ValueError:
        print('\n[ERROR] "count" parameter must be an integer.\n   Correct syntax: python run.py [name (string)] [filename (string)] [temperature (float)] [count (int)] [angle phi (float or lambda)] [angle theta (float or lambda)] [target x (float)] [target y (float)] [target z (float)] [verbose (bool)]\nMore information on https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/run.html')
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



def angle():
    angle = ["rand()*2*pi","rand()*pi"]

    # Look at parameters given in argument in the python command
    try:
        global n
        phi = argv[n]
        n += 1
        if phi[0] == angle[-1] in ["'",'"']: phi = phi[1:-2]
        phi.replace(" ","")
        eval(phi)
        angle[0] = phi

    # Possible errors
    except IndexError:
        pass
    except:
        print('\n[ERROR] "phi" parameter not correct. It must be a number or an expression that can be evaluated by python (ex: rand()*2*pi)\n   Correct syntax: python run.py [name (string)] [filename (string)] [temperature (float)] [count (int)] [angle phi (float or lambda)] [angle theta (float or lambda)] [target x (float)] [target y (float)] [target z (float)] [verbose (bool)]\nMore information on https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/run.html')
        raise
 
    # No argument, so the program will directly ask the user
    lock = True
    while lock:
        try:
            phi = input("\nAngle phi [rand()*2*pi]: ")
            phi.replace(" ","")
            if phi== "": phi = "rand()*2*pi"; print("rand()*2*pi")
            float(eval(phi))
            lock = False
            angle[0] = phi

        # Possible errors
        except KeyboardInterrupt:
            endProgram()
        except:
            print("\n[Error] Incorrect value. You must enter a float value that represent your angle phi in radian. You can also enter an expression that will be evaluated to get the angle. Ex: rand()*2*pi")
            raise


    # Look at parameters given in argument in the python command
    try:
        theta = argv[n]
        n += 1
        if theta[0] == theta[-1] in ["'",'"']: theta = theta[1:-2]
        theta.replace(" ","")
        eval(theta)
        angle[1] = theta

    # Possible errors
    except IndexError:
        pass
    except:
        print('\n[ERROR] "tehta" parameter not correct. It must be a number or an expression that can be evaluated by python (ex: rand()*pi)\n   Correct syntax: python run.py [name (string)] [filename (string)] [temperature (float)] [count (int)] [angle phi (float or lambda)] [angle theta (float or lambda)] [target x (float)] [target y (float)] [target z (float)] [verbose (bool)]\nMore information on https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/run.html')
        raise
 
    # No argument, so the program will directly ask the user
    lock = True
    while lock:
        try:
            theta = input("\nAngle theta [rand()*pi]: ")
            theta.replace(" ","")
            if theta == "": theta = "rand()*pi"; print("rand()*pi")
            float(eval(theta))
            lock = False
            angle[1] = theta

        # Possible errors
        except KeyboardInterrupt:
            endProgram()
        except:
            print("\n[Error] Incorrect value. You must enter a float value that represent your angle theta in radian. You can also enter an expression that will be evaluated to get the angle. Ex: rand()*2*pi")
            raise

    return angle



#--------------------------------------------------
# Ask target to user
#--------------------------------------------------



def target():
    
    # Look at parameters given in argument in the python command
    try:
        global n
        Tx = argv[n]
        n += 1
        if Tx[0] == Tx[-1] in ["'",'"']: Tx = Tx[1:-2]
        Tx.replace(" ","")
        eval(Tx)
        Ty = argv[n]
        n+=1
        if Ty[0] == Tx[-1] in ["'",'"']: Ty = Ty[1:-2]
        Ty.replace(" ","")
        eval(Ty)

        return [Tx,Ty]

    # Possible errors
    except IndexError:
        pass
    except:
        print('\n[ERROR] "Tx" parameter not correct. It must be a number or an expression that can be evaluated by python (ex: rand() * 2 * pi)\n   Correct syntax: python run.py [name (string)] [filename (string)] [temperature (float)] [count (int)] [angle phi (float or lambda)] [angle theta (float or lambda)] [target x (float)] [target y (float)] [target z (float)] [verbose (bool)]\nMore information on https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/run.html')
        raise

    # No argument for Tx, so the program will directly ask the user
    lock = True
    while lock:
        try:
            Tx = input("\nTarget position X [rand()]: ")
            Tx.replace(" ","")
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
            Ty.replace(" ","")
            if Ty == "": Ty = "rand()"; print("rand()")
            float(eval(Ty))
            lock = False

        # Possible errors
        except KeyboardInterrupt:
            endProgram()
        except:
            print("\n[Error] Incorrect value. You must enter a float value that represent the Y coordinate of the photon's target point (must be included beetween 0 and 1). You can also enter an expression that will be evaluated to get this coordinate. Ex: rand()")
    
    # No argument for Ty, so the program will directly ask the user
    lock = True
    while lock:
        try:
            Tz = input("\nTarget position Z. Do not take care to this question if your grain is in 2D. Tz will be set to 0 if in this case [rand()]: ")
            Tz.replace(" ","")
            if Tz == "": Tz = "rand()"; print("rand()")
            float(eval(Tz))
            lock = False

        # Possible errors
        except KeyboardInterrupt:
            endProgram()
        except:
            print("\n[Error] Incorrect value. You must enter a float value that represent the Z coordinate of the photon's target point (must be included beetween 0 and 1). You can also enter an expression that will be evaluated to get this coordinate. Ex: rand()")
    
    return [Tx,Ty,Tz]



#--------------------------------------------------
# Ask verbose to user
#--------------------------------------------------



def verbose():
    
    # Look at parameters given in argument in the python command
    try:
        global n
        verbose = argv[n].lower() in ["1", "true", "t","y","yes"]
        n += 1
        return verbose

    # Possible errors
    except ValueError:
        print('\n[ERROR] "verbose" parameter must be set to "True" or "False".\n   Correct syntax: python run.py [name (string)] [filename (string)] [temperature (float)] [count (int)] [angle phi (float or lambda)] [angle theta (float or lambda)] [target x (float)] [target y (float)] [target z (float)] [verbose (bool)]\nMore information on https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/run.html')
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
