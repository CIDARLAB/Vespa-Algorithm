from ConstraintFunctions import findallConnectedNodes
from TestAlgorithm import getfileList, buildFlowGraph, locateValveAndCOonFE, fp_flag, checkandappend, calculate_false_pos_rate
import AlgorithmComparison
import random
from collections import Counter
import networkx as nx
import os
import numpy as np
import ast
import pandas as pd
from networkx.drawing.nx_agraph import read_dot


pos = {}
if __name__ == '__main__':
    # Section loop
    Result_list_metric = ["User Requirement", "Naive estimate", "Dijkstra estimate", "A* estimate", "BOCS estimate",
                          "Naive success", "Dijkstra success", "A* success", "BOCS success",
                          "Constraint List", "Naive control List", "Dijkstra control list", "A star control list", "BOCS control list",
                          "ConstraintNodesGroup", "Naive path", "Dijkstra path", "A* path", "BOCS path",
                          "Naive path length", "Dijkstra path length", "A* path length",
                          "BOCS path length", "Naive runtime", "Dijkstra runtime", "A* runtime", "BOCS runtime"]
    Result_list_cases = []
    column = []
    for i in range(1, 5):
        Result_list_section = []
        path = f"TestCaseFiles/lrb"
        control_graph_path = f"{path}/lrb{i}_control.dot"
        flow_graph_path = f"{path}/lrb{i}_flow.dot"
        valve_co_txt = f"{path}/lrb{i}_ValveLocation.txt"
        column = []
        constraint_ur_path = f"{path}/Constraint_UR_lrb{i}.csv"
        df = pd.read_csv(constraint_ur_path, index_col=None, header=0).to_dict()
        URConstraintInfoAll = []
        for j in range(len(df["User Requirement"])):
            ele = {"UR": df["User Requirement"][j], "CL": df["Constraint List"][j]}
            ele["UR"] = eval(ele["UR"])
            ele["CL"] = eval(ele["CL"])
            URConstraintInfoAll.append(ele)

        # scan all elements in URConstraintInfoAll
        for j in range(len(URConstraintInfoAll)):
            # divide the ur list inside one URCInfo element and check each ur respectively.
            for k in range(len(URConstraintInfoAll[j]["UR"])):
                uri = URConstraintInfoAll[j]["UR"][k]
                column.append(f"lrb{i}|benchmark{j+1}_{k+1}")
                g, pos = buildFlowGraph(flow_graph_path)
                g_c = read_dot(control_graph_path)
                g_c = g_c.to_undirected()
                ConstraintList = URConstraintInfoAll[j]["CL"]

                # Create a dictionary shows the flow edge on which each valve and other control component locates
                VCO2FEdictionary, FE2VCOdictionary = locateValveAndCOonFE(valve_co_txt)

                # Algorithm comparison
                NaiveTime, NaivePath, NaiveLength = AlgorithmComparison.naive_search(g, uri)
                DijkstraTime, DijkstraPath, DijkstraLength = AlgorithmComparison.dijkstra_search(g, uri)
                AstarTime, AstarPath, AstarLength = AlgorithmComparison.astar_search(g, pos, uri)

                # Update the flow edge info after we get RandomConstraintList and use it in BOCS_search
                g_BOCS = g.copy()
                BOCSTime, BOCSPath, BOCSLength, flagFalseNegative = AlgorithmComparison.BOCS_search(g_BOCS, g_c, pos,
                                                                                ConstraintList, VCO2FEdictionary, uri)

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

                # Calculate the false positive rate for each algorithm
                Nr, Dr, Ar, Br, t1, t2, t3, t4, nodeslist = calculate_false_pos_rate(NaiveLength, DijkstraLength, AstarLength, BOCSLength,
                ConstraintList, NaiveControlNodeList, DijkstraControlNodeList, AstarControlNodeList, BOCSControlNodeList, g_c,
                                                                                     flagFalseNegative)

                l_currentcase = [uri, Nr, Dr, Ar, Br, t1, t2, t3, t4, ConstraintList, NaiveControlNodeList,
                                 DijkstraControlNodeList, AstarControlNodeList, BOCSControlNodeList, nodeslist,
                                 NaivePath, DijkstraPath, AstarPath, BOCSPath, NaiveLength, DijkstraLength, AstarLength,
                                 BOCSLength, NaiveTime, DijkstraTime, AstarTime, BOCSTime]
                Result_list_section.append(l_currentcase)

        # NaiveFPR, DijkstraFPR, AstarFPR = calculate_false_pos_rate(Result_list_section) !!!!*****@!!!
        # Result_list_cases.extend(Result_list_section)

        outcsvpath = f"TestCaseFiles/lrb{i}.csv"
        dictionary = dict(zip(column, Result_list_section))
        with open(outcsvpath, 'w', newline='') as f:
            dataframe = pd.DataFrame.from_dict(dictionary, orient='index', columns=Result_list_metric)
            dataframe.to_csv(outcsvpath)
            print()
