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
for i in range(1, 4):
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

complexity_all = []
for i in range(len(edge_num_all)):
    for count in range(len(edge_num_all[i])):
        comp = edge_num_all[i][count] + node_num_all[i][count//10] * 2
        complexity_all.append(comp)




# average edge and node number for each cluster
edge_num_avg = []
for ii in edge_num_all:
    edge_num_avg.append(mean(ii))

node_num_avg = []
for ii in node_num_all:
    node_num_avg.append(mean(ii))

print("Average Node number: ", node_num_mean)
print("Average Edge number: ", edge_num_mean)

complexity = []
for i in range(len(node_num_avg)):
    complexity.append(2*node_num_avg[i]+edge_num_avg[i])

print("Average Complexity: ", complexity)

outpath = f"{folder_path}/CompleixtyInfo.txt"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
with open(outpath, 'w') as f:
    for ii in complexity_all:
        f.writelines(f"{ii}\n")
