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
    LF.Latexify(fig_width = 12.65076*0.98, fig_height = 12.65076*0.98*0.5)

    q = MS.MalariaStatistics("mutation")

    gammas = q.parameters["ReplacementSpeed"].unique()
    mus = q.parameters["MutationSpeed"].unique()
    
    q.timelineIndex = [np.where( (q.parameters["MaxAntigenValue"] == 3) & (q.parameters["ReplacementSpeed"] == np.max(gammas))
     & (q.parameters["MutationSpeed"] == 0) )[0][0] + 1 , 1]
    fig, ax = plt.subplots()
    q.ImportTimeline()
    q.ImportStrainCounter()
    q.PlotTimeline(ax = ax, skip = 100)
    q.PlotStrainCounter(ax = ax, skip = 200)
    ax.set_xticks([0, 500, 1000, 1500, 2000])
    ax.set_yticks([0, 0.02, 0.04, 0.06, 0.08])
    q.PlotNiceAndSave(fig, ax, xlabel = "Time (gen)", ylabel = "Infected", fileName = "mutation_strainCounter1")

    q.timelineIndex = [np.where( (q.parameters["MaxAntigenValue"] == 3) & (q.parameters["ReplacementSpeed"] == np.max(gammas))
     & (q.parameters["MutationSpeed"] == 10**(-4)) )[0][0] + 1, 1]
    print(q.parameters.iloc[q.timelineIndex[0], :])
    fig, ax = plt.subplots()
    q.ImportTimeline()
    q.ImportStrainCounter()
    q.PlotTimeline(ax = ax, skip = 100)
    q.PlotStrainCounter(ax = ax, skip = 200)
    ax.set_xticks([0, 500, 1000, 1500, 2000])
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
    """Plot mean and extinction time"""
    fig = [],
    figBig = []
    figSimple = []
    figOdd = []
    ax = []
    axBig = []
    axSimple = []
    axOdd = []

    for i in range(4):
        figTemp, axTemp = plt.subplots()
        fig.append(figTemp), ax.append(axTemp)

        figTemp, axTemp = plt.subplots()
        figStrains.append(figTemp), axStrains.append(axTemp)

        figTemp, axTemp = plt.subplots()
        figMean.append(figTemp), axMean.append(axTemp)

    qCross = MS.MalariaStatistics("crossNonCross")
    qNon = MS.MalariaStatistics("crossNonCross")
    qCrossBig = MS.MalariaStatistics("crossBig")
    qNonBig = MS.MalariaStatistics("crossBig")
    qOdd = MS.MalariaStatistics("crossOdd")
    qSimple = MS.MalariaStatistics("crossSimple")
    
    qDiff = MS.MalariaStatistics("crossNonCross")
    qDiffBig = MS.MalariaStatistics("crossBig")
    qDiffSimple = MS.MalariaStatistics("crossSimple")

    qCross.ApplyMask(qCross.parameters["SpecificStrains"][:].values =="cross")
    qNon.ApplyMask(qNon.parameters["SpecificStrains"][:].values == "nonCross")
    qDiff.ApplyMask(qDiff.parameters["SpecificStrains"][:].values == "nonCross")
    qCrossBig.ApplyMask(qCrossBig.parameters["SpecificStrains"][:].values =="crossBig")
    qNonBig.ApplyMask(qNonBig.parameters["SpecificStrains"][:].values == "nonCrossBig")
    qDiffBig.ApplyMask(qDiffBig.parameters["SpecificStrains"][:].values == "nonCrossBig")

    """ New values being calculated """
    qDiff.dataEnd["mean"] = abs(qNon.dataEnd["mean"].values - qCross.dataEnd["mean"].values)
    qDiff.dataEnd["run"] = abs(qNon.dataEnd["run"].values - qCross.dataEnd["run"].values)
    qDiff.dataEnd["strains"] = abs(qNon.dataEnd["strains"].values - qCross.dataEnd["strains"].values)
    qDiff.dataEnd["avgResistances"] = abs(qNon.dataEnd["avgResistances"].values - qCross.dataEnd["avgResistances"].values)
    qDiff.dataEnd["run_error"] = abs(qCross.dataEnd["mean"].values*0)

    qDiffBig.dataEnd["mean"] = abs(qNonBig.dataEnd["mean"].values - qCrossBig.dataEnd["mean"].values)
    qDiffBig.dataEnd["run"] = abs(qNonBig.dataEnd["run"].values - qCrossBig.dataEnd["run"].values)
    qDiffBig.dataEnd["strains"] = abs(qNonBig.dataEnd["strains"].values - qCrossBig.dataEnd["strains"].values)
    qDiffBig.dataEnd["avgResistances"] = abs(qNonBig.dataEnd["avgResistances"].values - qCrossBig.dataEnd["avgResistances"].values)
    qDiffBig.dataEnd["run_error"] = abs(qCrossBig.dataEnd["mean"].values*0)

    qDiffSimple.dataEnd["mean"] = abs(qSimple.dataEnd["mean"].values - qCross.dataEnd["mean"].values)
    qDiffSimple.dataEnd["run"] = abs(qSimple.dataEnd["run"].values - qCross.dataEnd["run"].values)
    qDiffSimple.dataEnd["strains"] = abs(qSimple.dataEnd["strains"].values - qCross.dataEnd["strains"].values)
    qDiffSimple.dataEnd["avgResistances"] = abs(qSimple.dataEnd["avgResistances"].values - qCross.dataEnd["avgResistances"].values)
    qDiffSimple.dataEnd["run_error"] = abs(qCross.dataEnd["mean"].values*0)

    """ Plotting begins """
    qCross.PlotExtinctionTime(ax[0], "InfectionSpeed")
    qNon.PlotExtinctionTime(ax[0], "InfectionSpeed")
    qDiff.PlotExtinctionTime(ax[0], "InfectionSpeed")
    qCrossBig.PlotExtinctionTime(ax[1], "InfectionSpeed")
    qNonBig.PlotExtinctionTime(ax[1], "InfectionSpeed")
    qDiffBig.PlotExtinctionTime(ax[1], "InfectionSpeed")
    qSimple.PlotExtinctionTime(ax[2], "InfectionSpeed")
    qCross.PlotExtinctionTime(ax[2], "InfectionSpeed")
    qSimpleDiff.PlotExtinctionTime(ax[2], "InfectionSpeed")
    qOdd.PlotExtinctionTime(ax[3], "InfectionSpeed")

    qCross.PlotExtinctionTime(axStrains[0], "InfectionSpeed")
    qNon.PlotExtinctionTime(axStrains[0], "InfectionSpeed")
    qDiff.PlotExtinctionTime(axStrains[0], "InfectionSpeed")
    qCrossBig.PlotExtinctionTime(axStrains[1], "InfectionSpeed")
    qNonBig.PlotExtinctionTime(axStrains[1], "InfectionSpeed")
    qDiffBig.PlotExtinctionTime(axStrains[1], "InfectionSpeed")
    qSimple.PlotExtinctionTime(axStrains[2], "InfectionSpeed")
    qCross.PlotExtinctionTime(axStrains[2], "InfectionSpeed")
    qSimpleDiff.PlotExtinctionTime(axStrains[2], "InfectionSpeed")
    qOdd.PlotExtinctionTime(axStrains[3], "InfectionSpeed")

    qCross.PlotMeanInfection(ax2, "InfectionSpeed", errorBars=False)
    qNon.PlotMeanInfection(ax2, "InfectionSpeed", errorBars=False)
    qDiff.PlotMeanInfection(ax2, "InfectionSpeed", errorBars=False)

    #ax3.plot(qCross.parameters["InfectionSpeed"], qCross.dataEnd["strains"], '-o', markersize=3.0, linewidth=0.5)
    #ax3.plot(qNon.parameters["InfectionSpeed"], qNon.dataEnd["strains"], '-o', markersize=3.0, linewidth=0.5)
    #ax3.plot(qDiff.parameters["InfectionSpeed"], qDiff.dataEnd["strains"], '-o', markersize=3.0, linewidth=0.5)

    qCross.PlotAvgResistances(ax4, "InfectionSpeed")
    qNon.PlotAvgResistances(ax4, "InfectionSpeed")
    qDiff.PlotAvgResistances(ax4, "InfectionSpeed")

    ax1.legend(["Cross", "Not", "Diff"])
    ax2.legend(["Cross", "Not", "Diff"])
    ax3.legend(["Cross", "Not", "Diff"])
    ax4.legend(["Cross", "Not", "Diff"])
    x_ticks = [0.35, 0.4, 0.45, 0.5, 0.55, 0.6]   
    ax1.set_xticks(x_ticks)
    ax2.set_xticks(x_ticks)
    ax3.set_xticks(x_ticks)
    ax3.set_yticks( np.arange(0, np.max(qCross.dataEnd["strains"].values) + 1) )
    ax4.set_xticks(x_ticks)
    qCross.PlotNiceAndSave(fig1, ax1, r"$\alpha$", ylabel = "Extinction time (gen)", fileName = "cross" + addition + "extinctionTime")
    qCross.PlotNiceAndSave(fig2, ax2, r"$\alpha$", ylabel = "Mean infected", fileName = "cross" + addition + "_mean")
    qCross.PlotNiceAndSave(fig3, ax3, r"$\alpha$", ylabel = "Number of end strains", fileName = "cross" + addition + "_strains")
    qCross.PlotNiceAndSave(fig4, ax4, r"$\alpha$", ylabel = "Average resistances per host", fileName = "cross" + addition + "_resistances")

    return

def crossTimeSeries():
    plt.style.use("seaborn")
    LF.Latexify(fig_width = 12.65076*0.98, fig_height = 12.65076*0.98*0.5)
    q = MS.MalariaStatistics("crossNonCross")
    
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
    q.PlotNiceAndSave(fig, ax, xlabel = "Time (gen)", ylabel = "Infected", fileName = "cross_strainCounter1")

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
    q.PlotNiceAndSave(fig, ax, xlabel = "Time (gen)", ylabel = "Infected", fileName = "nonCross_strainCounter1")

def crossBigTimeSeries():
    plt.style.use("seaborn")
    LF.Latexify(fig_width = 12.65076*0.98, fig_height = 12.65076*0.98*0.5)
    #q = MS.MalariaStatistics("crossNonCross")
    q = MS.MalariaStatistics("crossBig")

    for_infectionSpeed = 0.40
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
    q.PlotNiceAndSave(fig, ax, xlabel = "Time (gen)", ylabel = "Infected", fileName = "crossBig_strainCounter1")

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
    q.PlotNiceAndSave(fig, ax, xlabel = "Time (gen)", ylabel = "Infected", fileName = "nonCrossBig_strainCounter1")
