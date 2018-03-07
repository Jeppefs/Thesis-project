import numpy as np
import matplotlib.pyplot as plt
import glob as glob

testData = np.loadtxt("data/test.txt")
pop = 10000

plt.figure()
plt.plot(testData / pop)
plt.xlabel("Run")
plt.ylabel("Infected")
#plt.yticks(np.arange(0, max(), 0.1))
plt.grid()
figName = "plot" + str(len(glob.glob("/plots/*"))) + ".png"
plt.savefig("plots/"+figName)

plt.show()

