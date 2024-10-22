#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from factory import Graph
import GraphDSL.backend.networkx
import GraphDSL.backend.igraph
import networkx as nx

import timeit
		
@Graph(directed=True)
def g(c, l):
	(42) -{}> (84)
	


print (g.ast)

p = g(parameters={'c': 'red', 'l': 42})
		

print (p)


import sys
from networkx.drawing.nx_agraph import write_dot
import networkx as nx

import matplotlib
import matplotlib.pyplot

fig = matplotlib.pyplot.figure()
pos = nx.spring_layout(p)
labels = {n: p.nodes[n].get('label', n) for n in p.nodes()}
colors = [node[1]['color'] for node in p.nodes(data=True)]
nx.draw(p, pos, ax=fig.add_subplot(), labels=labels, node_color=colors)
nx.draw_networkx_edge_labels(p, pos)

fig.savefig("/Users/ep/graph.png")
	