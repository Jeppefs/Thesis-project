import MalariaStatistics as MS 

import numpy as np
import matplotlib.pyplot as plt
import pandas as pandas
import scipy.optimize as op
import nestle 

def DeathRate():
    q = MS.MalariaStatistics("DeathRate", timeLineIndex = [10,0])
    q.GetMeanAndVarianceFromRepeat()
    q.CalcNewMean(int(10**7 / q.saveSpace), int(2*10**7 / q.saveSpace))

    #q.PlotExtinctionTime("DeathSpeed")
    plt.figure()
    q.PlotMeanInfection("DeathSpeed", newFigure = False)
    #op.minimize( MS.Loglike2D, method="Powell", x0 = tuple([0.5, 1, 400]), 
    #args=tuple([q.parameters["deathRate"][2:-1], q.dataEndRepeat["mean"][2:-1], np.sqrt( dataEndRepeat["variance"][2:-1]/len(dataEndRepeat["variance"][2:-1]) ), FitFunc_Power]) )
    #q.PlotTimeLinePlot()
    
    return

DeathRate()
plt.show()
