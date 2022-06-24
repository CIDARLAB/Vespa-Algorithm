import time
import networkx as nx
import os
import matplotlib.pyplot as plt
from ConstraintFunctions import NodeGroupConstraintMatrixgenerator, updateGraphByNGConstraint, NodeGroupTruthTableBuilder, \
    Node_NG_Constraint_translater, findallConnectedNodes
from collections import Counter
pos = {}


def multiURChecker(g, ur):
    NetxSPPath = []
    NetxSPLen = 0
    if isinstance(ur[0], list) and isinstance(ur[1], list):
        for ur0 in ur[0]:
            for ur1 in ur[1]:
                try:
                    multipath = nx.shortest_path(g, source=ur0, target=ur1)
                except nx.NetworkXNoPath:
                    return [], -1, time.time()
                NetxSPPath.append(multipath)
                NetxSPLen += nx.dijkstra_path_length(g, source=ur0, target=ur1)
    elif isinstance(ur[0], list):
        for ur0 in ur[0]:
            try:
                multipath = nx.shortest_path(g, source=ur0, target=ur[1])
            except nx.NetworkXNoPath:
                return [], -1, time.time()
            NetxSPPath.append(multipath)
            NetxSPLen += nx.dijkstra_path_length(g, source=ur0, target=ur[1])
    elif isinstance(ur[1], list):
        for ur1 in ur[1]:
            try:
                multipath = nx.shortest_path(g, source=ur[0], target=ur1)
            except nx.NetworkXNoPath:
                return [], -1, time.time()
            NetxSPPath.append(multipath)
            NetxSPLen += nx.dijkstra_path_length(g, source=ur[0], target=ur1)
    else:
        try:
            multipath = nx.shortest_path(g, source=ur[0], target=ur[1])
        except nx.NetworkXNoPath:
            return [], -1, time.time()
        NetxSPPath.append(multipath)
        NetxSPLen += nx.dijkstra_path_length(g, source=ur[0], target=ur[1])
    end = time.time()
    return NetxSPPath, NetxSPLen, end


def netxsp_search(g, ur):
    # NetxSP searching algorithm
    start = time.time()
    NetxSPPath, NetxSPLen, end = multiURChecker(g, ur)
    NetxSPTime = end - start
    return NetxSPTime, NetxSPPath, NetxSPLen


def h_function(a, b):
    (x1, y1) = pos[a]
    (x2, y2) = pos[b]
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def astar_search(g, position, ur):
    global pos
    pos = position
    AstarPath = []
    AstarLength = 0
    start = time.time()
    if isinstance(ur[0], list) and isinstance(ur[1], list):
        for ur0 in ur[0]:
            for ur1 in ur[1]:
                try:
                    multipath = nx.astar_path(g, source=ur0, target=ur1, heuristic=h_function, weight="weight")
                except nx.NetworkXNoPath:
                    end = time.time()
                    print(f"No such a path from {ur[0]} to {ur[1]} using A Star searching algorithm")
                    return end - start, [], -1
                AstarPath.append(multipath)
                AstarLength += nx.astar_path_length(g, source=ur0, target=ur1, heuristic=h_function, weight="weight")
    elif isinstance(ur[0], list):
        for ur0 in ur[0]:
            try:
                multipath = nx.astar_path(g, source=ur0, target=ur[1], heuristic=h_function, weight="weight")
            except nx.NetworkXNoPath:
                end = time.time()
                print(f"No such a path from {ur[0]} to {ur[1]} using A Star searching algorithm")
                return end - start, [], -1
            AstarPath.append(multipath)
            AstarLength += nx.astar_path_length(g, source=ur0, target=ur[1], heuristic=h_function, weight="weight")
    elif isinstance(ur[1], list):
        for ur1 in ur[1]:
            try:
                multipath = nx.astar_path(g, source=ur[0], target=ur1, heuristic=h_function, weight="weight")
            except nx.NetworkXNoPath:
                end = time.time()
                print(f"No such a path from {ur[0]} to {ur[1]} using A Star searching algorithm")
                return end - start, [], -1
            AstarPath.append(multipath)
            AstarLength += nx.astar_path_length(g, source=ur[0], target=ur1, heuristic=h_function, weight="weight")
    else:
        try:
            multipath = nx.astar_path(g, source=ur[0], target=ur[1], heuristic=h_function, weight="weight")
        except nx.NetworkXNoPath:
            end = time.time()
            print(f"No such a path from {ur[0]} to {ur[1]} using A Star searching algorithm")
            return end - start, [], -1
        AstarPath.append(multipath)
        AstarLength += nx.astar_path_length(g, source=ur[0], target=ur[1], heuristic=h_function, weight="weight")

    end = time.time()
    AstarTime = end - start
    return AstarTime, AstarPath, AstarLength


# One row in the table means one graph
def VeSpAGraphGenerator(table, nodes_group_list, vcofe, g):
    g_list = []
    edge_remove_listall = []
    for row in table:
        g_VeSpA = g.copy()
        edge_remove_list = []
        # cut the edges when there are valves onside be set to 0 in a row
        for i in range(len(row)):
            # 0 means that node group keep closed in this situation
            if row[i] == 0:
                # all edges have control nodes in nodes_group_list[i] should be removed

                for n in nodes_group_list[i]:
                    if n[0] != 'c' or n[1] == 'o':
                        edge = vcofe[n]
                        edgerepeatflag = 0
                        for e in edge_remove_list:
                            if Counter(e) == Counter(edge):
                                edgerepeatflag = 1
                                break
                        if len(edge_remove_list) == 0 or edgerepeatflag == 0:
                            edge_remove_list.append(edge)

        repeatflag = 0
        for e in edge_remove_listall:
            e1 = e.copy()
            e2 = edge_remove_list.copy()
            e3 = e1 + e2
            l1 = len([list(t) for t in set(tuple(_) for _ in e1)])
            l2 = len([list(t) for t in set(tuple(_) for _ in e2)])
            e4 = [list(t) for t in set(tuple(_) for _ in e3)]
            if l1 == len(e4) and l2 == len(e4):
                repeatflag = 1
        if repeatflag == 1:
            continue
        for e in edge_remove_list:
            for edge in g_VeSpA.edges():
                if Counter(e) == Counter(edge):
                    g_VeSpA.remove_edge(e[0], e[1])
        g_list.append(g_VeSpA)
        edge_remove_listall.append(edge_remove_list)
    return g_list


# for constraint type 2, generate all possible graphs keeping the constraint.
# !!!!!! Tricky part:
# All node[0] node[1] here will be totally same or different at all. If they have intersection node, they will be
# connected by the findallConnectedNodes() function. So, we can transfer the current d to a list of tuples consists
# of two node groups, all nodes in the group should be open or close together.
def enumerateVeSpAgraphs(g, d, vcofe, listlen):
    conflict = 0
    # creat node group constraint list
    conflict, ConstraintNGList, nodes_group_list = Node_NG_Constraint_translater(d)
    if conflict == 1:
        return 1, []
    # create a truth table including all node groups according to the ConstraintGroupList
    conflict, table, fp = NodeGroupTruthTableBuilder(nodes_group_list, ConstraintNGList, listlen)
    # Use the table to generate graphs which lose some edges compared with the original graph.
    g_list = VeSpAGraphGenerator(table, nodes_group_list, vcofe, g)
    return conflict, g_list, fp


def VeSpA_search(g, g_c, position, ConstraintList, VCO2FEdictionary, ur, listlen):
    global pos
    pos = position
    start = time.time()

    # Create a constraint dictionary list represents the constraint equation in matrix way
    Conflict, NGConstraintMatrix = NodeGroupConstraintMatrixgenerator(ConstraintList, g, g_c)
    # update graph with removing the edges in constraint type 1
    g, ConstraintMatrixNew = updateGraphByNGConstraint(VCO2FEdictionary, g, NGConstraintMatrix)
    # generate all graphs satisfy the constraint type 2 as a list
    Conflict, g_list, flagFalseNegative = enumerateVeSpAgraphs(g, ConstraintMatrixNew, VCO2FEdictionary, listlen)
    if Conflict == 1:
        print("Constraint conflict 2!", ConstraintList)
        end = time.time()
        return end - start, [], -2, -1
    VeSpAPathMin = []
    VeSpALengthMin = 0
    # If the list is too big, we can randomly choose 1000 graphs from the big list to speedup the procedure. (random way)
    # Here we choose graphs in order from truth table elements are all 1 to all 0. (Our way)
    # if len(g_list) > listlen:
    #     flagFalseNegative = 1
    #     g_list = random.sample(g_list, listlen)
    for gb in g_list:
        _, VeSpAPath, VeSpALength = netxsp_search(gb, ur)
        if len(VeSpAPathMin) == 0 or VeSpALengthMin > VeSpALength > 0:
            VeSpAPathMin = VeSpAPath
            VeSpALengthMin = VeSpALength
    end = time.time()
    if not VeSpAPathMin:
        print(f"No such a path from {ur[0]} to {ur[1]} using VeSpA I={listlen} searching algorithm")
        return end - start, [], -1, flagFalseNegative
    VeSpATime = end - start
    return VeSpATime, VeSpAPathMin, VeSpALengthMin, flagFalseNegative


def control_search(path, dictionary):
    VCOList = []
    for pathj in path:
        for i in range(len(pathj)-1):
            edge = (pathj[i], pathj[i+1])
            if edge in dictionary.keys():
                VCO = dictionary[edge]
                for vi in VCO:
                    if vi in VCOList:
                        continue
                    else:
                        VCOList.append(vi)
            else:
                edge = (pathj[i+1], pathj[i])
                if edge in dictionary.keys():
                    VCO = dictionary[edge]
                    for vi in VCO:
                        if vi in VCOList:
                            continue
                        else:
                            VCOList.append(vi)
    return VCOList


def findall_control_path(VCOList, g_c):
    ControlNodeList = VCOList.copy()
    ControlEdgeList = []
    ControlNodeList = findallConnectedNodes(ControlNodeList, g_c.edges)
    for edge in g_c.edges:
        # find edges consists of nodes in VCOList
        if edge[0] in VCOList:
            ControlEdgeList.append(edge)
        elif edge[1] in VCOList:
            ControlEdgeList.append(edge)
    return ControlNodeList, ControlEdgeList


def simulateFlowPathway(time, path, outputfolderpath, EdgeNum, g, GraphListInfo):
    color_list = ['green' for i in range(len(g.nodes()))]
    if not os.path.exists(outputfolderpath):
        os.makedirs(outputfolderpath)
    if time > 0:
        for ele in path:
            index = list(g.nodes()).index(ele)
            color_list[index] = 'red'
        outputpath = f"{outputfolderpath}/{GraphListInfo[EdgeNum][:5]}.png"
    else:
        if not os.path.exists(f"{outputfolderpath}/Fail/"):
            os.makedirs(f"{outputfolderpath}/Fail/")
        outputpath = f"{outputfolderpath}/Fail/{GraphListInfo[EdgeNum][:5]}.png"
    nx.draw_networkx(g, pos, nodelist=g.nodes(), node_color=color_list)
    plt.savefig(outputpath)


def simulateControlPathway(time, path, filepath, j, graph, GraphListInfo):
    pass


def simulate(NodeInfo, NetxSPTime, NetxSPPath, NCP, DijkstraTime, DijkstraPath, DCP, AstarTime, AstarPath, ACP, VeSpATime,
             VeSpAPath, BCP, i, j, g, g_c, gli):
    # NetxSP simulate flow pathway
    outputfolderpath = f"TestCaseFiles/NetxSP_result/Section_{i}/{NodeInfo}"
    simulateFlowPathway(NetxSPTime, NetxSPPath, outputfolderpath, j, g, gli)

    # Dijkstra simulate flow pathway
    outputfolderpath = f"TestCaseFiles/Dijkstra_result/Section_{i}/{NodeInfo}"
    simulateFlowPathway(DijkstraTime, DijkstraPath, outputfolderpath, j, g, gli)

    # A star simulate flow pathway
    outputfolderpath = f"TestCaseFiles/A*_result/Section_{i}/{NodeInfo}"
    simulateFlowPathway(AstarTime, AstarPath, outputfolderpath, j, g, gli)

    # VeSpA simulate flow pathway
    outputfolderpath = f"TestCaseFiles/VeSpA_result/Section_{i}/{NodeInfo}"
    simulateFlowPathway(VeSpATime, VeSpAPath, outputfolderpath, j, g, gli)

    # NetxSP simulate control layer pathway
    outputfolderpath = f"TestCaseFiles/NetxSP_result/Section_{i}/{NodeInfo}"
    simulateControlPathway(NetxSPTime, NetxSPPath, outputfolderpath, j, g, gli)

    # Dijkstra simulate control layer pathway
    outputfolderpath = f"TestCaseFiles/Dijkstra_result/Section_{i}/{NodeInfo}"
    simulateControlPathway(DijkstraTime, DijkstraPath, outputfolderpath, j, g, gli)

    # A star simulate control layer pathway
    outputfolderpath = f"TestCaseFiles/A*_result/Section_{i}/{NodeInfo}"
    simulateControlPathway(AstarTime, AstarPath, outputfolderpath, j, g, gli)

    # VeSpA simulate control pathway
    outputfolderpath = f"TestCaseFiles/VeSpA_result/Section_{i}/{NodeInfo}"
    simulateControlPathway(VeSpATime, VeSpAPath, outputfolderpath, j, g, gli)
