from TestAlgorithm import buildFlowGraph, locateValveAndCOonFE
from MetricsGenerator import calculate_false_pos
import AlgorithmComparison
import pandas as pd
from networkx.drawing.nx_agraph import read_dot


pos = {}
if __name__ == '__main__':
    # Section loop
    Result_list_metric = ["User Requirement", "Netx Shortest Path (Dijkstra) estimate", "A* estimate", "Vespa 1 estimate", "Vespa 100 estimate",
                          "Vespa INF estimate", "Netx Shortest Path (Dijkstra) success", "A* success", "Vespa 1 success", "Vespa 100 success",
                          "Vespa INF success", "Constraint List", "Netx Shortest Path (Dijkstra) control List", "A star control list",
                          "Vespa 1 control list", "Vespa 100 control list", "Vespa INF control list", "ConstraintNodesGroup",
                          "Netx Shortest Path (Dijkstra) path", "A* path", "Vespa 1 path", "Vespa 100 path", "Vespa INF path",
                          "Netx Shortest Path (Dijkstra) path length", "A* path length", "Vespa 1 path length", "Vespa 100 path length",
                          "Vespa INF path length", "Netx Shortest Path (Dijkstra) runtime", "A* runtime", "Vespa 1 runtime", "Vespa 100 runtime",
                          "Vespa INF runtime", "Num Of Graph", "Failure caused by Leakage Vespa 1", "Failure caused by Leakage Vespa 2",
                          "Failure caused by Leakage Vespa 3"]
    Result_list_cases = []
    for i in range(4, 6):
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

                # Update the flow edge info after we get RandomConstraintList and use it in Vespa_search
                g_Vespa = g.copy()
                VespaTime1, VespaPath1, VespaLength1, flagFalseNegative1, _, leakage1 = AlgorithmComparison.Vespa_search(g_Vespa, g_c, pos,
                                                                                ConstraintList, VCO2FEdictionary, uri, 1)
                g_Vespa = g.copy()
                VespaTime2, VespaPath2, VespaLength2, flagFalseNegative2, _, leakage2 = AlgorithmComparison.Vespa_search(g_Vespa, g_c, pos,
                                                                                                    ConstraintList, VCO2FEdictionary, uri, 100)
                g_Vespa = g.copy()
                VespaTime, VespaPath, VespaLength, flagFalseNegative, I_best, leakage3 = AlgorithmComparison.Vespa_search(g_Vespa, g_c, pos,
                                                                                                    ConstraintList, VCO2FEdictionary, uri, 0)

                # Find all valves and other control components which are involved in the searching path
                NetxSPVCOList = AlgorithmComparison.control_search(NetxSPPath, FE2VCOdictionary)
                AstarVCOList = AlgorithmComparison.control_search(AstarPath, FE2VCOdictionary)
                VespaVCOList1 = AlgorithmComparison.control_search(VespaPath1, FE2VCOdictionary)
                VespaVCOList2 = AlgorithmComparison.control_search(VespaPath2, FE2VCOdictionary)
                VespaVCOList = AlgorithmComparison.control_search(VespaPath, FE2VCOdictionary)

                # Find all control edges and control ports being searched in the path
                NetxSPControlNodeList, NetxSPControlEdgeList = AlgorithmComparison.findall_control_path(NetxSPVCOList, g_c)
                AstarControlNodeList, AstarControlEdgeList = AlgorithmComparison.findall_control_path(AstarVCOList, g_c)
                VespaControlNodeList1, VespaControlEdgeList1 = AlgorithmComparison.findall_control_path(VespaVCOList1, g_c)
                VespaControlNodeList2, VespaControlEdgeList2 = AlgorithmComparison.findall_control_path(VespaVCOList2, g_c)
                VespaControlNodeList, VespaControlEdgeList = AlgorithmComparison.findall_control_path(VespaVCOList, g_c)

                # Calculate the false positive rate for each algorithm
                l, t, nodeslist = calculate_false_pos([NetxSPLength, AstarLength, VespaLength1, VespaLength2, VespaLength], ConstraintList,
                                                      [NetxSPControlNodeList, AstarControlNodeList, VespaControlNodeList1, VespaControlNodeList2,
                                                       VespaControlNodeList], g_c, [flagFalseNegative1, flagFalseNegative2, flagFalseNegative], g, uri)

                l_currentcase = [uri, l[0], l[1], l[2], l[3], l[4], t[0], t[1], t[2], t[3], t[4], ConstraintList, NetxSPControlNodeList,
                                 AstarControlNodeList, VespaControlNodeList1, VespaControlNodeList2, VespaControlNodeList,
                                 nodeslist, NetxSPPath, AstarPath, VespaPath1, VespaPath2, VespaPath, NetxSPLength,
                                 AstarLength, VespaLength1, VespaLength2, VespaLength, format(NetxSPTime, '.5f'), format(AstarTime, '.5f'),
                                 format(VespaTime1, '.5f'), format(VespaTime2, '.5f'), format(VespaTime, '.5f'), I_best, leakage1, leakage2, leakage3]
                Result_list_section.append(l_currentcase)

        # NetxSPFPR, DijkstraFPR, AstarFPR = calculate_false_pos_rate(Result_list_section) !!!!*****@!!!
        # Result_list_cases.extend(Result_list_section)

        outcsvpath = f"TestCaseFiles/lrb/lrb{i}.csv"
        dictionary = dict(zip(column, Result_list_section))
        with open(outcsvpath, 'w', newline='') as f:
            dataframe = pd.DataFrame.from_dict(dictionary, orient='index', columns=Result_list_metric)
            dataframe.to_csv(outcsvpath)
            print()
