""" 
This file takes care of all the plotting. You can run specfic section through
ipython and get a view of specific plots
"""

"""Set current path as sys path for import of files"""
import sys
import os 
sys.path.append(os.getcwd() + "/statistics")

"""Global packages"""
import numpy as np
import pandas as pd 
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

"""Local Packages"""
import malaria_statistics as MS
from Latexifier import LatexifierFunctions as LF
#print("Importing done")

def mutation():
    LF.Latexify(fig_width=6.19893, label_size=[1.0, 2.5])

    q = MS.MalariaStatistics("mutation")
    gamma = q.parameters["ReplacementSpeed"].unique()[2]
    mus = np.sort(q.parameters["MutationSpeed"].unique())

    """Plot mean and extinction time"""
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()
    fig3, ax3 = plt.subplots()

    for mu in mus:
        q = MS.MalariaStatistics("mutation")
        mask = ( ((q.parameters["ReplacementSpeed"][:] == gamma).as_matrix()) & ((q.parameters["MutationSpeed"][:] == mu).as_matrix()) )
        q.ApplyMask(mask=mask)

        q.PlotExtinctionTime(ax1, "MaxAntigenValue")
        q.PlotMeanInfection(ax2, "MaxAntigenValue", errorBars=False)
        ax3.plot(q.parameters["MaxAntigenValue"], q.dataEnd["strains"], '-o', markersize=3.0, linewidth=0.5)

    #fig1.tight_layout(pad=0.5)
    #fig2.tight_layout(pad=0.5)
    #fig3.tight_layout(pad=0.5)

    box = ax2.get_position()
    #ax2.set_position([box.x0, box.y0, box.x1*0.5, box.y1], )

    box = ax3.get_position()
    #ax3.set_position([box.x0, box.y0, box.x1*0.5, box.y1], )
    print(box)

    ax1.legend([r"$\mu$="+str(mus[0]),r"$\mu$="+"{:.0E}".format(mus[1]),r"$\mu$="+"{:.0E}".format(mus[2]),r"$\mu$="+"{:.0E}".format(mus[3])])
    ax2.legend([r"$\mu$="+str(mus[0]),r"$\mu$="+"{:.0E}".format(mus[1]),r"$\mu$="+"{:.0E}".format(mus[2]),r"$\mu$="+"{:.0E}".format(mus[3])], 
     bbox_to_anchor=[0.5, 1.15], loc=10, ncol=2)
    ax3.legend([r"$\mu$="+str(mus[0]),r"$\mu$="+"{:.0E}".format(mus[1]),r"$\mu$="+"{:.0E}".format(mus[2]),r"$\mu$="+"{:.0E}".format(mus[3])], 
     bbox_to_anchor=[0.5, 1.15], loc=10, ncol=2)                   
    ax1.set_xticks([0, 5, 10, 15, 20])
    ax2.set_xticks([0, 5, 10, 15, 20])
    ax2.set_yticks([0, 0.05, 0.10, 0.15, 0.20, 0.25])    
    ax3.set_xticks([0, 5, 10, 15, 20])
    ax3.set_yticks([0, 5, 10, 15, 20])
    q.PlotNiceAndSave(fig1, ax1, "Initial strains", ylabel = "Extinction time (gen)", fileName = "mutation_extinctionTime")
    q.PlotNiceAndSave(fig2, ax2, "Initial strains", ylabel = "Mean infected", fileName = "mutation_mean")
    q.PlotNiceAndSave(fig3, ax3, "Initial strains", ylabel = "Number of end strains", fileName = "mutation_strains")
    
    return

def mutation2D():
    plt.style.use("seaborn")
    LF.Latexify(fig_width = 6.19893, label_size=[1.0, 1.0])
    #matplotlib.rc('font',**{'family':'serif', 'serif':['Computer Modern Roman']})
    #matplotlib.rc('text', usetex=True)

    q = MS.MalariaStatistics("mutation2D")
    mus = np.sort(q.parameters["MutationSpeed"].unique())

    for mu in mus:
        q = MS.MalariaStatistics("mutation2D")
        mask = (q.parameters["MutationSpeed"][:] == mu).as_matrix()
        q.ApplyMask(mask)

        fig, ax = plt.subplots()
        q.Plot2D(fig, ax, "MaxAntigenValue", "InfectionSpeed", "run", ticks = [0,500,1000,1500,2000])
        ax.grid(False)
        ax.set_xticks([1,5,10,15,20,25])
        q.PlotNiceAndSave(fig, ax, "Strains", r"$\alpha$", "mutation2D_extinctionTime" + "{:.0E}".format(mu))

        fig, ax = plt.subplots()
        q.Plot2D(fig, ax, "MaxAntigenValue", "InfectionSpeed", "mean", ticks = [0,0.1,0.2,0.3,0.4,0.5])
        ax.grid(False)
        ax.set_xticks([1,5,10,15,20,25])
        q.PlotNiceAndSave(fig, ax, "Strains", r"$\alpha$", "mutation2D_mean" + "{:.0E}".format(mu))

    return

def mutationTimeSeries():
    q = MS.MalariaStatistics("mutationTimeSeries")

    mus = q.parameters["MutationSpeed"].unique()
    As = q.parameters["MaxAntigenValue"].unique()
    gammas = q.parameters["ReplacementSpeed"].unique()

    for mu in mus:    
        fig, ax = plt.subplots()
        for gamma in gammas:
            q = MS.MalariaStatistics("mutationTimeSeries")
            mask =( ((q.parameters["ReplacementSpeed"][:] == gamma).as_matrix()) & ((q.parameters["MutationSpeed"][:] == mu).as_matrix()) )
            q.ApplyMask(mask)
            q.PlotExtinctionTime(ax=ax, vary="MaxAntigenValue")
        ax.legend(gammas)
        q.PlotNiceAndSave(fig, ax, "Strains", "Extinction time (gen)", str(mu))

    return