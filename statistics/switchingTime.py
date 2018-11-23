import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import malaria_statistics as MS
from Latexifier import LatexifierFunctions as LF

def getSwitchTime(pairs, strainCounter):
    strainMean = np.mean(np.mean(strainCounter, axis=1)) 
    N_strains_in_pairs = len(pairs[0])
    lower_threshold = strainMean / 10
    upper_threshold = strainMean
    data_length = len(strainCounter)

    state = -1 # Can be -1, 0 or 1. 0 if pair 0 is lower, 1 if pair 1 is lower, and -1 if neither is. 

    start = []
    end = []

    time_adjustment = 0.1

    for i in range(data_length):

        if state is -1:
            if np.mean(strainCounter[i, pairs[0]])  < lower_threshold:
                #print(i*time_adjustment, state)
                start.append(i*time_adjustment)
                state = 0
            if np.mean(strainCounter[i, pairs[1]]) < lower_threshold:
                #print(i*time_adjustment, state)
                start.append(i*time_adjustment)
                state = 1
        elif state == 0:
            if np.mean(strainCounter[i, pairs[0]])> upper_threshold:
                #print(i*time_adjustment, state)
                end.append(i*time_adjustment)
                state = -1
        elif state == 1:
            if np.mean(strainCounter[i, pairs[1]]) > upper_threshold:
                #print(i*time_adjustment, state)
                end.append(i*time_adjustment)
                state = -1
    
    
    # If it never ended or started, simply make the switching time 2000.
    if len(end) == 0 or len(start) == 0:
        switch_time = 2000
    # Remove last element of the end list, if there never was an end to switching.
    elif len(start) > len(end):
        start.pop()
        if len(start) != len(end):
            print("Start and end not equal!", start, end)
            start.pop(-1)
            #plt.plot(np.arange(data_length), strainCounter)
            #plt.show()
        if len(start) == 0:
            switch_time = 2000
        switch_time = np.array(end) - np.array(start)
    else:
        if len(start) != len(end):
            print("Start and end not equal!", start, end)
        switch_time = np.array(end) - np.array(start)
    return switch_time

def getAllSwitchingTimes(name, strain_name, pairs):
    q = MS.MalariaStatistics(name)

    switching_times_means = []
    switching_times_errors = []

    for infection_rate in q.parameters["InfectionSpeed"].unique():
        switch_time = np.array([])
        for current_repeat in range(q.settings["Repeat"][0]): 
            q.timelineIndex = [np.where( (q.parameters["InfectionSpeed"] == infection_rate) & (q.parameters["SpecificStrains"] == strain_name))[0][0] + 1, current_repeat + 1]
            q.ImportTimeline()
            q.ImportStrainCounter()
            switch_time = np.append(switch_time, getSwitchTime(pairs, q.strainCounter))

            #print(switch_time)

        switch_time_mean = np.mean(switch_time)
        switch_time_variance = np.var(switch_time)

        print(infection_rate, switch_time)
        print(infection_rate, "mean", switch_time_mean)
        print(infection_rate, "error:", np.sqrt(switch_time_variance/q.settings["Repeat"][0]))
        
        switching_times_means.append(switch_time_mean)
        switching_times_errors.append(np.sqrt(switch_time_variance/q.settings["Repeat"][0]))

    return switching_times_means, switching_times_errors, q.parameters["InfectionSpeed"].unique()

switching_times_means, switching_times_errors, infection_rates = getAllSwitchingTimes("crossNonCross", "cross", [[0,2], [1,3]])
switching_times_means_big, switching_times_errors_big, infection_rates_big = getAllSwitchingTimes("crossBig", "crossBig", [[0,2,4], [1,3,5]])

plt.style.use("seaborn")
LF.Latexify(fig_width = 12.65076*0.6, label_size=[1.0, 1.0])
matplotlib.rc('font',**{'family':'serif', 'serif':['Computer Modern Roman']})
matplotlib.rc('text', usetex=True)

fig, ax = plt.subplots()
ax.errorbar(infection_rates[5:16], switching_times_means[5:16], switching_times_errors[5:16], fmt='-o', markersize=6, linewidth=1.0, elinewidth=0.5, zorder=1)
ax.errorbar(infection_rates_big[5:16], switching_times_means_big[5:16], switching_times_errors_big[5:16], fmt='-o', markersize=6, linewidth=1.0, elinewidth=0.5, zorder=1)

ax.legend(["Cross", "Cross big"])
ax.set_xlabel(r"$\alpha$")
ax.set_ylabel("Switching time (gen)")
fig.tight_layout(pad=0.1)

fileName = "switchingTime"
figName = fileName + ".pdf"
fig.savefig(figName + "", format="pdf")

plt.show()