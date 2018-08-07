import numpy as np 
import matplotlib.pyplot as plt

class RungeKutta():

    def __init__(self, initialConditions, equation, param, dt = 0.001):
        self.NValues = len(initialConditions)
        self.values = initialConditions
        self.valuesRate = np.zeros(self.NValues)
        self.equation = equation
        self.param = np.copy(param)

        self.t = 0.0
        self.dt = dt

    def Run(self, maxRuns):

        self.savedValues = np.zeros((self.NValues, maxRuns + 1))
        self.savedValues[:,0] = self.values

        for run in range(maxRuns):
            self.Progress()
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
    
    def PlotTimePlot(self):
        plt.figure()
        for i in range(self.NValues):
            plt.plot(self.savedValues[i,:]) 
        
        return

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
