
import matplotlib.pyplot as plt
from numpy.random.mtrand import rand
import numpy as np
import os
from multiprocessing import Pool
import math

distrib = lambda n: np.exp(-n/100) / 100
minimum = 0
maximum = 100
precision = 1 # for a precision of 10^-precision (ex: precision = 3 for a precision of 10^-3, 5 for 10^-5 etc.)
number_of_test = 10000


# Generate a random variable according to a distribution

def randomV2(f,min=0,max=1,precision=0.001):

    x = np.arange(min,max,precision)

    p = f(x)
    return np.random.choice(x,p=p/np.sum(p))

def random(f, min=0, max=1, precision = 0.001):
    return randomV2(f,min,max,precision)

    if not callable(f): f = distrib # only used for tests
    x = min + rand()*(max-min)
    u = rand()
    while u > f(x):
        x = min + rand()*(max-min)
        u = rand()
    return x

# Return 2 lists, x and fx that can be easily plotted
def plot(f, min, max, step = 1):
    x = np.arange(min,max,step)
    return x,f(x)

if __name__ == "__main__":

    x, fx = plot(distrib, minimum, maximum, 10**(-precision))
    dict = {}

    for i in x: dict.update({i:0})

    poolParameters = [(None, minimum, maximum)]*number_of_test

    cores = max(os.cpu_count()-1,1)
    print("Testing distrib.random function on ", cores , " threads")
    with Pool(cores) as p:
        res = p.starmap(random,poolParameters)

    plt.subplot(121);   plt.plot(x,fx,'r--');   plt.title('Distribution');                          plt.xlabel("x");    plt.ylabel("f(x)")
    plt.subplot(122);   plt.hist(res,bins=50);        plt.title('Test of "random" function');    plt.xlabel("x");    plt.ylabel("n(x)")
    plt.show()

    
