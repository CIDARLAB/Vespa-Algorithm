import os
from statistics import mean
import numpy as np
import pandas as pd

# average constraint numbers of four benchmark sections
pp = []

for i in range(3, 4):
    # path = f"TestCaseFiles/lrb/URC/Constraint_UR_lrb{i}.csv"
    path = f"RandomCaseFiles/Constraint_b{i}.csv"
    df = pd.read_csv(path, header=None)
    df_c = df.values
    p = []
    for c in df_c:
        if isinstance(c[1], str):
            countc = c[1].count('2,') + c[1].count('1,')
            countc2 = c[1].count('2,')
            p.append(countc2)
    pp.append(p)

folder_path = f"RandomCaseFiles/"
outpath = f"{folder_path}/ConstraintInfo.csv"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
with open(outpath, 'w') as f:
    for p in pp:
        for ii in p:
            f.writelines(f"{ii}\n")