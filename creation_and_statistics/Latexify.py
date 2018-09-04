import matplotlib.pyplot as plt
import matplotlib

import numpy as np
import pandas as pd

def Latexify(fig_width=None, fig_height=None, columns=1):
    """Set up matplotlib's RC params for LaTeX plotting.
    Call this before plotting a figure.

    Parameters
    ----------
    fig_width : float, optional, inches
    fig_height : float,  optional, inches
    columns : {1, 2}
    """

    assert(columns in [1,2,3])

    if fig_width is None:
        fig_width = cmToInch(12.65076) # width in inches. The standard is report with 11pt font
    
    if columns == 1:
        fig_width = fig_width * 0.99
    elif  columns == 2:
        fig_width = fig_width * 0.49
    elif columns == 3:
        fig_width = fig_width * 0.32 

    if fig_height is None:
        golden_mean = (np.sqrt(5)-1.0)/2.0 # Aesthetic ratio
        fig_height = fig_width*golden_mean # height in inches

    params = {'backend': 'ps',
              #'text.latex.preamble': ['\usepackage{gensymb}'],
              'axes.labelsize': 8, # fontsize for x and y labels (was 10)
              'axes.titlesize': 8,
              #'text.fontsize': 8, # was 10
              'legend.fontsize': 8, # was 10
              'xtick.labelsize': 8,
              'ytick.labelsize': 8,
              'text.usetex': True,
              'figure.figsize': [fig_width,fig_height]
             # 'font.family': 'serif'
    }

    matplotlib.rcParams.update(params)


    return 

def cmToInch(cm):
    return cm * 0.393701

def LatexifyTest():
    Latexify()

    plt.figure()
    plt.plot(np.arange(0,10,0.1), np.arange(0,100,1))
    plt.xlabel("Hey")
    plt.ylabel("Girl")

    plt.savefig("LatexifyTest.pdf", format="pdf")

    return