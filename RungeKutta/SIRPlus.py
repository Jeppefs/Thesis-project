import numpy as np 
import matplotlib.pyplot as plt
import RungeKutta as RK

def SIRPlus(param, values, t):
    valuesRate = np.zeros(len(values))
    
    valuesRate[0] = -param[0]*values[0]*(values[1] + values[3]) + param[1] * values[1] + param[2] * values[3]
    valuesRate[1] = param[0]*values[0]*(values[1] + values[3]) - param[1] * values[1] - param[3] * values[1] 
    valuesRate[2] = - param[4] * values[2] * (values[1] + values[3]) + param[3]*values[1] + param[5] * values[3] 
    valuesRate[3] = param[4] * values[2] * (values[1] + values[3]) - param[2] * values[3] - param[5] * values[3]

    return valuesRate

#RK.TestRungeKutta()
q = RK.RungeKutta(initialConditions = np.array([0.99, 0.01, 0.0, 0.0]), equation = SIRPlus, param = np.array([2.1, 0.0, 0.0, 1.0, 2.1, 2.0]), dt = 0.001)
q.Run(75000)
q.PlotTimePlot()
plt.legend(["S","I","R","R_I"])
plt.show()