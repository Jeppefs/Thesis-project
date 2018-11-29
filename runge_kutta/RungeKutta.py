import numpy as np 
import matplotlib.pyplot as plt

class RungeKutta():

    def __init__(self, initialConditions, equation, param, dt = 0.001):
        self.NValues = len(initialConditions)
        self.initialConditions = initialConditions
        self.values = initialConditions
        self.valuesRate = np.zeros(self.NValues)
        self.equation = equation
        self.param = np.copy(param)

        self.t = 0.0
        self.dt = dt

    def Run(self, maxRuns):

        self.savedValues = np.zeros((self.NValues, maxRuns + 1))
        self.savedValues[:,0] = self.values
        self.times = np.zeros(maxRuns + 1)

        for run in range(maxRuns):
            self.Progress()
            self.times[run+1] = self.t
            self.savedValues[:,run+1] = self.values
        return

    def Progress(self):
        k1 = self.equation(self.param, self.values, self.t)
        k1Values = self.values + (self.dt * k1) / 2.0
        k2 = self.equation(self.param, k1Values, self.t + self.dt/2)
        k2Values = self.values + (self.dt * k2) / 2.0
        k3 = self.equation(self.param, k2Values, self.t + self.dt/2)
        k3Values = self.values + (self.dt * k3)
        k4 = self.equation(self.param, k3Values, self.t + self.dt)

        self.values += (k1 + k2*2 + k3*2 + k4)*self.dt/6
        self.t += self.dt
        
        return
    
    def ParameterSearch(self, paramIndex = 0, paramList = [1], runs=10000):
        endingValues = np.zeros((self.NValues, len(paramList)))
        i = 0
        for paramVal in paramList:
            self.param[paramIndex] = paramVal
            self.Run(runs)
            endingValues[:,i] = self.values
            self.values = self.initialConditions
            self.valuesRate = np.zeros(self.NValues)
            i += 1

        return endingValues

    def PlotTimePlot(self):
        fig, ax = plt.subplots() 
        for i in range(self.NValues):
            plt.plot(self.savedValues[i,:], linewidth = 0.5) 
        
        return ax 

def TestRungeKutta():
    q = RungeKutta(np.array([0.99, 0.01, 0.0]), SIR, np.array([1.0,1.0]), dt = 0.001)
    q.Run(100000)
    q.PlotTimePlot()
    plt.legend(["S","I","R"])
    plt.tight_layout()
    plt.show()

    return

def SIR(param, values, t):
    valuesRate = np.zeros(len(values))
    valuesRate[0] = -param[0]*values[0]*values[1]
    valuesRate[1] = param[0]*values[0]*values[1] - param[1]*values[1]
    valuesRate[2] = param[1]*values[1]
    return valuesRate
