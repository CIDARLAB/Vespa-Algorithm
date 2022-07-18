import os
from statistics import mean
import numpy as np
import pandas as pd

pp = []
for i in range(1, 5):
    # path = f"TestCaseFiles/lrb/URC/Constraint_UR_lrb{i}.csv"
    path = f"RandomCaseFiles/Constraint_b{i}.csv"
    df = pd.read_csv(path)
    df_c = df.values
    p = []
    for c in df_c:
        if isinstance(c[1], str):
            countc = c[1].count('2,') + c[1].count('1,')
            p.append(countc)
    print(mean(p))
    pp.append(round(mean(p), 2))
print(pp)
