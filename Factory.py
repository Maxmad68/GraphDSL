#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import inspect
from io import BytesIO
from Builder import GraphBuilder
from Compiler import GraphCompiler

class GraphFactory:
	def __init__(self, f, **kwargs):
		
		self.directed = kwargs.get('directed', True)
		
		source = inspect.getsource(f)
		b = BytesIO(source.encode('utf-8')).readline
		self.parser = GraphCompiler(b, True, graph_directed=self.directed)
		self.ast = self.parser.compile_to_ast()
		
	def __call__(self, *args, **kwargs):
		builder = GraphBuilder(self.ast, graph_directed=self.directed)
		builder.parameters = kwargs
		return builder.build()
	
	
def Graph(**kwargs):
	def wrapper(f):
		return GraphFactory(f, **kwargs)
	
	return wrapper
	