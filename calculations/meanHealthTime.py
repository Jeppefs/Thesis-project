import numpy as np

# This script calculates the mean time it takes for a host to become healthy given the antigen size and antibodies he has that are features in the antigen.

def CalcProbabilities(features, antibodies):
    maxLength = features + 1
    p = np.zeros(maxLength)
    for antibody in range(0, maxLength):
        temp = 0
        if antibody != 0: 
            for j in range(0, antibody):
                if j == 0:
                    temp = 1
                else:
                    temp = temp * ( 1-(j/features))
        p[antibody] = (antibody/features) * temp
    if np.sum(p) != 1:
        print("WARNING! PROBABILITY DOES NOT SUM TO ONE!")
    mask = np.ones(maxLength, dtype=bool)
    mask[0:antibodies] = False
    p = p[mask]
    p = p / np.sum(p)
    return p

features = 4
antibodies = 3
p = CalcProbabilities(features, antibodies)

betas = np.arange(1,features-antibodies+2)
print(p, np.sum(p*betas))
