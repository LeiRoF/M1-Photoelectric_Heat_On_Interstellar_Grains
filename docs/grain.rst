grain.py
========

This file contain the generating function of the dust grains, but also usefull tools to manage them.

**Execute the file via the console**

You can run this file directly to generate a new grain. To do so, just enter the following command in a command-line terminal:

.. code-block::

    python grain.py

The shape of the grain is described by a 2D or 3D matrix composed of 0 and 1. 0 indicates that the space is empty, 1 indicates that the space is occupied by the grain. Here is a representation in black and white of this matrix:

.. image:: https://vincent.foriel.xyz/wp-content/uploads/2021/10/Capture-decran-2021-10-10-112938.png

.. note::

    More information on the `start page <https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/start.html>`_

checkExampleGrain
-----------------

This function will check if the file ``grains/example.txt`` exist. If it doesn't exist, it will generate the grain by calling the ``generated`` function

This function as no parameter, so it's usage and how it work are trivial.

group
-----

No description here.

generate
--------

This function will generate a matrix in 2D or 3D that represent the shape of the dust grain.

Usage
~~~~~

.. code-block:: python

    generate(N, sigma_dens, beta, doplot = 0, writeFile = True, verbose = False, name = None, in3D = False)

Parameters:

- ``N``: ``int`` size of the matrix.
- ``sigma_dens``: ``float`` Width of the density distribution (must be included between 0 and 1)
- ``beta``: ``float`` Slope of the power spectrum (=probability density function)
- ``doplot``: ``int`` 0, 1 or 2, represent wich data you want to plot. 0 wil not plot anything.
- ``writeFile``: ``boolean`` set to True if you want to save the generated grain in a file.
- ``verbose``: boolean: allows to display events occurring during the generation
- ``name``: ``str`` the name of your grain. If the name is ``None``, it will be automatically generated using parameters values
- ``in3D``: ``boolean`` set it to ``True`` if you want to generate a 3D grain. Else, the function will generate a 2D one.

Return types:

- ``grain``: ``numpy.array`` containing the matrix that represent the grain
- ``name``: ``str`` the name of the grain

getSize
-------

Get the size of the grain

Usage
~~~~~

.. code-block::

    getSize(grain)

Parameters:

- ``grain``: ``numpy.array`` the matrix that represent your grain.

Return types:

- ``size``: ``float``

How it works
~~~~~~~~~~~~

The first iteration of this function just get the first and the last line where a case of the matrix is 1. Then the distance between these 2 lines are the diameter, so it return this distance divided by 2. But this method has a problem: if the grain is very scattered, this radius will be high but not representative of the grain volume.

To fixe this problem, this function was totally re-written to count each pixel that is set so 1, and then use the inverse of the area formula of a disk to get a representative radius.