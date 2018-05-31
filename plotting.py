import numpy as np
import matplotlib.pyplot as plt
import pandas as pandas

class MalariaStatistics():

    def __init__(self, fileName):
        self.fileName = fileName 
        self.data = pandas.read_csv("data/" + fileName + "_data.csv")
        self.parameters = pandas.read_csv("parameters/" + fileName + "_param.csv")
        self.settings = pandas.read_csv("parameters/" + fileName + "_set.csv")

        self.plotSettings = {}

    # Makes a plot of the development of the number of infected over time. 
    def PlotTimeLinePlot(self):
        return

    # Creates a plot with extinction time with whatever parameter given. 
    def PlotExtinctionTime(self, vary):
        plt.figure()
        plt.plot(self.parameters[vary], self.data["run"])
        plt.xlabel(vary)
        plt.ylabel("run")
        figName = "plots/" + fileName + ".png"
        plt.savefig(figName)
        return

    # Creates a plot of the mean and variance. 
    def PlotMeanAndVariance(self):
        return

fileName = "simplest_infectionRate"
q = MalariaStatistics(fileName)
q.PlotExtinctionTime("InfectionSpeed")

fileName = "MaxAntigenLen3"
q = MalariaStatistics(fileName)
q.PlotExtinctionTime("MaxAntigenValue")


plt.show()




