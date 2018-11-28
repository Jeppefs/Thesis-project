import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import malaria_statistics as MS
from Latexifier import LatexifierFunctions as LF

def getSwitchTime(pairs, strainCounter):
    strainMean = np.mean(np.mean(strainCounter, axis=1)) 
    N_strains_in_pairs = len(pairs[0])
    lower_threshold = strainMean / 10
    upper_threshold = strainMean * 1.25
    data_length = len(strainCounter)

    state = -1 # Can be -1, 0 or 1. 0 if pair 0 is lower, 1 if pair 1 is lower, and -1 if neither is. 
    state_counter = np.array([0, 0, 0])

    start = []
    end = []

    time_adjustment = 0.1

    for i in range(data_length - 2):
        
        # If we currently are in a merged state
        if state is -1:
            state_counter[0] += 1
            if np.mean(strainCounter[i, pairs[0]])  < lower_threshold and np.mean(strainCounter[i, pairs[1]]) > upper_threshold:
                #print(i*time_adjustment, state)
                start.append(i*time_adjustment)
                state = 0
            if np.mean(strainCounter[i, pairs[1]]) < lower_threshold and np.mean(strainCounter[i, pairs[0]]) > upper_threshold:
                #print(i*time_adjustment, state)
                start.append(i*time_adjustment)
                state = 1
        # If we currently are in a state where pair 1 is dominating
        elif state == 0:
            state_counter[1] += 1
            # Shoud be true a bit into the future to avoid spikes
            if np.mean(strainCounter[i, pairs[0]]) > upper_threshold and np.mean(strainCounter[i+2, pairs[0]]) > upper_threshold: 
                #print(i*time_adjustment, state)
                end.append(i*time_adjustment)
                state = -1
        # If we currently are in a state where pair0 is dominating
        elif state == 1:
            state_counter[2] += 1
            if np.mean(strainCounter[i, pairs[1]]) > upper_threshold and np.mean(strainCounter[i+2, pairs[1]]) > upper_threshold:
                #print(i*time_adjustment, state)
                end.append(i*time_adjustment)
                state = -1
    
    
    # If it never ended or started, simply make the switching time 2000.
    if len(end) == 0 or len(start) == 0:
        switch_time = data_length / 10
    # Remove last element of the end list, if there never was an end to switching.
    elif len(start) > len(end):
        start.pop()
        if len(start) != len(end):
            print("Start and end not equal!", start, end)
            start.pop(-1)
            #plt.plot(np.arange(data_length), strainCounter)
            #plt.show()
        if len(start) == 0:
            switch_time = data_length / 10 
        else:
            switch_time = np.array(end) - np.array(start)
    else:
        if len(start) != len(end):
            print("Start and end not equal!", start, end)
        switch_time = np.array(end) - np.array(start)
    #print(start, end)
    print(state_counter[0]/(sum(state_counter)))
    return switch_time, state_counter[0]/(sum(state_counter))

def getAllSwitchingTimes(name, strain_name, pairs):
    q = MS.MalariaStatistics(name)

    #infection_rates = [0.47, 0.48] 
    infection_rates = q.parameters["InfectionSpeed"].unique()

    switching_times_means = []
    switching_times_errors = []
    time_in_shared_mean = []

    for infection_rate in infection_rates:
        switch_time = np.array([])
        time_in_shared = np.array([])
        for current_repeat in range(q.settings["Repeat"][0]): 
            q.timelineIndex = [np.where( (q.parameters["InfectionSpeed"] == infection_rate) & (q.parameters["SpecificStrains"] == strain_name))[0][0] + 1, current_repeat + 1]
            q.ImportTimeline()
            q.ImportStrainCounter()
            switch_timeTemp, time_in_sharedTemp = getSwitchTime(pairs, q.strainCounter)
            switch_time = np.append(switch_time, switch_timeTemp)
            time_in_shared = np.append(time_in_shared, time_in_sharedTemp)

            #print(switch_time)
            #fig, ax = plt.subplots()
            #q.PlotStrainCounter(ax, skip = 10)

        switch_time_mean = np.mean(switch_time)
        switch_time_variance = np.var(switch_time)

        time_in_shared_mean = np.append(time_in_shared_mean, np.mean(time_in_shared))

        switching_times_means.append(switch_time_mean)
        switching_times_errors.append(np.sqrt(switch_time_variance/len(switch_time)))

        print(infection_rate, switch_time)
        print(infection_rate, "mean", switch_time_mean)
        print(infection_rate, "error:", np.sqrt(switch_time_variance/len(switch_time)))

    return switching_times_means, switching_times_errors, infection_rates, time_in_shared_mean

switching_times_means, switching_times_errors, infection_rates, time_in_shared = getAllSwitchingTimes("crossSwitchingTime", "cross", [[0,2], [1,3]])
switching_times_means_big, switching_times_errors_big, infection_rates_big, time_in_shared_big = getAllSwitchingTimes("crossSwitchingTime", "crossBig", [[0,2,4], [1,3,5]])

plt.style.use("seaborn")
LF.Latexify(fig_width = 6.19893, label_size=[1.0, 1.0])
matplotlib.rc('font',**{'family':'serif', 'serif':['Computer Modern Roman']})
matplotlib.rc('text', usetex=True)

fig, ax = plt.subplots()
ax.errorbar(infection_rates, switching_times_means, switching_times_errors, fmt='-o', markersize=5, linewidth=1.0, elinewidth=0.75, capssize=1.0, zorder=1)
ax.errorbar(infection_rates_big, switching_times_means_big, switching_times_errors_big, fmt='-o', markersize=5, linewidth=1.0, elinewidth=0.75, capsize=1.0, zorder=1)

ax.set_xticks([0.4, 0.42, 0.44, 0.46, 0.48, 0.5])
ax.legend(["Cross", "Cross big"])
ax.set_xlabel(r"$\alpha$")
ax.set_ylabel("Switching time (gen)")
fig.tight_layout(pad=0.1)

fileName = "switchingTime"
figName = fileName + ".pdf"
fig.savefig(figName + "", format="pdf")

fig, ax = plt.subplots()
ax.plot(infection_rates, time_in_shared, '-o', markersize=5, linewidth=1.0, zorder=1)
ax.plot(infection_rates_big, time_in_shared_big, '-o', markersize=5, linewidth=1.0, zorder=1)

ax.set_xticks([0.4, 0.42, 0.44, 0.46, 0.48, 0.5])
ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.legend(["Cross", "Cross big"])
ax.set_xlabel(r"$\alpha$")
ax.set_ylabel("Proportion time")
fig.tight_layout(pad=0.1)

fileName = "sharedState"
figName = fileName + ".pdf"
fig.savefig(figName + "", format="pdf")

print(time_in_shared, time_in_shared_big)

plt.show()