# throwOnePhoton.py

This file contains a function that simulates a photon hitting the grain passed in parameter.

When this file is executed directly with the command `python throwOnePhton.py`, the function is executed with the option `verbose=True`. The sequence of events is then displayed in the console. At the end of the simulation, the different parameters that occurred during the simulation are displayed in a plot like this one

![](https://vincent.foriel.xyz/wp-content/uploads/2021/09/Capture-decran-2021-09-29-150141-1.png)

> If the phoon passes by the grain, if it passes through or if its absorption does not cause any electron emission, some of these graphs will not be displayed. You will have to restart the simulation several times for all the events to take place.

## throwOnePhoton()

### Usage

```
energy = throwOnePhoton(file, verbose = False)
```

Parameters:

* `file`: path to the file containing the grain shape.
* `verbose`: allows to display all parameters and events occurring during the simulation

Return type:

* `energy`: `[optional] float` corresponding to the energy of the electron. If an event does not take place, this return can take negative values:
  * -1 if the photon passes through the grain
  * -2 if the photon is absorbed but no electron is emitted
  * -3 if an electron is emitted but is re-absorbed by the grain

### How it works

This function retrieves a path to a file. It then calls the `getGrainFromFile()` function to retrieve the shape of the grain in a variable of type `numpy.array`, which facilitates its exploitation.

This shape is described by a 2D matrix composed of 0 and 1. 0 indicates that the space is empty, 1 indicates that the space is occupied by the grain. Here is a representation in black and white of this matrix:

![](https://vincent.foriel.xyz/wp-content/uploads/2021/09/Capture-decran-2021-09-29-160144.png)

The function will then launch a photon along one of the lines (chosen randomly) of the matrix. From there, a series of events can follow:

* If the photon passes by the grain, nothing happens, the function returns `None`.
* If the photon hits the grain, a distance `da` is randomly generated according to the probability distribution of the propagation distance of a photon in the grain. This distribution is defined by: `P=exp(-da/la)/la` where `la = 100` or 100 pixels, which corresponds here to 100 angstroms because the function considers that 1 pixel = 1 angstrom.
  * If at the end of this distance, the photon has left the grain, then nothing happens, the function returns `-1`.
  * If at the end of this distance, the photon continues to be within the grain, it is absorbed. An electron will then be emitted with a certain probability, depending on the energy of the photon received. This probability is defined by `Y=0.5*(1+Th[(E-E0)/2])` where `E0 = 8 eV`.
    * If no electron is emitted, then the program stops and returns the value `-2`.
    * If an electron is emitted, then a distance `of` is randomly generated according to the probability amplitude distribution of the propagation distance of a photon in the grain. This distribution is defined by: `P=exp(-de/le)/le` where `le = 10` or 10 angstroms. The trajectory of the generated electron is no longer along the line. It is now any (defined randomly during its emission)
      * If at the end of this distance, the electron is still in the grain, it is reabsorbed and the program stops by returning `-3`.
      * If at the end of this distance, the electron is out of the grain, then the program returns its kinetic energy, defined by `Ec = E - Ei` where `E` is the energy of the photon at the arrival and `Ei` is the energy necessary for the ionization of the molecule within the grain.