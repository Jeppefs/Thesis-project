import numpy as np
import matplotlib.pyplot as plt
import pandas as pandas

class MalariaStatistics():

    def __init__(self, folderName):
        self.fileName = folderName 
        self.dataEnd = pandas.read_csv("data/" + folderName + "/" + "dataEnd.csv")
        self.parameters = pandas.read_csv("data/" + folderName + "/" + "parameters.csv")
        self.settings = pandas.read_csv("data/" + folderName + "/" + "settings.csv")

        self.plotSettings = {}

    # Makes a plot of the development of the number of infected over time. 
    def PlotTimeLinePlot(self, number):
        plt.figure()
        plt.plot()
        return

    # Creates a plot with extinction time with whatever parameter given. 
    def PlotExtinctionTime(self, vary):
        plt.figure()
        plt.plot(self.parameters[vary], self.dataEnd["run"], '.-')
        plt.xlabel(vary)
        plt.ylabel("run")
        figName = "plots/" + self.fileName + ".png"
        plt.savefig(figName)
        return

    def PlotMeanInfection(self, vary):
        plt.figure()
        plt.errorbar(self.parameters[vary], self.dataEnd[" mean"], np.sqrt(self.dataEnd[" variance "]))
        plt.xlabel(vary)
        plt.ylabel("Mean infected")
        figName = "plots/" + self.fileName + "" + ".png"
        plt.savefig(figName)
        return

    # Creates a plot of the mean and variance. 
    def PlotMeanAndVariance(self):
        return

q = MalariaStatistics("simpleDeath")
q.PlotExtinctionTime("DeathSpeed")
print(q.dataEnd.keys())
q.PlotMeanInfection("DeathSpeed")

plt.show()




