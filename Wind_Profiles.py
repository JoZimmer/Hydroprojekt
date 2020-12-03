import numpy as np 
import matplotlib.pyplot as plt

def plot_DIN (vb, category):

    # profile functions
    #categories = ['I','II','III','IV']
    z = np.arange(0,500,0.5)
    
    #TODO: split z array an stelle von z min und erstelle array 0 bis zmin mit vz0 wert--> concatenate them
    if category == 'I':
        zmin, vmin, Imin = 2, 0.97, 0.17
        a, b = 1.18, 0.12
        aI, bI = 0.14, -0.12
    elif category == 'II':
        zmin, vmin, Imin = 4, 0.86, 0.22
        a, b = 1.0, 0.16
        aI, bI = 0.19, -0.16
    elif category == 'III':
        zmin, vmin, Imin = 8, 0.73, 0.29
        a, b = 0.77, 0.22
        aI, bI = 0.28, -0.22
    elif category == 'IV':
        zmin, vmin, Imin = 16, 0.64, 0.37
        a, b = 0.56, 0.30
        aI, bI = 0.43, -0.30
    
    z1 = z[2*zmin+1:]
    v_z0 = np.full(2*zmin+1, vmin*vb)
    Iv_z0 = np.full(2*zmin+1, Imin)
    v_z = np.concatenate((v_z0, a*vb*(z1/10)**b), axis = 0)
    Iv_z = np.concatenate((Iv_z0, aI*(z1/10)**bI), axis = 0)

    return v_z, Iv_z, z

def plot_DIN_all (vb, v_ref, z_ref):

    # profile functions
    fig = plt.figure('DIN profiles')
    ax = fig.add_subplot(111)
    categories = ['I','II','III','IV']
    colors = ['b', 'g', 'r', 'orange']
    z = np.arange(0,100,0.5)
    for i, category in enumerate(categories):
        #TODO: split z array an stelle von z min und erstelle array 0 bis zmin mit vz0 wert--> concatenate them
        if category == 'I':
            zmin, vmin, Imin = 2, 0.97, 0.17
            a, b = 1.18, 0.12
            aI, bI = 0.14, -0.12
        elif category == 'II':
            zmin, vmin, Imin = 4, 0.86, 0.22
            a, b = 1.0, 0.16
            aI, bI = 0.19, -0.16
        elif category == 'III':
            zmin, vmin, Imin = 8, 0.73, 0.29
            a, b = 0.77, 0.22
            aI, bI = 0.28, -0.22
        elif category == 'IV':
            zmin, vmin, Imin = 16, 0.64, 0.37
            a, b = 0.56, 0.30
            aI, bI = 0.43, -0.30
        
        z1 = z[2*zmin+1:]
        v_z0 = np.full(2*zmin+1, vmin*vb)
        Iv_z0 = np.full(2*zmin+1, Imin)
        v_z = np.concatenate((v_z0, a*vb*(z1/10)**b), axis = 0)
        Iv_z = np.concatenate((Iv_z0, aI*(z1/10)**bI), axis = 0)


        ax.plot(Iv_z, z/z_ref, color = colors[i])
        ax.plot(v_z/v_ref, z/z_ref, label = 'DIN - category '+category, color = colors[i])

    ax.set_xlabel(' Iv(z), v(z)/v_ref')
    ax.set_ylabel('z/z_ref')
    ax.legend()
    ax.grid()
    plt.show()

#plot_DIN_all(30,20,10)