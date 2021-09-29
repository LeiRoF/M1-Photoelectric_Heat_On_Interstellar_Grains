
import matplotlib.pyplot as plt
from numpy.random.mtrand import rand
import numpy as np

# Generate a random variable according to a distribution
def randomInDistrib(distrib, min=0, max=1):
    x = min + rand()*(max-min)
    u = rand()
    while u > distrib(x):
        x = min + rand()*(max-min)
        u = rand()
    return x

# Return 2 lists, x and fx that can be easily plotted
def plotDistrib(distrib, min, max, step = 1, name = None):

    x = np.arange(min,max,step)
    fx = []
    for i in x: fx.append(distrib(i))

    return x,fx


if __name__ == "__main__":

    min = 0
    max = 100
    precision = 1 # for a precision of 10^-precision (ex: precision = 3 for a precision of 10^-3, 5 for 10^-5 etc.)
    distrib = lambda n: np.exp(-n/100) / 100
    number_of_test = 100000

    x, fx = plotDistrib(distrib, min, max, 10**(-precision))
    dict = {}

    for i in x: dict.update({i:0})

    for i in range(number_of_test):
        r = round(randomInDistrib(distrib, min, max), precision)
        try:
            dict.update({r:dict[r]+1})
        except KeyError:
            pass

    f2x = []
    for i in dict.values(): f2x.append(i)

    plt.subplot(121)
    plt.plot(x,fx,'r--')
    plt.title('Distribution')
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.subplot(122)
    plt.bar(x, f2x)
    plt.title('Test of "randomInDistrib" function')
    plt.xlabel("x")
    plt.ylabel("n(x)")
    plt.show()

    
