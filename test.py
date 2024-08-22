#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from Factory import Graph
import networkx as nx
		
@Graph(directed=True)
def g():
	(1, {color:'red'})	-{coucou:42}>	(2, {color: 'blue'})		-{}>		(3, {color:'yellow'})
		


p = g()
print (p)


import sys
from networkx.drawing.nx_agraph import write_dot
import networkx as nx

import matplotlib
import matplotlib.pyplot

fig = matplotlib.pyplot.figure()
pos = nx.spring_layout(p)
nx.draw(p, pos, ax=fig.add_subplot(), node_color=[node[1]['color'] for node in p.nodes(data=True)])
nx.draw_networkx_edge_labels(p, pos)
nx.draw_networkx_labels(p, pos)

matplotlib.use("Agg")
fig.savefig("/Users/maxime/graph.png")


#write_dot(p, sys.stdout)