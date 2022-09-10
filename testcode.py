import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os


path = f"TestCaseFiles/Constraint_b1.csv"
if os.path.isfile(path):
    df = pd.read_csv(path, index_col=0, header=None).squeeze("columns").to_dict()
    constriant = []
    for v in df.values():
        constriant.append(eval(v))
    dictionary = dict(zip(df.keys(), constriant))
    print(dictionary)

