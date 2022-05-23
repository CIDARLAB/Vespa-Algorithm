import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import write_dot
import os

g_flow = nx.DiGraph()
g_control = nx.DiGraph()

flow_node_list = ["f1", "f2", "f3", "f4"]
for i in range(12):
    ss = f"fo{i+1}"
    flow_node_list.append(ss)

control_node_list = []
for i in range(8):
    ss = f"c{i+1}"
    control_node_list.append(ss)
for i in range(8):
    ss = f"v{i+1}"
    control_node_list.append(ss)

flow_edge_list = [("f1", "fo1", 2), ("fo1", "fo2", 2), ("fo2", "fo3", 2), ("fo3", "fo10", 2),
                  ("f2", "fo4", 2), ("fo4", "fo5", 2), ("fo5", "fo7", 2),
                  ("f3", "fo6", 2), ("fo6", "fo7", 2), ("fo7", "fo8", 2), ("fo8", "fo9", 2), ("fo9", "fo10", 2),
                  ("fo10", "fo11", 2), ("fo11", "fo12", 2), ("fo12", "f4", 2)
                  ]

control_edge_list = [("v1", "c1", 1), ("v2", "c2", 1), ("v3", "c3", 1), ("v4", "c4", 1), ("v5", "c5", 1),
                     ("v6", "c6", 1), ("v7", "c7", 1), ("v8", "c8", 1)]

ValveLocation = [["v1", "f1", "fo1"], ["v2", "f2", "fo4"], ["v3", "f3", "fo6"], ["v4", "fo6", "fo7"], ["v5", "fo7", "fo5"],
                 ["v6", "fo10", "fo9"], ["v7", "fo3", "fo10"], ["v8", "fo11", "fo12"]]

g_flow.add_nodes_from(flow_node_list)
g_flow.add_weighted_edges_from(flow_edge_list)

folder_path = "../TestCaseFiles/lrb/"

outpath1 = f"{folder_path}/lrb2_control.dot"
outpath2 = f"{folder_path}/lrb2_flow.dot"
outpath = f"{folder_path}/lrb2_ValveLocation.txt"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

write_dot(g_control, outpath1)
write_dot(g_flow, outpath2)
with open(outpath, 'w') as f:
    for s in ValveLocation:
        s = str(s) + '\n'
        f.writelines(s)
