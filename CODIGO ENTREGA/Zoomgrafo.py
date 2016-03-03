import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

filename = 'labe.png'
G = nx.complete_graph(10)
pos = nx.spring_layout(G)
xy = np.row_stack([point for key, point in pos.iteritems()])
x, y = np.median(xy, axis=0)
fig, ax = plt.subplots()
nx.draw(G, pos, with_labels=False, node_size=1)
ax.set_xlim(x-0.25, x+0.25)
ax.set_ylim(y-0.25, y+0.25)
plt.savefig(filename, bbox_inches=0, orientation='landscape', pad_inches=0.1)