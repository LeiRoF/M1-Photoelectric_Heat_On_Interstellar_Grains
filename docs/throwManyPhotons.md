# throwManyPhotons.py

This file contains only one function that simulates many photons hitting the grain passed in parameter.

When this file is executed directly with the command `python throwManyPhotons.py`, the function is executed with the option `verbose=True`. The result of each photon throwed on the grain is then displayed in the console. At the end of the simulation, an histogram will appear to show the energy distribution of emitted electrons. Moreover, another figure will shox you the proportion of all events that occured for each photons.

![](https://vincent.foriel.xyz/wp-content/uploads/2021/10/Capture-decran-2021-10-01-114019-1.png)

## throwOnePhoton

This function simulate many photons that hit (or not) the grain and put results at the end of a file (with the same name as the file passed to it as a parameter)

### Usage

```python
throwManyPhoton(count, file, verbose = False)
```

Parameters:

* `count`: `int`: number of photons that will be throwed on the grain
* `file`: `string`: path to the file containing the grain shape.
* `verbose`: `boolean`: allows to display all parameters and events occurring during the simulation

No return

### How it works

This function only consistto call the `throwOnePhoton` function in a loop, and print some informations if `verbose` is set to `True`