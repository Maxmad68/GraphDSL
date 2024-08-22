#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from GraphAst import *
import networkx as nx
import uuid

class GraphBuilder:
	def __init__(self, ast, **kwargs):
		self.ast = ast
		
		self.parameters = {}
		
		self.definitions = {}
		
		self.built_nodes = []
		
		self.nodes = {}
		
		self.graph_directed = kwargs.get('graph_directed')
		self.graph_init = kwargs.get('graph_init')
		
	def build_add_node(self, value, g, data):
		identifier = id(value)
		if value is None:
			identifier = value = uuid.uuid4()
			
		if data is None:
			g.add_node(value)
		else:
			parsed_data = {k: self.parse_value(v) for k, v in data.items()}
			
			g.add_node(value, **parsed_data)
		
		
		self.nodes[identifier] = value
		return identifier
	
	def build_add_edge(self, n1, n2, data, g):
		node1 = self.nodes[n1]
		node2 = self.nodes[n2]
		
		parsed_data = {k: self.parse_value(v) for k, v in data.items()}
		
		g.add_edge(node1, node2, **parsed_data)
		
	def parse_assignation(self, node, g):
		assert isinstance(node, GraphAstAssignation)
		
		name = node.name
		value = self.parse_node(node.value, g)
		
		self.definitions[name] = value
		
		return value
	
	def parse_getnode(self, node, g):
		assert isinstance(node, GraphAstGetNode)
		
		name = node.name
		if name not in self.definitions.keys():
			raise GraphNotDefinedException.NotDefined(name)
		n = self.definitions[name]
		
		return n
	
	def parse_nodedef(self, node, g):
		assert isinstance(node, GraphAstNodedef)
		
		v = self.parse_value(node.value)
		
		n = self.build_add_node(v, g, node.data)
		
		return n
	
	def parse_edge(self, node, g):
		assert isinstance(node, GraphAstEdge)
		
		n1 = self.parse_node(node.node1, g)
		n2 = self.parse_node(node.node2, g)
		
		if self.graph_directed and node.left_char == '-' and node.right_char == '-':
			self.build_add_edge(n1, n2, node.data, g)
		elif node.left_char == '-' and node.right_char == '>':
			self.build_add_edge(n1, n2, node.data, g)
		elif node.left_char == '<' and node.right_char == '-':
			self.build_add_edge(n2, n1, node.data, g)
		elif node.left_char == '<' and node.right_char == '>':
			self.build_add_edge(n1, n2, node.data, g)
			self.build_add_edge(n2, n1, node.data, g)
			
		return n1
	
	
	
	def parse_node(self, node, g):
		assert isinstance(node, GraphNode)
		
		if isinstance(node, GraphAstNodedef):
			n = self.parse_nodedef(node, g)
		elif isinstance(node, GraphAstGetNode):
			n = self.parse_getnode(node, g)
		elif isinstance(node, GraphAstAssignation):
			n = self.parse_assignation(node, g)
		elif isinstance(node, GraphAstEdge):
			n = self.parse_edge(node, g)
			
		self.built_nodes.append(n)
		
		return n
	
	
	def parse_literal_value(self, node):
		assert isinstance(node, GraphAstLitteralValue)
		
		return node.value
	
	
	def parse_get_value(self, node):
		assert isinstance(node, GraphAstGetValue)
		return self.parameters[node.name]
	
	
	def parse_value(self, node):
		assert isinstance(node, GraphAstValue)
		
		
		if isinstance(node, GraphAstLitteralValue):
			v = self.parse_literal_value(node)
		elif isinstance(node, GraphAstGetValue):
			v = self.parse_get_value(node)
			
		return v
			
	
	def parse(self, ast, g):
		assert isinstance(self.ast, GraphDef)
		
		for n in ast.nodes:
			self.parse_node(n, g)
			
			
	def build(self):
		if self.graph_init is not None:
			if isinstance(self.graph_init, tuple):
				g = self.graph_init[0].__call__(*self.graph_init[1:])
			else:
				g = self.graph_init.__call__()
		else:
			if self.graph_directed:
				g = nx.MultiDiGraph()
			else:
				g = nx.MultiGraph()
		
		self.parse(self.ast, g)
		
		return g
	