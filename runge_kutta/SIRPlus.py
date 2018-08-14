import numpy as np 
import matplotlib.pyplot as plt
import RungeKutta as RK

from matplotlib import rc
from matplotlib import rcParams

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

def Ross(param, values, t):
    valuesRate = np.zeros(len(values))
    
    valuesRate[0] = param[0] * param[1] * param[2] * values[1] * (1 - values[0]) - param[3] * values[0]
    valuesRate[1] = param[0] * param[4] * values[0] * (1 - values[1]) - param[5] * values[1]
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

def Macdonald(param, values, t):
    valuesRate = np.zeros(len(values))
    return valuesRate

def SimpleInfectionSteadyState(param, values, t):
    valuesRate = np.zeros(len(values))

    valuesRate[0] = param[0]*values[0]*values[1] - param[1]*values[0]
    valuesRate[1] = - param[0]*values[0]*values[1] + param[1]*values[0]
    return valuesRate

def SimpleInfection(param, values, t):
    valuesRate = np.zeros(len(values))

    valuesRate[0] = - param[0] * values[0] * (values[1] + values[2])
    valuesRate[1] = param[0] * values[0] * (values[1] + values[2]) - param[1] * values[1]
    valuesRate[2] = param[0] * values[3] * (values[1] + values[2]) + param[1] * values[1] - param[1] * values[2]
    valuesRate[3] = - param[0] * values[3] * (values[1] + values[2]) + param[1] * values[2] 
    return valuesRate

def Replacement(p, v, t):
    valuesRate = np.zeros(len(v))

    valuesRate[0] = - p[0] * v[0] * (v[1] + v[2]) + p[2] * (v[1]+v[2]+v[3])
    valuesRate[1] = p[0] * v[0] * (v[1] + v[2]) - p[1] * v[1] - p[2] * v[1] 
    valuesRate[2] = p[0] * v[3] * (v[1] + v[2]) + p[1] * v[1] - p[1] * v[2] - p[2] * v[2]
    valuesRate[3] = - p[0] * v[3] * (v[1] + v[2]) + p[1] * v[2]  - p[2] * v[3]
    return valuesRate

def PlotSimple(func, initial, param, legend, runs = 50000, xlabel = "", ylabel = ""):
    q = RK.RungeKutta(initialConditions = initial, equation = func, param = param, dt = 0.01)
    q.Run(runs)
    print(q.values, np.sum(q.values))
    q.PlotTimePlot()
    rcParams.update({'font.size': 16})
    plt.legend(legend)
    plt.xlabel(xlabel, fontsize=16)
    plt.ylabel(ylabel, fontsize=16)
    plt.tick_params(labelsize=14)
    plt.tight_layout()
    plt.savefig("runge_kutta/temp.pdf", format="pdf")
    plt.show()
    return


#PlotSimple(func = SimpleInfection, initial = [0.99, 0.01, 0.0, 0.0], param = [0.9, 1.0], legend = ["S", "I", "I_R", "S_R"], runs=10000, xlabel="Iteration", ylabel="Proportion")
#PlotSimple(func = SimpleInfectionSteadyState, initial = [0.99, 0.01], param = [1.1, 1.0], legend = ["$I_R$", "$S_R$"], runs=10000, xlabel="Iteration", ylabel="Proportion")

PlotSimple(Replacement, initial = [0.99, 0.01, 0.0, 0.0], param = [0.99, 1.0, 0.1], legend = ["S","I","$I_R$", "$S_R$"], runs=10000, xlabel="Iteration", ylabel="Proportion")

#PlotSimple(func = Ross, initial = [0.1, 0.1], param = [0.09, 0.2, 2.0, 0.01, 0.5, 0.1], legend = ["$I_h$","$I_m$"], runs=100000, xlabel="Iterations", ylabel="Proportion infected")


#RK.TestRungeKutta()
#q = RK.RungeKutta(initialConditions = np.array([0.99, 0.01, 0.0, 0.0]), equation = SIRPlus, param = np.array([2.1, 0.0, 0.0, 1.0, 2.1, 2.0]), dt = 0.001)
#q.Run(75000)
#q.PlotTimePlot()
#plt.legend(["S","I","R","R_I"])
#plt.show()