#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .abstract import Backend
from GraphDSL.exceptions import GraphBackendException
import uuid

try:
	import networkx as nx
except ImportError:
	imported = False
else:
	imported = True

class NetworkXBackend(Backend):
	def __init__(self):
		
		if not imported:
			raise GraphBackendException("Can't import module networkx")
			
		self.__name__ = 'networkx'
		
		self.nodes = {}
		
	def create_directed_graph(self):
		return nx.MultiDiGraph()
	
	def create_undirected_graph(self):
		return nx.MultiGraph()
	
	def add_node(self, graph, value, data):
		if value is None:
			value = len(self.nodes)
		
		identifier = value
		
			
		if data is None:
			graph.add_node(value)
		else:
			graph.add_node(value, **data)
			
			
		self.nodes[identifier] = value
		return identifier
	
	def add_edge(self, graph, n1, n2, data):
		node1 = self.nodes[n1]
		node2 = self.nodes[n2]
		
		graph.add_edge(node1, node2, **data)

	
default = NetworkXBackend
	
	
def draw_nx(p):
	from networkx.drawing.nx_agraph import write_dot
	import networkx as nx
	
	import matplotlib
	import matplotlib.pyplot
	
	fig = matplotlib.pyplot.figure()
	pos = nx.spring_layout(p)
	labels = {n: p.nodes[n].get('label', n) for n in p.nodes()}
	colors = [node[1].get('color','black') for node in p.nodes(data=True)]
	nx.draw(p, pos, ax=fig.add_subplot(), labels=labels, node_color=colors)
	nx.draw_networkx_edge_labels(p, pos)