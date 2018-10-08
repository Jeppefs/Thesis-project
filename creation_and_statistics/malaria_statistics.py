import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pandas
from Latexifier import LatexifierFunctions as LF 


class PlotSettings():
    """ 
    A container for plotsettings 
    """

    def __init__(self):
        self.xTimeLabel = "Time (gen)"
        self.yTimeLabel = "Extinction time (gen)"
        self.saveFigs = True
        self.savePath = None

        return

class MalariaStatistics():

    def __init__(self, simulationName, timelineIndex = [0,0], timeConversion = None, plotSettings = None):
        
        self.simulationName = simulationName
        self.pathName = "data/" + self.simulationName + "/"
        self.timelineIndex = timelineIndex

        self.dataEnd = pandas.read_csv(self.pathName + "dataEnd.csv")
        self.parameters = pandas.read_csv(self.pathName + "parameters.csv")
        self.settings = pandas.read_csv(self.pathName + "settings.csv")

        self.NUniqueSimulations = len(self.parameters['NHosts']) 
        self.NSimulations = len(self.dataEnd['run'])

        if timeConversion == None:
            self.timeConversion = 1/self.parameters['NHosts'][0]
        else:
            self.timeConversion = timeConversion 
        self.ApplyTimeConversion()

        if plotSettings == None:
            self.plotSettings = PlotSettings()
            self.plotSettings.savePath = self.pathName + "plots" + "/" + self.simulationName + "_"
        else:
            self.plotSettings = plotSettings

        if timelineIndex[0] > 0:
            self.ImportTimeline()
            self.ImportStrainCounter()

        if self.settings["Repeat"][0] > 1:
            self.isRepeated = True
            self.dataEndRepeat = self.GetRepeatedMeanAndVariance()
        else: 
            self.isRepeated = False

    def ApplyTimeConversion(self):
        self.dataEnd['run'] = self.dataEnd['run']*self.timeConversion
        return

    def ApplyMask(self, mask):
        self.dataEndCopy = self.dataEnd.copy()
        self.parametersCopy = self.parameters.copy()

        self.dataEnd = self.dataEnd[mask]
        self.parameters = self.parameters[mask]
        
        self.NUniqueSimulations = len(self.parameters["NHosts"])
        self.NSimulations = len(self.dataEnd["run"])

        return

    def RemoveMask(self):
        self.dataEnd = self.dataEndCopy.copy()
        self.parameters = self.parametersCopy.copy()

        self.NUniqueSimulations = len(self.parameters['NHosts'])
        self.NSimulations = len(self.dataEnd["run"])

        return

    def ImportTimeline(self): 
        temp = np.genfromtxt(self.pathName + "timeline/" + str(self.timelineIndex[0]) + "_" + str(self.timelineIndex[1]) + ".csv", delimiter=",", skip_header=1)
        self.timelineRuns = temp[:,0]*self.timeConversion
        self.timelineNInfected = temp[:,1]
        return

    def ImportStrainCounter(self):
        self.strainCounter = np.genfromtxt(self.pathName + "timeline/" + str(self.timelineIndex[0]) + "_" + str(self.timelineIndex[1]) + "strainCounter" + ".csv", delimiter=",")
        if len(self.strainCounter.shape) <= 1:
            self.strainCounter = np.expand_dims(self.strainCounter, axis=1)
        self.NStrains = self.strainCounter.shape[1]

        return

    # Calculates mean and variance of repeated runs. 
    def GetRepeatedMeanAndVariance(self):
        dataEndRepeat = pandas.DataFrame(data=None, index=np.arange(self.NUniqueSimulations), columns=self.dataEnd.keys()) 

        r = self.settings["Repeat"][0]
        for i in range(self.NUniqueSimulations):
            for key in self.dataEnd.keys():
                dataEndRepeat.loc[i,key] = np.mean(self.dataEnd[key][i*r:i*r+r])
            dataEndRepeat.loc[i,"run_error"] = np.sqrt(np.var(self.dataEnd["run"][i*r:i*r+r]))
            dataEndRepeat.loc[i, "halfMean_error"] = np.sqrt(np.var(self.dataEnd["halfMean"][i*r:i*r+r]))
        
        return dataEndRepeat

    # Creates a plot with extinction time with whatever parameter given. 
    def PlotExtinctionTime(self, vary, ax = None, xlabel = "vary", plotAllMeasurements = False):
        if ax == None:
            _, ax = plt.subplots()
        
        if self.isRepeated:
            ax.errorbar(self.parameters[vary], self.dataEndRepeat["run"], self.dataEndRepeat["run_error"], fmt='o', markersize=2, elinewidth = 0.5)
        else:
            ax.plot(self.parameters[vary], self.dataEnd["run"], 'o', markersize=2, elinewidth = 0.5)
            
        if plotAllMeasurements == True:
            for i in range(self.settings["Repeat"][0]):
                ax.plot(self.parameters[vary], self.dataEnd["run"][0+i::self.settings["Repeat"][0]],  color = "red", linestyle = "None",  marker='.', alpha=0.1)

        if self.plotSettings.saveFigs: self.PlotNiceAndSave(ax, xlabel, self.plotSettings.yTimeLabel, "extinctionTime")

        return

    # Creates a plot of the mean and variance. 
    def PlotMeanInfection(self, vary, ax = None, xlabel = "vary"):
        if ax == None:
            _, ax = plt.subplots()
        
        if self.isRepeated:
            ax.errorbar(self.parameters[vary], self.dataEndRepeat["halfMean"]/self.parameters["NHosts"], self.dataEndRepeat["halfMean_error"]/self.parameters["NHosts"],
            fmt='o', markersize=2, elinewidth=0.5, zorder=1)
        else: 
            ax.errorbar(self.parameters[vary], self.dataEnd["halfMean"]/self.parameters["NHosts"], np.sqrt(self.dataEnd["halfVariance"])/self.parameters["NHosts"],
            fmt='o', markersize=2, elinewidth=0.5, zorder=1)
            

        if self.plotSettings.saveFigs: self.PlotNiceAndSave(ax, xlabel, "Mean infected", "mean")

        return

    # Makes a plot of the development of the number of infected over time. 
    def PlotTimeline(self, ax = None, axis = []):
        if ax == None: 
            _, ax = plt.subplots()
        if len(axis) == 0:
            ax.plot(self.timelineRuns, self.timelineNInfected/self.parameters["NHosts"][self.timelineIndex[0]-1])

        if self.plotSettings.saveFigs: self.PlotNiceAndSave(ax, self.plotSettings.xTimeLabel, "Infected", "timeLine" + str(self.timelineIndex))

        return

    # Plots strain counter 
    def PlotStrainCounter(self, ax = None, axis = []):
        if ax == None:
            _, ax = plt.subplots()
        for strain in range(self.NStrains):
            if len(axis) == 0:
                ax.plot(self.timelineRuns, self.strainCounter[:, strain]/self.parameters["NHosts"][self.timelineIndex[0]-1], alpha=0.6)

        if self.plotSettings.saveFigs: self.PlotNiceAndSave(ax, self.plotSettings.xTimeLabel, "Infected", "strainCounter")

        return 

    # vary1 is x-axis and vary2 is y 
    def Plot2D(self, vary1, vary2, ax = None):
        if ax == None: 
            _, ax = plt.subplots()

        x = np.unique(self.parameters[vary1])
        y = np.unique(self.parameters[vary2])
        
        xStep = x[1] - x[0]
        yStep = y[1] - y[0]

        Z = np.zeros((len(x),len(y)))

        i = 0
        for x1 in x:
            j = 0
            for y1 in y:
                Z[i,j] = self.dataEnd["run"][(x1 == self.parameters[vary1]) & (y1 == self.parameters[vary2])]
                j += 1
            i += 1

        ax.imshow(np.transpose(Z), origin='lower', aspect='auto', extent=(np.min(x)-xStep/2, np.max(x)+xStep/2, np.min(y)-yStep/2, np.max(y)+yStep/2), vmin=0, vmax=2*10**7 )    
        plt.colorbar(format='%.1e')
        return Z
    
    def Plot2DResidual(self, vary1, vary2, newFigure = True):
        return

    def PlotNiceAndSave(self, ax, xlabel, ylabel, fileName):
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        LF.format_axes(ax)
        plt.tight_layout(pad=0.1)

        figName = self.plotSettings.savePath + fileName + ".pdf"
        plt.savefig(figName, format="pdf")

    def IsEndemic(self):
        repeat = 0
        repeatMax = self.settings["Repeat"][0]
        for i in range(self.NSimulations):
            repeat += 1
            if repeat >= repeatMax:
                repeat = 0  
            
                
        return 

def FindThreshold(x, y, yExpectedValue):
    """
    This function finds in time series data, when it starts to .
    Specifically, it simply checks when timeseries hits the expected value for the second time. If it never does, return 0 
    """
    length = len(x)
    count = 0
    side = None
    skip = 0 # Start at 10 to avoid initial conditions 
    if y[skip] < yExpectedValue:
        side = "below"
    else: 
        side = "above"

    for i in range(10, length): 

        if side == "below":
            if y[i] > yExpectedValue:
                count += 1
                side = "above"
        elif side == "above":
            if y[i] < yExpectedValue:
                count += 1
                side = "below"
            
        if count == 2:
            return x[i], y[i], i

    return None, None, None

def IsItConstant(x, y): 
    
    return 

def LinearFit(x, y):

    mean_x = np.mean(x)
    mean_y = np.mean(y)

    mean_xy = np.mean(x*y)
    mean_x_squared = np.mean(x**2)

    linearFitResults = {}

    linearFitResults["slope"] = (mean_xy - mean_x*mean_y) / (mean_x_squared - mean_x**2) 
    linearFitResults["intersect"] = mean_y - linearFitResults["slope"] * mean_x
    #self.LinearFitResults["slope_err"] = 0
    #self.LinearFitResults["intersect_err"] = 0
    
    return linearFitResults

def Loglike2D(param, X, Y, Y_err, fitFunc):
    #loglike = -1* ( np.sum( np.log(1/(np.sqrt(2*np.pi)*Y_err)) ) + np.sum( (Y - fitFunc(X, param))**2 / (Y_err**2) ) )
    loglike = 1* np.sum( (Y - fitFunc(X, Y, param))**2 / (Y_err**2) )
    return loglike

def Func_Power(X, Y, param):
    return param[1]*X**param[0] + param[2]

def Func_Parabolar(X, Y, param):
    return param[0]*X**2 + param[1]*X + param[2]

def Func_PowerPlusLinear(X, Y, param):
    return param[1]*X**param[0] + param[2] * X + param[3]

def Func_XOverPlusOne(X, Y, param):
    return (param[1]*X**param[2])/(param[0]+param[1]*X**param[2])/(1+Y[0]) + Y[0]

def CalcChi2():
    return







# Recalculates dataEnd, such that it finds the mean and variance from the repeat cases. 
    #def GetRepeatedMeanAndVariance(self):
        #dataEndRepeat = pandas.DataFrame(data=None, index=np.arange(self.NUniqueSimulations), columns=self.dataEnd.keys()) 

        #for i in range(self.NUniqueSimulations):
            #for key in 

        # r = self.settings["Repeat"][0]
        # if r != 1:
        #     for i in range(self.NUniqueRuns):
        #         for key in self.dataEnd.keys():
        #             self.dataEndRepeat.loc[i,key] = np.mean(self.dataEnd[key][i*r:i*r+r])
        #         self.dataEndRepeat.loc[i,"run_error"] = np.sqrt(np.var(self.dataEnd["run"][i*r:i*r+r])/(self.settings["Repeat"][0]-1))
        # else:
        #    for i in range(self.NUniqueRuns):
        #         for key in self.dataEnd.keys():
        #             self.dataEndRepeat.loc[i,key] = np.mean(self.dataEnd[key][0:-1])
        
        #return dataEndRepeat

    
    # def CalcNewMean(self):

    #     self.dataEndRepeat["mean_variance"] =  pandas.Series(index=np.arange(self.NUniqueRuns))

    #     stop = int(self.settings["Runs"] / self.settings["SkipSaving"])
    #     start = int(stop / 2)
        
    #     if self.settings["Repeat"][0] > 1:
    #         for i in range(self.NUniqueRuns):
    #             mean = 0
    #             var = 0
    #             count = 0
    #             for j in range(self.settings["Repeat"][0])+1:
    #                 if self.dataEnd["run"][i*self.settings["Repeat"][0]+j] >= stop:

    #                     loaded = np.genfromtxt(self.pathName + "/timeline" + str(i+1) + "_" + str(j) + ".csv", delimiter=",")
    #                     mean += np.mean(loaded[start:stop])
    #                     var += np.var(loaded[start:stop])
    #                     count += 1
    #             if count > 0:
    #                 mean = mean / count
    #                 var = var / count

    #             self.dataEndRepeat.loc[i, "mean"] = mean
    #             self.dataEndRepeat.loc[i, "variance"] = var
    #     else:
    #         #for i in range(self.NUniqueRuns):
    #         for i in range(1):
    #             mean = 0
    #             var = 0

    #             loaded = np.genfromtxt(self.pathName + "timeline/" + str(i+1) + "_" + str(1) + ".csv", delimiter=",", skip_header = 1)
    #             print(loaded[start:stop])
    #             #mean = np.mean(loaded[start:stop, 1])
    #             #var = np.var(loaded[start:stop, 1])

    #             self.dataEndRepeat.loc[i, "mean"] = mean
    #             self.dataEndRepeat.loc[i, "variance"] = var
           
    #     return        