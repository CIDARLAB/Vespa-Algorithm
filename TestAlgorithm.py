# User Requirement for all graphs: f1 to f2 (check)
# ******
# Constraint for all graphs: (Sunday)
# 1. Randomly choose a valve or other control component always be closed;
# 2. Or two valve or other control component cannot be opened together

from ConstraintFunctions import findallConnectedNodes
from ConstraintMaker import createRandomConstraint
import AlgorithmComparison
import random
from collections import Counter
import networkx as nx
import os
import numpy as np
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


def fp_flag(a, b):
    # true positive
    if a == 1 and b == 1:
        return 1
    # false positive
    if a == 1 and b == 0:
        return 0
    # true negative for VeSpA, becasue it scaned all the possible graphs
    if a == 0:
        return 2


def checkandappend(nodeslist, b):
    repeatflag = 0
    for n in nodeslist:
        if Counter(n) == Counter(b):
            repeatflag = 1
            break
    if repeatflag == 0:
        nodeslist.append(b)
    return nodeslist


def VeSpA_checker(t4, l4, flag):
    if l4 == -2 or flag == -1:
        t4 = 2
    elif flag == 1:
        t4 = 23
    else:
        t4 = fp_flag(l4, t4)
    return t4, l4


def calculate_false_pos_rate(p1, p2, p3, p4, p5, p6, cl, c1, c2, c3, c4, c5, c6, g_c, flag10, flag50, flag):
    # l means the result of predict value, t means true value in the beginning and fp flag in the end.
    l1, l2, l3, l4, l5, l6, t1, t2, t3, t4, t5, t6 = 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
    if p1 == -1:
        l1 = 0
    if p2 == -1:
        l2 = 0
    if p3 == -1:
        l3 = 0
    if p4 == -1:
        l4 = 0
    if p5 == -1:
        l5 = 0
    if p6 == -1:
        l6 = 0
    nodeslist = []
    for c in cl:
        if c[0] == 1:
            nodes = findallConnectedNodes([c[1]], g_c.edges())
            for n in nodes:
                if n in c1:
                    t1 = 0
                if n in c2:
                    t2 = 0
                if n in c3:
                    t3 = 0
                if n in c4:
                    t4 = 0
                if n in c5:
                    t5 = 0
                if n in c6:
                    t6 = 0
            nodeslist = checkandappend(nodeslist, nodes)
        elif c[0] == 2:
            nodes1 = findallConnectedNodes([c[1]], g_c.edges())
            nodes2 = findallConnectedNodes([c[2]], g_c.edges())
            for n in nodes1:
                for nn in nodes2:
                    if n in c1 and nn in c1:
                        t1 = 0
                    if n in c2 and nn in c2:
                        t2 = 0
                    if n in c3 and nn in c3:
                        t3 = 0
                    if n in c4 and nn in c4:
                        t4 = 0
                    if n in c5 and nn in c5:
                        t5 = 0
                    if n in c6 and nn in c6:
                        t6 = 0
            nodeslist = checkandappend(nodeslist, nodes1)
            nodeslist = checkandappend(nodeslist, nodes2)
    # true positive = 1, false positive = 0, true negative= = 2, false negative = 3
    t1 = fp_flag(l1, t1)
    t2 = fp_flag(l2, t2)
    t3 = fp_flag(l3, t3)
    t4, l4 = VeSpA_checker(t4, l4, flag10)
    t5, l5 = VeSpA_checker(t5, l5, flag50)
    t6, l6 = VeSpA_checker(t6, l6, flag)
    # other algorithm can find a path without breaking the constraint, that means VeSpA is false negative
    if t1 == 1 or t2 == 1 or t3 == 1:
        if t4 in [23, 2]:
            t4 = 3
        if t5 in [23, 2]:
            t5 = 3
        if t6 in [23, 2]:
            t6 = 3
    return l1, l2, l3, l4, l5, l6, t1, t2, t3, t4, t5, t6, nodeslist


pos = {}
if __name__ == '__main__':
    # Section loop
    Result_list_metric = ["User Requirement", "Naive estimate", "Dijkstra estimate", "A* estimate", "VeSpA 10 estimate", "VeSpA 50 estimate",
                          "VeSpA estimate", "Naive success", "Dijkstra success", "A* success", "VeSpA 10 success", "VeSpA 50 success", "VeSpA success",
                          "Constraint List", "Naive control List", "Dijkstra control list", "A star control list", "VeSpA 10 control list",
                          "VeSpA 50 control list", "VeSpA control list", "ConstraintNodesGroup", "Naive path", "Dijkstra path", "A* path",
                          "VeSpA 10 path", "VeSpA 50 path", "VeSpA path", "Naive path length", "Dijkstra path length", "A* path length",
                          "VeSpA 10 path length", "VeSpA 50 path length", "VeSpA path length", "Naive runtime", "Dijkstra runtime", "A* runtime",
                          "VeSpA 10 runtime", "VeSpA 50 runtime", "VeSpA runtime"]
    Result_list_cases = []
    column = []
    for i in range(1, 5):
        Result_list_section = []
        path = f"RandomCaseFiles/Section_{i}"
        # Build a dictionary saved all edge info file names as value, keys are the nodes info
        AllDirInOneSection = getfileList(path)
        column = []
        ColumnDetail = []
        node_num = 0
        constraint_path = f"TestCaseFiles/Constraint_b{i}.csv"
        ConstraintInfoAll = {}
        if os.path.isfile(constraint_path):
            df = pd.read_csv(constraint_path, index_col=0, header=None).squeeze("columns").to_dict()
            constriant = []
            for v in df.values():
                constriant.append(eval(v))
            ConstraintInfoAll = dict(zip(df.keys(), constriant))
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
                column.append(f"Sec{i}|{NodeInfo[:index]}|{GraphListInfo[j][:5]}")
                ColumnDetail.append(f"Sec{i}|{NodeInfo[:index1]}|{GraphListInfo[j][:5]}_{GraphListInfo[j][6:index2]}")
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
                if VandCOlength < 10:
                    ConstraintNum = random.randint(1, VandCOlength)
                else:
                    ConstraintNum = random.randint(1, 10)

                if len(ConstraintInfoAll) == 0:
                    ConstraintList = ConstraintInfoAll[column[-1]]
                else:
                    ConstraintList = createRandomConstraint(ControlNodes, ConstraintNum, VandCOlength)

                # Create a dictionary shows the flow edge on which each valve and other control component locates
                VCO2FEdictionary, FE2VCOdictionary = locateValveAndCOonFE(valve_co_txt)

                # Algorithm comparison, set ur as ['f1', 'f2']
                ur = ['f1', 'f2']
                NaiveTime, NaivePath, NaiveLength = AlgorithmComparison.naive_search(g, ur)
                DijkstraTime, DijkstraPath, DijkstraLength = AlgorithmComparison.dijkstra_search(g, ur)
                AstarTime, AstarPath, AstarLength = AlgorithmComparison.astar_search(g, pos, ur)

                # Update the flow edge info after we get RandomConstraintList and use it in VeSpA_search
                g_VeSpA = g.copy()
                VeSpATime10, VeSpAPath10, VeSpALength10, flagFalseNegative10 = AlgorithmComparison.VeSpA_search(g_VeSpA, g_c, pos,
                                                                                                            ConstraintList, VCO2FEdictionary, ur, 10)
                g_VeSpA = g.copy()
                VeSpATime50, VeSpAPath50, VeSpALength50, flagFalseNegative50 = AlgorithmComparison.VeSpA_search(g_VeSpA, g_c, pos,
                                                                                                            ConstraintList, VCO2FEdictionary, ur, 50)
                g_VeSpA = g.copy()
                VeSpATime, VeSpAPath, VeSpALength, flagFalseNegative = AlgorithmComparison.VeSpA_search(g_VeSpA, g_c, pos,
                                                                                                    ConstraintList, VCO2FEdictionary, ur, 100)

                # Find all valves and other control components which may be involved giving the searched path
                NaiveVCOList = AlgorithmComparison.control_search(NaivePath, FE2VCOdictionary)
                DijkstraVCOList = AlgorithmComparison.control_search(DijkstraPath, FE2VCOdictionary)
                AstarVCOList = AlgorithmComparison.control_search(AstarPath, FE2VCOdictionary)
                VeSpAVCOList10 = AlgorithmComparison.control_search(VeSpAPath10, FE2VCOdictionary)
                VeSpAVCOList50 = AlgorithmComparison.control_search(VeSpAPath50, FE2VCOdictionary)
                VeSpAVCOList = AlgorithmComparison.control_search(VeSpAPath, FE2VCOdictionary)

                # Find all control edges and control ports being searched in the path
                NaiveControlNodeList, NaiveControlEdgeList = AlgorithmComparison.findall_control_path(NaiveVCOList, g_c)
                DijkstraControlNodeList, DijkstraControlEdgeList = AlgorithmComparison.findall_control_path(DijkstraVCOList, g_c)
                AstarControlNodeList, AstarControlEdgeList = AlgorithmComparison.findall_control_path(AstarVCOList, g_c)
                VeSpAControlNodeList10, VeSpAControlEdgeList10 = AlgorithmComparison.findall_control_path(VeSpAVCOList10, g_c)
                VeSpAControlNodeList50, VeSpAControlEdgeList50 = AlgorithmComparison.findall_control_path(VeSpAVCOList50, g_c)
                VeSpAControlNodeList, VeSpAControlEdgeList = AlgorithmComparison.findall_control_path(VeSpAVCOList, g_c)

                # Calculate the false positive rate for each algorithm
                Nr, Dr, Ar, Br1, Br2, Br3, t1, t2, t3, t4, t5, t6, nodeslist = calculate_false_pos_rate(NaiveLength, DijkstraLength, AstarLength,
                                                                                                        VeSpALength10, VeSpALength50, VeSpALength,
                                                                                                        ConstraintList, NaiveControlNodeList,
                                                                                                        DijkstraControlNodeList, AstarControlNodeList,
                                                                                                        VeSpAControlNodeList10, VeSpAControlNodeList50,
                                                                                                        VeSpAControlNodeList, g_c, flagFalseNegative10,
                                                                                                        flagFalseNegative50, flagFalseNegative)

                l_currentcase = [ur, Nr, Dr, Ar, Br1, Br2, Br3, t1, t2, t3, t4, t5, t6, ConstraintList, NaiveControlNodeList,
                                 DijkstraControlNodeList, AstarControlNodeList, VeSpAControlNodeList10, VeSpAControlNodeList50, VeSpAControlNodeList,
                                 nodeslist, NaivePath, DijkstraPath, AstarPath, VeSpAPath10, VeSpAPath50, VeSpAPath, NaiveLength, DijkstraLength,
                                 AstarLength, VeSpALength10, VeSpALength50, VeSpALength, NaiveTime, DijkstraTime, AstarTime, VeSpATime10, VeSpATime50,
                                 VeSpATime]
                Result_list_section.append(l_currentcase)
                j += 3
                print()

        # NaiveFPR, DijkstraFPR, AstarFPR = calculate_false_pos_rate(Result_list_section) !!!!*****@!!!
        # Result_list_cases.extend(Result_list_section)

        outcsvpath = f"TestCaseFiles/csv_10_50_100_combined/benchmark-{i}.csv"
        dictionary = dict(zip(ColumnDetail, Result_list_section))
        with open(outcsvpath, 'w', newline='') as f:
            dataframe = pd.DataFrame.from_dict(dictionary, orient='index', columns=Result_list_metric)
            dataframe.to_csv(outcsvpath)
            print()
