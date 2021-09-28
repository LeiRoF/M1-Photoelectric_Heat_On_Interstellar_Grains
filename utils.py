
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

def getShortestDistance(vector,origin,point):
     # Getting perpendicular vector

    c = origin['x']; d = vector['x']
    g = origin['y']; h = vector['y']

    perpVect = {'x':-h,'y':d}

    a = point['x']; b = perpVect['x']
    e = point['y']; f = perpVect['y']

    """
    I consider 2 points
    - one on the direction defined by de "vector"
        -> r1 = (c,g) + B(d,h)
    - the other one in on the direction defined by "perpVect"
        -> r2 = (a,e) + A(b,f)

    It gives us an equation system:
        x = a + A*b  (1)
        x = c + B*d  (2)
        y = e + A*f  (3)
        y = g + B*h  (4)

    I solve this system to find A and B
    """
    
    # (1) = (2)
    # A = (B * d + c - a)/b   but I don't need to find A, I only need to know one of the two parameters A and B

    # (3) = (4) with the new expression of A
    B = ((a-c)/b + (g-e)/f) / (d/b - h/f)

    """
    With this A and B, r1 = r2 -> it's th intersection point. I will call it "i"
    """

    i = {'x':c+B*d,'y':g+B*h} # Intersection point

    x = i['x']-point['x']   # Distance x between intersection and target point
    y = i['y']-point['y']   # Distance y between intersection and target point

    dist = numpy.sqrt(x*x+y*y) # Shortest distance beetween my vector and the target point

    print("Distance = ", dist)

    return dist






if __name__ == "__main__":

    getShortestDistance({'x':1,'y':1},{'x':0,'y':5},{'x':0,'y':2})

    dict={}
    for i in range(10000):
        #r = randomInDistrib(lambda x: numpy.exp(-x/100)/100,0,50)               # P = exp(-da/la) / la
        r = randomInDistrib(lambda x: 0.5*(1+numpy.tanh((x-8)/2)), 0, 1000)       # Y = 0.5*(1+Th[(E-E0)/2])
        try:
            dict.update({int(r) : dict[int(r)]+1})
        except KeyError:
            dict.update({int(r) : 1})
        
    # Sorting dictionary
    dict = {k:v for k, v in sorted(dict.items(), key=lambda x: x[0])}


    plt.bar(range(len(dict)), list(dict.values()), align='center')
    plt.xticks(range(len(dict)), list(dict.keys()))
    plt.show()
    
    
