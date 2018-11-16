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
import matplotlib.pyplot as plt

"""Local Packages"""
import malaria_statistics as MS
from Latexifier import LatexifierFunctions as LF
print("Importing done")

def mutation():
    
    q = MS.MalariaStatistics("mutation")
    alpha = q.parameters["InfectionSpeed"].unique()[0]
    mus = q.parameters["MutationSpeed"].unique()

    print(mus)

    """Plot mean and extinction time"""
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()
    fig3, ax3 = plt.subplots()

    for mu in mus:
        q = MS.MalariaStatistics("mutation")
        mask = ( ((q.parameters["InfectionSpeed"][:] == alpha).as_matrix()) & ((q.parameters["MutationSpeed"][:] == mu).as_matrix()) )
        q.ApplyMask(mask=mask)

        q.PlotExtinctionTime(ax1, "MaxAntigenValue")
        q.PlotMeanInfection(ax2, "MaxAntigenValue", errorBars=False)
        ax3.plot(q.parameters["MaxAntigenValue"], q.dataEnd["strains"], '-o', markersize=3.0, linewidth=0.5)


    ax1.legend([r"$\mu$="+str(mus[0]),r"$\mu$="+str(mus[1]),r"$\mu$="+str(mus[2]),r"$\mu$="+str(mus[3])])
    ax2.legend([r"$\mu$="+str(mus[0]),r"$\mu$="+str(mus[1]),r"$\mu$="+str(mus[2]),r"$\mu$="+str(mus[3])])
    ax3.legend([r"$\mu$="+str(mus[0]),r"$\mu$="+str(mus[1]),r"$\mu$="+str(mus[2]),r"$\mu$="+str(mus[3])])        
    ax1.set_xticks([0, 5, 10, 15, 20, 25])
    ax2.set_xticks([0, 5, 10, 15, 20, 25])    
    ax3.set_xticks([0, 5, 10, 15, 20, 25])
    ax3.set_yticks([0, 5, 10, 15, 20, 25])
    q.PlotNiceAndSave(fig1, ax1, "Initial strains", ylabel = "Extinction time (gen)", fileName = "mutation_extinctionTime")
    q.PlotNiceAndSave(fig2, ax2, "Initial strains", ylabel = "Mean infected", fileName = "mutation_mean")
    q.PlotNiceAndSave(fig3, ax3, "Initial strains", ylabel = "Number of end strains", fileName = "mutation_strains")

        

    
    
    return

def mutation2D():
    
    
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