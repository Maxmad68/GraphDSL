#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from Decorator import Graph		
		
@Graph
def g():
	('A') -{}> ('B') -{}> ('E') -{}> ('D') -{}> ('C') -{}> ('B')
	('A') -{}> ('D') -{}> ('B')
	


p = g()
print (p)


import sys
from networkx.drawing.nx_agraph import write_dot
import networkx as nx

import matplotlib
import matplotlib.pyplot

fig = matplotlib.pyplot.figure()
pos = nx.spring_layout(p)
nx.draw(p, pos, ax=fig.add_subplot())
nx.draw_networkx_edge_labels(p, pos)
nx.draw_networkx_labels(p, pos)

matplotlib.use("Agg")
fig.savefig("/Users/maxime/graph.png")


#write_dot(p, sys.stdout)