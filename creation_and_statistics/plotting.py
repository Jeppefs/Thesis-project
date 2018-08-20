import malaria_statistics as MS 

import numpy as np
import matplotlib.pyplot as plt
import pandas as pandas
import scipy.optimize as op

def simple():
    q = MS.MalariaStatistics("simple")

    q.PlotExtinctionTime("InfectionSpeed", xlabel = r"$\alpha$")
    plt.figure()
    plt.plot(np.arange(1.0, 1.05, 0.0001), 10000*(np.arange(1.0, 1.05, 0.0001)-1), color="r")
    q.PlotMeanInfection("InfectionSpeed", xlabel = r"$\alpha$", newFigure=False)
    

    q.timelineIndex = [1, 1]
    print("InfectionSpeed", q.parameters["InfectionSpeed"][q.timelineIndex[0]])
    q.ImportTimeline()
    q.PlotTimeline()

    q.timelineIndex = [40, 5]
    print("InfectionSpeed", q.parameters["InfectionSpeed"][q.timelineIndex[0]])
    q.ImportTimeline()
    q.PlotTimeline()
    return

def replacement(): 
    q = MS.MalariaStatistics("replacement")

    q.PlotExtinctionTime("ReplacementSpeed", xlabel = r"$\gamma$")
    q.PlotMeanInfection("ReplacementSpeed", xlabel = r"$\gamma$")

    #q.timelineIndex = [10, 1]
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

def features():
    q = MS.MalariaStatistics("features", saveFigs=False)

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
            res = op.minimize(fun=MS.Loglike2D, x0=np.array([1,1, 1000]),
            args=(q.parameters["MaxAntigenValue"][mask].values-1, q.dataEnd["halfMean"][mask].values, np.sqrt(q.dataEnd["halfVariance"][mask].values), MS.Func_Parabolar),
            method='Nelder-Mead')
            print(res)
            plt.plot(q.parameters["MaxAntigenValue"][mask], (MS.Func_Parabolar(q.parameters["MaxAntigenValue"][mask].values-1, res.x))/q.parameters["NHosts"], color="k", alpha=0.3)
        q.RemoveMask()
    
    q.PlotNiceAndSave(xlabel="Surface features" , ylabel="Proportion infected", fileName = "mean")

    timelineMask = ((q.parameters["InfectionSpeed"] == 0.6) & (q.parameters["ReplacementSpeed"] == 0.005) & (q.parameters["MaxAntigenValue"] == 4.0))
    timelineIndex = q.parameters[timelineMask].index.values[0]
    q.saveFigs = False
    q.timelineIndex = [timelineIndex,1]
    print(q.parameters.iloc[timelineIndex])
    q.ImportTimeline()
    q.ImportStrainCounter()
    q.PlotTimeline()
    q.PlotStrainCounter(newFigure=False)
    q.PlotNiceAndSave(xlabel="Iteration" , ylabel="Infected", fileName = "strainCounter")

    timelineMask = ((q.parameters["InfectionSpeed"] == 0.6) & (q.parameters["ReplacementSpeed"] == 0.005) & (q.parameters["MaxAntigenValue"] == 4.0))
    timelineIndex = q.parameters[timelineMask].index.values[0]
    q.timelineIndex = [timelineIndex,1]
    print(q.parameters.iloc[timelineIndex])
    q.ImportTimeline()
    q.PlotTimeline()
    q.ImportStrainCounter()
    q.PlotStrainCounter(newFigure=False)
    q.PlotNiceAndSave(xlabel="Iteration" , ylabel="Infected", fileName = "strainCounter2")

    return

def complexFeatures():
    q = MS.MalariaStatistics("complexFeatures", saveFigs=False)

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
        print(np.max(np.arange(0,24,1)*LinearFitResults["slope"] + q.dataEnd["run"][mask].iloc[0]) )
        if np.max(np.arange(0,24,1)*LinearFitResults["slope"] + q.dataEnd["run"][mask].iloc[0]) < maxRuns + 100:
            plt.plot(np.arange(0,24,1)+2, np.arange(0,24,1)*LinearFitResults["slope"] + q.dataEnd["run"][mask].iloc[0], color="k", alpha=0.3)
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
            res = op.minimize(fun=MS.Loglike2D, x0=np.array([1,1, 1000]),
            args=(q.parameters["MaxAntigenValue"][mask].values-1, q.dataEnd["halfMean"][mask].values, np.sqrt(q.dataEnd["halfVariance"][mask].values), MS.Func_Parabolar),
            method='Nelder-Mead')
            print(res)
            plt.plot(q.parameters["MaxAntigenValue"][mask], (MS.Func_Parabolar(q.parameters["MaxAntigenValue"][mask].values-1, res.x))/q.parameters["NHosts"], color="k", alpha=0.3)
        q.RemoveMask()
    
    q.PlotNiceAndSave(xlabel="Surface features" , ylabel="Proportion infected", fileName = "mean")


    q.saveFigs = False
    q.timelineIndex = [4,1]
    print(q.parameters.iloc[4])
    q.ImportTimeline()
    q.ImportStrainCounter()
    q.PlotTimeline()
    q.PlotStrainCounter(newFigure=False)
    q.PlotNiceAndSave(xlabel="Iteration" , ylabel="Infected", fileName = "strainCounter")

    q.timelineIndex = [100,1]
    print(q.parameters.iloc[100])
    q.ImportTimeline()
    q.PlotTimeline()
    q.ImportStrainCounter()
    q.PlotStrainCounter(newFigure=False)
    q.PlotNiceAndSave(xlabel="Iteration" , ylabel="Infected", fileName = "strainCounter2")

    return

def complexFun():
    q = MS.MalariaStatistics("complexFun", timelineIndex = [4,1])
    
    plt.figure()
    q.PlotExtinctionTime(vary = "MaxAntigenValue", newFigure=False)
    linearFitResults = MS.LinearFit(q.parameters["MaxAntigenValue"], q.dataEnd["run"])
    plt.plot(np.arange(2,21), linearFitResults["slope"]*np.arange(2,21)+linearFitResults["intersect"])

    q.PlotMeanInfection(vary = "MaxAntigenValue")
    
    q.PlotTimeline()
    q.ImportStrainCounter
    q.PlotStrainCounter(newFigure=False)
    
    #for i in np.arange(19)+1:
    #    q.timelineIndex = [i,1]
    #    q.ImportTimeline()
    #    q.ImportStrainCounter()
    #    q.PlotTimeline(newFigure = True)
    #    q.PlotStrainCounter(newFigure=False)
    
    return

def complexFunReplacement():
    q = MS.MalariaStatistics("complexFunReplacement", timelineIndex = [4,1])
    
    plt.figure()
    q.PlotExtinctionTime(vary = "MaxAntigenValue", newFigure=False)
    #linearFitResults = MS.LinearFit(q.parameters["MaxAntigenValue"], q.dataEnd["run"])
    #plt.plot(np.arange(2,21), linearFitResults["slope"]*np.arange(2,21)+linearFitResults["intersect"])

    q.PlotMeanInfection(vary = "MaxAntigenValue")

    q.PlotTimeline()
    q.ImportStrainCounter()
    q.PlotStrainCounter(newFigure=False)
   
    


