import numpy as np 
import matplotlib.pyplot as plt
import RungeKutta as RK

def SIRPlus(param, values, t):
    valuesRate = np.zeros(len(values))
    
    valuesRate[0] = -param[0] * values[0] * (values[1] + values[3]) + param[1] * values[1] + param[2] * values[3]
    valuesRate[1] = param[0] * values[0] * (values[1] + values[3]) - param[1] * values[1] - param[3] * values[1] 
    valuesRate[2] = - param[4] * values[2] * (values[1] + values[3]) + param[3]*values[1] + param[5] * values[3] 
    valuesRate[3] = param[4] * values[2] * (values[1] + values[3]) - param[2] * values[3] - param[5] * values[3]

    return valuesRate

def UltraSIR(param, values, t):
    valuesRate = np.zeros(len(values))

    valuesRate[0] = param[0]   
    valuesRate[1] = 0
    valuesRate[2] = 0
    valuesRate[3] = 0
    valuesRate[4] = 0
    valuesRate[5] = 0
    valuesRate[6] = 0
    valuesRate[7] = 0
    valuesRate[8] = 0
    valuesRate[9] = 0
    valuesRate[10] = 0
    valuesRate[11] = 0
    valuesRate[12] = 0
    valuesRate[13] = 0
    valuesRate[14] = 0
    valuesRate[15] = 0
    valuesRate[16] = 0

    return valuesRate

def Deitz(param, values, t):
    valuesRate = np.zeros(len(values))

    valuesRate[0] = param[0] + param[1] * values[5] - 1
    valuesRate[1] = param[1]
    valuesRate[2] = param[2] 
    valuesRate[3] = 0
    valuesRate[4] = 0
    valuesRate[5] = 0
    valuesRate[6] = 0
    
    return valuesRate

def Ross(param, values, t):
    valuesRate = np.zeros(len(values))
    
    valuesRate[0] = 1
    valuesRate[1] = 1 
    return valuesRate

#RK.TestRungeKutta()
q = RK.RungeKutta(initialConditions = np.array([0.99, 0.01, 0.0, 0.0]), equation = SIRPlus, param = np.array([2.1, 0.0, 0.0, 1.0, 2.1, 2.0]), dt = 0.001)
q.Run(75000)
q.PlotTimePlot()
plt.legend(["S","I","R","R_I"])
plt.show()