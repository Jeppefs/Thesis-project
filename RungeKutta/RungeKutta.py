import numpy as np 

class RungeKutta():

    def __init__(self, NValues, equation, param):
        self.NValues = NValues
        self.values = np.zeros(NValues)
        self.valuesRate = np.zeros(NValues)
        self.equation = equation
        self.param = np.copy(param)

    def Run(self, maxRuns):
        for run in range(maxRuns):
            self.Progress()
        return

    def Progress(self):
        self.values += self.equation(self.param, self.values)*dt

        
        return

def TestRungeKutta():
    return

def SIR(param, values):
    ValuesRate = np.zeros(len(values))
    valuesRate[0] = -param[0]*values[0]*values[1]
    valuesRate[1] = param[0]*values[0]*values[1] - param[1]*values[1]
    valuesRate[2] = param[1]*values[1]
    return valuesRate
