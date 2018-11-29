import numpy as np 

def SIR(p, v, t):
    valuesRate = np.zeros(len(v))

    valuesRate[0] = - p[0]*v[0]*v[1]  
    valuesRate[1] = p[0]*v[0]*v[1] - p[1]*v[1]
    valuesRate[2] = p[1]*v[1]

    return valuesRate

def SIR_vital(p, v, t):
    valuesRate = np.zeros(len(v))

    valuesRate[0] = - p[0]*v[0]*v[1] + p[2]*(v[1] + v[2])
    valuesRate[1] = p[0]*v[0]*v[1] - p[1]*v[1] - p[2]*v[1]
    valuesRate[2] = p[1]*v[1] - p[2]*v[2]

    return valuesRate

def SI(param, values, t):
    valuesRate = np.zeros(len(values))

    valuesRate[0] = - param[0] * values[0] + param[1] * values[1]
    valuesRate[1] = param[0] * values[0] - param[1] * values[1]

    return valuesRate

def Ross(param, values, t):
    valuesRate = np.zeros(len(values))
    
    valuesRate[0] = param[0] * param[1] * param[2] * values[1] * (1 - values[0]) - param[3] * values[0]
    valuesRate[1] = param[0] * param[4] * values[0] * (1 - values[1]) - param[5] * values[1]
    return valuesRate

def Dietz(param, values, t):
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