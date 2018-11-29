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
            ax.plot(q.times, q.savedValues[i,:], linewidth = 1.0) 
        else:
            ax.plot(q.times, q.savedValues[i,:], linewidth = 1.0, color = color[i])
    ax.legend(legend)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    LF.format_axes(ax)
    fig.tight_layout(pad = 0.1)
    fig.savefig("runge_kutta/plots/"+filename+".pdf", format="pdf")
    return

def SIR_vitalRastaScan():

    plt.style.use("seaborn")
    LF.Latexify(fig_width = standard_width, label_size = [1.0, 1.0])
    matplotlib.rc('font',**{'family':'serif', 'serif':['Computer Modern Roman']})
    matplotlib.rc('text', usetex=True)

    alphaStep = 0.01
    gammaStep = 0.01
    alphas = np.arange(1.0, 2.0+0.0000001, alphaStep)
    gammas = np.arange(0.0, 0.5+0.0000001, gammaStep)
    beta = 1.0
    infected = np.zeros((len(alphas), len(gammas)))

    for i, alpha in enumerate(alphas):
        for j, gamma in enumerate(gammas):
            q = RK.RungeKutta(initialConditions = [0.90, 0.10, 0.0], param = [alpha, beta, gamma], equation = DS.SIR_vital, dt = 0.01)
            q.Run(10000)
            infected[i, j] = q.values[1]
        print(i)

    fig, ax = plt.subplots()

    ax.grid(False)
    im = ax.imshow(infected, origin='lower', extent=(np.min(gammas)-gammaStep/2,np.max(gammas)+gammaStep/2,np.min(alphas)-alphaStep/2,np.max(alphas)+alphaStep/2), aspect='auto', cmap='cividis')    
    ax.set_xlabel(r"$\gamma$")
    ax.set_ylabel(r"$\alpha$")
    ax.set_yticks([1.0, 1.2, 1.4, 1.6, 1.8, 2.0])
    ax.set_xticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5])
    fig.colorbar(im)
    ax.tick_params()
    ax.set_aspect('auto')
    fig.tight_layout(pad = 0.1)
    fig.savefig("runge_kutta/plots/SIR_vital2D.pdf", format="pdf")

def ReplacementParameterRasta(filename="temp"):
    q = RK.RungeKutta(initialConditions = [0.95, 0.05, 0.0, 0.0], param = [0.80, 1.0, 0.00], equation = DS.Replacement, dt = 0.01)
    paramList = np.arange(0, 1+0.00001, 0.01)
    alphaList = np.array([0.6, 0.8, 0.95, 1.05])
    fig, ax = plt.subplots()
    for alpha in alphaList:
        q.param[0] = alpha
        endingValues = q.ParameterSearch(paramIndex = 2, paramList = paramList, runs = 20000) 
        ax.plot(paramList, endingValues[1,:] + endingValues[2,:], linewidth=1.0)
    ax.legend([r"$\alpha=0.60$", r"$\alpha=0.80$", r"$\alpha=0.95$", r"$\alpha=1.05$"])
    ax.set_xlabel(r"$\gamma$")
    ax.set_ylabel("Proportion infected")
    LF.format_axes(ax)
    fig.tight_layout(pad=0.1)
    fig.savefig("runge_kutta/plots/"+filename+".pdf", format="pdf")
    return

def ReplacementRastaScan():
    
    alphaStep = 0.01 #0.01
    gammaStep = 0.01 #0.01
    alphas = np.arange(0.5, 1.10+0.000001, alphaStep)
    gammas = np.arange(0, 1.0+0.000001, gammaStep)
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

    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()
    fig3, ax3 = plt.subplots()

    ## Survival
    ax1.imshow(gridSurvival, origin='lower', extent=(np.min(gammas)-gammaStep/2,np.max(gammas)+gammaStep/2,np.min(alphas)-alphaStep/2,np.max(alphas)+alphaStep/2), aspect='auto',cmap='cividis' )    
    ax1.grid(False)
    ax1.set_xlabel(r"$\gamma$")
    ax1.set_ylabel(r"$\alpha$")
    ax1.tick_params()
    ax1.set_aspect('auto')
    fig1.tight_layout(pad = 0.1)
    fig1.savefig("runge_kutta/plots/replacement_gridSurvival.pdf", format="pdf")

    ## Infected
    im = ax2.imshow(gridInfected, origin='lower', extent=(np.min(gammas)-gammaStep/2,np.max(gammas)+gammaStep/2,np.min(alphas)-alphaStep/2,np.max(alphas)+alphaStep/2), aspect='auto', cmap='cividis')    
    ax2.grid(False)
    ax2.set_xlabel(r"$\gamma$")
    ax2.set_ylabel(r"$\alpha$")
    fig2.colorbar(im)
    ax2.tick_params()
    ax2.set_aspect('auto')
    fig2.tight_layout(pad = 0.1)
    fig2.savefig("runge_kutta/plots/replacement_gridInfected.pdf", format="pdf")

    ## Resistant
    im = ax3.imshow(gridResistant, origin='lower', extent=(np.min(gammas)-gammaStep/2,np.max(gammas)+gammaStep/2,np.min(alphas)-alphaStep/2,np.max(alphas)+alphaStep/2), aspect='auto', cmap='cividis')    
    ax3.grid(False)
    ax3.set_xlabel(r"$\gamma$")
    ax3.set_ylabel(r"$\alpha$")
    fig3.colorbar(im)
    ax3.tick_params()
    ax3.set_aspect('auto')
    fig3.tight_layout(pad = 0.1) 
    fig3.savefig("runge_kutta/plots/replacement_gridResistant.pdf", format="pdf")

    return


"""Latexify. fig_width is 12.65076*0.99 for full page fig and 6.19893 for sub plots"""
standard_width = 6.19893
full_width = 12.65076

plt.style.use("seaborn")
LF.Latexify(fig_width = standard_width, label_size = [1.0, 1.0])
matplotlib.rc('font',**{'family':'serif', 'serif':['Computer Modern Roman']})
matplotlib.rc('text', usetex=True)

"""Epedimic Models"""
#PlotSimple(DS.SIR, initial = [0.99, 0.01, 0.0], param = [0.95, 1.0], legend = ["S", "I", "R"], runs = 4000, xlabel = "Time", ylabel = "Proportion", filename="SIR1")
#PlotSimple(DS.SIR, initial = [0.99, 0.01, 0.0], param = [1.5, 1.0], legend = ["S", "I", "R"], runs = 4000, xlabel = "Time", ylabel = "Proportion", filename="SIR2")
#PlotSimple(DS.SI, initial = [0.99, 0.01], param = [0.5, 1.0], legend = ["S", "I"], runs = 1000, xlabel = "Time", ylabel = "Proportion", filename="SI1")
#PlotSimple(DS.SI, initial = [0.99, 0.01], param = [1.5, 1.0], legend = ["S", "I"], runs = 1000, xlabel = "Time", ylabel = "Proportion", filename="SI2")
#PlotSimple(DS.SIR_vital, initial = [0.9, 0.1, 0.0], param = [0.95, 1.0, 0.5], legend = ["S", "I", "R"], runs = 4000, xlabel = "Time", ylabel = "Proportion", filename="SIR_vital1")
#PlotSimple(DS.SIR_vital, initial = [0.9, 0.1, 0.0], param = [1.5, 1.0, 0.1], legend = ["S", "I", "R"], runs = 4000, xlabel = "Time", ylabel = "Proportion", filename="SIR_vital2")
#SIR_vitalRastaScan()

"""Ross"""
#PlotSimple(func = DS.Ross, initial = [0.1, 0.1], param = [0.05, 0.2, 2.0, 0.01, 0.5, 0.1], legend = ["$I_h$","$I_m$"], runs=100000,
# xlabel="Iterations", ylabel="Proportion infected", filename= "Ross1")

"""Simple function and plotting"""
#PlotSimple(func = DS.SimpleInfection, initial = [0.99, 0.01, 0.0, 0.0], param = [0.9, 1.0], legend = ["$S$", "$I$", "$I_R$", "$S_R$"], runs=10000, xlabel="Iteration", ylabel="Proportion")
#PlotSimple(func = DS.SimpleInfectionSteadyState, initial = [0.99, 0.01], param = [1.1, 1.0], legend = ["$I_R$", "$S_R$"], runs=10000, xlabel="Iteration", ylabel="Proportion", color = ['g','r'])

"""Replacement"""
#PlotSimple(DS.Replacement, initial = [0.99, 0.01, 0.0, 0.0], param = [0.95, 1.0, 0.01], legend = ["S","I","$I_R$", "$S_R$"], runs=10000,
#  xlabel="Iteration", ylabel="Proportion", filename="replacement_deterministic_0_01")
#PlotSimple(DS.Replacement, initial = [0.99, 0.01, 0.0, 0.0], param = [0.95, 1.0, 0.1], legend = ["S","I","$I_R$", "$S_R$"], runs=10000,
# xlabel="Iteration", ylabel="Proportion", filename="replacement_deterministic_0_1")
#ReplacementParameterRasta(filename="replacement_deterministic_gamma")
#LF.Latexify(fig_width=full_width*0.8)
ReplacementRastaScan()




# a, b, m, r, c, \mu 

"""Test"""
#RK.TestRungeKutta()
#q = RK.RungeKutta(initialConditions = np.array([0.99, 0.01, 0.0, 0.0]), equation = DS.SIRPlus, param = np.array([2.1, 0.0, 0.0, 1.0, 2.1, 2.0]), dt = 0.001)
#q.Run(75000)
#q.PlotTimePlot()
#plt.legend(["S","I","R","R_I"])
#plt.show()

plt.show()
print("Congrats! All done!")