import networkx
import pylab

#Build a graph (Node attribute 's' determines the node shape here)
G = networkx.Graph()
G.add_node(0, s="^", b=1)
G.add_node(1, s="x", b=2)

''''G.add_node(2, s="o", b=3)
G.add_node(3, s="o", b=4)

G.add_node(4, s="v", b=5)
G.add_node(5, s="v", b=6)'''

G.add_path([0,1])
#G.add_path([0,2,5])
''''G.add_path([1,4,3,0])
G.add_path([2,4,0,5])'''

#Drawing the graph
#First obtain the node positions using one of the layouts
nodePos = networkx.layout.spring_layout(G)

#The rest of the code here attempts to automate the whole process by
#first determining how many different node classes (according to
#attribute 's') exist in the node set and then repeatedly calling 
#draw_networkx_node for each. Perhaps this part can be optimised further.

#Get all distinct node classes according to the node shape attribute
nodeShapes = set((aShape[1]["s"] for aShape in G.nodes(data = True)))

#For each node class...
for aShape in nodeShapes:
    #...filter and draw the subset of nodes with the same symbol in the positions that are now known through the use of the layout.
    networkx.draw_networkx_nodes(G,nodePos,node_shape = aShape, nodelist = [sNode[0] for sNode in filter(lambda x: x[1]["s"]==aShape,G.nodes(data = True))])

pos=networkx.get_node_attributes(G,'pos')
#Finally, draw the edges between the nodes
'''etiquetas={}
for n in pos.keys():
    etiquetas[n]=[pos[n][0]+0.05,pos[n][1]+0.01]'''
            
networkx.draw_networkx_edges(G,nodePos)
#networkx.draw_networkx_labels(G)

#And show the final result
pylab.show()