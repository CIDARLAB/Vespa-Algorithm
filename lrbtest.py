from ConstraintFunctions import findallConnectedNodes
from TestAlgorithm import getfileList, buildFlowGraph, locateValveAndCOonFE, fp_flag, checkandappend, calculate_false_pos_rate
import AlgorithmComparison
import pandas as pd
from networkx.drawing.nx_agraph import read_dot


pos = {}
if __name__ == '__main__':
    # Section loop
    Result_list_metric = ["User Requirement", "Naive estimate", "Dijkstra estimate", "A* estimate", "VeSpA 5 estimate", "VeSpA 25 estimate",
                          "VeSpA 125 estimate", "Naive success", "Dijkstra success", "A* success", "VeSpA 5 success", "VeSpA 25 success", "VeSpA 125 success",
                          "Constraint List", "Naive control List", "Dijkstra control list", "A star control list", "VeSpA 5 control list",
                          "VeSpA 25 control list", "VeSpA 125 control list", "ConstraintNodesGroup", "Naive path", "Dijkstra path", "A* path",
                          "VeSpA 5 path", "VeSpA 25 path", "VeSpA path", "Naive path length", "Dijkstra path length", "A* path length",
                          "VeSpA 5 path length", "VeSpA 25 path length", "VeSpA 125 path length", "Naive runtime", "Dijkstra runtime", "A* runtime",
                          "VeSpA 5 runtime", "VeSpA 25 runtime", "VeSpA 125 runtime"]
    Result_list_cases = []
    column = []
    for i in range(5, 6):
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

                # Update the flow edge info after we get RandomConstraintList and use it in VeSpA_search
                g_VeSpA = g.copy()
                VeSpATime5, VeSpAPath5, VeSpALength5, flagFalseNegative5 = AlgorithmComparison.VeSpA_search(g_VeSpA, g_c, pos,
                                                                                ConstraintList, VCO2FEdictionary, uri, 5)
                g_VeSpA = g.copy()
                VeSpATime25, VeSpAPath25, VeSpALength25, flagFalseNegative25 = AlgorithmComparison.VeSpA_search(g_VeSpA, g_c, pos,
                                                                                                    ConstraintList, VCO2FEdictionary, uri, 25)
                g_VeSpA = g.copy()
                VeSpATime, VeSpAPath, VeSpALength, flagFalseNegative = AlgorithmComparison.VeSpA_search(g_VeSpA, g_c, pos,
                                                                                                    ConstraintList, VCO2FEdictionary, uri, 125)

                # Find all valves and other control components which may be involved giving the searched path
                NaiveVCOList = AlgorithmComparison.control_search(NaivePath, FE2VCOdictionary)
                DijkstraVCOList = AlgorithmComparison.control_search(DijkstraPath, FE2VCOdictionary)
                AstarVCOList = AlgorithmComparison.control_search(AstarPath, FE2VCOdictionary)
                VeSpAVCOList5 = AlgorithmComparison.control_search(VeSpAPath5, FE2VCOdictionary)
                VeSpAVCOList25 = AlgorithmComparison.control_search(VeSpAPath25, FE2VCOdictionary)
                VeSpAVCOList = AlgorithmComparison.control_search(VeSpAPath, FE2VCOdictionary)

                # Find all control edges and control ports being searched in the path
                NaiveControlNodeList, NaiveControlEdgeList = AlgorithmComparison.findall_control_path(NaiveVCOList, g_c)
                DijkstraControlNodeList, DijkstraControlEdgeList = AlgorithmComparison.findall_control_path(DijkstraVCOList, g_c)
                AstarControlNodeList, AstarControlEdgeList = AlgorithmComparison.findall_control_path(AstarVCOList, g_c)
                VeSpAControlNodeList5, VeSpAControlEdgeList5 = AlgorithmComparison.findall_control_path(VeSpAVCOList5, g_c)
                VeSpAControlNodeList25, VeSpAControlEdgeList25 = AlgorithmComparison.findall_control_path(VeSpAVCOList25, g_c)
                VeSpAControlNodeList, VeSpAControlEdgeList = AlgorithmComparison.findall_control_path(VeSpAVCOList, g_c)

                # Calculate the false positive rate for each algorithm
                Nr, Dr, Ar, Br1, Br2, Br3, t1, t2, t3, t4, t5, t6, nodeslist = calculate_false_pos_rate(NaiveLength, DijkstraLength, AstarLength,
                VeSpALength5, VeSpALength25, VeSpALength, ConstraintList, NaiveControlNodeList, DijkstraControlNodeList, AstarControlNodeList,
                VeSpAControlNodeList5, VeSpAControlNodeList25, VeSpAControlNodeList, g_c, flagFalseNegative5, flagFalseNegative25, flagFalseNegative)

                l_currentcase = [uri, Nr, Dr, Ar, Br1, Br2, Br3, t1, t2, t3, t4, t5, t6, ConstraintList, NaiveControlNodeList,
                                 DijkstraControlNodeList, AstarControlNodeList, VeSpAControlNodeList5, VeSpAControlNodeList25, VeSpAControlNodeList,
                                 nodeslist, NaivePath, DijkstraPath, AstarPath, VeSpAPath5, VeSpAPath25, VeSpAPath, NaiveLength, DijkstraLength,
                                 AstarLength, VeSpALength5, VeSpALength25, VeSpALength, NaiveTime, DijkstraTime, AstarTime, VeSpATime5, VeSpATime25,
                                 VeSpATime]
                Result_list_section.append(l_currentcase)

        # NaiveFPR, DijkstraFPR, AstarFPR = calculate_false_pos_rate(Result_list_section) !!!!*****@!!!
        # Result_list_cases.extend(Result_list_section)

        outcsvpath = f"TestCaseFiles/lrb{i}.csv"
        dictionary = dict(zip(column, Result_list_section))
        with open(outcsvpath, 'w', newline='') as f:
            dataframe = pd.DataFrame.from_dict(dictionary, orient='index', columns=Result_list_metric)
            dataframe.to_csv(outcsvpath)
            print()
