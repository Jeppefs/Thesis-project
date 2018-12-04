import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from Latexifier import LatexifierFunctions as LF 

def OptimalGamma(a):
    return (2*a)**(1/3) - 1

def GammaDeath(a):
    return a/2 + (a**(1/2)*(a + 4)**(1/2))/2 - 1
    #OR a/2 - (a**(1/2)*(a + 4)**(1/2))/2 - 1

alphas = np.arange(0.5,2.0,0.01)

sns.set_color_codes()
sns.set_palette(palette='deep')
p = sns.color_palette()
plt.style.use("seaborn")
LF.Latexify(fig_width = 6.19893, label_size = [1.0, 1.0])
matplotlib.rc('font',**{'family':'serif', 'serif':['Computer Modern Roman']})
matplotlib.rc('text', usetex=True)
matplotlib.rcParams.update({'axes.spines.left': False, 'axes.spines.bottom': False})

fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
ax1.plot(alphas, OptimalGamma(alphas))
ax2.plot(alphas, GammaDeath(alphas))
ax1.set_xlabel(r"$\alpha$")
ax1.set_ylabel(r"$\gamma$")
ax2.set_xlabel(r"$\alpha$")
ax2.set_ylabel(r"$\gamma$")
fig1.tight_layout(pad=0.1)
fig2.tight_layout(pad=0.1)
fig1.savefig("replacement_optimal.pdf", format="pdf")
fig2.savefig("replacement_death.pdf", format="pdf")

plt.show()