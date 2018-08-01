import malaria_statistics as MS 

import numpy as np
import matplotlib.pyplot as plt
import pandas as pandas
import scipy.optimize as op

def deathRate():
    q = MS.MalariaStatistics("DeathRate", timelineIndex = [10,1])
    q.GetMeanAndVarianceFromRepeat()
    q.CalcNewMean()

    #q.PlotExtinctionTime("DeathSpeed")
    plt.figure()
    q.PlotMeanInfection("DeathSpeed", newFigure = False)
    #op.minimize( MS.Loglike2D, method="Powell", x0 = tuple([0.5, 1, 400]), 
    #args=tuple([q.parameters["deathRate"][2:-1], q.dataEndRepeat["mean"][2:-1], np.sqrt( dataEndRepeat["variance"][2:-1]/len(dataEndRepeat["variance"][2:-1]) ), FitFunc_Power]) )
    #q.PlotTimeLinePlot()
    
    return

def complexFun():
    q = MS.MalariaStatistics("complexFun", timelineIndex = [5,1])
    
    q.PlotExtinctionTime(vary = "MaxAntigenValue")
    q.PlotMeanInfection(vary = "MaxAntigenValue")
    
    for i in np.arange(19)+1:
        q.timelineIndex = [i,1]
        q.ImportTimeline()
        q.ImportStrainCounter()
        q.PlotTimeline(newFigure = True)
        q.PlotStrainCounter(newFigure=False)
    
    return

complexFun()
plt.show()
