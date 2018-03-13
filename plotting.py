import numpy as np
import matplotlib.pyplot as plt
import glob as glob

def MakeTimeLinePlot(fileName):
    global pop
    testData = np.loadtxt("data/" + fileName)
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
    plt.xlabel(str())
    plt.ylabel("Extinction time:")
    figName = fileName[0:-3] + ".png"
    plt.savefig("plots/"+figName)


pop = 10000

#MakeTimeLinePlot("test.txt")

#MakeAveragePlot("avgFile4.txt")



plt.show()



