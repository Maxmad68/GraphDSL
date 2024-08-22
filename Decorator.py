#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import inspect
from io import BytesIO
from Builder import GraphBuilder
from Compiler import GraphCompiler

class GraphFactory:
	def __init__(self, f):
		source = inspect.getsource(f)
		b = BytesIO(source.encode('utf-8')).readline
		self.parser = GraphCompiler(b)
		self.ast = self.parser.compile_to_ast()
		
	def __call__(self, *args, **kwargs):
		builder = GraphBuilder(self.ast)
		builder.parameters = kwargs
		print (args)
		return builder.build()
	
Graph = GraphFactory