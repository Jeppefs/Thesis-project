import numpy as np
import matplotlib.pyplot as plt
import glob as glob

def MakeTimeLinePlot(fileName):
    plt.figure()
    plt.plot(testData / pop)
    plt.xlabel("Run")
    plt.ylabel("Infected")
    #plt.yticks(np.arange(0, max(), 0.1))
    plt.grid()
    figName = "plot" + str(len(glob.glob("/plots/*"))) + ".png"
    plt.savefig("plots/"+figName)

def MakeAveragePlot(fileName):
    plt.figure()
    avgData = np.loadtxt("data/" + fileName)
    plt.plot(avgData[:,4], avgData[:,0], '.')
    figName = fileName[0:-3] + ".png"
    plt.savefig("plots/"+figName)

testData = np.loadtxt("data/test.txt")
pop = 10000

MakeAveragePlot("avgFile4.txt")


plt.show()



