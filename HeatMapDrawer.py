import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from altair import *


path1 = f"TestCaseFiles/DataCollector/heatmapdata_erC.csv"
path2 = f"TestCaseFiles/DataCollector/heatmapdata_tC.csv"
df = pd.read_csv(path1, index_col=0)

# cm = plt.cm.get_cmap("YlGnBu")
# x0 = list(df.columns)
# y0 = list(df.index)
# x = []
# y = []
# for xx in x0:
#     x.append(int(xx))
#
# lenx = len(x)
# x = x * len(y0)
# for yy in y0:
#     for i in range(lenx):
#         y.append(yy)
#
# z = []
# for v in df.values:
#     z.extend(v)
# plt.figure(figsize=(20, 10))
# sc = plt.scatter(x, y, c=z, cmap=cm)
# plt.colorbar(sc)
# outputpath = f"TestCaseFiles/DataCollector/heatmap_erC_scatter.png"
# plt.savefig(outputpath)

df = df.iloc[::-1]
f, ax = plt.subplots(figsize=(12, 15))
ax = sns.heatmap(df, cmap="YlGnBu_r", cbar_kws={'label': 'Error Rate'})
# ax = sns.heatmap(df, cmap="YlGnBu_r", vmax=1000, cbar_kws={'label': 'Avg. Run Time'})
# ax.set_title('Heatmap of the error rate between Complexity / Constraint Number and Super Parameter I', fontsize=20)
ax.set_xlabel('Super Parameter: I', fontsize=16)
ax.set_ylabel('Complexity / Constraint Number', fontsize=16)
# plt.show()
# ax.set(xlabel='Super Parameter: I', ylabel='Avg. Constraint Number')
outputpath1 = f"TestCaseFiles/DataCollector/heatmap_erC.png"
outputpath2 = f"TestCaseFiles/DataCollector/heatmap_tC.png"
# outputpath3 = f"TestCaseFiles/DataCollector/heatmap_erCtr.png"
# outputpath4 = f"TestCaseFiles/DataCollector/heatmap_tCtr.png"
plt.savefig(outputpath1)
