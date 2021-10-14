Analysis
========

During this project, I made a lot of simulation with diffrenet kinds of grain, different angles and differents energies. You can see beloaw some exemple of results.

I was trying here to compare how the grain shape imapact the distribution of the final electron energie. On the following picture, each window correspond to a grain. Windows on the left correspond to grains with ``beta = 0.5`` and it goes to ``2.0`` in the windows on the right (with a step of ``0.5``). Every windows on the same row share the same ``sigma_dens`` parameter, set to ``0.5`` at the bottom and ``1`` at the top.

In short, the more you look at a windows at the bottom right, the more the considered grain is shattered.

All these simulation were made with the following set of parameters:

- Grain size = 100
- Random photon angle
- Random target
- 100 000 photons

In the first time, I made several simulation with a random photon energy, included between 3 and 15 and I get those results:

.. image:: https://vincent.foriel.xyz/wp-content/uploads/2021/10/Capture-decran-2021-10-14-201302.png

-> To see details on the image, go on `https://vincent.foriel.xyz/wp-content/uploads/2021/10/Capture-decran-2021-10-14-201302.png <https://vincent.foriel.xyz/wp-content/uploads/2021/10/Capture-decran-2021-10-14-201302.png>`_

For the histogram part, I was excpecting something like this because it only consider emitted electron, wich are emited proportionally to the Yield that describe the same curve.

Moreover, I was exprecting to not have significative variations between grain shapes, or at least between these kind of shape (gaussian + perturbations) because the photon or the electron have statistically the same distance to travel into the grain. The only thing that really change in the photon or electron point of view is the number of changes of environnement. But these changes have no influence on the physical models that we use here.

.. note::

    During a course (on Thursday, October 14) held by a former student that had this project when it was in this master, he showed us some of his results and his grains and the shape was completely differents. I don't know if it is because he completely changed the way that grains are generated or if my function have a problem, but with his grains, we can expect really different results that we can see here.

.. image:: https://vincent.foriel.xyz/wp-content/uploads/2021/10/Capture-decran-2021-10-14-195004.png
    
-> To see details on the image, go on `https://vincent.foriel.xyz/wp-content/uploads/2021/10/Capture-decran-2021-10-14-195004.png <https://vincent.foriel.xyz/wp-content/uploads/2021/10/Capture-decran-2021-10-14-195004.png>`_

Once again, I was excpecting thos results because the curve correspond to the mix of the Yield and the spectral radiance of the star. In fact, photon energy in not random anymore, so it has influence on the Yield parameters, and so on the results. Here, the energy of the photon are often high, so the curve is mainly described by the spectral radiance of the star (a high energy photon will almost always emit an electron when it will be absorbed).

The thing that amazes me the most is the proportion of photons that pass through the grain without being absorbed. When we take a look at the travel distance density function, we can see that most of photons will not travel more than 30 angstoms in the grain. But the grain is in average 70 angstrom wide.
It can be explained by the angle and the target position that can make the photon pass on a side of the grain and so travel a short distance into the grain before getting out. To be sure about that, a solution may be create a dynamic plot that will show the photons trajectories.

.. note::

    The first event type is always 0, but it is actually a bug

However, after making several tests, the spikes on the right side of the histograms seems not bu due to a bug, but I can't explain why it make this, it actually really disturb me...