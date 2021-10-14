Physical description
====================

The objective of this program is to simulate the photoelectric effect on a dust grain. This grain is reprented by a 2D or 3D matrix, generated via a gaussian function in wich we added some perturbations to create fractal properties.

.. image:: https://vincent.foriel.xyz/wp-content/uploads/2021/10/Capture-decran-2021-10-10-112938.png

After generating a grain, throw a photon on it with a certain energy. This energy is mostly determined by the star temperature. We approximate here the radiative spectrum of the star with a black-body radiation spectrum:

.. math::
    
    B = \frac{2 h c^2}{\lambda^5 (e^{\frac{h c}{\lambda k T}} - 1)}

Where :math:`B` is the spectral radiance (expressed in :math:`W·m−2·sr−1`, :math:`h` and :math:`k` respectively is the Planck and Boltzmann constants, :math:`c` the speed of light, :math:`T` the temperature of the star and :math:`\lambda` the considered wavelength.

The spectral radiance can be considered as the "intensity" of light for given wavelenght, so it is proportional to the probability, for a random photon that is emitted from the star, to have an energy corresponding to this wavelenght.

The relation between wavelenght and photon energy is given by:

.. math::

    E = h \frac{c}{\lambda} 6.242*10^{18}

Where :math:`6.242*10^{18}` allow to express :math:`E` (the energy) in electron-volts, wich is more conveniant to use in this situation than Joules.

.. image:: https://vincent.foriel.xyz/wp-content/uploads/2021/10/Capture-decran-2021-10-14-160227.png

So, we normalize the expression of :math:`B` to get a density function. Then we chose a random energy value using this density function.

After that, we throw the photon on the grain and see if it will be absorbed. To do so, we are looking at the following equation:

.. math::

    P = \frac{1}{I_a} e^{-d_a/I_a}

Where :math:`P` represent the density function for to photon to traveling a distance :math:`d_a` in the grain, and :math:`I_a = 100 Å` is the attenuation distance.

Again, we generate a random :math:`d_a` value that represent the distance that our photon will be able to travel in the grain. We look at the photon trajectory and if the distance in the grain is upper than :math:`d_a`, the photon is absorbed.

.. image:: https://vincent.foriel.xyz/wp-content/uploads/2021/10/Capture-decran-2021-10-14-160255.png

If it is absorbed, several events can occure, but the only one we are focusing on is the emission of an electron (with a random angle).

To know if an electron will be emitted, we use the folowing density probability function, also called "Ionisation Yield":

.. math:: 

    Y = 0.5 * (1 + \frac{tanh(E-E_0)}{2})

Where :math:`E` is the energy of the photon, :math:`E_0 = 8 eV` is an empirically determined tipping energy, and :math:`Y` is the yield (or the probability of emitting the electron).

.. image:: https://vincent.foriel.xyz/wp-content/uploads/2021/10/Capture-decran-2021-10-14-160313.png

If an electron is emited, as the photon before, it will have to travel into the grain. It also have a density function that represent the distance it can travel:

.. math::

    P = \frac{1}{I_e} e^{-d_e/I_e}

Where :math:`d_e` is the distance that the electron can travel and :math:`I_e = 10 Å` the attenuation factor for the electron.

.. image:: https://vincent.foriel.xyz/wp-content/uploads/2021/10/Capture-decran-2021-10-14-160331.png

Again, we generate a random distance value and see the distance that the electron will have to travel in the grain and we only consider electrons that escape the grain.

When an electron is emitted, it's energy is defined by:

.. math::

    E_c = E - E_i

Where :math:`E_c` is the kinetic energy of the electron, :math:`E` is the energy of the photon and :math:`E_i` is the energy of ionisation of the grain.

This energy of ionisation is given by:

.. math::

    E_i = 4.4 + (Z + \frac{1}{2}) \frac{25.1}{\sqrt{N_c}} 

Where :math:`N_c` the number of carbon atoms and :math:`Z = 0` is the electronic affinity, here equal to 0 because we consider that our grain as a neutral electric charge.

The number of carbon atom is defined by:

.. math::
    N_c = 0.5*a^3

Where :math:`a` in angstrom, correspond to the radius of the grain.