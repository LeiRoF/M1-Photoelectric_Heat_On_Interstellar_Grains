
import matplotlib.pyplot as plt
from numpy.random.mtrand import rand
import numpy as np
import os
from multiprocessing import Pool

distrib = lambda n: np.exp(-n/100) / 100
minimum = 0
maximum = 100
precision = 1 # for a precision of 10^-precision (ex: precision = 3 for a precision of 10^-3, 5 for 10^-5 etc.)
number_of_test = 10000


# Generate a random variable according to a distribution
def random(f, min=0, max=1):
    if not callable(f): f = distrib # only used for tests
    x = min + rand()*(max-min)
    u = rand()
    while u > f(x):
        x = min + rand()*(max-min)
        u = rand()
    return x

# Return 2 lists, x and fx that can be easily plotted
def plot(distrib, min, max, step = 1):

    x = np.arange(min,max,step)
    fx = []
    for i in x: fx.append(distrib(i))

    return x,fx

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

    
