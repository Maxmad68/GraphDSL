#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .abstract import Backend
from Exceptions import GraphBackendException
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
		identifier = id(value)
		if value is None:
			identifier = value = uuid.uuid4()
			
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
	