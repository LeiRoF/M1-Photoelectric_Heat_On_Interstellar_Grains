matrix.py
=========

Matrix.py contain 2 tool functions that help to manage matrices.

This file can't executed as a main file.

Reduce
------

A function to remove empty parts of the matrix to improve performances.

Usage
~~~~~

.. code-block:: python

    newGrain = reduce(grain)

Parameters:

- ``grain``: ``numpy.array`` the grain shape.

Return types:

- ``newGrain``: ``numpy.array`` the same grain shape but in a smaller matrix.

How it works
~~~~~~~~~~~~

This function use built-in numpy function to filter rows and columns that are not empty, and create a new matrix by assembling these rows and columns.

Squarify
--------

Allow to make make the matrix square. Usefull to avoid having to manage size of each axe.

Usage
~~~~~

.. code-block:: python

    newGrain = squarify(grain)

Parameters:

- ``grain``: ``numpy.array`` the grain shape.

Return types:

- ``newGrain``: ``numpy.array`` the same grain shape but in a square matrix.

How it works
~~~~~~~~~~~~

The function compute the diffrence of size between the diffrents dimensions and use the built-in numpy ``pad`` function to add layers to make the matrix square