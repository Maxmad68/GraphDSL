#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tokenize

class GraphException(Exception):
	pass


class GraphSyntaxException(GraphException):
	
	@staticmethod
	def BadFollow(token1, token2):
		return GraphSyntaxException(f'"{token1.string}" can\'t be followed by "{token2.string}"')
	
	@staticmethod
	def Expected(what=[], got='(eol)'):
		if isinstance(got, tokenize.TokenInfo):
			got = f'"{got.string}"'
			
		return GraphSyntaxException(f'Expected {what} but got {got}')
	
	
class GraphNotDefinedException(GraphException):
	@staticmethod
	def NotDefined(name):
		return GraphNotDefinedException(f'Parameter "{name}" not defined')