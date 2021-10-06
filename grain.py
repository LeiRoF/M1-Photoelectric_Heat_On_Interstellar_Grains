from PIL.Image import new
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import pylab as pl
import os
from GRF_routines import addGRF
from multiprocessing import Pool

def reduceMatrix(grain):

    mask = grain == 0
    rows = np.flatnonzero((~mask).sum(axis=1))
    cols = np.flatnonzero((~mask).sum(axis=0))

    crop = grain[rows.min():rows.max()+1, cols.min():cols.max()+1]


    return squarify(crop)

def squarify(grain,val = 0):
    (a,b)=grain.shape
    if a>b:
        padding=((0,0),(0,a-b))
    else:
        padding=((0,b-a),(0,0))
    return np.pad(grain,padding,mode='constant',constant_values=val)

def askParameters(N, sigma_dens, beta):
    # size of the grain image (default = 100)
    if not N:
        lock = True
        while lock:
            N = input("Size of the grain (int>0, default:100): ")
            try:
                N = int(N)
                lock = False
            except ValueError:
                print("Invalid value")

    # Width of the density distribution (default = 1.0)
    if not sigma_dens:
        lock = True
        while lock:
            sigma_dens = input("Width of the density distribution (float>0, default:1.0): ")
            try:
                sigma_dens = float(sigma_dens)
                lock = False
            except ValueError:
                print("Invalid value")

    # Slope of the power spectrum (=probability density function=PDF) for k>Kmin (default = 3.0)
    if not beta:
        lock = True
        while lock:
            beta = input("Slope of the power spectrum (float>0, default:3.0): ")
            try:
                beta = float(beta)
                lock = False
            except ValueError:
                print("Invalid value")

    return N, sigma_dens, beta

def generate3D(N = None, sigma_dens = None, beta = None, path = "./grains/", doplot = 0, writeFile = True, verbose = False, name = None):
    N, sigma_dens, beta = askParameters(N, sigma_dens, beta)
    if N % 2 == 1: N = N+1

    poolParameter = []
    for i in range(0,N+1):
        size = int(round(N*np.sin(np.arccos(2*(i)/N - 1)),0))
        print(i,size)
        if size > 0:
            if size % 2 == 1: size = size+1
            poolParameter.append((size, sigma_dens, beta, path, 0, False, False, i))

    cores = max(os.cpu_count()-1,1)
    print("Generating grain on ", cores , " threads")
    with Pool(cores) as p:
        grain = p.starmap(generate,poolParameter)

    grain.sort(key = lambda x: x[0])
    grain = [np.ndarray.tolist(x[1]) for x in grain]


    for i in range(len(grain)):
        diff = int((N - len(grain[i]))/2)
        for j in range(len(grain[i])):
            grain[i][j] = [0]*diff + [int(k) for k in grain[i][j]] + [0]*diff
        grain[i] = [[0]*N]*diff + grain[i] + [[0]*N]*diff
    
    diff = N - len(grain)

    for i in range(diff):
        grain = [[[0]*N]*N] + grain
        if diff%2==0: grain = grain + [[[0]*N]*N]
    
    grain = np.array(grain)

    for section in grain:
        for row in section:
            print(row)
        print("")

    if writeFile:
        if not os.path.isdir(path):
            os.makedirs(path)

        if name is None:
            name = "3D-N{}_S{}p{}_B{}p{}.txt".format(int(N),int(sigma_dens),int(sigma_dens*10%10),int(beta),int(beta*10%10))
        else:
            name = name + ".txt"

        with open(path + name,"w+") as file:
            for section in grain:
                for row in section:
                    file.write(" ".join([str(x) for x in row]) + "\n")
                    
    return
    

# Identify the pixels attached to the main region
def group(grain, x0,y0, N, doplot = 0):
    # Warning: no precaution for edges
    goon = 1
    progress = np.zeros(np.shape(grain))
    progress[x0,y0] = 2
    if (doplot==2): pl.ion()
    while (goon==1):
        goon = 0
        m = np.nonzero(progress==2)   # search last included friends
        for i in range(len(m[0])):
            i1, j1 = m[0][i], m[1][i]
            # Search only touching pixels
            if (0):
                searchind = [[i1+1,j1], [i1+1,j1-1], [i1,j1-1], [i1-1,j1-1], \
                            [i1-1,j1], [i1-1,j1+1], [i1,j1+1], [i1+1,j1+1]]
            # Search touching pixels + 1
            if (1):
                searchind = [[i1+1,j1], [i1+1,j1-1], [i1,j1-1], [i1-1,j1-1], \
                            [i1-1,j1], [i1-1,j1+1], [i1,j1+1], [i1+1,j1+1], \
                            [i1+2,j1], [i1+2,j1-1], [i1+2,j1-2], [i1+1,j1-2], \
                            [i1,j1-2], [i1-1,j1-2], [i1-2,j1-2], [i1-2,j1-1], \
                            [i1-2,j1], [i1-2,j1+1], [i1-2,j1+2], [i1-1,j1+2], \
                            [i1,j1+2], [i1+1,j1+2], [i1+2,j1+2], [i1+2,j1+1]]
            for inds in searchind:
                inds = np.asarray(inds)
                if ((np.all(inds>=0)) & (np.all(inds<N))):
                    if (grain[inds[0],inds[1]]==1):
                        if (progress[inds[0],inds[1]]==0): # not found before
                            progress[inds[0],inds[1]] = 3   # 3 for freshly identified
                            goon = 1
        if (doplot==2): pl.imshow(progress, origin='low', cmap='bone', interpolation='nearest')
        if (doplot==2): pl.pause(0.0001)
        progress[m] = 1
        progress[np.nonzero(progress==3)] = 2

    progress[np.nonzero(progress>1)] = 1
    pl.ioff()
    return progress

def generate(N = None, sigma_dens = None, beta = None, path = "./grains/", doplot = 0, writeFile = True, verbose = False, id3D = 0, name = None):
    """
    N.B.: the grains are generated randomly => a single grain is not necessarily 
        representative of the fractal parameters. Only a statistically significant
        sample can provide a reliable view of the underlying properties. 
    """
    N, sigma_dens, beta = askParameters(N, sigma_dens, beta)
    if N % 2 == 1: N = N+1

    # Tunable parameters
    Kmin = 3             # Minimum wavenumber for PDF slope = beta
    beta_in = 4          # Slope of PDF between k=0 and Kmin
    Npad = 0           # Padding around the map to get rid of the peak near k=0
    Adens = 1.           # Mean density - should not impact dust grain
    # doplot -> Visual check of grain calculation: 0= desactivated, 1= only final plot, 2= animation of search for the main group + final plot


    # while loop to make sure the peak is sufficiently close to the center of the cube
    tol = 0.4            # Tolerance for location of the density maximum - between 0 (very tolerant) and 0.49999 (very tough)
    mmax = [0,0]
    ii = 0
    while ((mmax[0]<N*tol) | (mmax[0]>N*(1-tol)) | (mmax[1]<N*tol) | (mmax[1]>N*(1-tol))):

        # Build a fractal cube using Gaussian Random Field
        cube = np.zeros((N,N))
        cube = addGRF(cube, sigma_dens, Adens, beta, Npad, Kmin, beta_in)

        # Search the location of the max value
        mmax = np.nonzero(cube==np.amax(cube))
        if verbose : print(mmax)
        ii += 1
        if (ii>1000):
            print("Failed generating a GRF with this tolerance value:", tol)
            print("Try a lower value. It should be between 0 (very tolerant) and 0.49999 (very tough).")
            exit()


    # Roll the cube to put the max at the center
    #cube = np.roll(cube, N/2-mmax[0][0], axis=0)
    #cube = np.roll(cube, N/2-mmax[1][0], axis=1)

    # Apodize the cube
    I, J = np.indices(np.shape(cube))
    Rad = (I-N/2)**2+(J-N/2)**2
    sig = N*0.03
    cube *= np.exp(-Rad/(2*sig**2))

    # Compute the location of the mass center
    cdm = [np.sum(J*cube)/np.sum(cube),np.sum(I*cube)/np.sum(cube)]

    if verbose : print(cdm)

    # Roll the cube to put the mass center at the center
    cube = np.roll(cube, int(N/2-cdm[0]), axis=0)
    cube = np.roll(cube, int(N/2-cdm[1]), axis=1)

    # Threshold
    grain = np.zeros(np.shape(cube))
    m = np.nonzero(cube>np.percentile(cube,70))
    grain[m] = 1.

    mmax = np.nonzero(cube==np.amax(cube))
    grain2 = group(grain, mmax[0][0], mmax[1][0], N, doplot)
    grain2 = reduceMatrix(grain2)

    # Write down the grain image in ASCII format (very inefficient format, but easy to control)
    if writeFile:
        if not os.path.isdir(path):
            os.makedirs(path)

        if name is None:
            name = "2D-N{}_S{}p{}_B{}p{}.txt".format(int(N),int(sigma_dens),int(sigma_dens*10%10),int(beta),int(beta*10%10))
        else:
            name = name + ".txt"

        np.savetxt(path + name, grain2, fmt='%i')

    if (doplot>=1):
        pl.figure(figsize=(20,10))
        pl.subplot(131)
        pl.title('Original gaussian density distribution')
        pl.plot(cdm[0], cdm[1], '+k')
        pl.imshow(np.log10(cube), origin='lower', interpolation='nearest')
        pl.colorbar(shrink=0.4)

        pl.subplot(132)
        pl.title('Threshold cut of the original distribution')
        pl.imshow(grain, origin='lower', cmap='bone', interpolation='nearest')
        pl.colorbar(shrink=0.4)

        pl.subplot(133)
        pl.title('Final Grain - only the central group')
        pl.imshow(grain2, origin='lower', cmap='bone', interpolation='nearest')
        pl.colorbar(shrink=0.4)

        if not __name__ == "__main__": pl.show()   
    
    return [id3D, grain2, name]



# Convert a grain stored in a txt file in an numpy.array
def getFromFile(file):
    """
    Convert txt file to numpy array
    """
    return np.loadtxt(file)


def getSize(grain):
    """
    Get radius
    """

    cpt = 0
    for row in grain:
        for pixel in row:
            if pixel == "1":
                return cpt   
        cpt += 1
    min = cpt

    cpt = len(grain)
    for row in reversed(grain):
        for pixel in row:
            if pixel == "1":
                return cpt
        cpt -= 1
    max = cpt

    return abs(max - min)/2 if type(min) == type(max) == int else None



def getCorrectedSize(grain):
    """
    Get corrected radius
    """

    area = 0

    # Getting area occuped by the grain
    for row in grain:
        for pixel in row:
            if pixel:
                area += 1

    # Area = pi * R^2 -> R =
    return np.sqrt(area / np.pi)

def getNbCarbon(grain = None, size = None):
    if type(grain) is np.ndarray: return 0.5*((getSize(grain)/(10**(-10)))**3)
    if size: return 0.5*((size/(10**(-10)))**3)

def getIonisationEnergy(grain = None, Nc = None):
    Z = -1 # for electrons, cf. Bakes & Tielens paper page 828
    if type(grain) is np.ndarray: return 4.4 + (Z + 1/2) * 25.1 / np.sqrt(getNbCarbon(grain)) # cf. Bakes & Tielens paper page 828, formula 24
    if Nc: return 4.4 + (Z + 1/2) * 25.1 / np.sqrt(Nc) # cf. Bakes & Tielens paper page 828, formula 24

if __name__ == "__main__":

    generate3D(writeFile=True)
    """
    _,_,name = generate(None, None, None,doplot=1)

    grain = getFromFile("grains/" + name)
    size = getCorrectedSize(grain)
    Nc = getNbCarbon(size=size)
    Ei = getIonisationEnergy(Nc = Nc)

    bad_size = getSize(grain)
    bad_Nc = getNbCarbon(size=bad_size)
    bad_Ei = getIonisationEnergy(Nc = bad_Nc)

    print("Uncorrected Size = ", round(bad_size,3), " Angstroms")
    print("Uncorrected Number of carbons = {:.3e}".format(bad_Nc))
    print("Uncorrected Ionisation energy = ", bad_Ei, " eV")

    print("")
    
    print("Size = ", round(size,3), " Angstroms")
    print("Number of carbons = {:.3e}".format(Nc))
    print("Ionisation energy = ", Ei, " eV")

    pl.show()
    #"""