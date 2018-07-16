import numpy as np
import matplotlib.pyplot as plt
import pandas as pandas

class MalariaStatistics():

    def __init__(self, folderName, timeLineIndex = [0,0]):
        
        self.simulationName = folderName
        self.pathName = "data/" + folderName + "/"

        self.dataEnd = pandas.read_csv(self.pathName + "dataEnd.csv")
        self.parameters = pandas.read_csv(self.pathName + "parameters.csv")
        self.settings = pandas.read_csv(self.pathName + "settings.csv")

        self.NUniqueRuns = len(self.parameters['NHosts'])

        self.plotSettings = {}

        if timeLineIndex[0] != 0:
            self.timeLine = np.genfromtxt(self.pathName + "xDataSim_" + str(timeLineIndex[0]) + "_" + str(timeLineIndex[1]) + ".csv", delimiter=",")

    # Makes a plot of the development of the number of infected over time. 
    def PlotTimeLinePlot(self):

        x = np.arange(100000, len(self.timeLine))*100
        y = self.timeLine[100000: len(self.timeLine)]

        plt.figure()
        plt.plot(np.arange(0, len(self.timeLine))*100, self.timeLine)
        plt.xlabel("Run")
        plt.ylabel("Infected")

        fitResults = q.LinearFit(x, y)
        print(fitResults)
        plt.plot(x, x*fitResults["slope"] + fitResults["intersect"])
        
        figName = "plots/" + self.simulationName + "TimeLine" + ".pdf" 
        plt.savefig(figName, format="pdf")

        return

    # Creates a plot with extinction time with whatever parameter given. 
    def PlotExtinctionTime(self, vary):
        plt.figure()
        plt.errorbar(self.parameters[vary], self.dataEndRepeat["run"], self.dataEndRepeat["run_error"], fmt='o')

        #for i in range(self.settings["Repeat"][0]):
            #print(self.dataEnd["run"][0+i::self.settings["Repeat"][0]])
            #plt.plot(self.parameters[vary], self.dataEnd["run"][0+i::self.settings["Repeat"][0]],  color = "red", linestyle = "None",  marker='.', alpha=0.1)

        plt.xlabel(vary)
        plt.ylabel("Extinction Time")
        figName = "plots/" + self.simulationName + ".pdf"
        plt.savefig(figName, format="pdf")

        return

    # Creates a plot of the mean and variance. 
    def PlotMeanInfection(self, vary):
        plt.figure()
        plt.errorbar(self.parameters[vary], self.dataEndRepeat["mean"], np.sqrt(self.dataEndRepeat["variance"]/self.settings["Repeat"][0]), fmt='o')
        plt.xlabel(vary)
        plt.ylabel("Mean infected")
        figName = "plots/" + self.simulationName + "Mean" + ".pdf"
        plt.savefig(figName, format="pdf")
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
        #print(self.dataEndRepeat)
        return

    def LinearFit(self, x, y):

        mean_x = np.mean(x)
        mean_y = np.mean(y)

        mean_xy = np.mean(x*y)
        mean_x_squared = np.mean(x**2)

        self.LinearFitResults = {}

        self.LinearFitResults["slope"] = (mean_xy - mean_x*mean_y) / (mean_x_squared - mean_x**2) 
        self.LinearFitResults["intersect"] = mean_y - self.LinearFitResults["slope"] * mean_x
        #self.LinearFitResults["slope_err"] = 0
        #self.LinearFitResults["intersect_err"] = 0
        
        return self.LinearFitResults

q = MalariaStatistics("DeathRate", timeLineIndex = [25,0])
#print(q.parameters)
q.GetMeanAndVarianceFromRepeat()

q.PlotExtinctionTime("DeathSpeed")
q.PlotMeanInfection("DeathSpeed")
#q.PlotTimeLinePlot()



#for i in range(25):
#    q.PlotTimeLinePlot(i+1,0)

plt.show()




