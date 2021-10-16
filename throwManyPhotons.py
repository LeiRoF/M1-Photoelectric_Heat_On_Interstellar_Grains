from numpy import zeros
import matplotlib.pyplot as plt
from multiprocessing import Pool
from utils import CPUcount
import data

import throwOnePhoton

import numpy as np # do not remove even if seems to be unused
from numpy import pi, cos, sin, tan, exp, log, arcsin, arccos, arctan, sinh, cosh, tanh, arcsinh, arccosh, arctanh, sqrt, round # do not remove even if seems to be unused
from numpy.random.mtrand import rand # do not remove even if seems to be unused

def throwManyPhotons(grain, count, angle = 0, target = ["rand()","rand()"], verbose = False, name = "grain"):

    y = []
    events = zeros(4)

    makeVerbose = count == 1 and verbose == True
    minimalVerbose = count > 1 and verbose == True

    # Creating a list of parameters that will be used for simulations (1 simulation = 1 photon)
    list = [(grain,angle,target,makeVerbose,name,minimalVerbose)]*count

    cores = min(count,CPUcount())
    print("Executing simulation on ", cores , " threads")

    with Pool(cores) as p: 
        p.starmap(throwOnePhoton.throwOnePhoton,list) # Creating pool to parrallelize simulations

    print("")
    if verbose and count > 1: data.analyse(["results/" + name + ".dat"])

if __name__ == "__main__":
    import run
    run.simulation("example.txt",1000,"rand()*2*pi",["rand()","rand()"],True,temperature=28890,name="example")
    
    
    