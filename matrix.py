import numpy as np

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