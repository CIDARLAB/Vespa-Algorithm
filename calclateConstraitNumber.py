import os
from statistics import mean
import numpy as np
import pandas as pd

# average constraint numbers of four benchmark sections
pp = []
# average every 10 constraints numbers and add the avg number into one list p_10
p_20 = []
for i in range(1, 4):
    # path = f"TestCaseFiles/lrb/URC/Constraint_UR_lrb{i}.csv"
    path = f"RandomCaseFiles/Constraint_b{i}.csv"
    df = pd.read_csv(path, header=None)
    df_c = df.values
    p = []
    for c in df_c:
        if isinstance(c[1], str):
            countc = c[1].count('2,') + c[1].count('1,')
            p.append(countc)
    count = 0
    a = []

    for pi in p:
        count += 1
        a.append(pi)
        if count == 20:
            p_20.append(mean(a))
            a = []
            count = 0
    pp.append(round(mean(p), 2))
    print(p)
print(p_20)
folder_path = f"RandomCaseFiles/"
outpath = f"{folder_path}/ConstraintInfo.csv"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
with open(outpath, 'w') as f:
    for ii in p_10:
        f.writelines(f"{ii}\n")