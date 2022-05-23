import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import read_dot

path = f"Section_1/Node1_10_7_3_5_2_1_2_0/Edge1|16_14_2_flow.dot"
G = read_dot(path)
pos = nx.spring_layout(G)
color_list = ['blue' for i in range(len(G.nodes()))]
nx.draw_networkx(G, pos, nodelist=G.nodes(), node_color=color_list)
plt.show()
