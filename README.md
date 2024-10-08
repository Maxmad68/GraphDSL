# GraphDSL - A Python DSL for Graph Manipulation

**GraphDSL** is a Python library that allows you to define, manipulate, and generate graphs (directed or undirected) in a simple and readable way using a Domain-Specific Language (DSL) embedded directly in Python. 

With this library, you can create graphs leveraging Python's syntax, making it easy to integrate into any Python script or Jupyter notebook. The defined graphs can then be manipulated with libraries such as **NetworkX** or **iGraph**.

## Installation

`pip install graphdsl`

## Usage

### Declaring a Graph

To define a graph, you need to create a function decorated with the `@Graph` decorator. This decorator allows you to specify whether the graph is **directed** or **undirected**.

- For an undirected graph: `@Graph(directed=False)`
- For a directed graph: `@Graph(directed=True)`

Within the function, you can define nodes and edges using a simple syntax based on parentheses and dashes.

#### Example: Undirected Graph

```python
@Graph(directed=False)
def g():
    (42) -{}- (72)
```

#### Example: Directed Graph

```python
@Graph(directed=True)
def g():
    (42) -{}> (72)  # Directed edge from 42 to 72
    (72) <{}- (42)  # Directed edge from 72 to 42
```

### DSL Syntax

The DSL offers an intuitive syntax for defining graphs, nodes, edges, and their properties.

#### Nodes

- A node is defined by parentheses: `(42)`

- A node can have a value and additional properties: `(42, {weight: 3, color: 'red'})`
  
  - Properties are optional, and keys do not need to be quoted.

#### Edges

Edges connect two nodes. The direction depends on whether the graph is directed or undirected.

##### Undirected Graph:

```python
@Graph(directed=False)
def g():
    (1) -{}- (2)
```

##### Directed Graph

```python
@Graph(directed=True)
def g():
    (1) -{}> (2)  # From 1 to 2
    (2) <{}- (1)  # From 2 to 1
```

#### Node and Edge Properties

You can add properties to both nodes and edges using a dictionary format.

##### Example with Properties:

```python
@Graph(directed=True)
def g():
    (42, {color: 'blue'}) -{length: 3}> (72, {color: 'green'})
```

#### Chaining Nodes

You can chain multiple nodes and edges in a single line:

```python
@Graph(directed=True)
def g():
    (1) -{}> (2) -{}> (3)
    (4) -{}> (5) -{}> (6)
```

#### Nodes Variables

You can assign nodes to variables for reuse:

```python
@Graph(directed=True)
def g():
    central_node = ('Center', {weight: 100})
    central_node -{}> (42)
    (72) -{}> central_node
```

#### Default Properties

You can define default properties for nodes and edges. These properties will be applied unless explicitly overridden.

```python
@Graph(directed=True, default_edge_params={'color': 'red'}, default_node_params={'size': 10})
def g():
    (42) -{}> (72) -{length: 3}> (93)
```

In this example, all nodes have the default property `size=10`, and edges have the default property `color='red'`. The edge between 72 and 93 has a redefined length of 3.

### Generating the Graph

#### Backends

To generate the graph defined using the DSL, simply call the corresponding function. By default, the **NetworkX** backend is used, but you can also specify other backends such as **iGraph**.

##### Example with NetworkX (default):

```python
p = g()  # Returns a NetworkX graph object
print(p.nodes)
```

##### Example with iGraph:

```python
p = g(backend=backend.igraph)  # Returns an iGraph object
print(p.average_path_length())
```

#### Initial Graph

If you want to start from a pre-generated graph, you can use the `graph_init` option to provide a graph generation function:

```python
p = g(graph_init=nx.house_graph)
```

Or with parameters:

```python
p = g(graph_init=(nx.star_graph, 5))
```

#### Function Parameters

Graph functions are isolated from the rest of the Python script. If the properties of nodes or edges need to depend on external variables, you can pass them as parameters to the graph function:

```python
@Graph(directed=True)
def g(c, l):
    (1, {color: c}) -{length: l}> (2, {color: c})

p = g(parameters={'c': 'red', 'l': 42})
```

## License

This project is licensed under the MIT License.
