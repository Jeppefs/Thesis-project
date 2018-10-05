"""This document is for testing test statistics that is robust for my purpose, which shows if a"""
import numpy as np 
import matplotlib.pyplot as plt
import scipy.stats as ss

np.random.seed(1)

def CreateCorreleatedNoiseData(mean, sigma, pullStrength):
    ## Create some data
    x = np.arange(0,2000) 
    N = len(x)
    y = np.zeros(N)
    y[0] = mean + np.random.normal(0, sigma)
    for i in range(N-1):
        y[i+1] = y[i] + np.random.normal(0, sigma) + pullStrength * (mean - y[i]) # The data is noise, plus linear movement towards the mean. 

    ## Make new means based on ten data points. 
    NCombined = int(N/10)
    xCombined = np.zeros(NCombined)
    yCombined = np.zeros(NCombined)
    ySigma = np.zeros(NCombined)
    for i in range(NCombined):
        xCombined[i] = np.mean(x[int(0+i*10):int(10+i*10)])
        yCombined[i] = np.mean(y[int(0+i*10):int(10+i*10)])
        ySigma[i] = np.sqrt(np.var(y[int(0+i*10):int(10+i*10)]))
    
    return x, y, N, xCombined, yCombined, NCombined, ySigma

def CreateCorreleatedNoiseDataIncreasing(mean, sigma, pullStrength):
    ## Create some data
    x = np.arange(0,2000) 
    N = len(x)
    y = np.zeros(N)
    y[0] = mean + np.random.normal(0, sigma)
    for i in range(N-1):
        y[i+1] = y[i] + np.random.normal(0, sigma) + pullStrength * (mean+0.01*(x[i]/x[-1]) - y[i]) # The data is noise, plus linear movement towards the mean. 

    ## Make new means based on ten data points. 
    NCombined = int(N/10)
    xCombined = np.zeros(NCombined)
    yCombined = np.zeros(NCombined)
    ySigma = np.zeros(NCombined)
    for i in range(NCombined):
        xCombined[i] = np.mean(x[int(0+i*10):int(10+i*10)])
        yCombined[i] = np.mean(y[int(0+i*10):int(10+i*10)])
        ySigma[i] = np.sqrt(np.var(y[int(0+i*10):int(10+i*10)]))
    
    return x, y, N, xCombined, yCombined, NCombined, ySigma

def CreateCorreleatedNoiseDataIncreasingAtEnd(mean, sigma, pullStrength):
    ## Create some data
    x = np.arange(0,2000) 
    N = len(x)
    y = np.zeros(N)
    y[0] = mean + np.random.normal(0, sigma)
    for i in range(N-1):
        y[i+1] = y[i] + np.random.normal(0, sigma) + pullStrength * (mean+(x[i] > 1500)*0.1 - y[i]) # The data is noise, plus linear movement towards the mean. 

    ## Make new means based on ten data points. 
    NCombined = int(N/10)
    xCombined = np.zeros(NCombined)
    yCombined = np.zeros(NCombined)
    ySigma = np.zeros(NCombined)
    for i in range(NCombined):
        xCombined[i] = np.mean(x[int(0+i*10):int(10+i*10)])
        yCombined[i] = np.mean(y[int(0+i*10):int(10+i*10)])
        ySigma[i] = np.sqrt(np.var(y[int(0+i*10):int(10+i*10)]))
    
    return x, y, N, xCombined, yCombined, NCombined, ySigma

def CreateCorreleatedNoiseDataSinus(mean, sigma, pullStrength):
    ## Create some data
    x = np.arange(0,2000) 
    N = len(x)
    y = np.zeros(N)
    y[0] = mean + np.random.normal(0, sigma)
    for i in range(N-1):
        y[i+1] = y[i] + np.random.normal(0, sigma) + pullStrength * (mean + np.sin(x[i]/10) - y[i]) # The data is noise, plus linear movement towards the mean. 

    ## Make new means based on ten data points. 
    NCombined = int(N/10)
    xCombined = np.zeros(NCombined)
    yCombined = np.zeros(NCombined)
    ySigma = np.zeros(NCombined)
    for i in range(NCombined):
        xCombined[i] = np.mean(x[int(0+i*10):int(10+i*10)])
        yCombined[i] = np.mean(y[int(0+i*10):int(10+i*10)])
        ySigma[i] = np.sqrt(np.var(y[int(0+i*10):int(10+i*10)]))
    
    return x, y, N, xCombined, yCombined, NCombined, ySigma


## Parameters
mean = 0.5
sigma = 0.1
pullStrength = 0.1

## Make linear tests. They should get it right. 
## Wilcoxon signed-rank test 
p = np.zeros(100)
pComb = np.zeros(100)
for i in range(100):
    x, y, N, xCombined, yCombined, NCombined, ySigma = CreateCorreleatedNoiseDataIncreasing(mean, sigma, pullStrength)
    _, p[i] = (ss.wilcoxon(y[0:int(N/2)],y[int(N/2):N]))
    _, pComb[i] = (ss.wilcoxon(yCombined[0:int(NCombined/2)],yCombined[int(NCombined/2):NCombined]))



## Plotting

plt.figure()
plt.plot(x,y)
plt.plot(x, np.ones(N)*mean)

plt.figure()
plt.errorbar(xCombined, yCombined, ySigma)
plt.plot(x, np.ones(N)*mean)

plt.figure()
plt.hist(p, alpha=0.5, color='b')
plt.hist(pComb, alpha=0.5, color='r')

plt.show()