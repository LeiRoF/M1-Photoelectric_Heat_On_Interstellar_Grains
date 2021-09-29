# throwOnePhoton

This file contains a function that simulates a photon hitting the grain passed in parameter.

When this file is executed directly with the command `python throwOnePhton.py`, the function is executed with the option `verbose=True`. The sequence of events is then displayed in the console. At the end of the simulation, the different parameters that occurred during the simulation are displayed in a plot like this one

![](https://vincent.foriel.xyz/wp-content/uploads/2021/09/Capture-decran-2021-09-29-150141.png)

> If the phoon passes by the grain, if it passes through or if its absorption does not cause any electron emission, some of these graphs will not be displayed. You will have to restart the simulation several times for all the events to take place.


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
