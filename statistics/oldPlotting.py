""" 
This file takes care of all the plotting. You can run specfic section through
ipython and get a view of specific plots
"""

"""Set current path as sys path for import of files"""
import sys
import os 
sys.path.append(os.getcwd() + "/statistics")

"""Global packages"""
import numpy as np
import pandas as pd 
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

"""Local Packages"""
import malaria_statistics as MS
from Latexifier import LatexifierFunctions as LF
#print("Importing done")

"""
|
|
Simple plotting:
|
|
"""

"""
|
|
Replacement plotting:
|
|
"""

"""
|
|
Strain plotting:
|
|
"""

def features():
    q = MS.MalariaStatistics("features")

    figs, axes = MS.CreateFigures(4)

    q.makeAllPlots(figs, axes, "InfectionSpeed")

    q.PlotNiceAndSave()

    return