import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import read_dot

path = f"Section_2/Node2_17_14_3_10_4_2_1_0/Edge8|15_14_1_flow.dot"
G = read_dot(path)
pos = nx.spring_layout(G)
color_list = ['blue' for i in range(len(G.nodes()))]
nx.draw_networkx(G, pos, nodelist=G.nodes(), node_color=color_list)
plt.show()
