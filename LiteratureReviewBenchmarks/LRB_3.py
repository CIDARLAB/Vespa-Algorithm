import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import write_dot

g_flow = nx.DiGraph()
g_control = nx.DiGraph()

flow_node_list = []
for i in range(9):
    str = f"f{i+1}"
    flow_node_list.append(str)

for i in range(15):
    str = f"fo{i+1}"
    flow_node_list.append(str)

control_node_list = []
for i in range(13):
    str = f"c{i+1}"
    control_node_list.append(str)
for i in range(25):
    str = f"v{i+1}"
    control_node_list.append(str)

flow_edge_list = [("f1", "fo1", 2), ("f2", "fo2", 2), ("f3", "fo4", 2), ("f4", "fo5", 2),
                  ("fo2", "fo1", 2), ("fo3", "fo2", 2), ("fo3", "fo4", 2), ("fo4", "fo5", 2),
                  ("fo3", "fo8", 2), ("fo8", "fo9", 2), ("f5", "fo8", 2),
                  ("fo6", "fo7", 2), ("fo9", "fo7", 2), ("fo10", "fo9", 2), ("fo11", "fo10", 2),
                  ("fo6", "fo12", 2), ("fo13", "fo7", 2), ("fo10", "fo14", 2), ("fo11", "fo15", 2),
                  ("f6", "fo12", 2), ("fo13", "f7", 2), ("f8", "fo14", 2), ("fo9", "fo15", 2)
                  ]

control_edge_list = [("v1", "c1", 1), ("v2", "c8", 1), ("v3", "c1", 1), ("v4", "c2", 1), ("v5", "c7", 1),
                     ("v6", "c8", 1), ("v7", "c7", 1), ("v8", "c2", 1), ("v9", "c13", 1), ("v10", "c3", 1),
                     ("v11", "c4", 1), ("v12", "c3", 1), ("v13", "c10", 1), ("v14", "c9", 1), ("v15", "c4", 1),
                     ("v16", "c9", 1), ("v17", "c10", 1), ("v18", "c5", 1), ("v19", "c6", 1), ("v20", "c5", 1),
                     ("v21", "c12", 1), ("v22", "c11", 1), ("v23", "c6", 1), ("v24", "c11", 1), ("v25", "c12", 1)
                     ]

ValveLocation = [["v1", "f1", "fo1"], ["v2", "f1", "fo1"], ["v3", "f2", "fo2"], ["v4", "f2", "fo2"], ["v5", "f3", "fo4"],
                 ["v6", "f3", "fo4"], ["v7", "f4", "fo5"], ["v8", "f4", "fo5"], ["v9", "f5", "fo8"], ["v10", "fo6", "fo12"],
                 ["v11", "fo6", "fo12"], ["v12", "fo13", "fo7"], ["v13", "fo13", "fo7"], ["v14", "fo9", "fo14"],
                 ["v15", "fo10", "fo14"], ["v16", "fo11", "fo15"], ["v17", "fo11", "fo15"], ["v18", "fo12", "f6"],
                 ["v19", "f6", "fo12"], ["v20", "fo13", "f7"], ["v21", "fo13", "f7"], ["v22", "f8", "fo14"],
                 ["v23", "f8", "fo14"], ["v24", "f9", "fo15"], ["v25", "fo9", "fo15"]
                 ]

g_flow.add_nodes_from(flow_node_list)
g_flow.add_weighted_edges_from(flow_edge_list)

outpath1 = f"TestCaseFiles/lrb3_control.dot"
outpath2 = f"TestCaseFiles/lrb3_flow.dot"
outpath = f"TestCaseFiles/lrb3_ValveLocation.txt"

write_dot(g_control, outpath1)
write_dot(g_flow, outpath2)
with open(outpath, 'w') as f:
    for i in ValveLocation:
        i = str(i).strip('[').strip(']').replace(',', '').replace('\'', '')+'\n'


