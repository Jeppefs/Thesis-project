import numpy as np 
import matplotlib.pyplot as plt
import matplotlib 
import RungeKutta as RK
import DifferentialSystems as DS
from Latexifier import LatexifierFunctions as LF 



def PlotSimple(func, initial, param, legend, runs = 50000, xlabel = "", ylabel = "", color = None):
    q = RK.RungeKutta(initialConditions = initial, equation = func, param = param, dt = 0.01)
    q.Run(runs)
    print(q.values, np.sum(q.values))

    fig, ax = plt.subplots() 
    for i in range(q.NValues):
        if color == None:
            ax.plot(q.savedValues[i,:], linewidth = 1.0) 
        else:
            ax.plot(q.savedValues[i,:], linewidth = 1.0, color = color[i])
    ax.legend(legend)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    LF.format_axes(ax)
    fig.tight_layout(pad = 0.1)
    fig.savefig("runge_kutta/temp.pdf", format="pdf")
    return

def ReplacementParameterRasta():
    q = RK.RungeKutta(initialConditions = [0.99, 0.01, 0.0, 0.0], param = [0.80, 1.0, 0.00], equation = Replacement, dt = 0.01)
    paramList = np.arange(0, 1+0.00001, 0.01)
    alphaList = np.array([0.6, 0.8, 0.9, 0.95])
    plt.figure()
    for alpha in alphaList:
        q.param[0] = alpha
        endingValues = q.ParameterSearch(paramIndex = 2, paramList = paramList, runs = 5000) 
        plt.plot(paramList, endingValues[1,:] + endingValues[2,:])
    plt.legend([r"$\alpha=0.60$", r"$\alpha=0.80$", r"$\alpha=0.9$", r"$\alpha=0.95$"])
    plt.xlabel(r"$\gamma$", fontsize=16)
    plt.ylabel("Proportion infected", fontsize=16)
    plt.tick_params(labelsize=14)
    plt.tight_layout(pad=0.1)
    plt.savefig("runge_kutta/temp.pdf", format="pdf")

    return


def ReplacementRastaScan():
    
    alphaStep = 0.02
    gammaStep = 0.005
    alphas = np.arange(0.5, 1.10+0.000001, alphaStep)
    gammas = np.arange(0, 0.6+0.000001, gammaStep)
    #alphas = np.array([0.5, 1.0])
    #gammas = np.array([0.1, 0.2])
    gridSurvival = np.zeros((len(alphas), len(gammas)))
    gridInfected = np.zeros((len(alphas), len(gammas)))
    gridResistant = np.zeros((len(alphas), len(gammas)))

    i = 0
    for alpha in alphas:
        j = 0
        for gamma in gammas:
            q = RK.RungeKutta(initialConditions = [0.99, 0.01, 0.0, 0.0], param = [alpha, 1.0, gamma], equation = Replacement, dt = 0.01)
            q.Run(10000)
            gridInfected[i,j] = q.values[1] + q.values[2] 
            gridResistant[i,j] = q.values[2] + q.values[3]
            j += 1
            print(i, j)
        i += 1

    gridSurvival = np.ceil(gridInfected-1/(10**3))

    ## Survival
    plt.figure()
    plt.imshow(gridSurvival, origin='lower', extent=(np.min(gammas)-gammaStep/2,np.max(gammas)+gammaStep/2,np.min(alphas)-alphaStep/2,np.max(alphas)+alphaStep/2), aspect='auto' )    
    plt.xlabel(r"$\gamma$", fontsize=18)
    plt.ylabel(r"$\alpha$", fontsize=18)
    plt.tick_params(labelsize=16)
    plt.tight_layout()
    plt.savefig("runge_kutta/gridSurvival.pdf", format="pdf")

    ## Infected
    plt.figure()
    plt.imshow(gridInfected, origin='lower', extent=(np.min(gammas)-gammaStep/2,np.max(gammas)+gammaStep/2,np.min(alphas)-alphaStep/2,np.max(alphas)+alphaStep/2), aspect='auto' )    
    plt.xlabel(r"$\gamma$", fontsize=18)
    plt.ylabel(r"$\alpha$", fontsize=18)
    plt.colorbar()
    plt.tick_params(labelsize=16)
    plt.tight_layout()
    plt.savefig("runge_kutta/gridInfected.pdf", format="pdf")

    ## Infected
    plt.figure()
    plt.imshow(gridResistant, origin='lower', extent=(np.min(gammas)-gammaStep/2,np.max(gammas)+gammaStep/2,np.min(alphas)-alphaStep/2,np.max(alphas)+alphaStep/2), aspect='auto' )    
    plt.xlabel(r"$\gamma$", fontsize=18)
    plt.ylabel(r"$\alpha$", fontsize=18)
    plt.colorbar()
    plt.tick_params(labelsize=16)
    plt.tight_layout() 
    plt.savefig("runge_kutta/gridResistant.pdf", format="pdf")

    return
    
LF.Latexify(fig_width = 12.65076*0.49, label_size = [1.05, 1.05])

"""Simple function and plotting"""
#PlotSimple(func = DS.SimpleInfection, initial = [0.99, 0.01, 0.0, 0.0], param = [0.9, 1.0], legend = ["$S$", "$I$", "$I_R$", "$S_R$"], runs=10000, xlabel="Iteration", ylabel="Proportion")
#PlotSimple(func = DS.SimpleInfectionSteadyState, initial = [0.99, 0.01], param = [1.1, 1.0], legend = ["$I_R$", "$S_R$"], runs=10000, xlabel="Iteration", ylabel="Proportion", color = ['g','r'])

"""Replacement"""
PlotSimple(DS.Replacement, initial = [0.99, 0.01, 0.0, 0.0], param = [0.95, 1.0, 0.1], legend = ["S","I","$I_R$", "$S_R$"], runs=10000, xlabel="Iteration", ylabel="Proportion")

"""Ross"""
#PlotSimple(func = Ross, initial = [0.1, 0.1], param = [0.09, 0.2, 2.0, 0.01, 0.5, 0.1], legend = ["$I_h$","$I_m$"], runs=100000, xlabel="Iterations", ylabel="Proportion infected")

"""Test"""
#RK.TestRungeKutta()
#q = RK.RungeKutta(initialConditions = np.array([0.99, 0.01, 0.0, 0.0]), equation = SIRPlus, param = np.array([2.1, 0.0, 0.0, 1.0, 2.1, 2.0]), dt = 0.001)
#q.Run(75000)
#q.PlotTimePlot()
#plt.legend(["S","I","R","R_I"])
#plt.show()

print("Congrats! All done!")