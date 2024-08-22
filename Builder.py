#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from GraphAst import *
import networkx as nx
import uuid

class GraphBuilder:
	def __init__(self, ast):
		self.ast = ast
		
		self.parameters = {}
		
		self.definitions = {}
		
		self.built_nodes = []
		
		self.nodes = {}
		
	def build_add_node(self, value, g):
		identifier = id(value)
		if value is None:
			identifier = value = uuid.uuid4()
		g.add_node(value)
		
		
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
		
		n = self.build_add_node(v, g)
		
		return n
	
	def parse_edge(self, node, g):
		assert isinstance(node, GraphAstEdge)
		
		n1 = self.parse_node(node.node1, g)
		n2 = self.parse_node(node.node2, g)
		
		e = self.build_add_edge(n1, n2, node.value, g)
		#e = g.add_edge(n1, n2, data=node.value)
		
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
		print (node.name)
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
		g = nx.DiGraph()
		
		self.parse(self.ast, g)
		
		return g
	