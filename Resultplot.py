import matplotlib.pyplot as plt
import numpy as np
benchmarks = ['Complexity <= 40', '40 < Complexity <= 100', '100 < Complexity <= 500', 'Complexity > 500', 'lrb1', 'lrb2', 'lrb3', 'lrb4', 'lrb5']

# set width of bar
barWidth = 0.08
fig = plt.subplots(figsize=(30, 8))

# set height of bar
Dijkstra = [0.48, 0.43, 0.435, 0.37, 0.4, 0.6, 0.4, 0.8, 0.6]
Astar = [0.445, 0.43, 0.43, 0.365, 0.4, 0.6, 0.4, 0.6, 0.4]
VeSpA10 = [0.98, 0.92, 0.78, 0.835, 1.0, 0.4, 0.4, 0.8, 0.6]
VeSpA50 = [1.0, 1.0, 0.955, 0.98, 1.0, 1.0, 1.0, 1.0, 1.0]
VeSpA100 = [1.0, 1.0, 1.0, 0.995, 1.0, 1.0, 1.0, 1.0, 1.0]

# Set position of bar on X axis
c2 = np.arange(len(Dijkstra))
c3 = [x + barWidth for x in c2]
c4 = [x + barWidth for x in c3]
c5 = [x + barWidth for x in c4]
c6 = [x + barWidth for x in c5]

# Make the plot
# plt.bar(c1, Naive, color='#f1d77e', width=barWidth,
#         edgecolor='grey', label='Naive')
plt.bar(c2, Dijkstra, color='#9394e7', width=barWidth, edgecolor='#f1d77e', label='Dijkstra')
plt.bar(c3, Astar, color='#ffbe7a', width=barWidth, edgecolor='#f1d77e', label='Astar')
plt.bar(c4, VeSpA10, color='#82b0d2', width=barWidth, edgecolor='#f1d77e', label='VeSpA I=2')
plt.bar(c5, VeSpA50, color='#beb8dc', width=barWidth, edgecolor='#f1d77e', label='VeSpA I=20')
plt.bar(c6, VeSpA100, color='#fa7f6f', width=barWidth, edgecolor='#f1d77e', label='VeSpA I=200')

# Adding Xticks
plt.xlabel('Benchmarks', fontweight='bold', fontsize=20)
plt.ylabel('Success Rate', fontweight='bold', fontsize=20)
plt.xticks([r + 3 * barWidth for r in range(len(Astar))],
           benchmarks)

plt.legend()
outputpath = f"TestCaseFiles/SuccessRateCompare.png"
plt.savefig(outputpath)
