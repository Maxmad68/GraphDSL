#!/usr/bin/env python3

import unittest
import context

from GraphDSL import Graph
from GraphDSL.graphAst import *
from GraphDSL.exceptions import *

class TestCompilingMethods(unittest.TestCase):
	
	def test_simple_node(self):
		@Graph(directed=True)
		def g():
			(42)
			
		expected = GraphDef(nodes=[
				GraphAstNodedef(
					value=GraphAstLitteralValue(value=42),
					data={}
				)
			])
			
		self.assertEqual(g.ast, expected)
		
	
		
	def test_two_nodedefs(self):
		@Graph(directed=True)
		def g():
			(1)
			('a')
			
		expected = GraphDef(nodes=[
			GraphAstNodedef(
				value=GraphAstLitteralValue(value=1),
				data={}
			),
			GraphAstNodedef(value=
				GraphAstLitteralValue(value='a'),
				data={}
			)
		])
		
		self.assertEqual(g.ast, expected)
		
		
	def test_two_nodedefs_with_properties(self):
		@Graph(directed=True)
		def g():
			(1, {label: "Hello World", weight: 123})
			(2, {color: 'red'})
			
		expected = GraphDef(nodes=[
			GraphAstNodedef(
				value=GraphAstLitteralValue(value=1),
				data={'label': GraphAstLitteralValue(value='Hello World'), 'weight': GraphAstLitteralValue(value=123)}),
			GraphAstNodedef(
				value=GraphAstLitteralValue(value=2),
				data={'color': GraphAstLitteralValue(value='red')}
			)
		])
		
		self.assertEqual(g.ast, expected)
		
	
	# Tests Assignation
		
	def test_node_assignation(self):
		@Graph(directed=True)
		def g():
			a = (1)
			
		expected = GraphDef(nodes=[
			GraphAstAssignation(
				name='a',
				value=GraphAstNodedef(
					value=GraphAstLitteralValue(value=1),
					data={}
				)
			)
		])
		
		self.assertEqual(g.ast, expected)
		
		
	def test_multiple_node_assignation_with_properties(self):
		@Graph(directed=True)
		def g():
			a = ('A', {letter: 1})
			b = (2, {property: 72})
			
		expected = GraphDef(nodes=[
			GraphAstAssignation(
				name='a',
				value=GraphAstNodedef(
					value=GraphAstLitteralValue(value='A'),
					data={'letter': GraphAstLitteralValue(value=1)}
				)
			),
			GraphAstAssignation(
				name='b',
				value=GraphAstNodedef(
					value=GraphAstLitteralValue(value=2),
					data={'property': GraphAstLitteralValue(value=72)})
			)
		])
		
		self.assertEqual(g.ast, expected)
	
	# Tests Get
	
	def test_get(self):
		@Graph(directed=True)
		def g():
			a
			
		expected = GraphDef(nodes=[
			GraphAstGetNode(name='a')
		])
		
		self.assertEqual(g.ast, expected)
		
		
	# Tests Edge
	
	def test_directed_edge(self):
		@Graph(directed=True)
		def g():
			(1) -{}> (2)
		
		expected = GraphDef(nodes=[
			GraphAstEdge(
				node1=GraphAstNodedef(value=GraphAstLitteralValue(value=1), data={}),
				node2=GraphAstNodedef(value=GraphAstLitteralValue(value=2), data={}),
				data={},
				left_char='-',
				right_char='>'
			)
		])
		
		self.assertEqual(g.ast, expected)
		
	def test_undirected_edge(self):
		@Graph(directed=False)
		def g():
			(1) -{}- (2)
			
		expected = GraphDef(nodes=[
			GraphAstEdge(
				node1=GraphAstNodedef(value=GraphAstLitteralValue(value=1), data={}),
				node2=GraphAstNodedef(value=GraphAstLitteralValue(value=2), data={}),
				data={},
				left_char='-',
				right_char='-'
			)
		])
		
		self.assertEqual(g.ast, expected)
		
	def test_directed_edge_with_properties(self):
		@Graph(directed=True)
		def g():
			(1) -{length: 42, color: 'red'}> (2)
			
		expected = GraphDef(nodes=[
			GraphAstEdge(
				node1=GraphAstNodedef(value=GraphAstLitteralValue(value=1), data={}),
				node2=GraphAstNodedef(value=GraphAstLitteralValue(value=2), data={}),
				data={'length': GraphAstLitteralValue(value=42), 'color': GraphAstLitteralValue(value='red')},
				left_char='-',
				right_char='>'
			)
		])
		
		
		self.assertEqual(g.ast, expected)
		
	def test_undirected_edge_on_directed_graph(self):
		'''
		Should raise a GraphException because adding an undirected edge to a directed Graph is forbidden
		'''
		
		def build_graph():
			@Graph(directed=True)
			def g():
				(1) -{}- (2)
			
		self.assertRaises(GraphException, build_graph)
		
	def test_directed_edge_on_undirected_graph(self):
		'''
		Should raise a GraphException because adding a directed edge to an undirected Graph is forbidden
		'''
		
		def build_graph():
			@Graph(directed=False)
			def g():
				(1) -{}> (2)
				
		self.assertRaises(GraphException, build_graph)
		
	def test_multiple_edges(self):
		@Graph(directed=True)
		def g():
			(1) -{}> (2) -{}> (3)
			(4) <{}- (5)
		
		expected = GraphDef(nodes=[
			GraphAstEdge(
				node1=GraphAstNodedef(value=GraphAstLitteralValue(value=1), data={}),
				node2=GraphAstEdge(
					node1=GraphAstNodedef(value=GraphAstLitteralValue(value=2), data={}),
					node2=GraphAstNodedef(value=GraphAstLitteralValue(value=3), data={}),
					data={},
					left_char='-',
					right_char='>'
				),
				data={},
				left_char='-',
				right_char='>'
			),
			GraphAstEdge(
				node1=GraphAstNodedef(value=GraphAstLitteralValue(value=4), data={}),
				node2=GraphAstNodedef(value=GraphAstLitteralValue(value=5), data={}),
				data={},
				left_char='<',
				right_char='-'
			)
		])
		
		self.assertEqual(g.ast, expected)
		
	def test_assignation_edges_with_properties(self):
		@Graph(directed=True)
		def g():
			a = (1, {color: 'blue'}) -{length: 42}> (2)
			a -{property: 72, length: 89}> (3)
		
		expected = GraphDef(nodes=[
			GraphAstAssignation(
				name='a',
				value=GraphAstEdge(
					node1=GraphAstNodedef(
						value=GraphAstLitteralValue(value=1),
						data={'color': GraphAstLitteralValue(value='blue')}
					),
					node2=GraphAstNodedef(
						value=GraphAstLitteralValue(value=2),
						data={}
					),
					data={'length': GraphAstLitteralValue(value=42)},
					left_char='-',
					right_char='>'
				)
			),
			GraphAstEdge(
				node1=GraphAstGetNode(name='a'),
				node2=GraphAstNodedef(
					value=GraphAstLitteralValue(value=3),
					data={}
				),
				data={'property': GraphAstLitteralValue(value=72), 'length': GraphAstLitteralValue(value=89)},
				left_char='-',
				right_char='>'
			)
		])
		
		self.assertEqual(g.ast, expected)
		
	# Tests Get Value
	
	def test_get_single_value(self):
		@Graph(directed=True)
		def g(ext):
			(ext)
			
		expected = GraphDef(nodes=[
			GraphAstNodedef(
				value=GraphAstGetValue(name='ext'),
				data={}
			)
		])
		
		self.assertEqual(g.ast, expected)
		
	def test_get_multiple_values(self):
		@Graph(directed=True)
		def g(val1, val2, length):
			(val1) -{length: length}> (val2)
		
		expected = GraphDef(nodes=[
			GraphAstEdge(
				node1=GraphAstNodedef(
					value=GraphAstGetValue(name='val1'),
					data={}
				),
				node2=GraphAstNodedef(
					value=GraphAstGetValue(name='val2'),
					data={}
				),
				data={'length': GraphAstGetValue(name='length')},
				left_char='-',
				right_char='>'
			)
		])
		
		self.assertEqual(g.ast, expected)
		
	def test_get_redefined_value(self):
		@Graph(directed=True)
		def g(a):
			a = (a)
			a -{}> a
			
		expected = GraphDef(nodes=[
			GraphAstAssignation(
				name='a',
				value=GraphAstNodedef(
					value=GraphAstGetValue(name='a'),
					data={}
				)
			),
			GraphAstEdge(
				node1=GraphAstGetNode(name='a'),
				node2=GraphAstGetNode(name='a'),
				data={},
				left_char='-',
				right_char='>'
			)
		])
		
		self.assertEqual(g.ast, expected)
		
		
	# Tests default properties
	
	def test_nodes_with_default_properties(self):
		@Graph(directed=True, default_node_params={'abc':42,'xyz':'Foo Bar'})
		def g():
			(42)
			(72)
			
		expected = GraphDef(nodes=[
			GraphAstNodedef(
				value=GraphAstLitteralValue(value=42),
				data={'abc': GraphAstLitteralValue(value=42), 'xyz': GraphAstLitteralValue(value='Foo Bar')}
			),
			GraphAstNodedef(
				value=GraphAstLitteralValue(value=72),
				data={'abc': GraphAstLitteralValue(value=42), 'xyz': GraphAstLitteralValue(value='Foo Bar')}
			)
		])
		
		self.assertEqual(g.ast, expected)
		
	def test_nodes_with_default_properties_merge(self):
		@Graph(directed=True, default_node_params={'abc':42,'xyz':'Foo Bar'})
		def g():
			(42, {foo: 'bar'})
			(72, {hello: 'world'})
			
		expected = GraphDef(nodes=[
			GraphAstNodedef(
				value=GraphAstLitteralValue(value=42),
				data={
					'abc': GraphAstLitteralValue(value=42),
					'xyz': GraphAstLitteralValue(value='Foo Bar'),
					'foo': GraphAstLitteralValue(value='bar')
				}
			),
			GraphAstNodedef(
				value=GraphAstLitteralValue(value=72),
				data={
					'abc': GraphAstLitteralValue(value=42),
					'xyz': GraphAstLitteralValue(value='Foo Bar'),
					'hello': GraphAstLitteralValue(value='world')
				}
			)
		])
		
		self.assertEqual(g.ast, expected)
		
	def test_nodes_with_default_properties_override(self):
		@Graph(directed=True, default_node_params={'abc':42,'xyz':'Foo Bar'})
		def g():
			(42, {abc: 72})
			(72, {xyz: 126})
			
		expected = GraphDef(nodes=[
			GraphAstNodedef(
				value=GraphAstLitteralValue(value=42),
				data={'abc': GraphAstLitteralValue(value=72), 'xyz': GraphAstLitteralValue(value='Foo Bar')}
			),
			GraphAstNodedef(
				value=GraphAstLitteralValue(value=72),
				data={'abc': GraphAstLitteralValue(value=42), 'xyz': GraphAstLitteralValue(value=126)}
			)
		])
		
		self.assertEqual(g.ast, expected)
			
			
	def test_edges_with_default_properties(self):
		@Graph(directed=True, default_edge_params={'abc':42,'xyz':'Foo Bar'})
		def g():
			(42) -{}> (72) -{}> (123)
			
		expected = GraphDef(nodes=[
			GraphAstEdge(
				node1=GraphAstNodedef(value=GraphAstLitteralValue(value=42), data={}),
				node2=GraphAstEdge(
					node1=GraphAstNodedef(value=GraphAstLitteralValue(value=72), data={}),
					node2=GraphAstNodedef(value=GraphAstLitteralValue(value=123), data={}),
					data={'abc': GraphAstLitteralValue(value=42),'xyz': GraphAstLitteralValue(value='Foo Bar')},
					left_char='-',
					right_char='>'
				),
				data={'abc': GraphAstLitteralValue(value=42), 'xyz': GraphAstLitteralValue(value='Foo Bar')},
				left_char='-',
				right_char='>')
		])
		
		
		self.assertEqual(g.ast, expected)
		
		
	def test_edges_with_default_properties_merge(self):
		@Graph(directed=True, default_edge_params={'abc':42,'xyz':'Foo Bar'})
		def g():
			(42) -{abc:'def'}> (72) -{xyz: 72}> (123)
			
		expected = GraphDef(nodes=[
			GraphAstEdge(
				node1=GraphAstNodedef(value=GraphAstLitteralValue(value=42), data={}),
				node2=GraphAstEdge(
					node1=GraphAstNodedef(value=GraphAstLitteralValue(value=72), data={}),
					node2=GraphAstNodedef(value=GraphAstLitteralValue(value=123), data={}),
					data={'abc': GraphAstLitteralValue(value=42), 'xyz': GraphAstLitteralValue(value=72)},
					left_char='-',
					right_char='>'
				),
				data={'abc': GraphAstLitteralValue(value='def'), 'xyz': GraphAstLitteralValue(value='Foo Bar')},
				left_char='-',
				right_char='>')
		])
		
		self.assertEqual(g.ast, expected)
		
		
	def test_edges_with_default_properties_override(self):
		@Graph(directed=True, default_edge_params={'abc':42,'xyz':'Foo Bar'})
		def g():
			(42) -{}> (72) -{}> (123)
			
		expected = GraphDef(nodes=[
			GraphAstEdge(
				node1=GraphAstNodedef(value=GraphAstLitteralValue(value=42), data={}),
				node2=GraphAstEdge(
					node1=GraphAstNodedef(value=GraphAstLitteralValue(value=72), data={}),
					node2=GraphAstNodedef(value=GraphAstLitteralValue(value=123), data={}),
					data={'abc': GraphAstLitteralValue(value=42),'xyz': GraphAstLitteralValue(value='Foo Bar')},
					left_char='-',
					right_char='>'
				),
				data={'abc': GraphAstLitteralValue(value=42), 'xyz': GraphAstLitteralValue(value='Foo Bar')},
				left_char='-',
				right_char='>')
		])
		
		
		self.assertEqual(g.ast, expected)
	
		

if __name__ == '__main__':
	unittest.main()