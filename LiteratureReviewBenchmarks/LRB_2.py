import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import write_dot

g_flow = nx.DiGraph()
g_control = nx.DiGraph()

flow_node_list = ["f1", "f2", "f3", "f4"]
for i in range(12):
    str = f"fo{i+1}"
    flow_node_list.append(str)

control_node_list = []
for i in range(8):
    str = f"c{i+1}"
    control_node_list.append(str)
for i in range(8):
    str = f"v{i+1}"
    control_node_list.append(str)

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

outpath1 = f"TestCaseFiles/lrb2_control.dot"
outpath2 = f"TestCaseFiles/lrb2_flow.dot"
outpath = f"TestCaseFiles/lrb2_ValveLocation.txt"

write_dot(g_control, outpath1)
write_dot(g_flow, outpath2)
with open(outpath, 'w') as f:
    for i in ValveLocation:
        i = str(i).strip('[').strip(']').replace(',', '').replace('\'', '')+'\n'
        f.writelines(i)

