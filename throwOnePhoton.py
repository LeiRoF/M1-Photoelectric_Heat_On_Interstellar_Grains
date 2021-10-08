import matplotlib.pyplot as plt
import grain as G
import os
import distrib

import numpy as np # do not remove even if seems to be unused
from numpy import pi, cos, sin, tan, exp, log, arcsin, arccos, arctan, sinh, cosh, tanh, arcsinh, arccosh, arctanh, sqrt, round # do not remove even if seems to be unused
from numpy.random.mtrand import rand # do not remove even if seems to be unused

#T = 5_778 # temperature at the surface of the start (5000 for the sun)
T = 5*5_778 # 5 times our sun temperature
h = 6.626e-34 # Planck constant
c = 3e+8 # speed of light
k = 1.38e-23 # Boltzmann constant

def radiation(wav):
    global T
    global h
    global c
    global k
    a = 2.0*h*c**2
    b = h*c/(wav*k*T)
    intensity = a/ ( (wav**5) * (exp(b) - 1.0) )
    return intensity

def getPhotonEnergy(verbose = False):
    wavelenght_min = 1 # in nanometer
    wavelenght_max = 1000 # in nanometer
    l = distrib.random(radiation,wavelenght_min*10**-9,wavelenght_max*10**-9,10**-9) # Real star radiation in nanometer
    global h
    global c
    E = h * c / l * 6.242e+18

    with open("test.dat","a") as test:
        test.write(str(l) + '\n')
    
    if verbose:
        plt.subplot(221)
        x = np.arange(wavelenght_min,l*10**9*5)
        f = radiation
        plt.plot(x,f(x*10**-9),'r--',l*10**9,f(l),'bs')
        plt.title("Black-body radiation at T = " + str(T) + " K")
        plt.xlabel("Wavelenght (um)")
        plt.ylabel("Spectral radiance (W m−2 sr−1 Hz−1")
        plt.legend(["Planck's law","Photon with E = " + str(round(E,2)) + " eV"])

    return E

def isAbsorbedV2(grain, dist, Rx, Ry, Dx, Dy, step= 0.1):
    #print("-----------------------------------")
    #print(f"Rx={round(Rx,2)}, Ry={round(Ry,2)}, Dx={round(Dx,2)}, Dy={round(Dy,2)}, Size={grain.shape}")
    dim = grain.ndim
    if dim == 2:
        x,y = grain.shape
        N = sqrt(x*x + y*y)
    elif dim == 3:
        x,y,z = grain.shape
        N = sqrt(x*x + y*y + z*z)

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
        return True, Rx + travelInGrain*Dx, Ry + travelInGrain*Dy, hit




def isAbsorbed(grain, dist, Rx, Ry, Dx, Dy, step= 0.1):
    #return isAbsorbedV2(grain, dist, Rx, Ry, Dx, Dy, step)
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

def throwOnePhoton(grain, angle = 0, target = ["rand()","rand()"], verbose = False, name="grain", minimalVerbose = False):

    if verbose:
        plt.figure(num=name)

    if not os.path.isdir("results"):
        os.makedirs("results")
    result = open("results/" + name + ".dat","a")
    # E = 3+rand()*12 # Photon energy 3 < E < 15 eV
    E = getPhotonEnergy(verbose)

    Ei = G.getIonisationEnergy(grain)
    angle = eval(angle)

    (sizeX,sizeY) = grain.shape
    size = sqrt(sizeX*sizeX+sizeY*sizeY)

    
    # Deplacment vector
    Dx = cos(angle)
    Dy = sin(angle)

    # Origin
    Ox = 0 if Dx > 0 else sizeX - 1
    Oy = 0 if Dy > 0 else sizeY - 1

    # Targeted point (the photon trajectory touch this point)
    Tx = eval(target[0])*sizeX
    Ty = eval(target[1])*sizeY

    if Dx == 0 and Dy == 0: 
        Dx = 1.0

    if Dx == 0: A = (Ty - Oy)/Dy
    elif Dy == 0: A = (Tx - Ox)/Dx
    else: A = min((Tx - Ox)/Dx, (Ty - Oy)/Dy)

    # Coordinates of the photon when it appear on the matrix
    Rx = Tx - Dx * A
    Ry = Ty - Dy * A

    if verbose:
        print("\n  - A photon appeared at Rx=", round(Rx,3), ", Ry=", round(Ry,3))
        print("  - The photon's direction is: Dx=", round(Dx,3), ", Dy=", round(Dy,3), " (angle = ", round(angle/pi,3), "pi rad)")
        print("  - It has an energy of ", round(E,3), " eV")
    
    # Getting random distance using the probability P=exp(-da/la) / la
    la = 100 # 10^-6 cm = 100 angstrom -> 100 pixels
    da = distrib.random(lambda x: exp(-x/la) / la,0,100)

    # Getting absorbtion position
    absorbed, Rx, Ry, hitPos = isAbsorbed(grain, da, Rx, Ry, Dx, Dy)
    
    """
    if absorbed:
        print(f"V1 Absorbed=True at Rx={round(Rx,2)}, Ry={round(Ry,2)}")
    else:
        print("V1 Absorbed=False")
    """

    """
    If the photon didn't hit the grain
    """

    if hitPos == []:
        if verbose: print("X - But... it missed the grain")
        if minimalVerbose: print("0",end="")
        result.write(str(-1) + '\n')
        return -1

    """
    If the photon entered in the grain
    """

    if verbose:
        print("0 - It hit the grain!") #at Rx=", hitPos[0], ", Ry=", hitPos[0])
        print("  - In these conditions, the photon will travel ", round(da,3), "angstroms through the grain")
        xaxis, fx = distrib.plot(lambda x: exp(-x/la) / la, 0, int(size+1), int(size+1)/1000)
        plt.subplot(222)
        plt.plot(xaxis,fx,'r--',da,exp(-da/la) / la,'bs')
        plt.title("Distance traveled by photon in the grain")
        plt.xlabel("Distance (da)")
        plt.ylabel("Probability amplitude distribution (P)")
        plt.legend(["P=exp(-da/la) / la","Random da"])

    """
    If the photon passed through the grain
    """

    if not absorbed: 
        if verbose: print("X - And... this distance was too high, it passed trhough the grain :/")
        result.write(str(-2) + '\n')
        plt.show()
        if minimalVerbose: print("1",end="")
        return -2
    
    """
    If the photon is absorbed
    """

    if verbose: print("0 - Oh, it was absorbed at Rx=", Rx, " Ry=", Ry)
    E0 = 8
    electron_emitted = rand() < 0.5*(1+tanh((E-E0)/2)) # Emit electron with probability Y=0.5*(1+Th[(E-E0)/2])
    if verbose:
        print("  - In these conditions, the probability of emitting an electron is ", round(0.5*(1+tanh((E-E0)/2)),3))
        xaxis, fx = distrib.plot(lambda x: 0.5*(1+tanh((x-E0)/2)), 0, max(15,E), max(15,E)/100)
        plt.subplot(223)
        plt.plot(xaxis,fx,'r--',E,0.5*(1+tanh((E-E0)/2)),'bs')
        plt.title("Electron emission")
        plt.xlabel("Energy of the photon (E)")
        plt.ylabel("Probability (Y)")
        plt.legend(["Y=0.5*(1+Th[(E-E0)/2])","Current situation"])

    """
    If no electron emitted
    """

    if not electron_emitted:
        if verbose: print("X - No electron was emitted :/")
        result.write(str(-3) + '\n')
        plt.show()
        if minimalVerbose: print("2",end="")
        return -3
            
    """
    If an electron is emitted
    """

    # Direction of the electron
    Dx = -1 + rand()*2
    Dy = -1 + rand()*2
    normalisationFactor = 1 / (sqrt(Dx*Dx+Dy*Dy))
    Dx = Dx*normalisationFactor
    Dy = Dy*normalisationFactor 

    if verbose:
        print("0 - An electron has been emitted at Rx=", Rx+0.5, " , Ry=", Ry+0.5)
        print("  - The electron's direction is: Dx=", round(Dx,3), " , Dy=", round(Dy,3))

    # Getting random distance traveld by the electron using the probability P=exp(-de/le) / le
    le = 10 # 10^-6 cm = 100 angstrom -> 100 pixels
    de = distrib.random(lambda x: exp(-x/le) / le,0,100)
    if verbose:
        print("  - In these conditions, the electron will travel ", round(de,3), "angstroms through the grain")

        xaxis, fx = distrib.plot(lambda x: exp(-x/le) / le, 0, int(size+1), int(size+1)/1000)
        plt.subplot(224)
        plt.plot(xaxis,fx,'r--',de,exp(-de/le) / le,'bs')
        plt.title("Distance traveled by electron in the grain")
        plt.xlabel("Distance (de)")
        plt.ylabel("Probability amplitude distribution (P)")
        plt.legend(["P=exp(-de/le)/le","Random de"])

    # Getting absorbtion position
    absorbed, Rx, Ry, hitPos = isAbsorbed(grain, de, Rx, Ry, Dx, Dy)

    """
    if absorbed:
        print(f"V1 Absorbed=True at Rx={round(Rx,2)}, Ry={round(Ry,2)}")
    else:
        print("V1 Absorbed=False")
    """

    """
    If the electron was re-absorbed
    """

    if absorbed:
        if verbose: print("X - The electron was re-absorbed at position: Rx=", round(Rx,3), ", Ry=", round(Ry,3))
        result.write(str(-4) + '\n')
        plt.show()
        if minimalVerbose: print("3",end="")
        return -4
    
    """
    If the electron get ou the grain
    """

    if verbose: print("0 - The electron was ejected with a kinetic energy of ", E - Ei, "eV")
    result.write(str(E - Ei) + '\n')
    plt.show()
    if minimalVerbose: print("\nElectron excaped with " + str(round(E-Ei,3)) + " eV\n",end="")
    return  E - Ei

if __name__ == "__main__":

    import run
    run.simulation("example.txt",1,"rand()*2*pi",["rand()","rand()"],True)
    