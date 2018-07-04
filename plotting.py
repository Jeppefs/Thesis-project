import numpy as np
import matplotlib.pyplot as plt
import pandas as pandas

class MalariaStatistics():

    def __init__(self, folderName):
        self.fileName = folderName 
        self.dataEnd = pandas.read_csv("data/" + folderName + "/" + "dataEnd.csv")
        self.parameters = pandas.read_csv("data/" + folderName + "/" + "parameters.csv")
        self.settings = pandas.read_csv("data/" + folderName + "/" + "settings.csv")

        self.NUniqueRuns = len(self.parameters['NHosts'])

        self.plotSettings = {}

    # Makes a plot of the development of the number of infected over time. 
    def PlotTimeLinePlot(self, number, repeatNumber = 0):
        plt.figure()
        dat = pandas.read_csv("data/" + self.fileName + "/" + "xDataSim_" + str(number) + "_" + str(repeatNumber) + ".csv")
        plt.plot(dat)
        plt.xlabel("")
        plt.ylabel("Infected")
        return

    # Creates a plot with extinction time with whatever parameter given. 
    def PlotExtinctionTime(self, vary):
        plt.figure()
        plt.errorbar(self.parameters[vary], self.dataEndRepeat["run"], self.dataEndRepeat["run_error"], fmt='o')

        for i in range(self.settings["Repeat"][0]):
            #print(self.dataEnd["run"][0+i::self.settings["Repeat"][0]])
            plt.plot(self.parameters[vary], self.dataEnd["run"][0+i::self.settings["Repeat"][0]],  color = "red", linestyle = "None",  marker='.')

        plt.xlabel(vary)
        plt.ylabel("Extinction Time")
        figName = "plots/" + self.fileName + ".svg"
        plt.savefig(figName, format="svg")

        

        return

    # Creates a plot of the mean and variance. 
    def PlotMeanInfection(self, vary):
        plt.figure()
        plt.errorbar(self.parameters[vary], self.dataEndRepeat["mean"], np.sqrt(self.dataEndRepeat["variance"]/self.settings["Repeat"][0]), fmt='o')
        plt.xlabel(vary)
        plt.ylabel("Mean infected")
        figName = "plots/" + self.fileName + "Mean" + ".svg"
        plt.savefig(figName, format="svg")
        return

    # Recalculates dataEnd, such that it finds the mean and variance from the repeat cases. 
    def GetMeanAndVarianceFromRepeat(self):
        self.dataEndRepeat = pandas.DataFrame(0, index=np.arange(self.NUniqueRuns), columns=self.dataEnd.keys())
        self.dataEndRepeat["run_error"] = pandas.Series(index=np.arange(self.NUniqueRuns))
        r = self.settings["Repeat"][0]
        for i in range(self.NUniqueRuns):
            for key in self.dataEnd.keys():
                self.dataEndRepeat.loc[i,key] = np.mean(self.dataEnd[key][i*r:i*r+r])
            self.dataEndRepeat.loc[i,"run_error"] = np.sqrt(np.var(self.dataEnd["run"][i*r:i*r+r])/(self.settings["Repeat"][0]-1))
        print(self.dataEndRepeat)
        return

    def LinearFit(self):
        return

q = MalariaStatistics("DeathRate")
q.GetMeanAndVarianceFromRepeat()

q.PlotExtinctionTime("DeathSpeed")
q.PlotMeanInfection("DeathSpeed")
q.PlotTimeLinePlot(5,0)

plt.show()




