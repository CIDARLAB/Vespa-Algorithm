import os
from statistics import mean
import numpy as np
import pandas as pd
from csv import reader

pp = []
path = f"TestCaseFiles/csv_2_20_200_combined/resulttable.csv"
csv_file = open(path, 'r')
df = reader(csv_file, delimiter='\t')
f = open("TestCaseFiles/csv_2_20_200_combined/resultinfo.csv", "a")
name = ["true positive", "false negative", "false positive", "true negative", "accuracy", "max time", "mean time", "avg time"]
flag = 0
result_list = []
sr_list = []
list_element = []
for c in df:
    if len(c) < 2:
        if len(list_element) != 0:
            result_list.append(list_element)
            print(list_element[5])
            for ee in range(len(list_element[5])):
                f.write(f"{list_element[5][ee]};")
            f.write('\n')
            list_element = []
            flag = 1
        continue
    # index = name.index(c[0])
    c_new = list(map(float, c[1:]))
    list_element.append(c_new)

# reverse the matrix of list_element[4]
# sr_list = pd.DataFrame(sr_list)
# sr_list_r = sr_list.transpose()
# ee = sr_list_r.values.tolist()
# for e in ee:
#     print(e)
f.close()
