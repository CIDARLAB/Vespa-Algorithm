import os
from statistics import mean

import numpy as np


def getfileList(targetfolderpath):
    names = []
    Allfile = {}
    # for dirpath in os.walk(targetfolderpath):
    #     i = 1
    # print(Allfile)
    NodeList = os.listdir(targetfolderpath)
    for node in NodeList:
        new_path = targetfolderpath + "/" + str(node)
        edgelist = os.listdir(new_path)
        edgelist.sort()
        Allfile[node] = edgelist
    return Allfile


node_num_all = []
edge_num_all = []
node_num_mean = []
edge_num_mean = []
for i in range(1, 5):
    node_num = []
    edge_num = []
    path = f"RandomCaseFiles/Section_{i}"
    AllFileInOneSection = getfileList(path)
    for NodeInfo in AllFileInOneSection.keys():
        j = 0
        GraphListInfo = AllFileInOneSection[NodeInfo]
        li = [i for i, x in enumerate(NodeInfo) if x == "_"]
        node_num.append(int(NodeInfo[li[0]+1: li[1]]))
        while j < len(AllFileInOneSection[NodeInfo]):
            control_graph_path = f"RandomCaseFiles/Section_{i}/{NodeInfo}/{GraphListInfo[j]}"
            flow_graph_path = f"RandomCaseFiles/Section_{i}/{NodeInfo}/{GraphListInfo[j+1]}"
            valve_txt = f"RandomCaseFiles/Section_{i}/{NodeInfo}/{GraphListInfo[j+2]}"

            index1 = GraphListInfo[j].index('|')
            index2 = GraphListInfo[j].index('_')
            edge_num.append(int(GraphListInfo[j][index1+1: index2]))
            j += 3
    print(node_num)
    print(edge_num)
    node_num_mean.append(mean(node_num))
    edge_num_mean.append(mean(edge_num))
    node_num_all.append(node_num)
    edge_num_all.append(edge_num)

folder_path = f"RandomCaseFiles/"
outpath = f"{folder_path}/nodeinfo.txt"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
with open(outpath, 'w') as f:
    for node_num_e in node_num_all:
        for ii in node_num_e:
            for j in range(8):
                f.writelines(f"{ii}\n")

outpath = f"{folder_path}/edgeinfo.txt"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
with open(outpath, 'w') as f:
    for edge_num_e in edge_num_all:
        for ii in edge_num_e:
            f.writelines(f"{ii}\n")
print()
print("Average Node number: ", node_num_all)
print("Average Edge number: ", edge_num_all)
