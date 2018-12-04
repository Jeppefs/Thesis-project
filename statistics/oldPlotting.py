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
import seaborn as sns
from matplotlib.font_manager import FontProperties

"""Local Packages"""
import malaria_statistics as MS
from Latexifier import LatexifierFunctions as LF
#print("Importing done")

"""
|
|
Simple plotting:
|
|
"""
def simple():
    q = MS.MalariaStatistics("simple")

    #isEndemic, ratio = q.CheckEndemic()

    fig, ax = plt.subplots()
    q.PlotExtinctionTime(ax, "InfectionSpeed", showErrorBars=True)
    ax.set_xticks([1.0, 1.01, 1.02, 1.03, 1.04, 1.05])
    q.PlotNiceAndSave(fig = fig, ax=ax, xlabel=r"$\alpha$", ylabel = "Extinction time (gen)", fileName = "simple_extinctionTime")    

    fig, ax = plt.subplots()
    q.PlotMeanInfection(ax, "InfectionSpeed", showErrorBars=True)
    #ax.plot(np.arange(1.0,1.05+0.0001,0.001), -1/np.arange(1.0,1.05+0.0001,0.001)+1, color="r", linewidth=1.0, zorder=5, alpha=0.5) 
    ax.set_xticks([1.0, 1.01, 1.02, 1.03, 1.04, 1.05])
    ax.set_yticks([0.0,0.01,0.02,0.03,0.04,0.05])
    q.PlotNiceAndSave(fig = fig, ax = ax, xlabel = r"$\alpha$", ylabel = "Proportion infected", fileName = "simple_mean")

    fig, ax = plt.subplots()
    q.timelineIndex = [np.where( (q.parameters["InfectionSpeed"] == 1.02) )[0][0], 2]
    print("InfectionSpeed", q.parameters["InfectionSpeed"][q.timelineIndex[0]])
    q.ImportTimeline()
    q.PlotTimeline(ax = ax)
    q.PlotNiceAndSave(fig = fig, ax=ax, xlabel="Time (gen)", ylabel = "Proportion infected", fileName = "simple_timeseries1")

    fig, ax = plt.subplots()
    q.timelineIndex = [np.where( (q.parameters["InfectionSpeed"] == 1.04) )[0][0], 3]
    print("InfectionSpeed", q.parameters["InfectionSpeed"][q.timelineIndex[0]])
    q.ImportTimeline()
    q.PlotTimeline(ax = ax)
    q.PlotNiceAndSave(fig = fig, ax=ax, xlabel="Time (gen)", ylabel = "Proportion infected", fileName = "simple_timeseries2")
    return

"""
|
|
Replacement plotting:
|
|
"""
def replacement():
    alphas = [0.6, 0.8, 0.95, 1.05]

    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()
    
    for alpha in alphas:
        q = MS.MalariaStatistics("replacement")
        mask = (q.parameters['InfectionSpeed'][:] == alpha).values
        q.ApplyMask(mask=mask)

        q.PlotExtinctionTime(ax1, "ReplacementSpeed", showErrorBars=True, linewidth=0.25, alpha = 0.8)
        q.PlotMeanInfection(ax2, "ReplacementSpeed", showErrorBars=False, alpha = 0.8)

    ax1.legend([r"$\alpha$=0.6",r"$\alpha$=0.8",r"$\alpha$=0.95",r"$\alpha$=1.05"], bbox_to_anchor=[1.05, 0.5], loc=5, ncol=1)
    ax2.legend([r"$\alpha$=0.6",r"$\alpha$=0.8",r"$\alpha$=0.95",r"$\alpha$=1.05"])
    q.PlotNiceAndSave(fig1, ax1, xlabel = r"$\gamma$", ylabel = "Extinction time (gen)", fileName = "replacement_extinctionTime")
    q.PlotNiceAndSave(fig2, ax2, xlabel = r"$\gamma$", ylabel = "Proportion infected", fileName = "replacement_mean")

    q = MS.MalariaStatistics("replacement")

    # Plot of alpha=0.8 and gamma=0.16961
    fig, ax = plt.subplots()
    q.timelineIndex = [np.where( (q.parameters["InfectionSpeed"].values == 0.8) & (q.parameters["ReplacementSpeed"].values == 0.17) )[0][0], 1]
    print(q.timelineIndex)
    q.ImportTimeline()
    q.PlotTimeline(ax = ax)
    q.PlotNiceAndSave(fig, ax, xlabel = "Time (gen)", ylabel = "Proportion infected", fileName = "replacement_timeline1")

    # Plot of alpha=1.05 and gamma=0.8 
    fig, ax = plt.subplots()
    q.timelineIndex = [np.where( (q.parameters["InfectionSpeed"].values == 1.05) & (q.parameters["ReplacementSpeed"].values == 0.75) )[0][0], 1]
    print(q.timelineIndex)
    q.ImportTimeline()
    q.PlotTimeline(ax = ax)
    q.PlotNiceAndSave(fig, ax, xlabel = "Time (gen)", ylabel = "Proportion infected", fileName = "replacement_timeline2")

"""
|
|
Strain plotting:
|
|
"""

def features():
    q = MS.MalariaStatistics("features")

    alphas = q.parameters["InfectionSpeed"].unique()

    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()
    fig3, ax3 = plt.subplots()
    fig4, ax4 = plt.subplots()

    for alpha in alphas:
        q = MS.MalariaStatistics("features")
        mask = (q.parameters["InfectionSpeed"][:] == alpha).values
        q.ApplyMask(mask)

        q.PlotExtinctionTime(ax1, "MaxAntigenValue", showErrorBars=True)
        q.PlotMeanInfection(ax2, "MaxAntigenValue", showErrorBars=True)
        q.PlotEndStrains(ax3, "MaxAntigenValue", alpha=0.8)
        q.dataEnd.loc[:, "avgResistances"] = q.dataEnd.loc[:, "avgResistances"].values / q.parameters.loc[:, "MaxAntigenValue"].values
        q.PlotAvgResistances(ax4, "MaxAntigenValue")
        
        if alpha == 0.8:
            restant_temp1 = q.dataEnd.loc[:, "avgResistances"].values / q.parameters.loc[:, "MaxAntigenValue"].values

        if alpha == 1.05:
            restant_temp2 = q.dataEnd.loc[:, "avgResistances"].values / q.parameters.loc[:, "MaxAntigenValue"].values

    fig, ax = plt.subplots()
    ax.plot(restant_temp1/restant_temp2)
    print(restant_temp1/restant_temp2)

    ax1.set_xticks([0, 5, 10, 15, 20, 25])    
    ax2.set_xticks([0, 5, 10, 15, 20, 25])       
    ax3.set_xticks([0, 5, 10, 15, 20, 25])     
    ax3.set_yticks([0, 5, 10, 15, 20, 25])
    ax4.set_xticks([0, 5, 10, 15, 20, 25])
    ax3.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4])    
    ax1.legend([r"$\alpha$=0.6",r"$\alpha$=0.8",r"$\alpha$=0.95",r"$\alpha$=1.05"], ncol=1)
    ax2.legend([r"$\alpha$=0.6",r"$\alpha$=0.8",r"$\alpha$=0.95",r"$\alpha$=1.05"], ncol=2)
    ax3.legend([r"$\alpha$=0.6",r"$\alpha$=0.8",r"$\alpha$=0.95",r"$\alpha$=1.05"], ncol=1)
    ax4.legend([r"$\alpha$=0.6",r"$\alpha$=0.8",r"$\alpha$=0.95",r"$\alpha$=1.05"], ncol=2)
    q.PlotNiceAndSave(fig1, ax1, "Strains", ylabel = "Extinction time (gen)", fileName = "features_extinctionTime")
    q.PlotNiceAndSave(fig2, ax2, "Strains", ylabel = "Proportion infected", fileName = "features_mean")
    q.PlotNiceAndSave(fig3, ax3, "Strains", ylabel = "End infected", fileName = "features_endStrains")
    q.PlotNiceAndSave(fig4, ax4, "Strains", ylabel = "Avg. resistances per strain", fileName = "features_resistances")

    """Time-series"""
    LF.Latexify(fig_width = 12.65076*0.98, fig_height = 12.65076*0.98*0.40)

    q = MS.MalariaStatistics("features")
    fig, ax = plt.subplots()
    q.timelineIndex = [np.where( (q.parameters["InfectionSpeed"].values == 0.6) & (q.parameters["MaxAntigenValue"].values == 2) )[0][0] + 1, 1]
    print(q.timelineIndex)
    q.ImportTimeline()
    q.ImportStrainCounter()
    q.PlotTimeline(ax = ax)
    q.PlotStrainCounter(ax=ax, alpha=0.8)
    q.PlotNiceAndSave(fig, ax, xlabel = "Time (gen)", ylabel = "Proportion infected", fileName = "features_timeline1")

    q = MS.MalariaStatistics("features")
    fig, ax = plt.subplots()
    q.timelineIndex = [np.where( (q.parameters["InfectionSpeed"].values == 0.6) & (q.parameters["MaxAntigenValue"].values == 4) )[0][0] + 1, 1]
    print(q.timelineIndex)
    q.ImportTimeline()
    q.ImportStrainCounter()
    q.PlotTimeline(ax = ax, skip=10)
    q.PlotStrainCounter(ax=ax, alpha=0.8, skip=10)
    q.PlotNiceAndSave(fig, ax, xlabel = "Time (gen)", ylabel = "Proportion infected", fileName = "features_timeline2")

    

    return

def features2D():
    q = MS.MalariaStatistics("features2D")

    q.dataEnd.loc[q.dataEnd.loc[:, "run"] < 200, "mean"] = 0

    fig, ax = plt.subplots()
    q.Plot2D(fig, ax, "MaxAntigenValue", "InfectionSpeed", "run",ticks=[0,500,1000,1500,2000])
    ax.grid(False)
    ax.set_xticks([1,5,10,15,20,25])
    q.PlotNiceAndSave(fig, ax, "Strains", r"$\alpha$", "features2D_extinctionTime")

    fig, ax = plt.subplots()
    q.Plot2D(fig, ax, "MaxAntigenValue", "InfectionSpeed", "mean", ticks=[0.0,0.1,0.2,0.3,0.4,0.5])
    ax.grid(False)
    ax.set_xticks([1,5,10,15,20,25])
    q.PlotNiceAndSave(fig, ax, "Strains", r"$\alpha$", "features2D_mean")

    return

def featuresStatisticalValues():
    q = MS.MalariaStatistics("features2D")
    return
