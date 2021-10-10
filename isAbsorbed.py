import numpy as np

def isAbsorbedV2(grain, dist, Rx, Ry, Dx, Dy, step= 0.1):
    #print("-----------------------------------")
    #print(f"Rx={round(Rx,2)}, Ry={round(Ry,2)}, Dx={round(Dx,2)}, Dy={round(Dy,2)}, Size={grain.shape}")
    dim = grain.ndim
    if dim == 2:
        x,y = grain.shape
        N = np.sqrt(x*x + y*y)
    elif dim == 3:
        x,y,z = grain.shape
        N = np.sqrt(x*x + y*y + z*z)

    N = int((N+1)/step)

    t = np.arange(0,N)
    t = np.array((t,t)).T # Array (t,t) avec t allant de 0 à N-1, représentant les différents "instants" auxquels on s'intéressera à la position de la particule

    ones = np.ones(N)
    r = np.array((ones,ones)).T * (Rx,Ry) # Array (Rx,Ry) représentant la position initiale de la particule
    v = np.array((ones,ones)).T * (Dx,Dy)*step # Array (Dx,Dy) représentant la direction de la particule (le vecteur est normalisé)

    traj = r + v*t # Calcul la position de la particule à chaque instant

    traj = traj.astype(int) # Convertit cette position en indice dans la matrice

    traj = traj[((traj[:,0] >= 0) & (traj[:,0] < x))] # Filtre les indices en dehors de la matrice
    traj = traj[((traj[:,1] >= 0) & (traj[:,1] < y))]

    traj = grain[traj[:,0],traj[:,1]] # Récupère une array contenant la valeur des différents pixels rencontrés sur la trajectoire
    #print(traj)

    travelInGrain = np.count_nonzero(traj == 1)*step # Compte le nombre de pixels de valeur 1 rencontrés sur la trajectoire (et donc la distance parcourue au sein du grain)
    
    #print(f"Travel={round(travelInGrain,2)} > Dist={round(dist,2)}")

    hit = False
    if travelInGrain > 0: hit = True

    if travelInGrain > dist:
        #print("")
        #t = dist
        #print(f"V2 Absorbed=True at Rx={round(Rx + t*Dx,2)}, Ry={round(Ry + t*Dy,2)}")
        return True, Rx + dist*Dx, Ry + dist*Dy, hit
    else:
        #t = travelInGrain
        #print(f"V2 Absorbed=False")
        return False, Rx + travelInGrain*Dx, Ry + travelInGrain*Dy, hit




def isAbsorbed(grain, dist, Rx, Ry, Dx, Dy, step= 0.1):
    return isAbsorbedV2(grain, dist, Rx, Ry, Dx, Dy, step)

    hitPos = []

    traj = []

    (sizeX,sizeY) = grain.shape
    
    da = dist

    while 0 <= Rx and Rx < sizeX and 0 <= Ry and Ry < sizeY and dist > 0:

        if grain[int(Rx)][int(Ry)]:
            if hitPos == []:
                hitPos = [Rx,Ry]
            dist -= step
        traj.append(grain[int(Rx)][int(Ry)])
        Rx += step*Dx
        Ry += step*Dy

    traj = np.array(traj)
    travelInGrain = np.count_nonzero(traj == 1)*step # Compte le nombre de pixels de valeur 1 rencontrés sur la trajectoire (et donc la distance parcourue au sein du grain)

    #print(traj)
    #print(f"Travel={round(travelInGrain,2)} > Dist={round(da,2)}")
    if dist <= 0:
        return True, Rx, Ry, hitPos
    else:
        return False, Rx, Ry, hitPos
