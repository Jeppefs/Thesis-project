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
import seaborn 
seaborn.set()

"""Local Packages"""
import malaria_statistics as MS
from Latexifier import LatexifierFunctions as LF


"""Have fun plotting!"""
plt.style.use("seaborn")
LF.Latexify(label_size = [1.0, 1.0])

#LF.Latexify(fig_width = 6.19893, label_size=[1.0, 1.0])
q = MS.MalariaStatistics("mutationTimeSeries")

mus = q.parameters["MutationSpeed"].unique()
As = q.parameters["MaxAntigenValue"].unique()
gammas = q.parameters["ReplacementSpeed"].unique()

for mu in mus:    
    fig, ax = plt.subplots()
    for gamma in gammas:
        #print(((q.parameters["ReplacementSpeed"][:] == gamma).as_matrix()), ((q.parameters["MutationSpeed"][:] == mu).as_matrix()))
        q = MS.MalariaStatistics("mutationTimeSeries")
        mask =( ((q.parameters["ReplacementSpeed"][:] == gamma).as_matrix()) & ((q.parameters["MutationSpeed"][:] == mu).as_matrix()) )
        q.ApplyMask(mask)
        q.PlotExtinctionTime(ax=ax, vary="MaxAntigenValue", xlabel = "Strains")
    ax.legend(gammas)
    q.PlotNiceAndSave(fig, ax, "Strains", "Extinction time (gen)", str(mu))

plt.show()
print("All done, congrats!")