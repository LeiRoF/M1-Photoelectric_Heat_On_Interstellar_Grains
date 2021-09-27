# Files description

## Generate grain

The file `generate_grain.py` have to be called directkly by python and will create a `.txt` file representing the grain. This file contain a matrix of 0 and 1 that indicate if the space (in 2D) is occuped or not by the grain.

When you run this file, you will have to answer to 3 questions:

1. Size of the grain: must be an int that represent the size of the matrix (1 "pixel" = 1 angstrom)
2. Width of the density distribution: define the compatcness of your grain
3. Slope of the power spectrum: determine the chaotic shape of your grain

## Get energies

This file `get_energies.py` will create a virtual photon that will hit (or not) the grain. The file countain multiple usefull functions for the main program, but if you execute it directly, it will return you all simulation parameters and results, using the `docs/Grain_N100_S1p0_B3p0.txt` file.

## Utils

`utils.py` file contain some usefull functions like a generator of random variable depending of a distribution.

When this file is executed directly by python, it will generate 10,000 random numbers that correspond to the probability distribution `P = exp(-x/100)/100` and plot them.

> If this file is called directly by python, the program can take some time to be executed.
