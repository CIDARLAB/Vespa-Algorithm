from ConstraintFunctions import findallConnectedNodes
from TestAlgorithm import getfileList, buildFlowGraph, locateValveAndCOonFE, fp_flag, checkandappend, calculate_false_pos_rate
import AlgorithmComparison
import pandas as pd
from networkx.drawing.nx_agraph import read_dot


pos = {}
if __name__ == '__main__':
    # Section loop
    Result_list_metric = ["User Requirement", "Netx Shortest Path (Dijkstra) estimate", "A* estimate", "VeSpA 2 estimate", "VeSpA 20 estimate",
                          "VeSpA 200 estimate", "Netx Shortest Path (Dijkstra) success", "A* success", "VeSpA 2 success", "VeSpA 20 success", "VeSpA 200 success",
                          "Constraint List", "Netx Shortest Path (Dijkstra) control List", "A star control list", "VeSpA 2 control list",
                          "VeSpA 20 control list", "VeSpA 200 control list", "ConstraintNodesGroup", "Netx Shortest Path (Dijkstra) path", "A* path",
                          "VeSpA 2 path", "VeSpA 20 path", "VeSpA 200 path", "Netx Shortest Path (Dijkstra) path length", "A* path length",
                          "VeSpA 2 path length", "VeSpA 20 path length", "VeSpA 200 path length", "Netx Shortest Path (Dijkstra) runtime", "A* runtime",
                          "VeSpA 2 runtime", "VeSpA 20 runtime", "VeSpA 200 runtime"]
    Result_list_cases = []
    column = []
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
                VeSpATime1, VeSpAPath1, VeSpALength1, flagFalseNegative1 = AlgorithmComparison.VeSpA_search(g_VeSpA, g_c, pos,
                                                                                ConstraintList, VCO2FEdictionary, uri, 2)
                g_VeSpA = g.copy()
                VeSpATime2, VeSpAPath2, VeSpALength2, flagFalseNegative2 = AlgorithmComparison.VeSpA_search(g_VeSpA, g_c, pos,
                                                                                                    ConstraintList, VCO2FEdictionary, uri, 20)
                g_VeSpA = g.copy()
                VeSpATime, VeSpAPath, VeSpALength, flagFalseNegative = AlgorithmComparison.VeSpA_search(g_VeSpA, g_c, pos,
                                                                                                    ConstraintList, VCO2FEdictionary, uri, 200)

                # Find all valves and other control components which are involved in the searching path
                NetxSPVCOList = AlgorithmComparison.control_search(NetxSPPath, FE2VCOdictionary)
                AstarVCOList = AlgorithmComparison.control_search(AstarPath, FE2VCOdictionary)
                VeSpAVCOList1 = AlgorithmComparison.control_search(VeSpAPath1, FE2VCOdictionary)
                VeSpAVCOList2 = AlgorithmComparison.control_search(VeSpAPath2, FE2VCOdictionary)
                VeSpAVCOList = AlgorithmComparison.control_search(VeSpAPath, FE2VCOdictionary)

                # Find all control edges and control ports being searched in the path
                NetxSPControlNodeList, NetxSPControlEdgeList = AlgorithmComparison.findall_control_path(NetxSPVCOList, g_c)
                AstarControlNodeList, AstarControlEdgeList = AlgorithmComparison.findall_control_path(AstarVCOList, g_c)
                VeSpAControlNodeList5, VeSpAControlEdgeList5 = AlgorithmComparison.findall_control_path(VeSpAVCOList1, g_c)
                VeSpAControlNodeList2, VeSpAControlEdgeList2 = AlgorithmComparison.findall_control_path(VeSpAVCOList2, g_c)
                VeSpAControlNodeList, VeSpAControlEdgeList = AlgorithmComparison.findall_control_path(VeSpAVCOList, g_c)

                # Calculate the false positive rate for each algorithm
                Nr, Ar, Br1, Br2, Br3, t1, t2, t3, t4, t5, nodeslist = calculate_false_pos_rate(NetxSPLength, AstarLength,
                VeSpALength1, VeSpALength2, VeSpALength, ConstraintList, NetxSPControlNodeList, AstarControlNodeList,
                VeSpAControlNodeList5, VeSpAControlNodeList2, VeSpAControlNodeList, g_c, flagFalseNegative1, flagFalseNegative2, flagFalseNegative)

                l_currentcase = [uri, Nr, Ar, Br1, Br2, Br3, t1, t2, t3, t4, t5, ConstraintList, NetxSPControlNodeList,
                                 AstarControlNodeList, VeSpAControlNodeList5, VeSpAControlNodeList2, VeSpAControlNodeList,
                                 nodeslist, NetxSPPath, AstarPath, VeSpAPath1, VeSpAPath2, VeSpAPath, NetxSPLength,
                                 AstarLength, VeSpALength1, VeSpALength2, VeSpALength, NetxSPTime, AstarTime, VeSpATime1, VeSpATime2,
                                 VeSpATime]
                Result_list_section.append(l_currentcase)

        # NetxSPFPR, DijkstraFPR, AstarFPR = calculate_false_pos_rate(Result_list_section) !!!!*****@!!!
        # Result_list_cases.extend(Result_list_section)

        outcsvpath = f"TestCaseFiles/lrb{i}.csv"
        dictionary = dict(zip(column, Result_list_section))
        with open(outcsvpath, 'w', newline='') as f:
            dataframe = pd.DataFrame.from_dict(dictionary, orient='index', columns=Result_list_metric)
            dataframe.to_csv(outcsvpath)
            print()
