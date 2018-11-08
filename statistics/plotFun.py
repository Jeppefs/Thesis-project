"""
This file is just for testing plots. THIS IS SHITTY CODE AND I KNOW IT! IT IS
NOT SUPPOSED TO BE GOOD!
"""

"""Set current path as sys path for import of files"""
import sys
import os 
sys.path.append(os.getcwd() + "/statistics")

"""Global packages"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

"""Local Packages"""
import malaria_statistics as MS
from Latexifier import LatexifierFunctions as LF


LF.Latexify(fig_width = 6.19893*3, label_size=[1.0, 1.0])
q = MS.MalariaStatistics("mutationTimeSeries")
q.plotSettings.saveFigs = False
q.dataEndRepeat = np.array([0])
q.CreateDataCopies()
skip = 1

mus = q.parameters["MutationSpeed"].unique()
As = q.parameters["MaxAntigenValue"].unique()
gammas = q.parameters["ReplacementSpeed"].unique()

fig, ax = plt.subplots()

q.timelineIndex = [np.where( (q.parameters["MutationSpeed"].values == mus[-1]) & 
(q.parameters["MaxAntigenValue"].values == As[-1]) & 
(q.parameters["ReplacementSpeed"].values == gammas[-1]) )[0][0] + 1, 1]

q.ImportTimeline()
q.ImportStrainCounter()

q.PlotTimeline(ax = ax, skip = skip)
q.PlotStrainCounter(ax = ax, skip = skip)
#q.PlotNiceAndSave(fig, ax, xlabel = "Time (gen)", ylabel = "Infected", fileName = "timeline_" + str(A) + "_" + str(gamma) + "_" + str(mu))



print("All done, congrats!")