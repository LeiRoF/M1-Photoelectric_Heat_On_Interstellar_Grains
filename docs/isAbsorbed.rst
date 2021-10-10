isAbsorbed
==========

This file contain 2 similar functions. These function allow to simulate the propagation of a particule inside the grain and determine if the particule will be absorbed or will escape the grain.

This file can't executed as a main file.

isAbsorbed
----------

Usage
~~~~~

.. code-block:: python

    absorbed, Ry, Ry, hit = isAbsorbed(grain, dist, Rx, Ry, Dx, Dy, step= 0.1)

Parameters:

- ``grain``: ``numpy.array`` the considered grain
- ``dist``: ``float`` the distance the particle can travel in the grain before being absorbed
- ``Rx`` & ``Ry``: ``float`` initial position of the particule
- ``Dx`` & ``Dy``: ``float`` direction of the particule

.. note::

    ``Dx`` & ``Dy`` should be normalized
    :math:`\sqrt{Dx^2 + Dy^2} = 1`

- ``step``: ``float`` precision of the propagation

Return types:

- ``absorbed``: ``boolean`` that indicated if the particle has been absorbed or not
- ``Rx`` & ``Ry``: ``float`` the new position of the particle
- ``hit``: ``boolean`` that indicate if the particle hit the grain

How it works
~~~~~~~~~~~~

This function have 2 versions. The first on consist on a loop that increment the position and look at if the particule is in the grain. If it's the case, the distance that the particle can travel in the grain is decremented. When this value comes to 0, the grain is absorbed. If the particle comes to a border of a matrix, then it excaped the grain.

In the second version, the function use the particle location and direction to generate an array containing several equally distant points that represent the trajectory. Then, the function use the location of these points tu generate an array containing the shape of the grain in 1D. This dimension correspond to the particule trajectory. Finally, the function just look at the amount of occuped space in this dimension. If it is higher than the distance the particle can travel in the grain, the particle is absorbed. Else, the particle excape the grain.

.. note::
    
    The second iteration is supposed to be more optimized because it use built-in numpy functions. However, the difference was not significant when tested at 50,000 photons