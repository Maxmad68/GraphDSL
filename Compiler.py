#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tokenize
from GraphAst import *
from Exceptions import *

class GraphCompiler:
	def __init__(self, source, debug_tokens=False, **kwargs):
		
		self.graph_directed = kwargs.get('graph_directed')
		self.default_node_params = {k: GraphAstLitteralValue(v) for k, v in kwargs.get('default_node_params').items()}
		self.default_edge_params = {k: GraphAstLitteralValue(v) for k, v in kwargs.get('default_edge_params').items()}
		
		self.tokens = tokenize.tokenize(source)
		
		# Debug
		if debug_tokens:
			t2 = [*self.tokens]
			self.tokens = iter(t2)
			
			for g in t2:
				print (g)
			
			
	def shift_start(self):
		# Jump to method content
		nl_level = 0
		for t in self.tokens:			
			if t.type == 4:
				nl_level += 1
			if nl_level == 2:
				break
			
	def parse_nodedef(self):
		'''
			nodedef: '(' value ')'
		'''
		# Opening parenthesis has alerady been removed by parse_node
		# First value should then be the value
		
		#Only supports single-value (int & string) for the moment
		
		vt = next(self.tokens, None)
		if vt is None:
			raise GraphSyntaxException.Expected('(value),"}"')
		elif vt.type == tokenize.OP and vt.string == ')': # Empty node
			return GraphAstNodedef(None, {**self.default_node_params})
		
		val = self.parse_value(vt)
	
		closing = next(self.tokens, None)
		if closing is None:
			raise GraphSyntaxException.Expected('")",","')
			
		elif not (closing.type == tokenize.OP and closing.string in (')',',')):
			raise GraphSyntaxException.Expected('")",","', closing.string)
			
		elif closing.type == tokenize.OP and closing.string == ')': # (42)
			return GraphAstNodedef(val, {**self.default_node_params})
			
		elif closing.type == tokenize.OP and closing.string == ',': # (42, {abc:def})
			n = next(self.tokens, None)
			if n is None:
				raise GraphSyntaxException.Expected('"{"')
			elif not (n.type == tokenize.OP and n.string == '{'):
				raise GraphSyntaxException.Expected('"{",","', n)
				
			data = self.parse_dict()
			
			n = next(self.tokens, None)
			if n is None:
				raise GraphSyntaxException.Expected('")"')
			elif not (n.type == tokenize.OP and n.string == ')'):
				raise GraphSyntaxException.Expected('")"', n)
				
			return GraphAstNodedef(val, {**self.default_node_params, **data})
			
			
				
	def parse_value(self, n=None):
		
		if n is None:
			n = next(self.tokens, None)
			
		if n is None:
			raise GraphSyntaxException.Expected('(value)')
		if n.type == tokenize.NAME:
			return GraphAstGetValue(n.string)
		if n.type not in (tokenize.STRING, tokenize.NUMBER):
			raise GraphSyntaxException.Expected('(value)', n)
		val = eval(n.string)
		
		return GraphAstLitteralValue(val)
	
	
	def parse_dict(self):
		data = {}	
		
		n = next(self.tokens, None)
		while n is None or not (n.type == tokenize.OP and n.string == '}'):
			
			if n is None:
				raise GraphSyntaxException.Expected('"}", (name)')
				
			if n.type == tokenize.NAME:
				key = n.string
				n = next(self.tokens, None)
				
				if n is None:
					raise GraphSyntaxException.Expected('":"')
				if not (n.type == tokenize.OP and n.string == ':'):
					raise GraphSyntaxException.Expected('":"', n)
					
				val = self.parse_value()
				data[key] = val
				
				
				n = next(self.tokens, None)
				if n is None:
					raise GraphSyntaxException.Expected('",", "}"')
				elif (n.type == tokenize.OP and n.string == '}'):
					break
				elif (n.type == tokenize.OP and n.string == ','):
					continue
				else:
					raise GraphSyntaxException.Expected('",", "}"', n)
					
			elif (n.type == tokenize.OP and n.string == '}'):
				break
			
			
			
		return data
	
	
	def parse_edge_data(self):
		n = next(self.tokens, None)
		if n is None:
			raise GraphSyntaxException.Expected('"{"')
		if not (n.type == tokenize.OP and n.string == '{'):
			raise GraphSyntaxException.Expected('"{"', n.string) 
			
		
		data = {**self.default_edge_params, **self.parse_dict()}
		return data
		
		
	def parse_edge(self, left_token, left_node):
		data = self.parse_edge_data()
		
		right_token = next(self.tokens, None)
		if right_token is None:
			raise GraphSyntaxException.Expected('">", "-"')
		elif not (right_token.type == tokenize.OP and right_token.string in ('>','-')):
			raise GraphSyntaxException.Expected('">", "-"', right_token)
			
		if self.graph_directed:
			if left_token.string == '-' and right_token.string == '-':
				raise GraphException("Can't add undirected edge to directed graph")
		else:
			if left_token.string != '-' or right_token.string != '-':
				raise GraphException("Can't add directed edge to undirected graph")
			
		right_node = self.parse_node()
		
		return GraphAstEdge(left_node, right_node, data, left_token.string, right_token.string)
	
	def parse_node(self, first=None):
		'''
			node: nodedef
					| name
					| node edge node 
					| name = node
		'''
		
#		print('\nParse node')
		
		if first is None:
			t = next(self.tokens)
		else:
			t = first
			
#		print ('\t', t)
		
		tree = None
		if t.type == tokenize.NAME: # a ...
			n = next(self.tokens, tokenize.ENDMARKER)
			if n.type == tokenize.OP and n.string == '=': # a = ...
		
				node = self.parse_node()
				return GraphAstAssignation(t.string, node)
			
			elif n.type == tokenize.OP and n.string == ':': # a := ...
				n = next(self.tokens, tokenize.ENDMARKER)
				if n is None:
					raise GraphSyntaxException.Expected('"="')
				if not (n.type == tokenize.OP and n.string == '='):
					raise GraphSyntaxException.Expected('"="', n)
	
				node = self.parse_node()
				return GraphAstAssignation(t.string, node)
	
			elif n.type == tokenize.OP and n.string in ('<','-'): # a -{}> ...
				edge = self.parse_edge(n, GraphAstGetNode(t.string))
				return edge
	
			elif n.type == tokenize.NEWLINE: # 'a'
				return GraphAstGetNode(t.string)
	
			else:
				raise GraphSyntaxException.Expected('(eol)', n)
				
				
		elif t.type == tokenize.OP and t.string == '(': # () ...
			tree = self.parse_nodedef()
			n = next(self.tokens, tokenize.ENDMARKER)
	
			if n.type == tokenize.OP and n.string in ('<', '-'): # () -{}> ...
				return self.parse_edge(n, tree)
	
			elif n.type == tokenize.NEWLINE:  # ()
				return tree
	
#		print ('\t end', t)
	
	
	def parse_graph(self):
		'''
			graph: node (nl+ node)*
		'''
		nodes = []
		
		for t in self.tokens:
			
			if t.type in (tokenize.NEWLINE, tokenize.NL):
				continue
			elif t.type not in (tokenize.INDENT, tokenize.DEDENT, tokenize.ENDMARKER):
				nodes.append(self.parse_node(t))
				
		return GraphDef(nodes)
	
	
	def compile_to_ast(self):
		self.shift_start()
		return self.parse_graph()
	