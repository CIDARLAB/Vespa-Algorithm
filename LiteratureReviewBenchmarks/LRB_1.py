import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import write_dot
import os

g_flow = nx.DiGraph()
g_control = nx.DiGraph()

flow_node_list = ["f1", "f2", "f3", "f4", "f5", "f6"]
for i in range(17):
    ss = f"fo{i+1}"
    flow_node_list.append(ss)

control_node_list = []
for i in range(10):
    ss = f"c{i+1}"
    control_node_list.append(ss)
for i in range(14):
    ss = f"v{i+1}"
    control_node_list.append(ss)

flow_edge_list = [("f1", "fo1", 2), ("fo1", "fo2", 2), ("fo2", "fo3", 2), ("fo3", "fo4", 2), ("fo4", "f6", 2),
                  ("fo1", "fo5", 2), ("fo3", "fo7", 2), ("fo4", "fo9", 2),
                  ("f2", "fo5", 2), ("fo5", "fo6", 2), ("fo6", "fo7", 2), ("fo7", "fo8", 2), ("fo8", "fo9", 2),
                  ("fo5", "fo10", 2), ("fo7", "fo12", 2), ("fo9", "fo14", 2),
                  ("f3", "fo10", 2), ("fo10", "fo11", 2), ("fo11", "fo12", 2), ("fo12", "fo13", 2), ("fo13", "fo14", 2), ("fo14", "f5", 2),
                  ("fo15", "fo10", 2), ("fo16", "fo12", 2), ("fo17", "fo14", 2),
                  ("fo15", "fo16", 2), ("fo16", "fo17", 2), ("fo16", "f4", 2)
                  ]

control_edge_list = [("v1", "c1", 1), ("v2", "c2", 1), ("v3", "c3", 1), ("v4", "c6", 1), ("v5", "c5", 1),
                     ("v6", "c4", 1), ("v7", "c6", 1), ("v8", "c4", 1), ("v9", "c7", 1), ("v10", "c7", 1),
                     ("v11", "c9", 1), ("v12", "c10", 1), ("v13", "c7", 1), ("v14", "c8", 1)]

ValveLocation = [["v1", "fo5", "fo1"], ["v2", "fo5", "fo10"], ["v3", "fo10", "f15"], ["v4", "fo3", "fo7"], ["v5", "fo7", "fo12"],
                 ["v6", "fo12", "fo16"], ["v7", "fo7", "fo8"], ["v8", "fo12", "fo13"], ["v9", "fo3", "fo4"], ["v10", "fo8", "fo9"],
                 ["v11", "fo13", "fo14"], ["v12", "fo16", "fo7"], ["v13", "fo4", "fo9"], ["v14", "fo9", "fo14"]]

g_flow.add_nodes_from(flow_node_list)
g_flow.add_weighted_edges_from(flow_edge_list)

folder_path = "../TestCaseFiles/lrb/"

outpath1 = f"{folder_path}/lrb1_control.dot"
outpath2 = f"{folder_path}/lrb1_flow.dot"
outpath = f"{folder_path}/lrb1_ValveLocation.txt"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

write_dot(g_control, outpath1)
write_dot(g_flow, outpath2)
with open(outpath, 'w') as f:
    for i in ValveLocation:
        i = str(i).strip('[').strip(']').replace(',', '').replace('\'', '')+'\n'
        f.writelines(i)
