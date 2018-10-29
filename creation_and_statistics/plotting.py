import malaria_statistics as MS 
from Latexifier import LatexifierFunctions as LF

import numpy as np
import matplotlib.pyplot as plt
import pandas as pandas
import scipy.optimize as op

def simple():
    LF.Latexify(fig_width=6.19893, label_size=[1.0, 1.0])
    q = MS.MalariaStatistics("simple")

    q.CalcNewMeans()
    isEndemic, ratio = q.CheckEndemic()

    fig, ax = plt.subplots()
    q.PlotExtinctionTime(ax, "InfectionSpeed", xlabel = r"$\alpha$")
    q.PlotNiceAndSave(fig = fig, ax=ax, xlabel=r"\alpha$", ylabel = "Extinction time (gen)", fileName = "extinctionTime")    

    fig, ax = plt.subplots()
    q.PlotMeanInfection(ax, "InfectionSpeed", xlabel = r"$\alpha$")
    ax.plot(np.arange(1.0,1.05+0.0001,0.001), -1/np.arange(1.0,1.05+0.0001,0.001)+1, color="r", linewidth=1.0, zorder=5, alpha=0.5) 
    q.PlotNiceAndSave(fig = fig, ax = ax, xlabel = r"$\alpha$", ylabel = "Mean infected", fileName = "mean")

    fig, ax = plt.subplots()
    q.timelineIndex = [10, 1]
    print("InfectionSpeed", q.parameters["InfectionSpeed"][q.timelineIndex[0]])
    q.ImportTimeline()
    q.PlotTimeline(ax = ax)
    q.PlotNiceAndSave(fig = fig, ax=ax, xlabel=r"\alpha$", ylabel = q.plotSettings.yTimeLabel, fileName = "extinctionTime")

    fig, ax = plt.subplots()
    q.timelineIndex = [30, 2]
    print("InfectionSpeed", q.parameters["InfectionSpeed"][q.timelineIndex[0]])
    q.ImportTimeline()
    q.PlotTimeline(ax = ax)
    q.PlotNiceAndSave(fig = fig, ax=ax, xlabel=r"\alpha$", ylabel = q.plotSettings.yTimeLabel, fileName = "extinctionTime")
    return

def replacement(): 
    LF.Latexify(fig_width = 6.19893, label_size=[1.0, 1.0])
    q = MS.MalariaStatistics("replacement")
    q.plotSettings.saveFigs = False
    q.CalcNewMeans()
    q.CreateDataCopies()

    alphas = [0.6, 0.8, 0.95, 1.05]

    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()
    
    for alpha in alphas:
        mask = (q.parametersCopy['InfectionSpeed'][:] == alpha).as_matrix()
        q.ApplyMask(mask=mask)

        q.PlotExtinctionTime(ax1, "ReplacementSpeed", xlabel = r"$\gamma$")
        q.PlotMeanInfection(ax2, "ReplacementSpeed", xlabel = r"$\gamma$")

    ax1.legend([r"$\alpha$=0.6",r"$\alpha$=0.8",r"$\alpha$=0.95",r"$\alpha$=1.05"])
    ax2.legend([r"$\alpha$=0.6",r"$\alpha$=0.8",r"$\alpha$=0.95",r"$\alpha$=1.05"])
    q.PlotNiceAndSave(fig1, ax1, r"$\gamma$", ylabel = "Extinction time (gen)", fileName = "extinctionTime")
    q.PlotNiceAndSave(fig2, ax2, r"$\gamma$", ylabel = "Mean infected", fileName = "mean")
    q.RemoveMask()

def replacementTimeSeries():
    LF.Latexify(fig_width = 6.19893, label_size=[1.0, 1.0])
    q = MS.MalariaStatistics("replacement")
    q.plotSettings.saveFigs = False

    #TODO: Change these timeline plots to values you actually want. 
    # Plot of alpha=0.8 and gamma=0.16961
    fig, ax = plt.subplots()
    q.timelineIndex = [np.where( (q.parameters["InfectionSpeed"].values == 0.8) & (q.parameters["ReplacementSpeed"].values == 0.17) )[0][0], 1]
    print("ReplacementSpeed", q.parameters["ReplacementSpeed"][q.timelineIndex[0]])
    q.ImportTimeline()
    q.PlotTimeline(ax = ax)
    q.PlotNiceAndSave(fig, ax, xlabel = "Time (gen)", ylabel = "Infected", fileName = "timeline1")

    # Plot of alpha=1.05 and gamma=0.8 
    fig, ax = plt.subplots()
    q.timelineIndex = [np.where( (q.parameters["InfectionSpeed"].values == 1.05) & (q.parameters["ReplacementSpeed"].values == 0.75) )[0][0], 1]
    print("ReplacementSpeed", q.parameters["ReplacementSpeed"][q.timelineIndex[0]])
    q.ImportTimeline()
    q.PlotTimeline(ax = ax)
    q.PlotNiceAndSave(fig, ax, xlabel = "Time (gen)", ylabel = "Infected", fileName = "timeline2")

    return

def features():
    LF.Latexify(fig_width = 6.19893, label_size=[1.0, 1.0])
    q = MS.MalariaStatistics("features")
    q.plotSettings.saveFigs = False
    q.CalcNewMeans()
    q.CreateDataCopies()

    alphas = [0.6, 0.8, 0.95, 1.05]

    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()

    for alpha in alphas:
        mask = (q.parametersCopy["InfectionSpeed"][:] == alpha).as_matrix()
        q.ApplyMask(mask=mask)

        q.PlotExtinctionTime(ax1, "MaxAntigenValue", xlabel = r"$\gamma$")
        q.PlotMeanInfection(ax2, "MaxAntigenValue", xlabel = r"$\gamma$")


    ax1.legend([r"$\alpha$=0.6",r"$\alpha$=0.8",r"$\alpha$=0.95",r"$\alpha$=1.05"])
    ax2.legend([r"$\alpha$=0.6",r"$\alpha$=0.8",r"$\alpha$=0.95",r"$\alpha$=1.05"])
    q.PlotNiceAndSave(fig1, ax1, r"$\gamma$", ylabel = "Extinction time (gen)", fileName = "extinctionTime")
    q.PlotNiceAndSave(fig2, ax2, r"$\gamma$", ylabel = "Mean infected", fileName = "mean")
    q.RemoveMask()
    q.RemoveMask()

    return


"""
def features2D():
    q = MS.MalariaStatistics("features2D", saveFigs=False)
    mask = (q.parameters["ReplacementSpeed"] == 0.005)
    q.ApplyMask(mask)
    q.Plot2D("MaxAntigenValue", "InfectionSpeed", newFigure=True)
    q.PlotNiceAndSave(xlabel="Strains" , ylabel=r"$\alpha$", fileName = "lowReplacement")
    q.RemoveMask

    q = MS.MalariaStatistics("features2D", saveFigs=False)
    mask = (q.parameters["ReplacementSpeed"] == 0.01)
    q.ApplyMask(mask)
    q.Plot2D("MaxAntigenValue", "InfectionSpeed", newFigure=True)
    q.PlotNiceAndSave(xlabel="Strains", ylabel=r"$\alpha$", fileName = "highReplacement")
    return

def complexDifference():
    q = MS.MalariaStatistics("complexDifference", saveFigs=False)
    
    q.timelineIndex = [1,8]
    q.ImportTimeline()
    q.ImportStrainCounter()
    q.PlotTimeline()
    q.PlotStrainCounter(newFigure=False)
    q.PlotNiceAndSave(xlabel="Iteration", ylabel="Proportion infected", fileName="timeline1")

    q.timelineIndex = [2,5]
    q.ImportTimeline()
    q.ImportStrainCounter()
    q.PlotTimeline()
    q.PlotStrainCounter(newFigure=False)
    q.PlotNiceAndSave(xlabel="Iteration", ylabel="Proportion infected", fileName="timeline2")
    
    return

def complexDifference2D():
    q = MS.MalariaStatistics("complexDifference2D", saveFigs=False)
    mask = (q.parameters["SpecificStrains"] == "nonCross")
    q.ApplyMask(mask)
    q.Plot2D("ReplacementSpeed", "InfectionSpeed", newFigure=True)
    q.PlotNiceAndSave(xlabel=r"$\gamma$" , ylabel=r"$\alpha$", fileName = "nonCross")
    q.RemoveMask()

    q = MS.MalariaStatistics("complexDifference2D", saveFigs=False)
    mask = (q.parameters["SpecificStrains"] == "cross")
    q.ApplyMask(mask)
    q.Plot2D("ReplacementSpeed","InfectionSpeed", newFigure=True)
    q.PlotNiceAndSave(xlabel=r"$\gamma$", ylabel=r"$\alpha$", fileName = "cross")
    
    return

def complexDifferenceMutation2D():
    q = MS.MalariaStatistics("complexDifferenceMutation2D", saveFigs=False)
    mask = (q.parameters["SpecificStrains"] == "nonCross")
    q.ApplyMask(mask)
    q.Plot2D("ReplacementSpeed", "InfectionSpeed", newFigure=True)
    q.PlotNiceAndSave(xlabel=r"$\gamma$" , ylabel=r"$\alpha$", fileName = "nonCross")
    q.RemoveMask()

    q = MS.MalariaStatistics("complexDifferenceMutation2D", saveFigs=False)
    mask = (q.parameters["SpecificStrains"] == "cross")
    q.ApplyMask(mask)
    q.Plot2D("ReplacementSpeed","InfectionSpeed", newFigure=True)
    q.PlotNiceAndSave(xlabel=r"$\gamma$", ylabel=r"$\alpha$", fileName = "cross")
"""
