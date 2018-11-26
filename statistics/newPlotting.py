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

"""
|
|
Mutation plotting:
|
|
"""

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
    q = MS.MalariaStatistics("mutation2D")
    mus = np.sort(q.parameters["MutationSpeed"].unique())

    for mu in mus:
        q = MS.MalariaStatistics("mutation2D")
        mask = (q.parameters["MutationSpeed"][:] == mu).values
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

        """Find out where extinction time is at 2000"""
        print(mu, np.min(q.parameters.loc[q.dataEnd["run"]>1980, "InfectionSpeed"]))

    return

def mutationTimeSeries():
    plt.style.use("seaborn")
    LF.Latexify(fig_width = 12.65076*0.98, fig_height = 12.65076*0.98*0.40)

    q = MS.MalariaStatistics("mutation")

    gammas = q.parameters["ReplacementSpeed"].unique()
    mus = q.parameters["MutationSpeed"].unique()
    
    q.timelineIndex = [np.where( (q.parameters["MaxAntigenValue"] == 3) & (q.parameters["ReplacementSpeed"] == np.max(gammas))
     & (q.parameters["MutationSpeed"] == 0) )[0][0] + 1 , 1]
    fig, ax = plt.subplots()
    q.ImportTimeline()
    q.ImportStrainCounter()
    q.PlotTimeline(ax = ax, skip = 100)
    q.PlotStrainCounter(ax = ax, skip = 100)
    ax.set_xticks([0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000])
    ax.set_yticks([0, 0.02, 0.04, 0.06, 0.08])
    q.PlotNiceAndSave(fig, ax, xlabel = "Time (gen)", ylabel = "Infected", fileName = "mutation_strainCounter1")

    q.timelineIndex = [np.where( (q.parameters["MaxAntigenValue"] == 3) & (q.parameters["ReplacementSpeed"] == np.max(gammas))
     & (q.parameters["MutationSpeed"] == 10**(-4)) )[0][0] + 1, 1]
    print(q.parameters.iloc[q.timelineIndex[0], :])
    fig, ax = plt.subplots()
    q.ImportTimeline()
    q.ImportStrainCounter()
    q.PlotTimeline(ax = ax, skip = 100)
    q.PlotStrainCounter(ax = ax, skip = 100)
    ax.set_xticks([0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000])
    ax.set_yticks([0, 0.02, 0.04, 0.06, 0.08])
    q.PlotNiceAndSave(fig, ax, xlabel = "Time (gen)", ylabel = "Infected", fileName = "mutation_strainCounter2")

    return

"""
|
|
Cross immunity plots:
|
|
"""

def crossNonCross():

    def calcDiff(q0, q1, q2):
        q0.dataEnd["mean"] = abs(q1.dataEnd["mean"].values - q2.dataEnd["mean"].values)
        q0.dataEnd["run"] = abs(q1.dataEnd["run"].values - q2.dataEnd["run"].values)
        q0.dataEnd["strains"] = abs(q1.dataEnd["strains"].values - q2.dataEnd["strains"].values)
        q0.dataEnd["avgResistances"] = abs(q1.dataEnd["avgResistances"].values - q2.dataEnd["avgResistances"].values)
        q0.dataEnd["run_error"] = abs(q1.dataEnd["mean"].values*0)
        return q0

    def makeAllPlots(q, axes, figs):
        q.PlotExtinctionTime(axes[0], "InfectionSpeed")
        q.PlotMeanInfection(axes[1], "InfectionSpeed", errorBars=False)
        q.PlotEndStrains(axes[2], "InfectionSpeed")
        q.PlotAvgResistances(axes[3], "InfectionSpeed")
        return

    def saveAndSetAllPlots(q, axes, figs, nameAddition, legend = ["Cross", "Not", "Diff"]):
        x_ticks = [0.35, 0.4, 0.45, 0.5, 0.55, 0.6]   

        axes[2].set_yticks( np.arange(0, np.max(q.dataEnd["strains"].values) + 1) )
        for ax in axes:
            ax.legend(legend)
            ax.set_xticks(x_ticks)
        
        q.PlotNiceAndSave(figs[0], axes[0], r"$\alpha$", ylabel = "Extinction time (gen)", fileName = "cross" + nameAddition + "_extinctionTime")
        q.PlotNiceAndSave(figs[1], axes[1], r"$\alpha$", ylabel = "Mean infected", fileName = "cross" + nameAddition + "_mean")
        q.PlotNiceAndSave(figs[2], axes[2], r"$\alpha$", ylabel = "Number of end strains", fileName = "cross" + nameAddition + "_strains")
        q.PlotNiceAndSave(figs[3], axes[3], r"$\alpha$", ylabel = "Average resistances per host", fileName = "cross" + nameAddition + "_resistances")


    """Write what you you want to plot"""
    dataAndMaskList = [["crossNonCross", "cross"], ["crossNonCross", "nonCross"], ["crossNonCross", "cross"],
    ["crossBig", "crossBig"], ["crossBig", "nonCrossBig"], ["crossBig", "crossBig"], 
    ["crossOdd", "odd"],
    ["crossNonCross", "cross"], ["crossSimple", "simple"],  ["crossNonCross", "cross"]]

    q = []
    for i, dataName in enumerate(dataAndMaskList):
        q.append(MS.MalariaStatistics(dataName[0]))
        q[i].ApplyMask(q[i].parameters["SpecificStrains"][:].values == dataName[1])

    q[2] = calcDiff(q[2], q[0], q[1])
    q[5] = calcDiff(q[5], q[3], q[4])
    q[9] = calcDiff(q[9], q[7], q[8])

    """ Now plotting begins """
    axes = []
    figs = []
    for i in range(16):
        figTemp, axTemp = plt.subplots()
        figs.append(figTemp)
        axes.append(axTemp)

    makeAllPlots(q[0], axes[0:4], figs[0:4])
    makeAllPlots(q[1], axes[0:4], figs[0:4])
    makeAllPlots(q[2], axes[0:4], figs[0:4])    
    makeAllPlots(q[3], axes[4:8], figs[4:8])
    makeAllPlots(q[4], axes[4:8], figs[4:8])
    makeAllPlots(q[5], axes[4:8], figs[4:8])
    makeAllPlots(q[6], axes[8:12], figs[8:12]) 
    makeAllPlots(q[7], axes[12:16], figs[12:16])
    makeAllPlots(q[8], axes[12:16], figs[12:16])
    makeAllPlots(q[9], axes[12:16], figs[12:16])
    
    saveAndSetAllPlots(q[0], axes[0:4], figs[0:4], nameAddition="")
    saveAndSetAllPlots(q[3], axes[4:8], figs[4:8], nameAddition="Big", legend = ["Cross big", "No cross big", "Diff"])
    saveAndSetAllPlots(q[6], axes[8:12], figs[8:12], nameAddition="Odd", legend=["Odd"])
    saveAndSetAllPlots(q[7], axes[12:16], figs[12:16], nameAddition="Simple", legend=["Cross", "Simple", "Diff"])

    return

def crossTimeSeries():
    plt.style.use("seaborn")
    LF.Latexify(fig_width = 12.65076*0.98, fig_height = 12.65076*0.98*0.45)
    q = MS.MalariaStatistics("crossNonCross")
    number = "1"

    for_infectionSpeed = 0.45
    x_ticks = [0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000]
    y_ticks = 0

    q.timelineIndex = [np.where( (q.parameters["InfectionSpeed"] == for_infectionSpeed) & (q.parameters["SpecificStrains"] == "cross"))[0][0] + 1, 1]
    print(q.parameters.iloc[q.timelineIndex[0], :])    
    fig, ax = plt.subplots()
    q.ImportTimeline()
    q.ImportStrainCounter()
    q.PlotTimeline(ax = ax, skip = 100)
    q.PlotStrainCounter(ax = ax, skip = 100)
    ax.set_xticks(x_ticks)
    ax.set_yticks([0.0, 0.02, 0.04, 0.06, 0.08, 0.1, 0.12, 0.14])
    leg = ax.legend(["Sum","1,2", "2,3", "3,4", "4,1"], bbox_to_anchor=[0.5, 1.05], loc=10, ncol=5)
    for legobj in leg.legendHandles:
        legobj.set_linewidth(2.0)
    q.PlotNiceAndSave(fig, ax, xlabel = "Time (gen)", ylabel = "Infected", fileName = "cross_strainCounter" + number)

    q.timelineIndex = [np.where( (q.parameters["InfectionSpeed"] == for_infectionSpeed) & (q.parameters["SpecificStrains"] == "nonCross"))[0][0] + 1, 1]
    print(q.parameters.iloc[q.timelineIndex[0], :])
    fig, ax = plt.subplots()
    q.ImportTimeline()
    q.ImportStrainCounter()
    q.PlotTimeline(ax = ax, skip = 100)
    q.PlotStrainCounter(ax = ax, skip = 100)
    ax.set_xticks(x_ticks)
    ax.set_yticks([0.0, 0.02, 0.04, 0.06, 0.08, 0.1, 0.12, 0.14, 0.16, 0.18])
    leg = ax.legend(["Sum","1,2","3,4","5,6","7,8"], bbox_to_anchor=[0.5, 1.05], loc=10, ncol=5)
    for legobj in leg.legendHandles:
        legobj.set_linewidth(2.0)
    q.PlotNiceAndSave(fig, ax, xlabel = "Time (gen)", ylabel = "Infected", fileName = "nonCross_strainCounter" + number)

def crossBigTimeSeries():
    plt.style.use("seaborn")
    LF.Latexify(fig_width = 12.65076*0.98, fig_height = 12.65076*0.98*0.45)
    q = MS.MalariaStatistics("crossBig")
    number = "1"

    for_infectionSpeed = 0.45
    x_ticks = [0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000]
    y_ticks = 0

    q.timelineIndex = [np.where( (q.parameters["InfectionSpeed"] == for_infectionSpeed) & (q.parameters["SpecificStrains"] == "crossBig"))[0][0] + 1, 1]
    print(q.parameters.iloc[q.timelineIndex[0] - 1, :])    
    fig, ax = plt.subplots()
    q.ImportTimeline()
    q.ImportStrainCounter()
    q.PlotTimeline(ax = ax, skip = 100)
    q.PlotStrainCounter(ax = ax, skip = 100)
    ax.set_xticks(x_ticks)
    #ax.set_yticks([0.0, 0.02, 0.04, 0.06, 0.08, 0.1, 0.12, 0.14])
    leg = ax.legend(["Sum","1,2", "2,3", "3,4", "4,5", "5,6", "6,1"], bbox_to_anchor=[0.5, 1.05], loc=10, ncol=7)
    for legobj in leg.legendHandles:
        legobj.set_linewidth(2.0)
    q.PlotNiceAndSave(fig, ax, xlabel = "Time (gen)", ylabel = "Infected", fileName = "crossBig_strainCounter" + number)

    q.timelineIndex = [np.where( (q.parameters["InfectionSpeed"] == for_infectionSpeed) & (q.parameters["SpecificStrains"] == "nonCrossBig"))[0][0] + 1, 1]
    print(q.parameters.iloc[q.timelineIndex[0] - 1, :])
    fig, ax = plt.subplots()
    q.ImportTimeline()
    q.ImportStrainCounter()
    q.PlotTimeline(ax = ax, skip = 100)
    q.PlotStrainCounter(ax = ax, skip = 100)
    ax.set_xticks(x_ticks)
    #ax.set_yticks([0.0, 0.02, 0.04, 0.06, 0.08, 0.1, 0.12, 0.14, 0.16, 0.18])
    leg = ax.legend(["Sum","1,2","3,4","5,6","7,8","9,10","11,12"], bbox_to_anchor=[0.5, 1.05], loc=10, ncol=7)
    for legobj in leg.legendHandles:
        legobj.set_linewidth(2.0)
    q.PlotNiceAndSave(fig, ax, xlabel = "Time (gen)", ylabel = "Infected", fileName = "nonCrossBig_strainCounter" + number)

def crossOdd():
    plt.style.use("seaborn")
    LF.Latexify(fig_width = 12.65076*0.98, fig_height = 12.65076*0.98*0.45)
    q = MS.MalariaStatistics("crossOdd")

    for_infectionSpeed = 0.45
    x_ticks = [0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000]
    y_ticks = 0

    q.timelineIndex = [np.where( (q.parameters["InfectionSpeed"] == for_infectionSpeed) & (q.parameters["SpecificStrains"] == "odd"))[0][0] + 1, 1]
    print(q.parameters.iloc[q.timelineIndex[0] - 1, :])    
    fig, ax = plt.subplots()
    q.ImportTimeline()
    q.ImportStrainCounter()
    q.PlotTimeline(ax = ax, skip = 100)
    q.PlotStrainCounter(ax = ax, skip = 100)
    ax.set_xticks(x_ticks)
    #ax.set_yticks([0.0, 0.02, 0.04, 0.06, 0.08, 0.1, 0.12, 0.14])
    leg = ax.legend(["Sum","1,2", "2,3", "3,4", "4,5", "5,1"], bbox_to_anchor=[0.5, 1.05], loc=10, ncol=7)
    for legobj in leg.legendHandles:
        legobj.set_linewidth(2.0)
    q.PlotNiceAndSave(fig, ax, xlabel = "Time (gen)", ylabel = "Infected", fileName = "crossOdd_strainCounter1")
