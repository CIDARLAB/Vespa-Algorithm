import os
from statistics import mean
import numpy as np
import pandas as pd
from csv import reader

pp = []
path = f"TestCaseFiles/csv_5_25_125_combined/resulttable.csv"
with open(path, 'r') as csv_file:
    df = reader(csv_file, delimiter='\t')

name = ["true positive", "false negative", "false positive", "true negative", "accuracy", "max time", "mean time", "avg time"]
flag = 1
for c in df:
    if len(c) < 2:
        continue
    index = name.index(c[0])
    c_new = list(map(int, c[1:]))
    print(c_new[0])

    f = open("TestCaseFiles/csv_5_25_125_combined/resulttable.txt", "a")
    f.write()
    f.close()