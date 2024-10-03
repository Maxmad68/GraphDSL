#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import inspect
import marshal
from io import BytesIO
from Builder import GraphBuilder
from Compiler import GraphCompiler
import backend.networkx

class GraphFactory:
	def __init__(self, f, **kwargs):
		
		# Get parameters
		self.directed = kwargs.get('directed', True)
		self.debug_tokens = kwargs.get('debug_tokens', False)
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
		
	def __call__(self, parameters={}, backend=backend.networkx, **kwargs):
		
		graph_init = kwargs.get('graph_init', None)
		
		builder = GraphBuilder(
			self.ast,
			backend,
			graph_directed=self.directed,
			graph_init=graph_init
		)
		
		builder.parameters = {**parameters}
		return builder.build()
		
	
def Graph(**kwargs):
	def wrapper(f):
		return GraphFactory(f, **kwargs)
	
	return wrapper
	