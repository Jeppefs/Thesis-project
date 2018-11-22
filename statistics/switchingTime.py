import numpy as np
import malaria_statistics as MS

def getSwitchTime(pairs, strainCounter):
    strainMean = np.mean(np.mean(strainCounter, axis=1)) 
    N_strains_in_pairs = len(pairs[0])
    lower_threshold = strainMean / 4
    upper_threshold = strainMean
    data_length = len(strainCounter)

    state = -1 # Can be -1, 0 or 1. 0 if pair 0 is lower, 1 if pair 1 is lower, and -1 if neither is. 

    for i in range(data_length):

        if state is -1:
            if np.mean(q.strainCounter[i, pairs[0]])  < lower_threshold:
                print(i/10, state)
                state = 0
            if np.mean(q.strainCounter[i, pairs[1]]) < lower_threshold:
                print(i/10, state)
                state = 1
        elif state == 0:
            if np.mean(q.strainCounter[i, pairs[0]])> upper_threshold:
                print(i/10, state)
                state = -1
        elif state == 1:
            if np.mean(q.strainCounter[i, pairs[1]]) > upper_threshold:
                print(i/10, state)
                state = -1
    
    return switch_time

q = MS.MalariaStatistics("CrossNonCross")

q.timelineIndex = [np.where( (q.parameters["InfectionSpeed"] == 0.45) & (q.parameters["SpecificStrains"] == "cross"))[0][0] + 1, 1]
q.ImportTimeline()
q.ImportStrainCounter()

pairs = [[0, 2], [1, 3]]


print(state)