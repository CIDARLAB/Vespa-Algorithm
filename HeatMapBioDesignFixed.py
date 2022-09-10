# User Requirement for all graphs: f1 to f2 (check)
# ******
# Constraint for all graphs: (Sunday)
# 1. Randomly choose a valve or other control component always be closed;
# 2. Or two valve or other control component cannot be opened together

from ConstraintMaker import createRandomConstraint
from MetricsGenerator import calculate_false_pos
from AlgorithmComparison import VeSpA_search, control_search, netxsp_search, astar_search, findall_control_path
import random
import csv
import networkx as nx
import os
import pandas as pd
from networkx.drawing.nx_agraph import read_dot


def getfileList(targetfolderpath):
    Allfile = {}
    NodeList = os.listdir(targetfolderpath)
    for node in NodeList:
        new_path = targetfolderpath + "/" + str(node)
        edgelist = os.listdir(new_path)
        edgelist.sort()
        Allfile[node] = edgelist
    return Allfile


def buildFlowGraph(flow_graph_path):
    # Build flow layer graph g
    g = read_dot(flow_graph_path)
    g = g.to_undirected()
    for edge in g.edges:
        g[edge[0]][edge[1]]['weight'] = int(g.get_edge_data(edge[0], edge[1])['weight'])
    pos = nx.spring_layout(g)
    return g, pos


def locateValveAndCOonFE(vco_path):
    data = pd.read_csv(vco_path, header=None, sep=" ")
    VCOFlist = data.values.tolist()
    VCO2FEdictionary = {}
    FE2VCOdictionary = {}
    for VCO in VCOFlist:
        VCO2FEdictionary[VCO[0]] = VCO[1:]
        tup_temp = tuple(VCO[1:])
        if tup_temp in FE2VCOdictionary.keys():
            FE2VCOdictionary[tup_temp].append(VCO[0])
        else:
            FE2VCOdictionary[tup_temp] = [VCO[0]]
    # data structure of FE2VCOdictionary is like {('F1','F2'): ['V1', 'V2'], ('F1','F3'): ['V3']}
    return VCO2FEdictionary, FE2VCOdictionary


pos = {}
if __name__ == '__main__':
    # Section loop

    Result_list_metric = []
    a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800]
    for i in a:
        Result_list_metric.append(f"I={i} flag")
    for i in a:
        Result_list_metric.append(f"I={i} runtime")

    Result_list_cases = []
    for i in range(3, 4):
        Result_list_section = []
        path = f"RandomCaseFiles/Section_{i}"
        # Build a dictionary saved all edge info file names as value, keys are the nodes info
        AllDirInOneSection = getfileList(path)
        ColumnDetail = []
        node_num = 0
        constraint_path = f"RandomCaseFiles/Constraint_b{i}.csv"
        ConstraintInfoAll = {}
        ConstraintEmptyFlag = 0
        if os.path.isfile(constraint_path):
            df = pd.read_csv(constraint_path, index_col=0, header=None).squeeze("columns").to_dict()
            constriant = []
            for v in df.values():
                constriant.append(eval(v))
            ConstraintInfoAll = dict(zip(df.keys(), constriant))
            ConstraintEmptyFlag = 1

        # Nodes info loop
        for NodeInfo in AllDirInOneSection.keys():
            j = 0
            node_num += 1
            GraphListInfo = AllDirInOneSection[NodeInfo]
            # Graph info loop
            jUpperBound = len(AllDirInOneSection[NodeInfo])
            while j < jUpperBound:
                print(f"Sec{i}, Node{node_num}, Edge{int(j/3)+1}")
                index = NodeInfo.index('_')
                index1 = NodeInfo.find('_', index+1)
                index2 = GraphListInfo[j].find('_')
                index0 = GraphListInfo[j].index('|')
                ColumnDetail.append(f"Sec{i}|{NodeInfo[:index1]}|{GraphListInfo[j][:index0]}_{GraphListInfo[j][index0+1:index2]}")
                print(ColumnDetail[-1])
                # remark = GraphListInfo[j][6]
                control_graph_path = f"{path}/{NodeInfo}/{GraphListInfo[j]}"
                flow_graph_path = f"{path}/{NodeInfo}/{GraphListInfo[j + 1]}"
                valve_co_txt = f"{path}/{NodeInfo}/{GraphListInfo[j + 2]}"
                # Build flow layer graph g
                g, pos = buildFlowGraph(flow_graph_path)

                # Create random constraints for each g_c -- control graph
                # Build control layer graph g_c
                g_c = read_dot(control_graph_path)
                g_c = g_c.to_undirected()
                ControlNodes = list(g_c.nodes())
                for edge in g_c.edges:
                    g_c[edge[0]][edge[1]]['weight'] = int(g_c.get_edge_data(edge[0], edge[1])['weight'])
                CPlength = 0
                for node in ControlNodes:
                    if node[0] == 'c' and node[1] != 'o':
                        CPlength += 1
                VandCOlength = len(ControlNodes) - CPlength

                # Constraint bound for each section: [1, 5, 10, 15]
                upboundconstraint = [1, 5, 10, 15]
                ConstraintNum = random.randint(upboundconstraint[i-1], upboundconstraint[i])

                # if no constraint list given, just generate a new one
                if ConstraintEmptyFlag != 0:
                    ConstraintList = ConstraintInfoAll[ColumnDetail[-1]]
                else:
                    ConstraintList = createRandomConstraint(ControlNodes, ConstraintNum, VandCOlength)
                ConstraintInfoAll[ColumnDetail[-1]] = ConstraintList
                # Create a dictionary shows the flow edge on which each valve and other control component locates
                VCO2FEdictionary, FE2VCOdictionary = locateValveAndCOonFE(valve_co_txt)

                # Algorithm comparison, set ur as ['f1', 'f2']
                ur = ['f1', 'f2']

                NetxSPTime, NetxSPPath, NetxSPLength = netxsp_search(g, ur)
                AstarTime, AstarPath, AstarLength = astar_search(g, pos, ur)
                NetxSPVCOList = control_search(NetxSPPath, FE2VCOdictionary)
                AstarVCOList = control_search(AstarPath, FE2VCOdictionary)
                NetxSPControlNodeList, NetxSPControlEdgeList = findall_control_path(NetxSPVCOList, g_c)
                AstarControlNodeList, AstarControlEdgeList = findall_control_path(AstarVCOList, g_c)
                PathLength = [NetxSPLength, AstarLength]
                CtrlNodeLists = [NetxSPControlNodeList, AstarControlNodeList]

                # Update the flow edge info after we get RandomConstraintList and use it in VeSpA_search
                VespaTime = []
                flagFN = []
                for ii in a:
                    g_VeSpA = g.copy()
                    VeSpATimeii, VeSpAPathii, VeSpALengthii, flag, _ = VeSpA_search(g_VeSpA, g_c, pos, ConstraintList, VCO2FEdictionary, ur, ii)
                    # Find all valves and other control components which may be involved giving the searched path
                    VeSpAVCOList = control_search(VeSpAPathii, FE2VCOdictionary)
                    VeSpAControlNodeList, VeSpAControlEdgeList = findall_control_path(VeSpAVCOList, g_c)

                    # add middle products into list
                    VespaTime.append(format(VeSpATimeii, '.5f'))
                    PathLength.append(VeSpALengthii)
                    flagFN.append(flag)
                    CtrlNodeLists.append(VeSpAControlNodeList)

                # Calculate the false positive for each algorithm
                l, t, nodeslist = calculate_false_pos(PathLength, ConstraintList, CtrlNodeLists, g_c, flagFN)
                l_currentcase = t[2:] + VespaTime
                Result_list_section.append(l_currentcase)
                j += 3
                print()
            f = open(constraint_path, 'w', newline='')
            z = csv.writer(f)
            for k, v in ConstraintInfoAll.items():
                z.writerow([k, v])
            f.close()

        outcsvpath = f"TestCaseFiles/DataCollector/benchmark-{i}.csv"
        dictionary = dict(zip(ColumnDetail, Result_list_section))
        with open(outcsvpath, 'w', newline='') as f:
            dataframe = pd.DataFrame.from_dict(dictionary, orient='index', columns=Result_list_metric)
            dataframe.to_csv(outcsvpath)
            print()
            f.close()
