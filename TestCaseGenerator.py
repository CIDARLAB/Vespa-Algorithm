import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import write_dot

num = 1
g_flow = nx.DiGraph()
g_control = nx.DiGraph()
flow_node_list = ["f1", "f2", "f3", "fo1"]
control_node_list = ["c1", "c2", "c3", "v1", "v2", "v3"]
flow_edge_list = [("f1", "fo1", 2), ("f2", "fo1", 2), ("fo1", "f3", 2)]
control_edge_list = [("v1", "c1", 1), ("v2", "c2", 1), ("v3", "c3", 1)]

g_flow.add_nodes_from(flow_node_list)
g_flow.add_weighted_edges_from(flow_edge_list)
pos = nx.spring_layout(g_flow)
print(g_flow.nodes())
print(nx.info(g_flow))
outpath = f"TestCaseFiles/test_flow{num}.dot"
write_dot(g_flow, outpath)
color_list = ['blue' for i in range(len(flow_node_list))]
nx.draw_networkx(g_flow, pos, nodelist=flow_node_list, node_color=color_list)
plt.show()

g_control.add_nodes_from(control_node_list)
g_control.add_weighted_edges_from(control_edge_list)
pos = nx.spring_layout(g_control)
print(g_control.nodes())
print(nx.info(g_control))
outpath = f"TestCaseFiles/test_control{num}.dot"
write_dot(g_control, outpath)
color_list = ['red' for i in range(len(control_node_list))]
nx.draw_networkx(g_control, pos, nodelist=control_node_list, node_color=color_list)
plt.show()

ValveLocation = [["v1", "f1", "fo1"], ["v2", "f2", "fo1"], ["v3", "fo1", "f3"]]
outpath = f"TestCaseFiles/test_ValveLocation{num}.txt"
with open(outpath, 'w') as f:
    for i in ValveLocation:
        i = str(i).strip('[').strip(']').replace(',', '').replace('\'', '')+'\n'
        f.writelines(i)
