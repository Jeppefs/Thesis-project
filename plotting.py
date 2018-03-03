import numpy as np
import matplotlib.pyplot as plt

testData = np.loadtxt("data/text10000.txt")

plt.figure()
plt.plot(testData)
plt.show()

