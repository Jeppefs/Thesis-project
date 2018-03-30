import numpy as np
import matplotlib.pyplot as plt
import glob as glob

# Makes a plot of the development of the number of infected over time. 
def MakeTimeLinePlot(fileName):
    global pop
    testData = np.loadtxt("data/" + fileName)
    plt.plot(testData / pop)
    plt.xlabel("Run")
    plt.ylabel("Infected")
    #plt.yticks(np.arange(0, max(), 0.1))
    plt.grid()
    figName = "plot" + str(len(glob.glob("/plots/*"))) + ".png"
    plt.savefig("plots/"+figName)
    return

# Creates a plot with extinction time with whatever parameter given. 
def MakeExtinctionTimePlot(fileName):
    plt.figure()
    avgData = np.loadtxt("data/" + fileName)
    plt.plot(avgData[:,8], avgData[:,0], '-o')
    #plt.plot(avgData[:,4], '.')
    plt.xlabel(str())
    plt.ylabel("Extinction time:")
    figName = fileName[0:-3] + ".png"
    plt.savefig("plots/"+figName)
    return

# Creates a plot of the mean and variance. 
def MakeAveragePlot():
    return

pop = 10000

#MakeTimeLinePlot("test.txt")

plt.figure()
MakeAveragePlot("avgFile3.txt")

plt.show()



