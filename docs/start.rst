.. _start:

Start
=====


You have 3 ways to run a simulation:

.. warning::

    For each way, please keep in mind that the programm will use every core of your processor and
    **can't be manually stopped**. Try to increment the complexity of the simulation progressively. 1000 photons is the maximum recommanded for the first
    try.

Guided
--------

In a command-line terminal, execute the following commands. The programm will ask you to enter your desired paramters.

**Generate a grain**

.. code-block:: bash

    python grain.py

**Start a simulation**

.. code-block:: bash

    python run.py

**Plot results**

.. code-block:: bash

    python data.py


Direct / In script
------------------

You can specify all or a part of these parameters by adding them after
the command.

**Generate a grain**

.. code-block::

    python grain.py [name] [3D] [size] [sigma_dens] [beta]

- ``name``: The name of the file that will be generated
- ``3D``: Must be set to ``True`` or ``False`` to indicate to the program if it have to generate a grain in 3D or in 2D.
- ``size``: An integer that represent the size of the generated matrix that contain the description of your grain.

.. note::

    In order to optimize the simulation, this size will be reduced to remove empty parts of the matrix that add unecessary computation time.

- ``sigma_den``: Width of the density distribution (must be included between 0 and 1)
- ``beta``: Slope of the power spectrum (=probability density function)

**Start a simulation**

.. code-block::

    python run.py [name] [files] [temperature] [count] [angle phi] [angle tetha] [x] [y] [z] [verbose]

Every parameters that are not precised here will be asked to the user.

- ``name``: The name of the file that will be generated (or the prefix of the generated files if you select more than 1 grain file)
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

- ``temperature``: Temperature of the star in Kelvin. Default is 5 times the temperature of the sun (5 * 5778 = 28890 K)
-  ``count``: Number of simulated photons
-  ``angle [phi,tetha]``: The angle of the incomming photons in radian. Note that theta parameter will be considered only if your grain is in 3D. You can also write an expression to let the programm decide of the angle. Ex: ``rand()*2*pi`` for phi and ``rand()*pi`` for tetha will throw a photon with a random angle. Several
   shortcuts are included from the numpy library:

   -  ``pi`` a constant containing the value of pi
   -  ``rand()`` that generate a random number between 0 and 1
   -  ``round()``
   -  ``sqrt()``
   -  ``exp()``, ``log()``
   -  ``cos()``, ``sin``, ``tan()`` using radians
   -  ``arccos()``, ``arcsin``, ``arctan()``
   -  ``cosh()``, ``sinh()``, ``tanh()``
   -  ``arccosh()``, ``arcsinh``, ``arctanh()``
   -  The rest of the numpy library is accessible via the namespace ``np``.
      Ex: ``np.foo()``
-  ``[x,y,z]``: The coordinate of the photon's target point. This coordinate
   must be included between 0 and 1 (0 is the beginning of the matrix, 1
   is the end of the matrix). You can also write an expression to let
   the programm decide of the target. Ex: ``rand()`` will throw a photon
   with a random target. You can use the same shortcuts as for the
   ``angle`` parameter. Note that the ``z`` coordinate will be considered only if your grain is in 3D.
-  ``verbose``: Let the program show you events that occurs. Must be set
   to ``True`` or ``False``

.. note::

    The verbose mode can slow down the simulation.

**Plot results**

.. code-block::

    python data.py [files]

-  ``files``: Files that contain the result data. The file list must be
   separated with comma. All files must be present in the ``results/``
   folder. Write ``all`` to analyse all data files in the
   ``results/`` folder.

.. note::
    
    Each space indicate the end of the parameter. Your files must
    not contain spaces. If your list contain unothorized caracters in
    yout terminal/script file, you can delimit it in several ways:
    ``"file_1","file_2"``, ``'file_1','file_2'``, ``"[file_1,file_2]"``,
    ``'[file_1,file_2]'``

Integrated as python module
---------------------------

To import a program as a module, put the source folder next to your
program and add the following line in your program:

.. code:: python

    import Photoelectric_Heating_On_Interstallar_Grains as phig

Then, in order to run a simulation, call the function:

.. code:: python

    phig.grain.generate(N,sigma_dens,beta,path,doplot,writeFile,verbose,name,in3D) # generate a grain
    phig.run.simulation(fileList,count,angle,target,verbose,name,temperature) # start a simulation
    phig.data.analyse(fileList) # plot results

Example:

.. code:: python

    phig.grain.generate(100,1.0,3.0,"grains/",0,True,False,"example",False) # generate a grain
    phig.run.simulation("example.txt",1,["rand()*2*pi","rand()*pi"],["rand()","rand()","rand()"],True,"example",5*5778)# start a simulation
    phig.data.analyse("example.dat") # plot results

.. note::

    This project was not made to use in another program. You may
    need to edit some part of the code to make it works correctly with
    your program.