import numpy as np
import matplotlib.pyplot as plt

testData = np.loadtxt("data/test.txt")

plt.figure()
plt.plot(testData)
plt.show()