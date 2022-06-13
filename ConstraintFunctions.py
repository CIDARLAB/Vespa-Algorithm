import networkx as nx
from networkx.drawing.nx_agraph import read_dot
from collections import Counter
import random


def findallConnectedNodes(node, edges):
    i = 0
    while i < len(node):
        for edge in edges:
            if edge[0] == node[i] and edge[1] not in node:
                node.append(edge[1])
            elif edge[1] == node[i] and edge[0] not in node:
                node.append(edge[0])
        i += 1
    return node


def OriginalConstraintTablebuilder(type, node, t):
    table = t.copy()
    node_new = node.copy()
    if type == 2:
        l = node_new[0] + node_new[1]
        plength = len(l)
        alength = len(set(l))
        if alength != plength:
            return [table[0]]
    return table


# for type 1, the element looks like: "[vi]": {Type: 1, Nodes: [vi, ci, vj], TruthTable:0}
# for type 2, the element looks like: "[vi, vj]": {Type: 2, Nodes: [[vi, ci], [vj, cj]], TruthTable: [[0, 0], [0, 1], [1, 0]]}
# for type 2, may have errors when build the dictionary. Assume vi and vj connect to the same ci.
# "[vi, vj]": {Type: 2, Nodes: [[vi, ci, vj], [vj, cj, vi]], TruthTable: [[0,0]]}, vi cannot open and close at the same time
# If we cannot generate a constraint dictionary, (not type1 and type2, may some other type)
# then that means the constraint is incorrect, show warning!!!!!
def NodeGroupConstraintMatrixgenerator(ConstraintList, g, g_c):
    d = []
    conflict = 0
    for c in ConstraintList:
        # constraint type 1
        di = {}
        if c[0] == 1:
            node = [c[1]]
            # find all nodes connect to elements in node[]
            node = findallConnectedNodes(node, g_c.edges())
            di = {"Type": 1, "TruthTable": 0, "Nodes": node}
        # constraint type 2
        if c[0] == 2:
            node1 = [c[1]]
            node2 = [c[2]]
            node1 = findallConnectedNodes(node1, g_c.edges())
            node2 = findallConnectedNodes(node2, g_c.edges())
            node = [node1, node2]
            initial_table = [[0, 0], [0, 1], [1, 0]]
            table = OriginalConstraintTablebuilder(2, node, initial_table)
            di = {"Type": 2, "TruthTable": table, "Nodes": node}
        d.append(di)
    return conflict, d


# !!!!!! Tricky part:
# remove the constraint ci from the list after we remove the edges related with ci.
# Because no matter how many valves / co located on the edge, it will be closed when one of the valve is closed.
# For type 2 constraint, we can also remove the edge where one or more valves onside are always set to 0.
def updateGraphByNGConstraint(VCO2F, g, d):
    l = []
    for i in range(len(d)):
        di = d[i]
        nodes = di["Nodes"].copy()
        # For type 1 constraint, remove the edge it falls in.
        if di["Type"] == 1:
            for node in nodes:
                if node in VCO2F.keys() and VCO2F[node] in g.edges():
                    g.remove_edge(VCO2F[node][0], VCO2F[node][1])
            l.append(i)
        elif di["Type"] == 2 and len(di["TruthTable"]) == 1:
            nodes_old = nodes[0] + nodes[1]
            nodes_new = []
            for n in nodes_old:
                if n[0] != 'c' or n[1] == 'o':
                    nodes_new.append(n)
            nodes_vco = list(set(nodes_new))
            for node in nodes_vco:
                if node in VCO2F.keys() and VCO2F[node] in g.edges():
                    g.remove_edge(VCO2F[node][0], VCO2F[node][1])
            l.append(i)
    d_new = d.copy()
    for le in sorted(l, reverse=True):
        del d_new[le]
    return g, d_new


def Node_NG_Constraint_translater(d):
    ConstraintGroupList = []
    nodes_group_list = []
    for di in d:
        RepeatFlag = 0
        nodes = di["Nodes"].copy()
        # create node group list and transfer the original constraint matrix to a new one which represent by node groups
        if di["Type"] == 2 and len(di["TruthTable"]) > 1:
            flag = -1
            for i in range(len(nodes_group_list)):
                n = nodes_group_list[i]
                if Counter(nodes[0]) == Counter(n):
                    flag = i
                    break
            if flag == -1:
                nodes_group_list.append(nodes[0])
                NodeGroupIndex = len(nodes_group_list) - 1
            else:
                NodeGroupIndex = flag
            flag = -1
            for i in range(len(nodes_group_list)):
                n = nodes_group_list[i]
                if Counter(nodes[1]) == Counter(n):
                    flag = i
                    break
            if flag == -1:
                nodes_group_list.append(nodes[1])
                NodeGroupIndex2 = len(nodes_group_list) - 1
            else:
                NodeGroupIndex2 = flag
            for ele in ConstraintGroupList:
                if Counter(ele) == Counter([NodeGroupIndex, NodeGroupIndex2]):
                    RepeatFlag = 1
                    break
            if RepeatFlag == 1:
                continue

            ConstraintGroupList.append([NodeGroupIndex, NodeGroupIndex2])
    return 0, ConstraintGroupList, nodes_group_list


# use recursion to create truth table
def createTruthTable(t, l, i, tab, cl):
    if i == len(l):
        v = list(t.values())
        conflictgraphflag = 0
        for con in cl:
            # protect the graph from having constraint conflict
            if v[con[0]] * v[con[1]] == 1:
                conflictgraphflag = 1
                break
        if conflictgraphflag == 0:
            tab.append(v.copy())
        return t, tab
    t[l[i]] = 0
    t, tab = createTruthTable(t, l, i+1, tab, cl)
    t[l[i]] = 1
    t, tab = createTruthTable(t, l, i+1, tab, cl)
    return t, tab


def NodeGroupTruthTableBuilder(nl, cl):
    conflict = 0
    table_col = len(nl)
    keys = range(table_col)
    values = [-1] * table_col
    d = dict(zip(keys, values))
    d, tab = createTruthTable(d, keys, 0, [], cl)
    if len(tab) == 0 and len(cl) != 0:
        conflict = 1
    return conflict, tab

