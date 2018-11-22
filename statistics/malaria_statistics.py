import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pandas
import os
from Latexifier import LatexifierFunctions as LF 

"""
Dette skal vi have i dataen
- run
- infected_mean
- infected_error
- strains
- 
"""

class PlotSettings():
    """ 
    A container for plotsettings 
    """

    def __init__(self):
        self.xTimeLabel = "Time (gen)"
        self.yTimeLabel = "Extinction time (gen)"
        self.saveFigs = False
        self.savePath = None

        return

class MalariaStatistics():

    def __init__(self, simulationName, plotSettings = None):
        
        self.simulationName = simulationName
        self.pathName = "data/" + self.simulationName + "/"
        self.plotSavePath = self.pathName + "plots/"

        self.dataEnd = pandas.read_csv(self.pathName + "dataEnd.csv")
        self.parameters = pandas.read_csv(self.pathName + "parameters.csv")
        self.settings = pandas.read_csv(self.pathName + "settings.csv")

        self.isRepeated = self.settings["Repeat"][0] > 1
        self.NUniqueSimulations = len(self.parameters['NHosts']) 
        self.NSimulations = len(self.dataEnd['run'])

        if os.path.exists(self.pathName + "dataEndOld.csv") == False:
            self.DoAllConversion()
            print("Data files converted")

        self.MakeBaseCopies() # Make base copies so you can apply and remove masks. 

        return

    """
    Data loading and conversion methods:
    """
    def DoAllConversion(self):
        """These methods has to be in order!!!"""
        self.SaveNotNeededData() # Save the data in another file, 
        self.ApplyConversion() # Divides some values with the number of hosts
        self.RecalculateData() # Recalulates the data for repated cases and/or from timeseries
        self.SaveRecalculatedData()

    def SaveNotNeededData(self):
        self.dataEnd.to_csv(self.pathName + "dataEndOld.csv", index=False)
        return

    def RecalculateData(self):
        # Create new dataframe with the same keys. 

        self.dataEnd.loc[:,"run_error"] = 0 # Simply create a 0 index for run_error - even if there is no error it may make things easier
        # If timeseries data is saved, recalculate a new mean which follows the
        # steady state
        if self.settings["ShouldSaveDataWhileRunning"][0]:
            self.CalcNewMeans()
        # If simulations are repeated, condense the data 
        if self.settings["Repeat"][0] > 1:
            # Crate a temporary object that will smaller that the origianl. 
            dataEndTemp = self.GetRepeatedMeanAndVariance()
            self.dataEnd = dataEndTemp.copy()
        return

    def ApplyConversion(self):
        self.dataEnd['run'] = self.dataEnd['run'] / self.parameters['NHosts'][0]
        self.dataEnd['mean'] = self.dataEnd['mean'] / self.parameters['NHosts'][0]
        self.dataEnd['variance'] = self.dataEnd['variance'] / self.parameters['NHosts'][0]
        return

    def SaveRecalculatedData(self):
        self.dataEnd.to_csv(self.pathName + "dataEnd.csv", index=False)
        return

    def MakeBaseCopies(self):
        self.dataEndBase = self.dataEnd.copy()
        self.parametersBase = self.parameters.copy()

    def ApplyMask(self, mask):
        """Puts a mask onto the data, so it can there after be plotted."""
        #self.dataEnd = self.dataEnd.repeat(mask, self.settings['Repeat']).copy()
        self.dataEnd = self.dataEnd[mask].copy()        
        self.parameters = self.parameters[mask].copy()

        self.NUniqueSimulations = len(self.parameters["NHosts"])
        self.NSimulations = len(self.dataEnd["run"])
        return

    def ImportTimeline(self): 
        temp = np.genfromtxt(self.pathName + "timeline/" + str(self.timelineIndex[0]) + "_" + str(self.timelineIndex[1]) + ".csv", delimiter=",", skip_header=1)
        self.timelineRuns = temp[:,0]/self.parameters["NHosts"][0]
        self.timelineNInfected = temp[:,1]/self.parameters["NHosts"][0]
        return

    def ImportStrainCounter(self):
        self.strainCounter = np.genfromtxt(self.pathName + "timeline/" + str(self.timelineIndex[0]) + "_" + str(self.timelineIndex[1]) + "strainCounter" + ".csv", delimiter=",")
        if len(self.strainCounter.shape) <= 1:
            self.strainCounter = np.expand_dims(self.strainCounter, axis=1)
        self.strainCounter = self.strainCounter / self.parameters['NHosts'][0]
        self.NStrains = self.strainCounter.shape[1]

        return

    def GetRepeatedMeanAndVariance(self):
        """ Calculates mean and variance of repeated runs. """
        dataEndTemp = pandas.DataFrame(0, index=np.arange(self.NUniqueSimulations), columns=self.dataEnd.keys())

        r = self.settings["Repeat"][0]
        for i in range(self.NUniqueSimulations):
            for key in self.dataEnd.keys():
                dataEndTemp.loc[i,key] = np.mean(self.dataEnd[key][i*r:i*r+r])
            # New keys
            dataEndTemp.loc[i,"run_error"] = np.sqrt(np.var(self.dataEnd["run"][i*r:i*r+r]))
        
        return dataEndTemp

    """
    Plotting methods
    """
    def PlotExtinctionTime(self, ax, vary, plotAllMeasurements = False):
        """ Creates a plot with extinction time with whatever parameter given """
        if self.isRepeated:
            ax.errorbar(self.parameters[vary], self.dataEnd["run"], self.dataEnd["run_error"], fmt='o', markersize=2, elinewidth = 0.5)
        else:
            ax.plot(self.parameters[vary], self.dataEnd["run"], '-o', markersize=3, linewidth=0.5)
            
        if plotAllMeasurements == True:
            for i in range(self.settings["Repeat"][0]):
                ax.plot(self.parameters[vary], self.dataEnd["run"][0+i::self.settings["Repeat"][0]],  color = "red", linestyle = "None",  marker='.', alpha=0.1)

        return

    def PlotMeanInfection(self, ax, vary, errorBars = True):
        """ Creates a plot of the mean and variance. """
        if errorBars:
            if self.isRepeated:
                ax.errorbar(self.parameters[vary], self.dataEnd["mean"], self.dataEnd["mean_error"],
                fmt='-o', markersize=6, linewidth=1.0, elinewidth=0.5, zorder=1)
            else: 
                ax.errorbar(self.parameters[vary], self.dataEnd["mean"], np.sqrt(self.dataEnd["variance"]),
                fmt='-o', markersize=4, linewidth=0.8, elinewidth=0.5, zorder=1)
        else:
            ax.plot(self.parameters[vary], self.dataEnd["mean"], '-o', markersize=3, linewidth=0.5)

        return

    def PlotAvgResistances(self, ax, vary):
        ax.plot(self.parameters[vary], self.dataEnd["avgResistances"], '-o', markersize=4, linewidth=0.5, zorder=1)
        return

    def PlotTimeline(self, ax, skip = 1):
        """ Makes a plot of the development of the number of infected over time. """
        ax.plot(self.timelineRuns[0::skip], self.timelineNInfected[0::skip], linewidth=0.75, alpha = 1.0)

        return

    def PlotStrainCounter(self, ax, skip = 1):
        """ Plots strain counter """
        for strain in range(self.NStrains):
            #ax.plot(self.timelineRuns[0::skip], self.strainCounter[0::skip, strain], linestyle="-.", dashes=(3, 3), linewidth=0.4, alpha=0.6)
            ax.plot(self.timelineRuns[0::skip], self.strainCounter[0::skip, strain], linestyle="-", linewidth=0.75, alpha=0.8)

        return 

    def Plot2D(self, fig, ax, vary1, vary2, vary3, ticks = None):
        """ vary1 is x-axis and vary2 is y """
        x = np.unique(self.parameters[vary1])
        y = np.unique(self.parameters[vary2])
        
        xStep = x[1] - x[0]
        yStep = y[1] - y[0]

        Z = np.zeros((len(x),len(y)))

        i = 0
        for x1 in x:
            j = 0
            for y1 in y:
                Z[i,j] = self.dataEnd[vary3][(x1 == self.parameters[vary1]) & (y1 == self.parameters[vary2])]
                j += 1
            i += 1
        
        if ticks is None:
            im = ax.imshow(np.transpose(Z), origin='lower', aspect='auto',
            extent=(np.min(x)-xStep/2, np.max(x)+xStep/2, np.min(y)-yStep/2, np.max(y)+yStep/2), vmin=0, vmax=max(Z), cmap='cividis' ) 
        else:
            im = ax.imshow(np.transpose(Z), origin='lower', aspect='auto',
            extent=(np.min(x)-xStep/2, np.max(x)+xStep/2, np.min(y)-yStep/2, np.max(y)+yStep/2), vmin=ticks[0], vmax=ticks[-1], cmap='cividis' ) 
  
        cbar = fig.colorbar(im, ticks = ticks)
        ax.tick_params()
        ax.set_aspect('auto')

        return
    
    def Plot2DResidual(self, vary1, vary2):
        return

    def PlotNiceAndSave(self, fig, ax, xlabel, ylabel, fileName):
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        #LF.format_axes(ax)
        fig.tight_layout(pad=0.2)

        figName = self.plotSavePath + fileName + ".pdf"
        fig.savefig(figName, format="pdf")
        return

    """
    Calculation and datachange methods
    """
    def CalcNewMeans(self):
        """ Calculates mean with calculated threshold based on the function FindThreshold. It does so based on the timeline files.
        The new calculated values are overwritten into the self.dataEnd and
        self.dataEndRepeat pandas objects. """

        mean = 0
        var = 0

        for simulation in range(self.NUniqueSimulations):
            for repeat in range(self.settings.loc[0, "Repeat"]):

                index = simulation*int(self.settings.loc[0, "Repeat"])+repeat

                self.timelineIndex = [simulation+1, repeat+1]
                self.ImportTimeline()
                
                _, _, i = FindThreshold(self.timelineRuns, self.timelineNInfected)
                
                if i == None: 
                    mean = 0
                    var = 0
                elif self.timelineRuns[-1] < 50:
                    mean = 0
                    var = 0
                else:
                    mean = np.mean(self.timelineNInfected[i:-1])
                    var = np.var(self.timelineNInfected[i:-1])

                self.dataEnd.loc[index, "mean"] = mean
                self.dataEnd.loc[index, "variance"] = var

        return

    def CheckEndemic(self, threshold = 500):
        
        isEndemic =  np.empty(self.NUniqueSimulations, dtype='U10')
        ratio = np.zeros(self.NUniqueSimulations)
        
        for simulation in range(self.NUniqueSimulations):
            for repeat in range(self.settings['Repeat'][0]):
                index = simulation*self.settings['Repeat'][0]+repeat

                ratio[simulation] += int(self.dataEnd['run'][index]>500)

            if ratio[simulation] >= 9:
                isEndemic[simulation] = "true"
            elif ratio[simulation] >= 6:
                isEndemic[simulation] = "maybe"
            else:
                isEndemic[simulation] = "false"

        return isEndemic, ratio

def FindThreshold(x, y, yExpectedValue = None):
    """
    This function finds in time series data, when it starts to . Specifically,
    it simply checks when timeseries hits the expected value for the second
    time. If it never does, return None
    """
    if yExpectedValue is None: 
        yExpectedValue = np.mean(y)
    length = len(x)
    count = 0
    side = None
    skip = 0  

    """Determine if the value starts below or above the expected value"""
    if y[skip] < yExpectedValue:
        side = "below"
    else: 
        side = "above"

    
    """Insert comment here"""
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

    """Return None to tell the reciever that no threshold was found"""
    return None, None, None

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
    #loglike = -1* ( np.sum( np.log(1/(np.sqrt(2*np.pi)*Y_err)) ) + np.sum( (Y -
    #fitFunc(X, param))**2 / (Y_err**2) ) )
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
