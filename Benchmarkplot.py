import matplotlib.pyplot as plt
import numpy as np
benchmarks = ['x<=40', '40<x<=100', '100<x<=500', 'x>500', 'lrb1', 'lrb2', 'lrb3', 'lrb4']
parameters = ['Number of Benchmarks', 'Avg. Node Number', 'Avg. Edge Number', 'Avg. Complexity', 'Avg. Constraint per Benchmark']
rate = [0.465, 0.425, 0.425, 0.39, 0.4, 0.6, 0.4, 0.8]

# set width of bar
barWidth = 0.1
fig = plt.subplots(figsize=(36, 12))

# set height of bar
b1 = [200, 200, 200, 200, 5, 5, 5, 5]
b2 = [11.24, 21.64, 75.16, 209.24, 47, 32, 62, 154]
b3 = [12.07, 25.54, 62.97, 232.04, 42, 23, 48, 197]
b4 = [34.55, 68.82, 213.29, 650.52, 136, 87, 172, 505]
b5 = [2.125, 3.835, 4.875, 5.34, 4.8, 3.8, 5.0, 5.4]
b = [b1, b2, b3, b4, b5]
# Set position of bar on X axis
c = np.arange(len(b1))
color = ['#f1d77e', '#b1ce46', '#63e398', '#9394e7', '#f27970']
for i in range(len(color)):
        # Make the plot
        plt.subplot(2,3,i+1)
        plt.bar(c, b[i], color=color[i], width=barWidth,
                edgecolor='grey', label=parameters[i])
        plt.xlabel(f"{parameters[i]}, x = 'Complexity'", fontweight='bold', fontsize=15)
        plt.ylabel('Value', fontweight='bold', fontsize=20)
        # plt.xticks([r + barWidth for r in range(len(b1))], benchmarks)
        plt.xticks(range(len(b1)), benchmarks)
        plt.legend()

outputpath = f"TestCaseFiles/BenchmarkDescription.png"
plt.savefig(outputpath)
plt.clf()

