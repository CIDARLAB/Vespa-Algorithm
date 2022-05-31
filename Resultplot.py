import matplotlib.pyplot as plt
import numpy as np
benchmarks = ['Complexity <= 40', '40 < Complexity <= 100', '100 < Complexity <= 500', 'Complexity > 500', 'lrb1', 'lrb2', 'lrb3', 'lrb4']
rate = [0.465, 0.425, 0.425, 0.39, 0.4, 0.6, 0.4, 0.8]

# set width of bar
barWidth = 0.1
fig = plt.subplots(figsize=(25, 8))

# set height of bar
Naive = [0.465, 0.425, 0.425, 0.39, 0.4, 0.6, 0.4, 0.8]
Dijkstra = [0.465, 0.425, 0.425, 0.39, 0.4, 0.6, 0.4, 0.8]
Astar = [0.465, 0.425, 0.425, 0.39, 0.4, 0.6, 0.4, 0.8]
VeSpA10 = [0.99, 0.975, 0.865, 0.88, 1, 1, 0.6, 1]
VeSpA50 = [1, 1, 0.97, 0.95, 1, 1, 1, 1]
VeSpA100 = [1, 1, 0.98, 0.975, 1, 1, 1, 1]

# Set position of bar on X axis
c1 = np.arange(len(Naive))
c2 = [x + barWidth for x in c1]
c3 = [x + barWidth for x in c2]
c4 = [x + barWidth for x in c3]
c5 = [x + barWidth for x in c4]
c6 = [x + barWidth for x in c5]

# Make the plot
plt.bar(c1, Naive, color='#f1d77e', width=barWidth,
        edgecolor='grey', label='Naive')
plt.bar(c2, Dijkstra, color='#b1ce46', width=barWidth,
        edgecolor='grey', label='Dijkstra')
plt.bar(c3, Astar, color='#63e398', width=barWidth,
        edgecolor='grey', label='Astar')
plt.bar(c4, VeSpA10, color='#9394e7', width=barWidth,
        edgecolor='grey', label='VeSpA10')
plt.bar(c5, VeSpA50, color='#f27970', width=barWidth,
        edgecolor='grey', label='VeSpA50')
plt.bar(c6, VeSpA100, color='#c82423', width=barWidth,
        edgecolor='grey', label='VeSpA100')

# Adding Xticks
plt.xlabel('Benchmarks', fontweight='bold', fontsize=20)
plt.ylabel('Success Rate', fontweight='bold', fontsize=20)
plt.xticks([r + 3 * barWidth for r in range(len(Astar))],
           benchmarks)

plt.legend()
outputpath = f"TestCaseFiles/SuccessRateCompare.png"
plt.savefig(outputpath)
