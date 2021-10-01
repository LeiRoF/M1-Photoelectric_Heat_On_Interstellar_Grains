# distributionTools.py

This file contains 2 functions that helps to manage distributions.

If the file is executed directly by running the command `python distributionTools.py`, it will run a debug function that will plot the distribution and a result of several randomly generated variables in this distribution.

You should get something like that:

![](https://vincent.foriel.xyz/wp-content/uploads/2021/09/Capture-decran-2021-09-29-133445.png)

This plot is for the folowing parameters:

```python
min = 0
max = 100
precision = 1
distrib = lambda n: np.exp(-n/100) / 100
number_of_test = 100000
```

You can find and edit these parameters at the end of the file.

**Execute the file via the console**

You can run the file by going to the directory where the source code is located, then running the following command:

```
python distributionTools.py
```

> This file is not supposed to be executed except for debugging. If you want to edit parameters, you must edit the source code.

## randomInDistrib

This function generate a random variable `x` according to a distribution of probability amplitude.

### Usage

```python
x = randomInDistrib(distrib, min, max)
```

Parameters:

* `distrib`: `function`: a function that take one parameter (must be a number)
* `min`: `float`: the minimum value that this function can generate
* `max`: `float`: the maximum value that this function can generate

Return type:

* `x`: `float`

### How it works

To randomly draw a value `x` following the probability density function `f(x)` from a uniform random
number generator:
1. Randomly draw a value of `x` with a uniform generator.
2. Randomly draw a number `u` between 0 and 1 with a uniform generator.
3. If `u < f(x)`, keep x, otherwise, redo from step 1, until `u < f(x)`.

## plotDistrib

This function help to plot a distribution by generating 2 lists `x` and `fx` that can by easliy plotted using th matplotlib function `plt.plot(x,fx)`

### Usage

```python
x, fx = plotDistrib(distrib, min, max, step = 1)
```

Parameters:

* `distrib`: `function`: a function that take one parameter (must be a number)
* `min`: `float`: the minimum value that will be plotted on the x-axes
* `max`: `float`: the maximum value that will be plotted on the x-axes
* `step`: `float`: the precision of the plot

Return types:

* `x`: `list` of `float` (or `int` if `min` and `step` has the type `int`)
* `fx`: `list` of `float`

### How it works

This function generate a list that contain every numbers included between `min` and `max` with the defined `step`. For each element `x`, it will compute the associated value `f(x)` and put the result in a second list.