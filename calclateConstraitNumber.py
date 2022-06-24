import os
from statistics import mean
import numpy as np
import pandas as pd

pp = []
for i in range(1, 2):
    # path = f"TestCaseFiles/lrb/Constraint_UR_lrb3.csv"
    path = "RandomCaseFiles/Constraint_b1.csv"
    df = pd.read_csv(path)
    df_c = df.values
    p = []
    for c in df_c:
        if isinstance(c[1], str):
            countc = c[1].count('2,') + c[1].count('1,')
            p.append(countc)
    print(mean(p))
    pp.append(mean(p))
print(pp)
