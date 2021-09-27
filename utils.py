
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
    dict={}
    for i in range(10000):
        #r = randomInDistrib(lambda x: numpy.exp(-x/100)/100,0,50)               # P = exp(-da/la) / la
        r = randomInDistrib(lambda x: 0.5*(1+numpy.tanh((x-8)/2)), 3, 15)       # Y = 0.5*(1+Th[(E-E0)/2])
        try:
            dict.update({int(r) : dict[int(r)]+1})
        except KeyError:
            dict.update({int(r) : 1})
        
    # Sorting dictionary
    dict = {k:v for k, v in sorted(dict.items(), key=lambda x: x[0])}


    plt.bar(range(len(dict)), list(dict.values()), align='center')
    plt.xticks(range(len(dict)), list(dict.keys()))
    plt.show()
    
    
