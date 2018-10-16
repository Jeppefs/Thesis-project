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

    alphas = [0.6, 0.8, 0.9, 0.95]

    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()
    
    for alpha in alphas:
        mask = (q.parametersCopy['InfectionSpeed'][:] == alpha).as_matrix()
        q.ApplyMask(mask=mask)

        q.PlotExtinctionTime(ax1, "ReplacementSpeed", xlabel = r"$\gamma$")
        q.PlotMeanInfection(ax2, "ReplacementSpeed", xlabel = r"$\gamma$")

    ax1.legend([r"$\alpha$=0.6",r"$\alpha$=0.8",r"$\alpha$=0.9",r"$\alpha$=0.95"])
    ax2.legend([r"$\alpha$=0.6",r"$\alpha$=0.8",r"$\alpha$=0.9",r"$\alpha$=0.95"])
    q.PlotNiceAndSave(fig1, ax1, r"$\gamma$", ylabel = "Extinction time (gen)", fileName = "extinctionTime")
    q.PlotNiceAndSave(fig2, ax2, r"$\gamma$", ylabel = "Mean infected", fileName = "mean")
    q.RemoveMask()

    #q.timelineIndex = [35, 1]
    #print("ReplacementSpeed", q.parameters["ReplacementSpeed"][q.timelineIndex[0]])
    #q.ImportTimeline()
    #q.PlotTimeline()
#
    #q.timelineIndex = [40, 1]
    #print("ReplacementSpeed", q.parameters["ReplacementSpeed"][q.timelineIndex[0]])
    #q.ImportTimeline()
    #q.PlotTimeline()
   
    #q2 = MS.MalariaStatistics("replacement2")
    #q2.PlotExtinctionTime("ReplacementSpeed", xlabel = r"$\gamma$")
    #q2.PlotMeanInfection("ReplacementSpeed", xlabel = r"$\gamma$")

    return
"""
def features(plotThis="..."):
    # If True, remember to change from -1 to -2
    if plotThis == "complex":
        q = MS.MalariaStatistics("complexFeatures", saveFigs=False)
        add = 2
    elif plotThis == "mutation":
        q = MS.MalariaStatistics("featuresMutationLow", saveFigs=False)
        add = 1
    else:
        q = MS.MalariaStatistics("features", saveFigs=False)
        add = 1

    maxRuns = np.max(q.dataEnd["run"])
    maxFeatures = np.max(q.parameters["MaxAntigenValue"])

    masks = []
    legendString = []
    uniqueAlphas = np.unique(q.parameters["InfectionSpeed"])
    uniqueGammas = np.unique(q.parameters["ReplacementSpeed"])
    for alpha in uniqueAlphas:
        for gamma in uniqueGammas:
            print(alpha, gamma)
            masks.append((q.parameters["InfectionSpeed"] == alpha) & (q.parameters["ReplacementSpeed"] == gamma))
            legendString.append(r"$\alpha=" + str(alpha) + "$ " + r"$\gamma=" + str(gamma) + "$")

    plt.figure()
    for mask in masks:
        q.ApplyMask(mask)
        q.PlotExtinctionTime("MaxAntigenValue", newFigure=False, xlabel="Surface features")
        q.RemoveMask()
    plt.legend(legendString)

    for mask in masks:
        q.ApplyMask(mask)
        LinearFitResults = MS.LinearFit(q.parameters["MaxAntigenValue"], q.dataEnd["run"])
        print("slope:", LinearFitResults["slope"], "intersection:", LinearFitResults["intersect"])
        plt.plot(np.arange(0,maxFeatures,1)+1, np.arange(0,maxFeatures,1)*LinearFitResults["slope"] + q.dataEnd["run"][mask].iloc[0], color="k", alpha=0.3)
        q.RemoveMask()

    q.PlotNiceAndSave(xlabel="Surface features" , ylabel="Extinction time", fileName = "extinctionTime")


    plt.figure()
    legendStringNew = []
    for mask in masks:
        q.ApplyMask(mask)
        if q.dataEnd["run"].iloc[-1] == maxRuns:
            q.PlotMeanInfection("MaxAntigenValue", newFigure=False, xlabel="Surface features")
            legendStringNew.append(r"$\alpha=" + str(q.parameters["InfectionSpeed"][mask].iloc[0]) + "$ " + r"$\gamma=" + str(q.parameters["ReplacementSpeed"][mask].iloc[0]) + "$")
        q.RemoveMask()
    
    plt.legend(legendStringNew)
    ## Fit
    
    for mask in masks:
        q.ApplyMask(mask)
        if q.dataEnd["run"].iloc[-1] == maxRuns:
            res = op.minimize(fun=MS.Loglike2D, x0=np.array([1, 1, 1]),
            args=(q.parameters["MaxAntigenValue"][mask].values-add, q.dataEnd["halfMean"][mask].values/q.parameters["NHosts"].iloc[0], np.sqrt(q.dataEnd["halfVariance"][mask].values)/10000, MS.Func_XOverPlusOne),
            method='Nelder-Mead')
            print(res)
            plt.plot(q.parameters["MaxAntigenValue"][mask], (MS.Func_XOverPlusOne(q.parameters["MaxAntigenValue"][mask].values-add, q.dataEnd["halfMean"][mask].values/10000, res.x)), color="k", alpha=0.3)
        q.RemoveMask()

    q.PlotNiceAndSave(xlabel="Surface features" , ylabel="Proportion infected", fileName = "mean")

    timelineMask = ((q.parameters["InfectionSpeed"] == 0.6) & (q.parameters["ReplacementSpeed"] == 0.02) & (q.parameters["MaxAntigenValue"] == 5.0))
    timelineIndex = q.parameters[timelineMask].index.values[0]
    q.saveFigs = False
    q.timelineIndex = [timelineIndex,1]
    print(q.parameters.iloc[timelineIndex])
    q.ImportTimeline()
    q.ImportStrainCounter()
    q.PlotTimeline()
    q.PlotStrainCounter(newFigure=False)
    q.PlotNiceAndSave(xlabel="Iteration" , ylabel="Infected", fileName = "strainCounter")

    timelineMask = ((q.parameters["InfectionSpeed"] == 0.8) & (q.parameters["ReplacementSpeed"] == 0.005) & (q.parameters["MaxAntigenValue"] == 5.0))
    timelineIndex = q.parameters[timelineMask].index.values[0]
    q.timelineIndex = [timelineIndex,1]
    print(q.parameters.iloc[timelineIndex])
    q.ImportTimeline()
    q.PlotTimeline()
    q.ImportStrainCounter()
    q.PlotStrainCounter(newFigure=False)
    q.PlotNiceAndSave(xlabel="Iteration" , ylabel="Infected", fileName = "strainCounter2")

    return

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
