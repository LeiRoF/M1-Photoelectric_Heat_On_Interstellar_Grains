bulk.py
=======

Bulk is an editable python file that allow to easily run several simulations from scratch.

.. warning::

    Depending of your computer, just one simulation can take lot of time. Do not make bulk simulations if you are not sure about the approximative time it will last.

Here is the default content of this file. You can edit it to make you own bulk simulations.

.. code-block:: python 

    import grain, run, data, numpy

    def bulk():

    for sigma_dens in numpy.arange(0.5,1.5,0.5): # Grain with sigma_dens = {0.5,1}
        for beta in numpy.arange(0.5,3.5,0.5): # Grain with beta = {0.5,1,1.5,2,2.5,3}
            
            print(f"Generating grain N=100, SigmaDens={sigma_dens}, Beta={beta}")
            grain.generate(100,sigma_dens,beta,in3D=False)

    run.simulation("all",1000,"rand()*2*pi",["rand()","rand()"],False,"bulk","28890")

    data.analyse("all")

    if __name__ == "__main__":
    bulk()

.. warning::

    Known issue: due to an unknown process, this file will be called by each thread. You must keep your code in a function and call it ony if the condition ``__name__ == "__main__"`` is satisfied.

 



