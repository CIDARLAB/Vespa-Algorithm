from ConstraintFunctions import findallConnectedNodes
from TestAlgorithm import getfileList, buildFlowGraph, locateValveAndCOonFE, fp_flag, checkandappend, calculate_false_pos_rate
import AlgorithmComparison
import pandas as pd
from networkx.drawing.nx_agraph import read_dot


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
    for i in range(1, 6):
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
                VeSpATime10, VeSpAPath10, VeSpALength10, flagFalseNegative10 = AlgorithmComparison.VeSpA_search(g_VeSpA, g_c, pos,
                                                                                ConstraintList, VCO2FEdictionary, uri, 10)
                g_VeSpA = g.copy()
                VeSpATime50, VeSpAPath50, VeSpALength50, flagFalseNegative50 = AlgorithmComparison.VeSpA_search(g_VeSpA, g_c, pos,
                                                                                                    ConstraintList, VCO2FEdictionary, uri, 50)
                g_VeSpA = g.copy()
                VeSpATime, VeSpAPath, VeSpALength, flagFalseNegative = AlgorithmComparison.VeSpA_search(g_VeSpA, g_c, pos,
                                                                                                    ConstraintList, VCO2FEdictionary, uri, 100)

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
                VeSpALength10, VeSpALength50, VeSpALength, ConstraintList, NaiveControlNodeList, DijkstraControlNodeList, AstarControlNodeList,
                VeSpAControlNodeList10, VeSpAControlNodeList50, VeSpAControlNodeList, g_c, flagFalseNegative10, flagFalseNegative50, flagFalseNegative)

                l_currentcase = [uri, Nr, Dr, Ar, Br1, Br2, Br3, t1, t2, t3, t4, t5, t6, ConstraintList, NaiveControlNodeList,
                                 DijkstraControlNodeList, AstarControlNodeList, VeSpAControlNodeList10, VeSpAControlNodeList50, VeSpAControlNodeList,
                                 nodeslist, NaivePath, DijkstraPath, AstarPath, VeSpAPath10, VeSpAPath50, VeSpAPath, NaiveLength, DijkstraLength,
                                 AstarLength, VeSpALength10, VeSpALength50, VeSpALength, NaiveTime, DijkstraTime, AstarTime, VeSpATime10, VeSpATime50,
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
