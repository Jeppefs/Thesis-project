import numpy as np
import matplotlib.pyplot as plt
import pandas as pandas

class MalariaStatistics():

    def __init__(self, folderName):
        self.simulationName = folderName
        self.pathName = "data/" + folderName + "/"
        self.dataEnd = pandas.read_csv(self.pathName + "dataEnd.csv")
        self.parameters = pandas.read_csv(self.pathName + "parameters.csv")
        self.settings = pandas.read_csv(self.pathName + "settings.csv")

        self.NUniqueRuns = len(self.parameters['NHosts'])

        self.plotSettings = {}

    # Makes a plot of the development of the number of infected over time. 
    def PlotTimeLinePlot(self, number, repeatNumber = 0):
        plt.figure()
        dat = pandas.read_csv(self.pathName + "xDataSim_" + str(number) + "_" + str(repeatNumber) + ".csv")
        plt.plot(dat)
        plt.xlabel("Run")
        plt.ylabel("Infected")

        print("hej")

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
        figName = "plots/" + self.simulationName + ".svg"
        plt.savefig(figName, format="svg")

        return

    # Creates a plot of the mean and variance. 
    def PlotMeanInfection(self, vary):
        plt.figure()
        plt.errorbar(self.parameters[vary], self.dataEndRepeat["mean"], np.sqrt(self.dataEndRepeat["variance"]/self.settings["Repeat"][0]), fmt='o')
        plt.xlabel(vary)
        plt.ylabel("Mean infected")
        figName = "plots/" + self.simulationName + "Mean" + ".svg"
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

q = MalariaStatistics("InfectionSpeedFull")
q.GetMeanAndVarianceFromRepeat()

q.PlotExtinctionTime("InfectionSpeed")
q.PlotMeanInfection("InfectionSpeed")
q.PlotTimeLinePlot(25,0)

#for i in range(25):
#    q.PlotTimeLinePlot(i+1,0)

plt.show()




