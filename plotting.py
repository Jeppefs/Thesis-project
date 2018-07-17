import MalariaStatistics as MS 

import numpy as np
import matplotlib.pyplot as plt
import pandas as pandas

def DeathRate():
    q = MS.MalariaStatistics("DeathRate", timeLineIndex = [10,0])
    q.GetMeanAndVarianceFromRepeat()

    q.PlotExtinctionTime("DeathSpeed")
    q.PlotMeanInfection("DeathSpeed")
    q.PlotTimeLinePlot()
    return

DeathRate()
plt.show()
