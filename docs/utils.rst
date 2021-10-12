utils.py
========

Utils contain functions that can be used in the whole program.

This file can't executed as a main file.

CPUcount
--------

Get the number of threads of the CPU

Usage
~~~~~

.. code-block:: python

    import utils
    count = utils.CPUcount()

No parameters

Return types:

- ``count``: ``int`` the number of threads.

.. note::

    Thread include physical and logical cores.

How it work
~~~~~~~~~~~

This function use a built-in fonction in the ``os`` lib to get the number of threads. Because getting CPU info can take time, the function store the result in a global variable to be able to re-send it quickly if the function is called several times in the program.

endProgram
----------

Usage
~~~~~

.. code-block:: python

    import utils
    utils.endProgram(reason)

Parameter:

- ``reason``: ``str`` why the program must end.

No returns

How it work
~~~~~~~~~~~

This function just use the built-in ``exit()`` function and print a message depending of the ``reason parameter``. It allow to avoid having the same message multiple times and therefore to facilitate the edition of these messages.*

CPUinfo
-------

Get the CPU name and basic info in a string.

Usage
~~~~~

.. code-block:: python

    import utils
    name = utils.CPUinfo()

No parameters

Return types:

- ``name``: ``str`` the name and basic informations about the CPU (with spaces remplaced by underscores)

How it work
~~~~~~~~~~~

This function use a built-in fonction in the ``cpuinfo`` lib to get the name of the CPU. Because getting CPU info can take time, the function store the result in a global variable to be able to re-send it quickly if the function is called several times in the program.
