photon.py
=========

This file contain 2 function relative to the photon energy.

This file can't executed as a main file.

These functions use a configuration variable that can be edited in this way:

.. code-block:: python

    import photon as p
    p.T = star_temperature

- ``p.T``: ``float`` the temperature of the star in Kelvin

radiation
---------

This function gives the spectral radiance for a given wavelength of a star with a given temperature.

Usage
~~~~~

The temperature parameter is a global variable, to allow the function to be a simple function with one parameter and one result, wich facilitate it's manipulation in functionnal python instructions.

.. code-block:: python

    import photon as p
    B = p.radiation(wav)

Parameters:

- ``wav``: ``float`` the wavelenght you want to consider

Return types:

- ``B``: ``float`` the spectral radiance (the power per unit solid angle and per unit of area normal to the propagation)

How it works
~~~~~~~~~~~~

This function only contain the physical formula of the spectral radiance, expressed by:

.. math::

    B_\nu(\nu,T) = \frac{2h\nu^3}{c^2} \frac{1}{e^{\frac{h\nu}{kT}}-1}

where

- :math:`B_\nu(\nu,T)` is the spectral radiance (the power per unit solid angle and per unit of area normal to the propagation) density of frequency :math:`\nu`  radiation per unit frequency at thermal equilibrium at temperature :math:`T`.
- :math:`h` is the Planck constant;
- :math:`c` is the speed of light in a vacuum;
- :math:`k` is the Boltzmann constant;
- :math:`\nu`  is the frequency of the electromagnetic radiation;
- :math:`T` is the absolute temperature of the body.

getPhotonEnergy
---------------

This function allow to generate a random photon energy with a probability that is proportional to the spectral radiance distribution.

Usage
~~~~~

.. code-block:: python

    import photon as p
    p.T = star_temperature
    E = p.getPhotonEnergy(verbose = False)

Parameters:

- ``verbose``: ``boolean`` tell to the function if you want to see the result on a plot or not.

.. note::

    The verbose mode was made to be used only inside the ``throwOnePhoton`` function. It use the subplot ``221`` and doesn't show the plot.

Return types:

- ``E``: ``float`` the energy of the photon

How it works
~~~~~~~~~~~~

This function only use the ``distrib.random`` function to generate a random variable depending of a distribution and convert the random variable, that is actually a wavelength in energy by using the formula

.. math::

    E = h*\frac{c}{\lambda} * 6.242*10^{18}

where

- :math:`E` is the energy of the photon in eV
- :math:`h` is the planck constant
- :math:`c` is the speed of light
- :math:`\lambda` is the wavelength
- :math:`6.242*10^{18}` is a coeficient to convert Joules (insternational metric system) to electron volts (that is more conveniant to use in this program)
