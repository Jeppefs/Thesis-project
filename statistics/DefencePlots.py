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
import seaborn as sns

"""Local Packages"""
import malaria_statistics as MS
from Latexifier import LatexifierFunctions as LF

#plt.style.use("seaborn")
#LF.Latexify(fig_width = 12.65076*0.98, fig_height = 12.65076*0.98*0.45)
#q = MS.MalariaStatistics("crossNonCrossInjection")
#number = "1"
#
#x_ticks = [0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000]
#y_ticks = 0
#
#q.timelineIndex = [3, 1]
#print(q.parameters.iloc[q.timelineIndex[0]-1, :])    
#fig, ax = plt.subplots()
#q.ImportTimeline()
#q.ImportStrainCounter()
#q.PlotTimeline(ax = ax, skip = 100)
#q.PlotStrainCounter(ax = ax, skip = 100)
#ax.set_xticks(x_ticks)
#ax.set_yticks([0.0, 0.02, 0.04, 0.06, 0.08, 0.1, 0.12, 0.14])
#leg = ax.legend(["Sum","1,2", "2,3", "3,4", "4,1"], bbox_to_anchor=[0.5, 1.05], loc=10, ncol=5)
#for legobj in leg.legendHandles:
#    legobj.set_linewidth(2.0)
#q.PlotNiceAndSave(fig, ax, xlabel = "Time (gen)", ylabel = "Infected", fileName = "cross_strainCounter" + number)

def crossInjection():

    def calcDiff(q0, q1, q2):
        q0.dataEnd["mean"] = abs(q1.dataEnd["mean"].values - q2.dataEnd["mean"].values)
        q0.dataEnd["run"] = abs(q1.dataEnd["run"].values - q2.dataEnd["run"].values)
        q0.dataEnd["strains"] = abs(q1.dataEnd["strains"].values - q2.dataEnd["strains"].values)
        q0.dataEnd["avgResistances"] = abs(q1.dataEnd["avgResistances"].values - q2.dataEnd["avgResistances"].values)
        q0.dataEnd["run_error"] = abs(q1.dataEnd["mean"].values*0)
        return q0

    def makeAllPlots(q, axes, figs):
        q.PlotExtinctionTime(axes[0], "InfectionSpeed")
        q.PlotMeanInfection(axes[1], "InfectionSpeed", showErrorBars=False)
        q.PlotEndStrains(axes[2], "InfectionSpeed")
        q.PlotAvgResistances(axes[3], "InfectionSpeed")
        return

    def saveAndSetAllPlots(q, axes, figs, nameAddition, legend = ["Cross", "No cross", "Diff"]):
        x_ticks = [0.35, 0.4, 0.45, 0.5, 0.55, 0.6]   

        axes[2].set_yticks( np.arange(0, np.max(q.dataEnd["strains"].values) + 1) )
        for ax in axes:
            ax.legend(legend)
            ax.set_xticks(x_ticks)
        
        q.PlotNiceAndSave(figs[0], axes[0], r"$\alpha$", ylabel = "Extinction time (gen)", fileName = "cross" + nameAddition + "_extinctionTime")
        q.PlotNiceAndSave(figs[1], axes[1], r"$\alpha$", ylabel = "Proportion infected", fileName = "cross" + nameAddition + "_mean")
        q.PlotNiceAndSave(figs[2], axes[2], r"$\alpha$", ylabel = "Number of end strains", fileName = "cross" + nameAddition + "_strains")
        q.PlotNiceAndSave(figs[3], axes[3], r"$\alpha$", ylabel = "Avg. resistances", fileName = "cross" + nameAddition + "_resistances")


    """Write what you you want to plot"""
    dataAndMaskList = [["crossNonCrossInjection", "cross"], ["crossNonCross", "cross"], ["crossNonCross", "cross"],
    ["crossNonCrossInjection", "nonCross"], ["crossNonCross", "nonCross"], ["crossNonCross", "nonCross"], 
    ["crossNonCrossInjection", "simple"], ["crossSimple", "simple"],  ["crossSimple", "simple"]]
    

    q = []
    for i, dataName in enumerate(dataAndMaskList):
        q.append(MS.MalariaStatistics(dataName[0]))
        q[i].ApplyMask(q[i].parameters["SpecificStrains"][:].values == dataName[1])

    q[2] = calcDiff(q[2], q[0], q[1])
    q[5] = calcDiff(q[5], q[3], q[4])
    q[8] = calcDiff(q[8], q[6], q[7])

    """ Now plotting begins """
    axes = []
    figs = []
    for i in range(12):
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
    makeAllPlots(q[7], axes[8:12], figs[8:12])
    makeAllPlots(q[8], axes[8:12], figs[8:12])
    
    saveAndSetAllPlots(q[0], axes[0:4], figs[0:4], nameAddition="_crossInjection", legend=["With Vaccine", "Without", "Diff"])
    saveAndSetAllPlots(q[3], axes[4:8], figs[4:8], nameAddition="_nonCrossInjection", legend=["With Vaccine", "Without", "Diff"])
    saveAndSetAllPlots(q[6], axes[8:12], figs[8:12], nameAddition="_simpleInjection", legend=["With Vaccine", "Without", "Diff"])

    return


def crossInjectionFast():

    def calcDiff(q0, q1, q2):
        q0.dataEnd["mean"] = abs(q1.dataEnd["mean"].values - q2.dataEnd["mean"].values)
        q0.dataEnd["run"] = abs(q1.dataEnd["run"].values - q2.dataEnd["run"].values)
        q0.dataEnd["strains"] = abs(q1.dataEnd["strains"].values - q2.dataEnd["strains"].values)
        q0.dataEnd["avgResistances"] = abs(q1.dataEnd["avgResistances"].values - q2.dataEnd["avgResistances"].values)
        q0.dataEnd["run_error"] = abs(q1.dataEnd["mean"].values*0)
        return q0

    def makeAllPlots(q, axes, figs):
        q.PlotExtinctionTime(axes[0], "InfectionSpeed")
        q.PlotMeanInfection(axes[1], "InfectionSpeed", showErrorBars=False)
        q.PlotEndStrains(axes[2], "InfectionSpeed")
        q.PlotAvgResistances(axes[3], "InfectionSpeed")
        return

    def saveAndSetAllPlots(q, axes, figs, nameAddition, legend = ["Cross", "No cross", "Diff"]):
        x_ticks = [0.35, 0.4, 0.45, 0.5, 0.55, 0.6]   

        axes[2].set_yticks( np.arange(0, np.max(q.dataEnd["strains"].values) + 1) )
        for ax in axes:
            ax.legend(legend)
            ax.set_xticks(x_ticks)
        
        q.PlotNiceAndSave(figs[0], axes[0], r"$\alpha$", ylabel = "Extinction time (gen)", fileName = "cross" + nameAddition + "_extinctionTime")
        q.PlotNiceAndSave(figs[1], axes[1], r"$\alpha$", ylabel = "Proportion infected", fileName = "cross" + nameAddition + "_mean")
        q.PlotNiceAndSave(figs[2], axes[2], r"$\alpha$", ylabel = "Number of end strains", fileName = "cross" + nameAddition + "_strains")
        q.PlotNiceAndSave(figs[3], axes[3], r"$\alpha$", ylabel = "Avg. resistances", fileName = "cross" + nameAddition + "_resistances")


    """Write what you you want to plot"""
    dataAndMaskList = [["crossNonCrossInjectionFast", "cross"], ["crossNonCross", "cross"], ["crossNonCross", "cross"],
    ["crossNonCrossInjectionFast", "nonCross"], ["crossNonCross", "nonCross"], ["crossNonCross", "nonCross"], 
    ["crossNonCrossInjectionFast", "simple"], ["crossSimple", "simple"],  ["crossSimple", "simple"]]
    

    q = []
    for i, dataName in enumerate(dataAndMaskList):
        q.append(MS.MalariaStatistics(dataName[0]))
        q[i].ApplyMask(q[i].parameters["SpecificStrains"][:].values == dataName[1])

    q[2] = calcDiff(q[2], q[0], q[1])
    q[5] = calcDiff(q[5], q[3], q[4])
    q[8] = calcDiff(q[8], q[6], q[7])

    """ Now plotting begins """
    axes = []
    figs = []
    for i in range(12):
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
    makeAllPlots(q[7], axes[8:12], figs[8:12])
    makeAllPlots(q[8], axes[8:12], figs[8:12])
    
    saveAndSetAllPlots(q[0], axes[0:4], figs[0:4], nameAddition="_crossInjectionFast", legend=["With Vaccine", "Without", "Diff"])
    saveAndSetAllPlots(q[3], axes[4:8], figs[4:8], nameAddition="_nonCrossInjectionFast", legend=["With Vaccine", "Without", "Diff"])
    saveAndSetAllPlots(q[6], axes[8:12], figs[8:12], nameAddition="_simpleInjectionFast", legend=["With Vaccine", "Without", "Diff"])

    return

def crossInjectionTimeSeries():

    plt.style.use("seaborn")
    LF.Latexify(fig_width = 12.65076*0.98, fig_height = 12.65076*0.98*0.45)
    q = MS.MalariaStatistics("crossNonCrossInjectionFast")
    number = "1"

    for_infectionSpeed = 0.50
    x_ticks = [0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000]
    y_ticks = 0

    q.timelineIndex = [np.where( (q.parameters["InfectionSpeed"] == for_infectionSpeed) & (q.parameters["SpecificStrains"] == "cross"))[0][0]+1, 1]
    print(q.parameters.iloc[q.timelineIndex[0], :])    
    fig, ax = plt.subplots()
    q.ImportTimeline()
    q.ImportStrainCounter()
    q.PlotTimeline(ax = ax, skip = 100)
    q.PlotStrainCounter(ax = ax, skip = 100)
    ax.set_xticks(x_ticks)
    #ax.set_yticks([0.0, 0.02, 0.04, 0.06, 0.08, 0.1, 0.12, 0.14])
    leg = ax.legend(["Sum","1,2", "2,3", "3,4", "4,1"], bbox_to_anchor=[0.5, 1.05], loc=10, ncol=5)
    for legobj in leg.legendHandles:
        legobj.set_linewidth(2.0)
    q.PlotNiceAndSave(fig, ax, xlabel = "Time (gen)", ylabel = "Infected", fileName = "cross_strainCounterInjection1" + number)

    q.timelineIndex = [np.where( (q.parameters["InfectionSpeed"] == for_infectionSpeed) & (q.parameters["SpecificStrains"] == "simple"))[0][0] + 1, 1]
    print(q.parameters.iloc[q.timelineIndex[0], :])
    fig, ax = plt.subplots()
    q.ImportTimeline()
    q.ImportStrainCounter()
    q.PlotTimeline(ax = ax, skip = 100)
    q.PlotStrainCounter(ax = ax, skip = 100)
    ax.set_xticks(x_ticks)
    #ax.set_yticks([0.0, 0.02, 0.04, 0.06, 0.08, 0.1, 0.12, 0.14, 0.16, 0.18])
    leg = ax.legend(["Sum","1,2","3,4"], bbox_to_anchor=[0.5, 1.05], loc=10, ncol=5)
    for legobj in leg.legendHandles:
        legobj.set_linewidth(2.0)
    q.PlotNiceAndSave(fig, ax, xlabel = "Time (gen)", ylabel = "Infected", fileName = "cross_strainCounterInjection2" + number)

    return