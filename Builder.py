#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from types import ModuleType

from GraphAst import *

class GraphBuilder:
	def __init__(self, ast, backend, **kwargs):
		self.ast = ast
		
		if isinstance(backend, ModuleType):
			backend = backend.default
			
		self.backend = backend()
		
		self.parameters = {}
		
		self.definitions = {}
		
		self.built_nodes = []
				
		self.graph_directed = kwargs.get('graph_directed')
		self.graph_init = kwargs.get('graph_init')
	
		
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
		
		if node.data is None:
			parsed_data = None
		else:
			parsed_data = {k: self.parse_value(v) for k, v in node.data.items()}
		
		n = self.backend.add_node(g, v, parsed_data)
		
		return n
	
	def parse_edge(self, node, g):
		assert isinstance(node, GraphAstEdge)
		
		n1 = self.parse_node(node.node1, g)
		n2 = self.parse_node(node.node2, g)
		
		
		parsed_data = {k: self.parse_value(v) for k, v in node.data.items()}
		
		if not self.graph_directed and node.left_char == '-' and node.right_char == '-':
			self.backend.add_edge(g, n1, n2, parsed_data)
		elif node.left_char == '-' and node.right_char == '>':
			self.backend.add_edge(g, n1, n2, parsed_data)
		elif node.left_char == '<' and node.right_char == '-':
			self.backend.add_edge(g, n2, n1, parsed_data)
		elif node.left_char == '<' and node.right_char == '>':
			self.backend.add_edge(g, n1, n2, parsed_data)
			self.backend.add_edge(g, n2, n1, parsed_data)
			
		return n1
	
	
	
	def parse_node(self, node, g):
		print (node)
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
		if node is None:
			return None
		
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
				g = self.backend.create_directed_graph()
			else:
				g = self.backend.create_undirected_graph()
		
		self.parse(self.ast, g)
		
		return g
	