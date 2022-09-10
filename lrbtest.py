from TestAlgorithm import buildFlowGraph, locateValveAndCOonFE
from MetricsGenerator import calculate_false_pos
import AlgorithmComparison
import pandas as pd
from networkx.drawing.nx_agraph import read_dot


pos = {}
if __name__ == '__main__':
    # Section loop
    Result_list_metric = ["User Requirement", "Netx Shortest Path (Dijkstra) estimate", "A* estimate", "VeSpA 1 estimate", "VeSpA 100 estimate",
                          "VeSpA INF estimate", "Netx Shortest Path (Dijkstra) success", "A* success", "VeSpA 1 success", "VeSpA 100 success",
                          "VeSpA INF success", "Constraint List", "Netx Shortest Path (Dijkstra) control List", "A star control list",
                          "VeSpA 1 control list", "VeSpA 100 control list", "VeSpA INF control list", "ConstraintNodesGroup",
                          "Netx Shortest Path (Dijkstra) path", "A* path", "VeSpA 1 path", "VeSpA 100 path", "VeSpA INF path",
                          "Netx Shortest Path (Dijkstra) path length", "A* path length", "VeSpA 1 path length", "VeSpA 100 path length",
                          "VeSpA INF path length", "Netx Shortest Path (Dijkstra) runtime", "A* runtime", "VeSpA 1 runtime", "VeSpA 100 runtime",
                          "VeSpA INF runtime", "Best I"]
    Result_list_cases = []
    for i in range(1, 7):
        Result_list_section = []
        path = f"TestCaseFiles/lrb"
        control_graph_path = f"{path}/graph_info/lrb{i}_control.dot"
        flow_graph_path = f"{path}/graph_info/lrb{i}_flow.dot"
        valve_co_txt = f"{path}/graph_info/lrb{i}_ValveLocation.txt"
        column = []
        constraint_ur_path = f"{path}/URC/Constraint_UR_lrb{i}.csv"
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
                NetxSPTime, NetxSPPath, NetxSPLength = AlgorithmComparison.netxsp_search(g, uri)
                AstarTime, AstarPath, AstarLength = AlgorithmComparison.astar_search(g, pos, uri)

                # Update the flow edge info after we get RandomConstraintList and use it in VeSpA_search
                g_VeSpA = g.copy()
                VeSpATime1, VeSpAPath1, VeSpALength1, flagFalseNegative1, _ = AlgorithmComparison.VeSpA_search(g_VeSpA, g_c, pos,
                                                                                ConstraintList, VCO2FEdictionary, uri, 1)
                g_VeSpA = g.copy()
                VeSpATime2, VeSpAPath2, VeSpALength2, flagFalseNegative2, _ = AlgorithmComparison.VeSpA_search(g_VeSpA, g_c, pos,
                                                                                                    ConstraintList, VCO2FEdictionary, uri, 100)
                g_VeSpA = g.copy()
                VeSpATime, VeSpAPath, VeSpALength, flagFalseNegative, I_best = AlgorithmComparison.VeSpA_search(g_VeSpA, g_c, pos,
                                                                                                    ConstraintList, VCO2FEdictionary, uri, 0)

                # Find all valves and other control components which are involved in the searching path
                NetxSPVCOList = AlgorithmComparison.control_search(NetxSPPath, FE2VCOdictionary)
                AstarVCOList = AlgorithmComparison.control_search(AstarPath, FE2VCOdictionary)
                VeSpAVCOList1 = AlgorithmComparison.control_search(VeSpAPath1, FE2VCOdictionary)
                VeSpAVCOList2 = AlgorithmComparison.control_search(VeSpAPath2, FE2VCOdictionary)
                VeSpAVCOList = AlgorithmComparison.control_search(VeSpAPath, FE2VCOdictionary)

                # Find all control edges and control ports being searched in the path
                NetxSPControlNodeList, NetxSPControlEdgeList = AlgorithmComparison.findall_control_path(NetxSPVCOList, g_c)
                AstarControlNodeList, AstarControlEdgeList = AlgorithmComparison.findall_control_path(AstarVCOList, g_c)
                VeSpAControlNodeList1, VeSpAControlEdgeList1 = AlgorithmComparison.findall_control_path(VeSpAVCOList1, g_c)
                VeSpAControlNodeList2, VeSpAControlEdgeList2 = AlgorithmComparison.findall_control_path(VeSpAVCOList2, g_c)
                VeSpAControlNodeList, VeSpAControlEdgeList = AlgorithmComparison.findall_control_path(VeSpAVCOList, g_c)

                # Calculate the false positive rate for each algorithm
                l, t, nodeslist = calculate_false_pos([NetxSPLength, AstarLength, VeSpALength1, VeSpALength2, VeSpALength], ConstraintList,
                                                      [NetxSPControlNodeList, AstarControlNodeList, VeSpAControlNodeList1, VeSpAControlNodeList2,
                                                       VeSpAControlNodeList],
                                                      g_c, [flagFalseNegative1, flagFalseNegative2, flagFalseNegative])

                l_currentcase = [uri, l[0], l[1], l[2], l[3], l[4], t[0], t[1], t[2], t[3], t[4], ConstraintList, NetxSPControlNodeList,
                                 AstarControlNodeList, VeSpAControlNodeList1, VeSpAControlNodeList2, VeSpAControlNodeList,
                                 nodeslist, NetxSPPath, AstarPath, VeSpAPath1, VeSpAPath2, VeSpAPath, NetxSPLength,
                                 AstarLength, VeSpALength1, VeSpALength2, VeSpALength, format(NetxSPTime, '.5f'), format(AstarTime, '.5f'),
                                 format(VeSpATime1, '.5f'), format(VeSpATime2, '.5f'), format(VeSpATime, '.5f'), I_best]
                Result_list_section.append(l_currentcase)

        # NetxSPFPR, DijkstraFPR, AstarFPR = calculate_false_pos_rate(Result_list_section) !!!!*****@!!!
        # Result_list_cases.extend(Result_list_section)

        outcsvpath = f"TestCaseFiles/lrb/lrb{i}.csv"
        dictionary = dict(zip(column, Result_list_section))
        with open(outcsvpath, 'w', newline='') as f:
            dataframe = pd.DataFrame.from_dict(dictionary, orient='index', columns=Result_list_metric)
            dataframe.to_csv(outcsvpath)
            print()
