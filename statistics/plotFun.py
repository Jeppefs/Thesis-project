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


"""Have fun plotting!"""
q = MS.MalariaStatistics("simple")
print(q.dataEnd)



print("All done, congrats!")