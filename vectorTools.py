import numpy as np

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

    dist = np.sqrt(x*x+y*y) # Shortest distance beetween my vector and the target point

    print("Distance = ", dist)

    return dist