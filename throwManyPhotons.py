from numpy import zeros
import matplotlib.pyplot as plt
from throwOnePhoton import throwOnePhoton
from multiprocessing import Pool
from os import cpu_count

import numpy as np # do not remove even if seems to be unused
from numpy import pi, cos, sin, tan, exp, ln, arcsin, arccos, arctan, sinh, cosh, tanh, arcsinh, arccosh, arctanh, sqrt, round # do not remove even if seems to be unused
from numpy.random.mtrand import rand # do not remove even if seems to be unused

def throwManyPhotons(grain, count, angle = 0, target = ["rand()","rand()"], verbose = False, name = "grain"):

    y = []
    events = zeros(4)

    makeVerbose = count == 1 and verbose == True
    minimalVerbose = count > 1 and verbose == True
    list = [(grain,angle,target,makeVerbose,name,minimalVerbose)]*count
    cores = min(count,cpu_count())
    print("Executing simulation on ", cores , " threads")
    with Pool(cores) as p:
        p.starmap(throwOnePhoton,list)
        

if __name__ == "__main__":
    import run
    run.simulation("example.txt",1000,"rand()*2*pi",["rand()","rand()"],True)
    
    
    