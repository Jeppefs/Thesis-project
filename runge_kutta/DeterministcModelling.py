import numpy as np 
import matplotlib.pyplot as plt
import matplotlib 
import RungeKutta as RK
import DifferentialSystems as DS
from Latexifier import LatexifierFunctions as LF 



def PlotSimple(func, initial, param, legend, runs = 50000, xlabel = "", ylabel = "", color = None, filename="temp"):
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
    fig.savefig("runge_kutta/"+filename+".pdf", format="pdf")
    return

def ReplacementParameterRasta(filename="temp"):
    q = RK.RungeKutta(initialConditions = [0.99, 0.01, 0.0, 0.0], param = [0.80, 1.0, 0.00], equation = DS.Replacement, dt = 0.01)
    paramList = np.arange(0, 1+0.00001, 0.01)
    alphaList = np.array([0.6, 0.8, 0.95, 1.05])
    fig, ax = plt.subplots()
    for alpha in alphaList:
        q.param[0] = alpha
        endingValues = q.ParameterSearch(paramIndex = 2, paramList = paramList, runs = 5000) 
        ax.plot(paramList, endingValues[1,:] + endingValues[2,:], linewidth=1.0)
    ax.legend([r"$\alpha=0.60$", r"$\alpha=0.80$", r"$\alpha=0.95$", r"$\alpha=1.05$"])
    ax.set_xlabel(r"$\gamma$")
    ax.set_ylabel("Proportion infected")
    LF.format_axes(ax)
    fig.tight_layout(pad=0.1)
    fig.savefig("runge_kutta/"+filename+".pdf", format="pdf")
    return

def ReplacementRastaScan():
    
    alphaStep = 0.2#0.02
    gammaStep = 0.05#0.005
    alphas = np.arange(0.5, 1.10+0.000001, alphaStep)
    gammas = np.arange(0, 0.6+0.000001, gammaStep)
    gridSurvival = np.zeros((len(alphas), len(gammas)))
    gridInfected = np.zeros((len(alphas), len(gammas)))
    gridResistant = np.zeros((len(alphas), len(gammas)))

    i = 0
    for alpha in alphas:
        j = 0
        for gamma in gammas:
            q = RK.RungeKutta(initialConditions = [0.99, 0.01, 0.0, 0.0], param = [alpha, 1.0, gamma], equation = DS.Replacement, dt = 0.01)
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
    plt.xlabel(r"$\gamma$")
    plt.ylabel(r"$\alpha$")
    plt.tick_params()
    plt.tight_layout(pad = 0.1)
    plt.savefig("runge_kutta/gridSurvival.pdf", format="pdf")

    ## Infected
    plt.figure()
    plt.imshow(gridInfected, origin='lower', extent=(np.min(gammas)-gammaStep/2,np.max(gammas)+gammaStep/2,np.min(alphas)-alphaStep/2,np.max(alphas)+alphaStep/2), aspect='auto' )    
    plt.xlabel(r"$\gamma$")
    plt.ylabel(r"$\alpha$")
    plt.colorbar()
    plt.tick_params()
    plt.tight_layout(pad = 0.1)
    plt.savefig("runge_kutta/gridInfected.pdf", format="pdf")

    ## Infectedå
    plt.figure()
    plt.imshow(gridResistant, origin='lower', extent=(np.min(gammas)-gammaStep/2,np.max(gammas)+gammaStep/2,np.min(alphas)-alphaStep/2,np.max(alphas)+alphaStep/2), aspect='auto' )    
    plt.xlabel(r"$\gamma$")
    plt.ylabel(r"$\alpha$")
    plt.colorbar()
    plt.tick_params()
    plt.tight_layout(pad = 0.1) 
    plt.savefig("runge_kutta/gridResistant.pdf", format="pdf")

    return

def PlotEpedimicModels():
    q = RK.RungeKutta(initialConditions = np.array([0.99, 0.01, 0.0]), param = np.array([1.0, 0.5, 0.1, 0.01]), equation = DS.SIRS, dt=0.001)
    q.Run(100000)

    fig, ax = plt.subplots()
    ax.plot(q.savedValues[1, :])
    return

"""Latexify. fig_width is 12.65076*0.99 for full page fig and 6.19893 for sub plots"""
standard_width = 6.19893
LF.Latexify(fig_width = 6.19893, label_size = [1.05, 1.05])

"""Epedimic Models"""
#PlotEpedimicModels()

"""Simple function and plotting"""
#PlotSimple(func = DS.SimpleInfection, initial = [0.99, 0.01, 0.0, 0.0], param = [0.9, 1.0], legend = ["$S$", "$I$", "$I_R$", "$S_R$"], runs=10000, xlabel="Iteration", ylabel="Proportion")
#PlotSimple(func = DS.SimpleInfectionSteadyState, initial = [0.99, 0.01], param = [1.1, 1.0], legend = ["$I_R$", "$S_R$"], runs=10000, xlabel="Iteration", ylabel="Proportion", color = ['g','r'])

"""Replacement"""
#PlotSimple(DS.Replacement, initial = [0.99, 0.01, 0.0, 0.0], param = [0.95, 1.0, 0.01], legend = ["S","I","$I_R$", "$S_R$"], runs=10000,
#  xlabel="Iteration", ylabel="Proportion", filename="replacement_deterministic_0_01")
#PlotSimple(DS.Replacement, initial = [0.99, 0.01, 0.0, 0.0], param = [0.95, 1.0, 0.1], legend = ["S","I","$I_R$", "$S_R$"], runs=10000,
# xlabel="Iteration", ylabel="Proportion", filename="replacement_deterministic_0_1")
ReplacementParameterRasta(filename="replacement_deterministic_gamma")
#LF.Latexify(fig_width=standard_width, fig_height=standard_width)
#ReplacementRastaScan()


"""Ross"""
#PlotSimple(func = DS.Ross, initial = [0.1, 0.1], param = [0.1, 0.2, 2.0, 0.01, 0.5, 0.1], legend = ["$I_h$","$I_m$"], runs=100000,
# xlabel="Iterations", ylabel="Proportion infected", filename= "Ross2")

"""Test"""
#RK.TestRungeKutta()
#q = RK.RungeKutta(initialConditions = np.array([0.99, 0.01, 0.0, 0.0]), equation = DS.SIRPlus, param = np.array([2.1, 0.0, 0.0, 1.0, 2.1, 2.0]), dt = 0.001)
#q.Run(75000)
#q.PlotTimePlot()
#plt.legend(["S","I","R","R_I"])
#plt.show()

plt.show()
print("Congrats! All done!")