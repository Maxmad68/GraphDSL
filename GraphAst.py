#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass

@dataclass
class GraphAst:
	pass
	
	
# Values	
@dataclass	
class GraphAstValue(GraphAst):
	pass
	
@dataclass
class GraphAstLitteralValue(GraphAstValue):
	value: object
	
@dataclass
class GraphAstGetValue(GraphAstValue):
	name: str
	
	
# Nodes
@dataclass
class GraphNode (GraphAst):
	pass
	
@dataclass
class GraphAstAssignation (GraphNode):
	name: str
	value: GraphNode
	
@dataclass
class GraphAstGetNode (GraphNode):
	name: str
	
@dataclass
class GraphAstNodedef (GraphNode):
	value: object
	
@dataclass
class GraphAstEdge (GraphNode):
	node1: GraphNode
	node2: GraphNode
	value: object
	left_char: str
	right_char: str
	
	
# Root
@dataclass	
class GraphDef (GraphAst):
	nodes: [GraphNode]