import numpy as np 
import matplotlib.pyplot as plt
import plotting as PT
import malaria_statistics as MS

"""
Full page width is 12.65076 cm 
Half page width is 6.19893 cm
Is there a way to automate how big the margins are (the part used for labels and such in the plots). 
"""

PT.simple()
print("Congrats! All done!")
plt.show()

"""
Tests:
"""
#x = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
#y = [1,2,3,4,5,6,7,8,9,10,9,8,7,6,5,4,3,2,1]
#yExpectedValue = 5
#print(MS.FindThreshold(x,y,yExpectedValue))