import matplotlib.pyplot as plt
import numpy as np
benchmarks = ['Complexity <= 40', '40 < Complexity <= 100', '100 < Complexity <= 500', 'Complexity > 500', 'lrb1', 'lrb2', 'lrb3', 'lrb4', 'lrb5']

# set width of bar
barWidth = 0.08
gapWidth = 0.1
fig = plt.subplots(figsize=(32, 8))

# set height of bar
Dijkstra = [0.48, 0.445, 0.355, 0.345, 0.4, 0.6, 0.4, 0.8, 0.4]
Astar = [0.46, 0.44, 0.35, 0.34, 0.4, 0.6, 0.4, 0.4, 0.3]
VeSpA2 = [0.975, 0.92, 0.76, 0.815, 0.4, 0.4, 0.0, 0.4, 0.5]
VeSpA20 = [1.0, 0.99, 0.96, 0.985, 1.0, 1.0, 0.4, 1.0, 0.8]
VeSpA200 = [1.0, 1.0, 0.995, 0.995, 1.0, 1.0, 1.0, 1.0, 1.0]

# Set position of bar on X axis
c2 = np.arange(len(Dijkstra))
c3 = [x + barWidth for x in c2]
c4 = [x + barWidth for x in c3]
c5 = [x + barWidth for x in c4]
c6 = [x + barWidth for x in c5]

# Make the plot
# plt.bar(c1, Naive, color='#f1d77e', width=barWidth,
#         edgecolor='grey', label='Naive')
plt.bar(c2, Dijkstra, color='#9394e7', width=barWidth, label='Dijkstra')
plt.bar(c3, Astar, color='#ffbe7a', width=barWidth,  label='Astar')
plt.bar(c4, VeSpA2, color='#82b0d2', width=barWidth, label='VeSpA I=2')
plt.bar(c5, VeSpA20, color='#fa7f6f', width=barWidth, label='VeSpA I=20')
plt.bar(c6, VeSpA200, color='#beb8dc', width=barWidth, label='VeSpA I=200')

# Adding Xticks
plt.xlabel('Benchmarks', fontweight='bold', fontsize=20)
plt.ylabel('Success Rate', fontweight='bold', fontsize=20)
plt.xticks([r + 3 * barWidth for r in range(len(Astar))],
           benchmarks)

plt.legend()
outputpath = f"TestCaseFiles/SuccessRateCompare.png"
plt.savefig(outputpath)
