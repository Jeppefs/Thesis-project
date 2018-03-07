import numpy as np
import matplotlib.pyplot as plt

testData = np.loadtxt("data/test.txt")
pop = 10000

plt.figure()
plt.plot(testData / pop)
plt.xlabel("Run")
plt.ylabel("Infected")
plt.yticks(np.arange(0,1.01,0.1))
plt.show()

