# -*- coding: utf-8 -*-
""" g-function maker.

    G-functions for a bore field are calculated for B/H rates varying from 0,02 to
    virtually infinite, applying uniform borehole wall temperature boundary conditions.

"""

import matplotlib.pyplot as plt
import numpy as np
from time import time as tic

import pygfunction as gt

# -------------------------------------------------------------------------
# Simulation parameters
# -------------------------------------------------------------------------
def g_function_maker(N_1, N_2, n_seg):
    t1 = tic()
    # Borehole dimensions
    D = 0                         # Borehole buried depth (m)
    H = 110                       # Borehole length (m)
    r_b = 0.055                     # Borehole radius (m)

    x = np.arange(0, 8, 0.3)
    B = 1.85 ** x + 1             # Borehole spacing (m)

    # Thermal properties
    alpha = 1.0e-6      # Ground thermal diffusivity (m2/s)

    # g-Function calculation options
    options = {'nSegments': n_seg,
               'disp': True}

    # Geometrically expanding time vector.
    dt = 100*3600.                  # Time step
    tmax = 3000. * 8760. * 3600.    # Maximum time
    Nt = 15                         # Number of time steps
    ts = H**2/(9.*alpha)            # Bore field characteristic time
    time = gt.utilities.time_geometric(dt, tmax, Nt)
    print (time)
    lntts = np.log(time/ts)


    # -------------------------------------------------------------------------
    # Borehole field (First bore field)
    # -------------------------------------------------------------------------

    # Field of 6x4 (n=24) boreholes
    N_1 = N_1
    N_2 = N_2

    fig, ax = plt.subplots()
    ax.set_xlabel('ln(t/ts)')
    ax.set_ylabel('g-function')
    #ax.set_ylim([0,15]) ##check limits


    for b in B:
        print(b/H)
        field = gt.boreholes.rectangle_field(N_1, N_2, b, b, H, 0, r_b)
        g_fun = gt.gfunction.gFunction(field, alpha, time=time, options=options, method='detailed')

        ax.plot(lntts,g_fun.gFunc)

        if  b/H < 1:
            ax.annotate(xy=(lntts[-1],g_fun.gFunc[-1]), xytext=(max(lntts),0), textcoords='offset points',
                        text=round(b/H,3), va='center')
        else:
            ax.annotate(xy=(lntts[-1], g_fun.gFunc[-1]), xytext=(max(lntts), 0), textcoords='offset points',
                        text='inf', va='center')
        print(g_fun.gFunc)


    t2 = tic()
    rb_h =  'Rb/H = ' + str(r_b/H)
    conf = 'Configuration ' + str(N_1) + 'x' + str(N_2)
    b_h  = 'B/H ='
    plt.grid(True)
    ax.set_xlim(right = max(lntts) + 1.5)
    plt.title(conf, loc = 'left')
    plt.title(rb_h, loc= 'center')
    plt.title(b_h, loc = 'right', size = 12)
    plt.tight_layout()
    plt.show()
    time = t2 - t1

    print('total time is ' + str(time))

g_function_maker(10, 10, 12)


