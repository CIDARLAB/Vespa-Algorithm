import os
from statistics import mean
import numpy as np
import pandas as pd

pp = []
for i in range(1, 5):
    path = f"TestCaseFiles/benchmark-{i}.csv"
    df = pd.read_csv(path)
    df_c = df["Constraint List"]
    p = []
    for c in df_c:
        if isinstance(c, str):
            countc = c.count('2,') + c.count('1,')
            p.append(countc)
    print(mean(p))
    pp.append(mean(p))
print(pp)
