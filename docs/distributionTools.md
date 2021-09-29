# distributionTools.py

This file contains 2 functions that helps to manage distributions.

If the file is executed directly by running the command `python distributionTools.py`, it will run a debug function that will plot the distribution and a result of several randomly generated variables in this distribution.

You should get something like that:

![](https://vincent.foriel.xyz/wp-content/uploads/2021/09/Capture-decran-2021-09-29-133445.png)

This plot is for the folowing parameters:

```
min = 0
max = 100
precision = 1
distrib = lambda n: np.exp(-n/100) / 100
number_of_test = 100000
```

You can find and edit these parameters at the end of the file.

## randomInDistrib

This function generate a random variable `x` according to a distribution of probability amplitude.

```
x = randomInDistrib(distrib, min, max)
```

Parameters:

* `distrib` is a function that take one parameter (must be a number)
* `min` is the minimum value that this function can generate
* `max` is the maximum value that this function can generate

Return type:

* `x`: `float`

## plotDistrib

This function help to plot a distribution by generating 2 lists `x` and `fx` that can by easliy plotted using th matplotlib function `plt.plot(x,fx)`

```
x, fx = plotDistrib(distrib, min, max, step = 1)
```

Parameters:

* `distrib` is a function that take one parameter (must be a number)
* `min` is the minimum value that will be plotted on the x-axes
* `max` is the maximum value that will be plotted on the x-axes
* `step` is the precision of the plot

Return types:

* `x`: `list` of `float` (or `int` if `min` and `step` has the type `int`)
* `fx`: `list` of `float`