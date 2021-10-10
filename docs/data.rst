data.py
=======

This file is dedicated to plot data files.

plotEnergy
----------

Allow to plot a data file in the ``results`` folder.

Usage
~~~~~

.. code-block::

    plotEnergy(file)

- ``files``: ``string`` contain the name **and** the extension of the data file

How it works
~~~~~~~~~~~~

This function is quite simple, it just read the data file and generate 2 lists:

- A list that contain energies (positive values in the file)
- A list that contain number of each events (``-1``, ``-2``, ``-3`` and ``-4`` values)

Then, these two lists are plot using matplotlib