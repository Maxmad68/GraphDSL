#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from Factory import Graph
import backend.networkx
import backend.igraph
import networkx as nx

import timeit
		
@Graph(directed=True)
def g(c, l):
	(1, {color: c}) -{length: l}> (2, {color: c})
	


print (g.ast)

p = g(parameters={'c': 'red', 'l': 42})
		

print (p)



#
import sys
from networkx.drawing.nx_agraph import write_dot
import networkx as nx

import matplotlib
import matplotlib.pyplot

fig = matplotlib.pyplot.figure()
pos = nx.spring_layout(p)
d = {n: p.nodes[n].get('label', n) for n in p.nodes()}
nx.draw(p, pos, ax=fig.add_subplot(), labels=d)#, node_color=[node[1]['color'] for node in p.nodes(data=True)])
nx.draw_networkx_edge_labels(p, pos)

matplotlib.use("Agg")
fig.savefig("/Users/ep/graph.png")
	