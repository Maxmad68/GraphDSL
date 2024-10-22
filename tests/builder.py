#!/usr/bin/env python3

import unittest
import unittest.mock
import context

from GraphDSL.Factory import Graph
from GraphDSL.backend.abstract import Backend

backend = Backend

class TestBuildingMethods(unittest.TestCase):
	
	def setUp(self):
		self.G = unittest.mock.Mock()
		self.N1 = unittest.mock.Mock()
		self.N2 = unittest.mock.Mock()
		self.N3 = unittest.mock.Mock()
		
		backend.create_directed_graph = unittest.mock.MagicMock(return_value=self.G)
		backend.create_undirected_graph = unittest.mock.MagicMock(return_value=self.G)
		backend.add_node = unittest.mock.MagicMock(side_effect=[self.N1, self.N2, self.N3])
		backend.add_edge = unittest.mock.MagicMock()
		
	# Tests Graph Creation
	
	def test_directed_graph(self):
		@Graph(directed=True)
		def g():
			(42)
			
		g(backend=backend)
		
		backend.create_directed_graph.assert_called_once()
		
	def test_undirected_graph(self):
		@Graph(directed=False)
		def g():
			(42)
			
		g(backend=backend)
		
		backend.create_undirected_graph.assert_called_once()
		
	# Tests Node Creation
	
	def test_simple_node(self):
		@Graph(directed=True)
		def g():
			(42)
			
		g(backend=backend)
		
		backend.add_node.assert_called_once_with(self.G, 42, {})
		
	def test_node_with_properties(self):
		@Graph(directed=True)
		def g():
			(42, {abc: 42, xyz: 'Foo Bar'})
			
		g(backend=backend)
		
		backend.add_node.assert_called_once_with(self.G, 42, {'abc': 42, 'xyz': 'Foo Bar'})
		
	def test_multiple_nodes(self):
		@Graph(directed=True)
		def g():
			(42)
			(72)
			
		g(backend=backend)
		
		self.assertEqual(backend.add_node.call_count, 2)
		
	def test_multiple_nodes_in_edge(self):
		@Graph(directed=True)
		def g():
			(42) -{}> (72)
			
		g(backend=backend)
		
		self.assertEqual(backend.add_node.call_count, 2)
		
	# Tests Edge
	
	def test_simple_edge(self):
		@Graph(directed=True)
		def g():
			(42) -{}> (72)
			
		g(backend=backend)
		
		backend.add_edge.assert_called_once_with(self.G, self.N1, self.N2, {})
		
	def test_edge_with_properties(self):
		@Graph(directed=True)
		def g():
			(42) -{len: 42, color:"blue"}> (72)
			
		g(backend=backend)
		
		backend.add_edge.assert_called_once_with(self.G, self.N1, self.N2, {'len': 42, 'color':"blue"})
		
	def test_multiple_edges(self):
		@Graph(directed=True)
		def g():
			(42) -{}> (72) -{}> (123)
			
		g(backend=backend)
		
		self.assertEqual(backend.add_edge.call_count, 2)
		backend.add_edge.assert_has_calls([
			unittest.mock.call(self.G, self.N2, self.N3, {}), # Last edges first
			unittest.mock.call(self.G, self.N1, self.N2, {}),
		],any_order=False)
		
	def test_multiple_edges_2(self):
		@Graph(directed=True)
		def g():
			a = (42)
			a -{}> (72) -{}> (123) -{}> a
			
		g(backend=backend)
		
		self.assertEqual(backend.add_edge.call_count, 3)
		backend.add_edge.assert_has_calls([
			unittest.mock.call(self.G, self.N3, self.N1, {}), # Last edges first
			unittest.mock.call(self.G, self.N2, self.N3, {}),
			unittest.mock.call(self.G, self.N1, self.N2, {}),
		],any_order=False)
		
		
	def test_multiple_edges_3(self):
		@Graph(directed=True)
		def g():
			(42) -{}> (72) <{}- (123)
			
		g(backend=backend)
		
		self.assertEqual(backend.add_edge.call_count, 2)
		backend.add_edge.assert_has_calls([
			unittest.mock.call(self.G, self.N3, self.N2, {}), # Last edges first
			unittest.mock.call(self.G, self.N1, self.N2, {}),
		],any_order=False)
		
		
	def test_edge_with_vars(self):
		@Graph(directed=True)
		def g():
			a = (42)
			b = (72)
			b -{}> a
			
		g(backend=backend)
		
		backend.add_edge.assert_called_once_with(self.G, self.N2, self.N1, {})
		
		
	# Tests params
	def test_node_with_param(self):
		@Graph(directed=True)
		def g(data):
			(data)
			
		g(backend=backend, parameters={'data': 126})
		
		backend.add_node.assert_called_once_with(self.G, 126, {})
		
		
	def test_node_with_param_in_properties(self):
		@Graph(directed=True)
		def g(data, clr):
			(data, {color: clr})
			
		g(backend=backend, parameters={'data': 126, 'clr':'red'})
		
		backend.add_node.assert_called_once_with(self.G, 126, {'color':'red'})
		
		
	# Test custom graph init
	
	def test_graph_custom_init_function(self):
		@Graph(directed=True)
		def g():
			(42) -{}> (72)
			
		mocked_G = unittest.mock.Mock()
		custom_init_method = unittest.mock.MagicMock(return_value=mocked_G)
			
		g(backend=backend, graph_init=custom_init_method)
		
		# Test mocked G in graph creation
		custom_init_method.assert_called_once()
		
		# Test mocked G in node creation
		backend.add_node.assert_has_calls([
			unittest.mock.call(mocked_G, 42, {}), # Last edges first
			unittest.mock.call(mocked_G, 72, {}),
		],any_order=False)
		self.assertEqual(backend.add_node.call_count, 2)
		
		# Test mocked G in edges creation
		backend.add_edge.assert_called_once_with(mocked_G, self.N1, self.N2, {})
		
		
	def test_graph_custom_init_tuple(self):
		@Graph(directed=True)
		def g():
			(42) -{}> (72)
			
		mocked_G = unittest.mock.Mock()
		custom_init_method = unittest.mock.MagicMock(return_value=mocked_G)
		
		g(backend=backend, graph_init=(custom_init_method, 1, 2))
		
		# Test mocked G in graph creation
		custom_init_method.assert_called_once_with(1, 2)
		
		# Test mocked G in node creation
		backend.add_node.assert_has_calls([
			unittest.mock.call(mocked_G, 42, {}), # Last edges first
			unittest.mock.call(mocked_G, 72, {}),
		],any_order=False)
		self.assertEqual(backend.add_node.call_count, 2)
		
		# Test mocked G in edges creation
		backend.add_edge.assert_called_once_with(mocked_G, self.N1, self.N2, {})

	
		
		
	
		
		
if __name__ == '__main__':
	unittest.main()