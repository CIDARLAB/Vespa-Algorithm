import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import write_dot

g_flow = nx.DiGraph()
g_control = nx.DiGraph()

flow_node_list = ["f1", "f2", "f3", "f4", "f5", "f6"]
for i in range(17):
    str = f"fo{i+1}"
    flow_node_list.append(str)

control_node_list = []
for i in range(10):
    str = f"c{i+1}"
    control_node_list.append(str)
for i in range(14):
    str = f"v{i+1}"
    control_node_list.append(str)

flow_edge_list = [("f1", "fo1", 2), ("fo1", "fo2", 2), ("fo1", "f3", 2)]

control_edge_list = [("v1", "c1", 1), ("v2", "c2", 1), ("v3", "c3", 1)]

g_flow.add_nodes_from(flow_node_list)
g_flow.add_weighted_edges_from(flow_edge_list)
print(g_flow.nodes())
print(nx.info(g_flow))
outpath1 = f"TestCaseFiles/literature_review_benchmark1.dot"


