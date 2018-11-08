import numpy as np
import matplotlib.pyplot as plt
import pandas as pandas
import scipy.optimize as op
import malaria_statistics as MS 
from Latexifier import LatexifierFunctions as LF

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

    #TODO: Change these timeline plots to values you actually want. 
    # Plot of alpha=0.8 and gamma=0.16961
    fig, ax = plt.subplots()
    q.timelineIndex = [np.where( (q.parameters["InfectionSpeed"].values == 0.8) & (q.parameters["ReplacementSpeed"].values == 0.17) )[0][0], 1]
    q.ImportTimeline()
    q.PlotTimeline(ax = ax)
    q.PlotNiceAndSave(fig, ax, xlabel = "Time (gen)", ylabel = "Infected", fileName = "timeline1")

    # Plot of alpha=1.05 and gamma=0.8 
    fig, ax = plt.subplots()
    q.timelineIndex = [np.where( (q.parameters["InfectionSpeed"].values == 1.05) & (q.parameters["ReplacementSpeed"].values == 0.75) )[0][0], 1]
    q.ImportTimeline()
    q.PlotTimeline(ax = ax)
    q.PlotNiceAndSave(fig, ax, xlabel = "Time (gen)", ylabel = "Infected", fileName = "timeline2")

    return

def features():
    LF.Latexify(fig_width = 6.19893, label_size=[1.0, 1.0])
    q = MS.MalariaStatistics("features")
    q.CalcNewMeans()
    q.CreateDataCopies()

    alphas = q.parameters["InfectionSpeed"].unique()

    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()

    for alpha in alphas:
        mask = (q.parametersCopy["InfectionSpeed"][:] == alpha).as_matrix()
        q.ApplyMask(mask=mask)

        q.PlotExtinctionTime(ax1, "MaxAntigenValue", xlabel = r"$\gamma$")
        q.PlotMeanInfection(ax2, "MaxAntigenValue", xlabel = r"$\gamma$")

    ax1.set_xticks([0, 5, 10, 15, 20, 25])    
    ax2.set_xticks([0, 5, 10, 15, 20, 25])        
    ax1.legend([r"$\alpha$=0.6",r"$\alpha$=0.8",r"$\alpha$=0.95",r"$\alpha$=1.05"])
    ax2.legend([r"$\alpha$=0.6",r"$\alpha$=0.8",r"$\alpha$=0.95",r"$\alpha$=1.05"])
    q.PlotNiceAndSave(fig1, ax1, "Strains", ylabel = "Extinction time (gen)", fileName = "extinctionTime")
    q.PlotNiceAndSave(fig2, ax2, "Strains", ylabel = "Mean infected", fileName = "mean")
    q.RemoveMask()

   

    """Time Series"""
    skip = 100
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()

    q.timelineIndex = [np.where( (q.parameters["InfectionSpeed"].values == 0.6) & (q.parameters["MaxAntigenValue"].values == 3) )[0][0], 1]
    q.ImportTimeline()
    q.ImportStrainCounter()
    q.PlotTimeline(ax = ax1, skip = skip)
    q.PlotStrainCounter(ax = ax1, skip = skip)
    q.PlotNiceAndSave(fig1, ax1, xlabel = "Time (gen)", ylabel = "Infected", fileName = "timeline1")
    
    q.timelineIndex = [np.where( (q.parameters["InfectionSpeed"].values == 0.6) & (q.parameters["MaxAntigenValue"].values == 5) )[0][0], 1]
    q.ImportTimeline()
    q.ImportStrainCounter()
    q.PlotTimeline(ax = ax2, skip = skip)
    q.PlotStrainCounter(ax = ax2, skip = skip)
    q.PlotNiceAndSave(fig2, ax2, xlabel = "Time (gen)", ylabel = "Infected", fileName = "timeline2")

    return

"""Number of strains in the system"""
def featuresStrains():
    LF.Latexify(fig_width = 6.19893, label_size=[1.0, 1.0])
    q = MS.MalariaStatistics("features")
    q.plotSettings.saveFigs = False
    q.CalcNewMeans()
    q.CreateDataCopies()

    alphas = q.parameters["InfectionSpeed"].unique()
    i = 0
    fig, ax = plt.subplots()
    ax.grid(True)
    for alpha in alphas:
        mask = (q.parametersCopy["InfectionSpeed"][:] == alpha).as_matrix()
        q.ApplyMask(mask=mask)

        ax.plot(q.parameters["MaxAntigenValue"], q.dataEnd["strains"], marker=".", markersize=4.0, linewidth=1.0, alpha=0.6)        
        i += 1

    ax.legend([r"$\alpha$=0.6",r"$\alpha$=0.8",r"$\alpha$=0.95",r"$\alpha$=1.05"])
    ax.set_xticks([0, 5, 10, 15, 20, 25])
    ax.set_yticks([0, 5, 10, 15, 20, 25])
    q.PlotNiceAndSave(fig, ax, xlabel = "Start Strains", ylabel = "End Strains", fileName = "endStrains")

    return

def features2D():
    LF.Latexify(fig_width=6.19893)
    q = MS.MalariaStatistics("features2D")
    q.plotSettings.saveFigs = False

    fig, ax = plt.subplots()
    q.Plot2D(fig, ax, "MaxAntigenValue", "InfectionSpeed", "run")
    q.PlotNiceAndSave(fig, ax, "Strains", r"$\alpha$", "extinctionTime")

    fig, ax = plt.subplots()
    q.Plot2D(fig, ax, "MaxAntigenValue", "InfectionSpeed", "halfMean")
    q.PlotNiceAndSave(fig, ax, "Strains", r"$\alpha$", "mean")

    return

def mutation():
    LF.Latexify(fig_width=6.19893, label_size=[1.0, 1.0])
    q = MS.MalariaStatistics("mutationLowReplacement")
    
    #alphas = q.parameters["InfectionSpeed"].unique()
    alpha = 0.6
    mus = q.parameters["MutationSpeed"].unique()

    q.CalcNewMeans()
    q.CreateDataCopies()


    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()

    for mu in mus:
        mask = ( ((q.parametersCopy["InfectionSpeed"][:] == alpha).as_matrix()) & ((q.parametersCopy["MutationSpeed"][:] == mu).as_matrix()) )
        #print((q.parametersCopy["InfectionSpeed"][:] == alpha).as_matrix(), (q.parametersCopy["MutationSpeed"][:] == mus[0]).as_matrix(), mask)
        q.ApplyMask(mask=mask)

        q.PlotExtinctionTime(ax1, "MaxAntigenValue", xlabel = r"$\gamma$")
        q.PlotMeanInfection(ax2, "MaxAntigenValue", xlabel = r"$\gamma$")

    ax1.legend([r"$\mu$="+str(mus[0]),r"$\mu$="+str(mus[1]),r"$\mu$="+str(mus[2]),r"$\mu$="+str(mus[3])])
    ax2.legend([r"$\mu$="+str(mus[0]),r"$\mu$="+str(mus[1]),r"$\mu$="+str(mus[2]),r"$\mu$="+str(mus[3])])
    q.PlotNiceAndSave(fig1, ax1, r"$\gamma$", ylabel = "Extinction time (gen)", fileName = "extinctionTime")
    q.PlotNiceAndSave(fig2, ax2, r"$\gamma$", ylabel = "Mean infected", fileName = "mean")
    q.RemoveMask()

    fig, ax = plt.subplots()
    ax.grid(True)
    for mu in mus:
        mask = (q.parametersCopy["MutationSpeed"][:] == mu).as_matrix()
        q.ApplyMask(mask=mask)

        ax.plot(q.parameters["MaxAntigenValue"], q.dataEnd["strains"], marker=".", markersize=4.0, linewidth=1.0, alpha=0.6)

    ax.set_xticks([0, 5, 10, 15, 20, 25])
    ax.set_yticks([0, 5, 10, 15, 20, 25])
    ax.legend([r"$\mu$="+str(mus[0]),r"$\mu$="+str(mus[1]),r"$\mu$="+str(mus[2]),r"$\mu$="+str(mus[3])])    
    q.PlotNiceAndSave(fig, ax, xlabel = "Start Strains", ylabel = "End Strains", fileName = "endStrains")
    
    return

def mutationTimeSeries():
    
    LF.Latexify(fig_width = 6.19893, label_size=[1.0, 1.0])
    q = MS.MalariaStatistics("mutationTimeSeries")
    q.plotSettings.saveFigs = False
    q.dataEndRepeat = np.array([0])
    q.CreateDataCopies()

    mus = q.parameters["MutationSpeed"].unique()
    As = q.parameters["MaxAntigenValue"].unique()
    gammas = q.parameters["ReplacementSpeed"].unique()
    skip = 1

    #for A in As:
    #    for gamma in gammas:
    #        for mu in mus:
    #            print(A, mu, gamma)
    #            fig, ax = plt.subplots()
#
    #            q.timelineIndex = [np.where( (q.parameters["MutationSpeed"].values == mu) & 
    #            (q.parameters["MaxAntigenValue"].values == A) & 
    #            (q.parameters["ReplacementSpeed"].values == gamma) )[0][0] + 1, 1]
    #           
    #            q.ImportTimeline()
    #            q.ImportStrainCounter()
    #            q.PlotTimeline(ax = ax, skip = skip)
    #            q.PlotStrainCounter(ax = ax, skip = skip)
    #            q.PlotNiceAndSave(fig, ax, xlabel = "Time (gen)", ylabel = "Infected", fileName = "timeline_" + str(A) + "_" + str(gamma) + "_" + str(mu))
    #            plt.close(fig)

    for mu in mus:    
        fig, ax = plt.subplots()
        for gamma in gammas:
            print(((q.parametersCopy["ReplacementSpeed"][:] == gamma).as_matrix()), ((q.parametersCopy["MutationSpeed"][:] == mu).as_matrix()))
            mask =( ((q.parametersCopy["ReplacementSpeed"][:] == gamma).as_matrix()) & ((q.parametersCopy["MutationSpeed"][:] == mu).as_matrix()) )
            q.ApplyMask(mask)
            q.PlotExtinctionTime(ax=ax, vary="MaxAntigenValue", xlabel = "Strains")


    return

def mutation2D():

    LF.Latexify(fig_width=6.19893, label_size=[1.0, 1.0])
    q = MS.MalariaStatistics("mutation2D")
    q.dataEndRepeat = q.dataEnd.copy()
    q.CreateDataCopies()

    mus = q.parameters["MutationSpeed"].unique()

    for mu in mus:
        mask = (q.parametersCopy["MutationSpeed"][:] == mu).as_matrix()
        q.ApplyMask(mask)

        fig, ax = plt.subplots()
        q.Plot2D(fig, ax, "MaxAntigenValue", "InfectionSpeed", "run")
        q.PlotNiceAndSave(fig, ax, "Strains", r"$\alpha$", "extinctionTime")

        fig, ax = plt.subplots()
        q.Plot2D(fig, ax, "MaxAntigenValue", "InfectionSpeed", "halfMean")
        q.PlotNiceAndSave(fig, ax, "Strains", r"$\alpha$", "mean")

        q.RemoveMask()
    
    return 