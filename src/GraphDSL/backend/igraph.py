#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .abstract import Backend
from GraphDSL.exceptions import GraphBackendException

try:
	import igraph as ig
except ImportError:
	imported = False
else:
	imported = True

class IGraphBackend(Backend):
	def __init__(self):
		
		if not imported:
			raise GraphBackendException("Can't import module igraph")
			
		self.__name__ = 'igraph'
		
		self.nodes = {}
		
		
	def create_directed_graph(self):
		return ig.Graph(directed=True)
	
	def create_undirected_graph(self):
		return ig.Graph(directed=False)
	
	def add_node(self, graph, value, data):
		if value is None:
			return graph.add_vertex(name=value, attr=data)
		
		if value in self.nodes.keys():
			return self.nodes[value]
		
		node = graph.add_vertex(name=value, attr=data)
		self.nodes[value] = node
		
		return node
		
	def add_edge(self, graph, n1, n2, data):
		return graph.add_edge(n1, n2, **data)
		
	
default = IGraphBackend
	