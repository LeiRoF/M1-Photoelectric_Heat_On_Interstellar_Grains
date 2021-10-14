import grain, run, data, numpy

def bulk():

    for sigma_dens in numpy.arange(0.5,1.5,0.5):
        for beta in numpy.arange(0.5,2.5,0.5):
            
            print(f"Generating grain N=100, SigmaDens={sigma_dens}, Beta={beta}")
            grain.generate(100,sigma_dens,beta,in3D=False)

    run.simulation("all",100000,"rand()*2*pi",["rand()","rand()"],False,"bulk","28890")

    data.analyse("all")

if __name__ == "__main__":
    bulk()