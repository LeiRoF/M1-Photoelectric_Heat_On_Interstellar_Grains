
import matplotlib.pyplot as plt
from numpy.random.mtrand import rand
import numpy

def randomInDistrib(distrib,min=0,max=1):
    x = min + rand()*(max-min)
    u = rand()
    while u > distrib(x):
        x = min + rand()*(max-min)
        u = rand()
    return x


if __name__ == "__main__":
    list = []
    max = 1000
    for i in range(max):
        list.append(0)
    for i in range(10000):
        r = randomInDistrib(lambda x: numpy.exp(-x/100)/100,0,max)
        list[int(r)] += 1
    plt.plot(list)
    plt.show()
    
