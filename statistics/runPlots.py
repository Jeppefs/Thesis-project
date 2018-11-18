import numpy as np 
import matplotlib
import matplotlib.pyplot as plt
import newPlotting as PT
import pandas as pandas
import malaria_statistics as MS
from Latexifier import LatexifierFunctions as LF


"""
Full page width is 12.65076 cm 
Half page width is 6.19893 cm
Use 1.0cm for both margins (though should be corrected, but I do not have the inclination, nor the time to do so - actually something with aspect might be exactly what I am looking for.)
"""

plt.style.use("seaborn")
LF.Latexify(fig_width = 6.19893, label_size=[1.0, 1.0])
matplotlib.rc('font',**{'family':'serif', 'serif':['Computer Modern Roman']})
matplotlib.rc('text', usetex=True)


print("Plotting started")
PT.mutation2D()
print("Congrats! All done!")
plt.show()

"""
Tests:
"""
#x = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
#y = [1,2,3,4,5,6,7,8,9,10,9,8,7,6,5,4,3,2,1]
#yExpectedValue = 5
#print(MS.FindThreshold(x,y,yExpectedValue))