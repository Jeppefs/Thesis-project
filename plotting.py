import numpy as np
import matplotlib.pyplot as plt

testData = np.loadtxt("data/text12000.txt")

plt.figure()
plt.plot(testData)
plt.show()

