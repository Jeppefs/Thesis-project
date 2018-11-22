import numpy as np
import malaria_statistics as MS

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
            if np.mean(q.strainCounter[i, pairs[0]])  < lower_threshold:
                #print(i*time_adjustment, state)
                start.append(i*time_adjustment)
                state = 0
            if np.mean(q.strainCounter[i, pairs[1]]) < lower_threshold:
                #print(i*time_adjustment, state)
                start.append(i*time_adjustment)
                state = 1
        elif state == 0:
            if np.mean(q.strainCounter[i, pairs[0]])> upper_threshold:
                #print(i*time_adjustment, state)
                end.append(i*time_adjustment)
                state = -1
        elif state == 1:
            if np.mean(q.strainCounter[i, pairs[1]]) > upper_threshold:
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
        if len(start) == 0:
            switch_time = 2000
        switch_time = np.array(end) - np.array(start)
    else:
        if len(start) != len(end):
            print("Start and end not equal!", start, end)
        switch_time = np.array(end) - np.array(start)
    return switch_time

q = MS.MalariaStatistics("CrossNonCross")

pairs = [[0, 2], [1, 3]]
switch_time = np.array([])

for current_repeat in range(q.settings["Repeat"][0]): 
    q.timelineIndex = [np.where( (q.parameters["InfectionSpeed"] == 0.45) & (q.parameters["SpecificStrains"] == "cross"))[0][0] + 1, current_repeat + 1]
    q.ImportTimeline()
    q.ImportStrainCounter()
    switch_time = np.append(switch_time, getSwitchTime(pairs, q.strainCounter))

    print(switch_time)

switch_time_mean = np.mean(switch_time)
switch_time_variance = np.var(switch_time)

print(switch_time_mean)
print(np.sqrt(switch_time_variance/q.settings["Repeat"][0]))