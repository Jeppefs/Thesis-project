import numpy as np
import matplotlib.pyplot as plt
import pandas as pandas

class MalariaStatistics():

    def __init__(self, simulationName, timelineIndex = [0,0], saveFigs = True):
        
        self.simulationName = simulationName
        self.pathName = "data/" + self.simulationName + "/"

        self.dataEnd = pandas.read_csv(self.pathName + "dataEnd.csv")
        self.parameters = pandas.read_csv(self.pathName + "parameters.csv")
        self.settings = pandas.read_csv(self.pathName + "settings.csv")

        self.NUniqueRuns = len(self.parameters['NHosts']) 
        self.NDifferentRuns = len(self.parameters['NHosts']) * self.settings["Repeat"]
        self.timelineIndex = timelineIndex
        
        self.saveFigs = True
        self.plotSettings = {}

        if timelineIndex[0] > 0:
            self.ImportTimeline()
            self.ImportStrainCounter()

    # Creates a plot with extinction time with whatever parameter given. 
    def PlotExtinctionTime(self, vary, newFigure = True, plotAllMeasurements = False):

        if newFigure: plt.figure()
        plt.errorbar(self.parameters[vary], self.dataEndRepeat["run"], self.dataEndRepeat["run_error"], fmt='o')

        if plotAllMeasurements == True:
            for i in range(self.settings["Repeat"][0]):
                plt.plot(self.parameters[vary], self.dataEnd["run"][0+i::self.settings["Repeat"][0]],  color = "red", linestyle = "None",  marker='.', alpha=0.1)

        plt.xlabel(vary)
        plt.ylabel("Extinction Time")
        
        if self.saveFigs == True:
            figName = self.pathName + "/plots/" + self.simulationName + "ExtinctionTime.pdf"
            plt.savefig(figName, format="pdf")

        return

    # Creates a plot of the mean and variance. 
    def PlotMeanInfection(self, vary, newFigure = True):
        if newFigure: plt.figure()
        plt.errorbar(self.parameters[vary], self.dataEndRepeat["mean"], np.sqrt(self.dataEndRepeat["variance"]/self.settings["Repeat"][0]), fmt='o')
        plt.xlabel(vary)
        plt.ylabel("Mean infected")

        if self.saveFigs == True:
            figName = self.pathName + "/plots/"  + self.simulationName + "Mean.pdf"
            plt.savefig(figName, format="pdf")
        return

    # Makes a plot of the development of the number of infected over time. 
    def PlotTimeline(self, newFigure = True):

        if newFigure: plt.figure()
        plt.plot(self.timelineRuns, self.timelineNInfected)

        plt.title("Timeline of N infected")
        plt.xlabel("Run")
        plt.ylabel("Infected")
        
        if self.saveFigs == True:
            figName = self.pathName + "/plots/" + self.simulationName  + "Timeline" + ".pdf" 
            plt.savefig(figName, format="pdf")

        return

    # Plots strain counter 
    def PlotStrainCounter(self, newFigure = True):
        if newFigure: plt.figure()
        for strain in range(self.NStrains):
            plt.plot(self.timelineRuns, self.strainCounter[:, strain])

        plt.title("Strain count")
        plt.xlabel("Run")
        plt.ylabel("NInfected")

        if self.saveFigs == True:
            figName = self.pathName + "/plots" + self.simulationName + "StrainCounter" + ".pdf"
            plt.savefig(figName, format="pdf")

        return


    def ImportTimeline(self): 
        temp = np.genfromtxt(self.pathName + "timeline/" + str(self.timelineIndex[0]) + "_" + str(self.timelineIndex[1]) + ".csv", delimiter=",", skip_header=1)
        self.timelineRuns = temp[:,0]
        self.timelineNInfected = temp[:,1]
        return

    def ImportStrainCounter(self):
        self.strainCounter = np.genfromtxt(self.pathName + "timeline/" + str(self.timelineIndex[0]) + "_" + str(self.timelineIndex[1]) + "strainCounter" + ".csv", delimiter=",")
        if len(self.strainCounter.shape) <= 1:
            self.strainCounter = np.expand_dims(self.strainCounter, axis=1)
        self.NStrains = self.strainCounter.shape[1]

        return

    # Recalculates dataEnd, such that it finds the mean and variance from the repeat cases. 
    def GetMeanAndVarianceFromRepeat(self):
        self.dataEndRepeat = pandas.DataFrame(0, index=np.arange(self.NUniqueRuns), columns=self.dataEnd.keys())
        self.dataEndRepeat["run_error"] = pandas.Series(index=np.arange(self.NUniqueRuns))
        r = self.settings["Repeat"][0]
        if r != 1:
            print(self.NUniqueRuns)
            for i in range(self.NUniqueRuns):
                for key in self.dataEnd.keys():
                    self.dataEndRepeat.loc[i,key] = np.mean(self.dataEnd[key][i*r:i*r+r])
                self.dataEndRepeat.loc[i,"run_error"] = np.sqrt(np.var(self.dataEnd["run"][i*r:i*r+r])/(self.settings["Repeat"][0]-1))
        else:
           for i in range(self.NUniqueRuns):
                for key in self.dataEnd.keys():
                    self.dataEndRepeat.loc[i,key] = np.mean(self.dataEnd[key][0:-1])
        
        return

    def CalcNewMean(self):

        self.dataEndRepeat["mean_variance"] =  pandas.Series(index=np.arange(self.NUniqueRuns))

        stop = int(self.settings["Runs"] / self.settings["SkipSaving"])
        start = int(stop / 2)
        
        if self.settings["Repeat"][0] > 1:
            for i in range(self.NUniqueRuns):
                mean = 0
                var = 0
                count = 0
                for j in range(self.settings["Repeat"][0])+1:
                    if self.dataEnd["run"][i*self.settings["Repeat"][0]+j] >= stop:

                        loaded = np.genfromtxt(self.pathName + "/timeline" + str(i+1) + "_" + str(j) + ".csv", delimiter=",")
                        mean += np.mean(loaded[start:stop])
                        var += np.var(loaded[start:stop])
                        count += 1
                if count > 0:
                    mean = mean / count
                    var = var / count

                self.dataEndRepeat.loc[i, "mean"] = mean
                self.dataEndRepeat.loc[i, "variance"] = var
        else:
            #for i in range(self.NUniqueRuns):
            for i in range(1):
                mean = 0
                var = 0

                loaded = np.genfromtxt(self.pathName + "timeline/" + str(i+1) + "_" + str(1) + ".csv", delimiter=",", skip_header = 1)
                print(loaded[start:stop])
                #mean = np.mean(loaded[start:stop, 1])
                #var = np.var(loaded[start:stop, 1])

                self.dataEndRepeat.loc[i, "mean"] = mean
                self.dataEndRepeat.loc[i, "variance"] = var
           
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

    


def Loglike2D(param, X, Y, Y_err, fitFunc):
    #loglike = -1* ( np.sum( np.log(1/(np.sqrt(2*np.pi)*Y_err)) ) + np.sum( (Y - fitFunc(X, param))**2 / (Y_err**2) ) )
    loglike = -1* np.sum( (Y - fitFunc(X, param))**2 / (Y_err**2) )
    return loglike

def FitFunc_Power(X, param):
    return param[1]*X**param[0] + param[2]


def CalcChi2():
    return