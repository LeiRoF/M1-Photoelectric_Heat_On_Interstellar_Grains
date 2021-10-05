Getting started
===============

Installation
------------

This project was made with **Python 3.9** and can not run correctly in
previous versions.

1. Get the source code

.. code-block:: bash

    git clone https://gitlab.com/LeiRoF/Photoelectric_Heating_On_Interstallar_Grains.git

2. Go in the source folder

.. code-block:: bash

    cd Photoelectric_Heating_On_Interstallar_Grains

3. Install project dependencies

.. code-block:: bash

    pip install -r requirements.txt

Start
-----

You have 3 ways to run a simulation:

.. warning::

    For each way, please keep in mind that the programm will use every core of your processor and
    **can't be stopped**. Try to increment the complexity of the simulation progressively. 1000 photons is the maximum recommanded for the first
    try.

**Guided**
~~~~~~~~~~

In a command-line terminal, execute the following command:

.. code-block:: bash

    python run.py

The programm will ask you to enter your desired paramters.

**Direct / In script**
~~~~~~~~~~~~~~~~~~~~~~

You can specify all or a part of these parameters by adding them after
the command:

.. code-block:: python

    python run.py [files] [count] [angle] [x] [y] [verbose]

Every parameters that are not precised here will be asked to the user.

-  ``files``: Files that represent your grain. The file list must be
   separated with comma. All files must be present in the ``grains/``
   folder. Write ``all`` to run a simulation for all files in the
   ``grains/`` folder.

.. note::
    
    Each space indicate the end of the parameter. Your files must
    not contain spaces. If your list contain unothorized caracters in
    yout terminal/script file, you can delimit it in several ways:
    ``"file_1","file_2"``, ``'file_1','file_2'``, ``"[file_1,file_2]"``,
    ``'[file_1,file_2]'``

-  ``count``: Number of simulated photons

-  ``angle``: The angle of the incomming photons in radian. You can also
   write an expression to let the programm decide of the angle. Ex:
   ``rand()*2*pi`` will throw a photon with a random angle. Several
   shortcuts are included from the numpy library:

   -  ``pi`` a constant containing the value of pi
   -  ``rand()`` that generate a random number between 0 and 1
   -  ``round()``
   -  ``sqrt()``
   -  ``exp()``, ``ln()``
   -  ``cos()``, ``sin``, ``tan()`` using radians
   -  ``arccos()``, ``arcsin``, ``arctan()``
   -  ``cosh()``, ``sinh()``, ``tanh()``
   -  ``arccosh()``, ``arcsinh``, ``arctanh()``
   -  The rest of the numpy library is accessible via the namespace ``np``.
      Ex: ``np.foo()``

-  ``x``: The x coordinate of the photon's target point. This coordinate
   must be included between 0 and 1 (0 is the beginning of the matrix, 1
   is the end of the matrix). You can also write an expression to let
   the programm decide of the target. Ex: ``rand()`` will throw a photon
   with a random target. You can use the same shortcuts as for the
   ``angle`` parameter.

-  ``y``: The y coordinate of the photon's target point. This coordinate
   must be included between 0 and 1 (0 is the beginning of the matrix, 1
   is the end of the matrix). You can also write an expression to let
   the programm decide of the target. Ex: ``rand()`` will throw a photon
   with a random target. You can use the same shortcuts as for the
   ``angle`` parameter.

-  ``verbose``: Let the program show you events that occurs. Must be set
   to ``True`` or ``False``

.. note::

    The verbose mode can slow down the simulation.

**Integrated as python module**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To import a program as a module, put the source folder next to you
program and add the following line in your program:

.. code:: python

    import Photoelectric_Heating_On_Interstallar_Grains as phig

Then, in order to run a simulation, call the function:

.. code:: python

    fig.run.simulation(file,count,angle,target,verbose)

Example:

.. code:: python

    fig.run.simulation("example.txt",1,"rand()*2*pi",["rand()","rand()"],True)

.. note::

    This project was not made to use in another program. You may
    need to edit some part of the code to make it works correctly with
    your program.
