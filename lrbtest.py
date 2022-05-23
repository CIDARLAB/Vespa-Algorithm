from ConstraintFunctions import findallConnectedNodes
from TestAlgorithm import getfileList, buildFlowGraph, locateValveAndCOonFE, fp_flag, checkandappend, calculate_false_pos_rate
import AlgorithmComparison
import random
from collections import Counter
import networkx as nx
import os
import numpy as np
import pandas as pd
from networkx.drawing.nx_agraph import read_dot


pos = {}
if __name__ == '__main__':
    # Section loop
    Result_list_metric = ["User Requirement", "Naive estimate", "Dijkstra estimate", "A* estimate", "BOCS estimate",
                          "Naive success", "Dijkstra success", "A* success", "BOCS success",
                          "Constraint List", "Naive control List", "Dijkstra control list", "A star control list", "BOCS control list",
                          "ControlNodesGroup", "Naive path", "Dijkstra path", "A* path", "BOCS path",
                          "Naive path length", "Dijkstra path length", "A* path length",
                          "BOCS path length", "Naive runtime", "Dijkstra runtime", "A* runtime", "BOCS runtime"]
    Result_list_cases = []
    column = []
    for i in range(1, 5):
        Result_list_section = []
        path = f"TestCaseFiles/lrb{i}"
        # Build a dictionary saved all edge info file names as value, keys are the nodes info
        AllDirInOneSection = getfileList(path)
        column = []
        node_num = 0
        constraint_path = f"TestCaseFiles/Constraint_b{i}.csv"
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
                column.append(f"Sec{i}|{NodeInfo[:index]}|{GraphListInfo[j][:5]}")
                # remark = GraphListInfo[j][6]
                control_graph_path = f"TestCaseFiles/Section_{i}/{NodeInfo}/{GraphListInfo[j]}"
                flow_graph_path = f"TestCaseFiles/Section_{i}/{NodeInfo}/{GraphListInfo[j + 1]}"
                valve_co_txt = f"TestCaseFiles/Section_{i}/{NodeInfo}/{GraphListInfo[j + 2]}"
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

                ConstraintList = ConstraintInfoAll[column[-1]]

                # Create a dictionary shows the flow edge on which each valve and other control component locates
                VCO2FEdictionary, FE2VCOdictionary = locateValveAndCOonFE(valve_co_txt)

                # Algorithm comparison
                NaiveTime, NaivePath, NaiveLength = AlgorithmComparison.naive_search(g)
                DijkstraTime, DijkstraPath, DijkstraLength = AlgorithmComparison.dijkstra_search(g)
                AstarTime, AstarPath, AstarLength = AlgorithmComparison.astar_search(g, pos)

                # Update the flow edge info after we get RandomConstraintList and use it in BOCS_search
                g_BOCS = g.copy()
                BOCSTime, BOCSPath, BOCSLength, flagFalseNegative = AlgorithmComparison.BOCS_search(g_BOCS, g_c, pos,
                                                                                ConstraintList, VCO2FEdictionary)

                # Find all valves and other control components which may be involved giving the searched path
                NaiveVCOList = AlgorithmComparison.control_search(NaivePath, FE2VCOdictionary)
                DijkstraVCOList = AlgorithmComparison.control_search(DijkstraPath, FE2VCOdictionary)
                AstarVCOList = AlgorithmComparison.control_search(AstarPath, FE2VCOdictionary)
                BOCSVCOList = AlgorithmComparison.control_search(BOCSPath, FE2VCOdictionary)

                # Find all control edges and control ports being searched in the path
                NaiveControlNodeList, NaiveControlEdgeList = AlgorithmComparison.findall_control_path(NaiveVCOList, g_c)
                DijkstraControlNodeList, DijkstraControlEdgeList = AlgorithmComparison.findall_control_path(DijkstraVCOList, g_c)
                AstarControlNodeList, AstarControlEdgeList = AlgorithmComparison.findall_control_path(AstarVCOList, g_c)
                BOCSControlNodeList, BOCSControlEdgeList = AlgorithmComparison.findall_control_path(BOCSVCOList, g_c)

                # Simulate control and flow layer pathways
                AlgorithmComparison.simulate(NodeInfo, NaiveTime, NaivePath, NaiveControlNodeList, DijkstraTime,
                                             DijkstraPath, DijkstraControlNodeList, AstarTime, AstarPath, AstarControlNodeList,
                                             BOCSTime, BOCSPath, BOCSControlNodeList, i, j, g, g_c, GraphListInfo)

                # Calculate the false positive rate for each algorithm
                Nr, Dr, Ar, Br, t1, t2, t3, t4, nodeslist = calculate_false_pos_rate(NaiveLength, DijkstraLength, AstarLength, BOCSLength,
                ConstraintList, NaiveControlNodeList, DijkstraControlNodeList, AstarControlNodeList, BOCSControlNodeList, g_c,
                                                                                     flagFalseNegative)

                l_currentcase = ["f1 -> f2", Nr, Dr, Ar, Br, t1, t2, t3, t4, ConstraintList, NaiveControlNodeList,
                                 DijkstraControlNodeList, AstarControlNodeList, BOCSControlNodeList, nodeslist,
                                 NaivePath, DijkstraPath, AstarPath, BOCSPath, NaiveLength, DijkstraLength, AstarLength,
                                 BOCSLength, NaiveTime, DijkstraTime, AstarTime, BOCSTime]
                Result_list_section.append(l_currentcase)
                j += 3
                print()

        # NaiveFPR, DijkstraFPR, AstarFPR = calculate_false_pos_rate(Result_list_section) !!!!*****@!!!
        # Result_list_cases.extend(Result_list_section)

        outcsvpath = f"TestCaseFiles/csv_p=50/benchmark-{i}.csv"
        dictionary = dict(zip(column, Result_list_section))
        with open(outcsvpath, 'w', newline='') as f:
            dataframe = pd.DataFrame.from_dict(dictionary, orient='index', columns=Result_list_metric)
            dataframe.to_csv(outcsvpath)
            print()
