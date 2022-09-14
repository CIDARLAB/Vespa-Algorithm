import os
from statistics import mean
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing

ranges = [1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,150,200,250,300,350,400,450,500,600,700,800]
pp = []
path = f"TestCaseFiles/DataCollector/heatmapdata.csv"
df = pd.read_csv(path, header=0, index_col=0)
df_c = df.values
p_min_indeces = []
for c in df_c:
    p = []
    for cc in c[:30]:
        p.append(cc)
    p_min = min(p)
    p_min_index = p.index(p_min)
    p_min_indeces.append(p_min_index)
    if p_min_index > 9:
        pp.append([ranges[p_min_index-1], ranges[p_min_index]])
    else:
        pp.append(ranges[p_min_index])
print(p_min_indeces)
print(pp)
folder_path = f"TestCaseFiles/DataCollector"
outpath = f"{folder_path}/I_best.csv"
with open(outpath, 'w') as f:
    for ii in pp:
        f.writelines(f"{ii}\n")

