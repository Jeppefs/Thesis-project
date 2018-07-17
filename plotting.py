import MalariaStatistics as MS 

import numpy as np
import matplotlib.pyplot as plt
import pandas as pandas

def DeathRate():
    q = MS.MalariaStatistics("DeathRate", timeLineIndex = [10,0])
    q.GetMeanAndVarianceFromRepeat()
    q.CalcNewMean(int(10**7 / q.saveSpace), int(2*10**7 / q.saveSpace))

    #q.PlotExtinctionTime("DeathSpeed")
    plt.figure()
    q.PlotMeanInfection("DeathSpeed", newFigure = False)
    #q.PlotTimeLinePlot()
    
    return

DeathRate()
plt.show()
