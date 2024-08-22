#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import inspect
from io import BytesIO
from Builder import GraphBuilder
from Compiler import GraphCompiler

class GraphFactory:
	def __init__(self, f, **kwargs):
		
		# Get parameters
		self.directed = kwargs.get('directed', True)
		self.debug_tokens = kwargs.get('debug_tokens', False)
		self.graph_init = kwargs.get('graph_init', None)
		self.default_node_params = kwargs.get('default_node_params', {})
		self.default_edge_params = kwargs.get('default_edge_params', {})
		
		source = inspect.getsource(f)
		b = BytesIO(source.encode('utf-8')).readline
		
		self.parser = GraphCompiler(
			b,
			self.debug_tokens,
			graph_directed=self.directed,
			default_node_params=self.default_node_params,
			default_edge_params=self.default_edge_params
		)
		
		self.ast = self.parser.compile_to_ast()
		
	def __call__(self, *args, **kwargs):
		builder = GraphBuilder(self.ast, graph_directed=self.directed, graph_init=self.graph_init)
		builder.parameters = kwargs
		return builder.build()
	
	
def Graph(**kwargs):
	def wrapper(f):
		return GraphFactory(f, **kwargs)
	
	return wrapper
	