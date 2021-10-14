run.py
======

Run.py is the file that manage simulations. It contain only one function that is called when the file is executed directly by python using the folowing command:

.. code-block::

    python run.py [parameters]

See `Start [start.rst]`_ page to get more information.
<https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/start.html>


simulation
----------

This function will get all and format all parameters and launch a simulation by running the `thowManyPhotons <https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/throwManyPhotons.html#throwmanyphotons>`_ function.

Usage
~~~~~

.. code-block:: python

    simulation(fileList, count, angle, target, verbose, name, temperature)

Parameters:

-  ``files``: ``list(str)`` Files that represent your grain. The file list must be
   separated with comma. All files must be present in the ``grains/``
   folder. Write ``all`` to run a simulation for all files in the
   ``grains/`` folder.
-  ``count``: ``int`` Number of simulated photons
-  ``angle``: ``list(str)`` The angles phi and theta of the incomming photons in radian. The ``str``` can contain the value or an expression that can be evaluated (cf. `Start <https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/start.html>`_)
-  ``target``: ``list(str)``  The x,y and z coordinates of the photon's target point. This coordinate
   must be included between 0 and 1 (0 is the beginning of the matrix, 1
   is the end of the matrix). The ``str``` can contain the value or an expression that can be evaluated (cf. `Start <https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/start.html>`_)
-  ``verbose``: Let the program show you events that occurs. Must be set
   to ``True`` or ``False``
- ``name``: The name of the file that will be generated (or the prefix of the generated files if you select more than 1 grain file)
- ``temperature``: Temperature of the star in Kelvin. Default is 5 times the temperature of the sun (5 * 5778 = 28890 K)


How it work
~~~~~~~~~~~

This function will just verify the format of each parameter to avoid crashes during a simulation. It will successively call the `ask <https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/ask.html>`_ functions. After that, thes parameters will be transmitted to the `thowManyPhotons <https://photoelectric-heating-on-interstallar-grains.readthedocs.io/en/latest/throwManyPhotons.html#throwmanyphotons>`_ function.

It will also get information about the CPU and will measure the time ellapsed during the simulation, and then write it in the ``timeStats.dat`` file.
