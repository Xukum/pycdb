"""Functional interface to graph methods and assorted utilities.
"""
#    Copyright (C) 2004-2012 by
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    All rights reserved.
#    BSD license.
#
import networkx as nx
__author__ = """\n""".join(['Aric Hagberg (hagberg@lanl.gov)',
                           'Pieter Swart (swart@lanl.gov)',
                           'Dan Schult(dschult@colgate.edu)'])
__all__ = ['nodes', 'edges', 'degree', 'degree_histogram', 'neighbors',
           'number_of_nodes', 'number_of_edges', 'density',
           'nodes_iter', 'edges_iter', 'is_directed','info',
           'freeze','is_frozen','subgraph','create_empty_copy',
           'set_node_attributes','get_node_attributes',
           'set_edge_attributes','get_edge_attributes',
           'all_neighbors','non_neighbors']

def nodes(G):
    """Return a copy of the nxgraph nodes in a list."""
    return G.nodes()

def nodes_iter(G):
    """Return an iterator over the nxgraph nodes."""
    return G.nodes_iter()

def edges(G,nbunch=None):
    """Return list of  edges adjacent to nodes in nbunch.

    Return all edges if nbunch is unspecified or nbunch=None.

    For digraphs, edges=out_edges
    """
    return G.edges(nbunch)

def edges_iter(G,nbunch=None):
    """Return iterator over  edges adjacent to nodes in nbunch.

    Return all edges if nbunch is unspecified or nbunch=None.

    For digraphs, edges=out_edges
    """
    return G.edges_iter(nbunch)

def degree(G,nbunch=None,weight=None):
    """Return degree of single node or of nbunch of nodes.
    If nbunch is ommitted, then return degrees of *all* nodes.
    """
    return G.degree(nbunch,weight)

def neighbors(G,n):
    """Return a list of nodes connected to node n. """
    return G.neighbors(n)

def number_of_nodes(G):
    """Return the number of nodes in the nxgraph."""
    return G.number_of_nodes()

def number_of_edges(G):
    """Return the number of edges in the nxgraph. """
    return G.number_of_edges()

def density(G):
    r"""Return the density of a nxgraph.

    The density for undirected graphs is

    .. math::

       d = \frac{2m}{n(n-1)},

    and for directed graphs is

    .. math::

       d = \frac{m}{n(n-1)},

    where `n` is the number of nodes and `m`  is the number of edges in `G`.

    Notes
    -----
    The density is 0 for an nxgraph without edges and 1.0 for a complete nxgraph.

    The density of multigraphs can be higher than 1.
    """
    n=number_of_nodes(G)
    m=number_of_edges(G)
    if m==0: # includes cases n==0 and n==1
        d=0.0
    else:
        if G.is_directed():
            d=m/float(n*(n-1))
        else:
            d= m*2.0/float(n*(n-1))
    return d

def degree_histogram(G):
    """Return a list of the frequency of each degree value.

    Parameters
    ----------
    G : Networkx nxgraph
       A nxgraph

    Returns
    -------
    hist : list
       A list of frequencies of degrees.
       The degree values are the index in the list.

    Notes
    -----
    Note: the bins are width one, hence len(list) can be large
    (Order(number_of_edges))
    """
    degseq=list(G.degree().values())
    dmax=max(degseq)+1
    freq= [ 0 for d in range(dmax) ]
    for d in degseq:
        freq[d] += 1
    return freq

def is_directed(G):
    """ Return True if nxgraph is directed."""
    return G.is_directed()


def freeze(G):
    """Modify nxgraph to prevent further change by adding or removing
    nodes or edges.

    Node and edge data can still be modified.

    Parameters
    -----------
    G : nxgraph
      A NetworkX nxgraph

    Examples
    --------
    >>> G=nx.Graph()
    >>> G.add_path([0,1,2,3])
    >>> G=nx.freeze(G)
    >>> try:
    ...    G.add_edge(4,5)
    ... except nx.NetworkXError as e:
    ...    print(str(e))
    Frozen nxgraph can't be modified

    Notes
    -----
    To "unfreeze" a nxgraph you must make a copy by creating a new nxgraph object:

    >>> nxgraph = nx.path_graph(4)
    >>> frozen_graph = nx.freeze(nxgraph)
    >>> unfrozen_graph = nx.Graph(frozen_graph)
    >>> nx.is_frozen(unfrozen_graph)
    False

    See Also
    --------
    is_frozen
    """
    def frozen(*args):
        raise nx.NetworkXError("Frozen nxgraph can't be modified")
    G.add_node=frozen
    G.add_nodes_from=frozen
    G.remove_node=frozen
    G.remove_nodes_from=frozen
    G.add_edge=frozen
    G.add_edges_from=frozen
    G.remove_edge=frozen
    G.remove_edges_from=frozen
    G.clear=frozen
    G.frozen=True
    return G

def is_frozen(G):
    """Return True if nxgraph is frozen.

    Parameters
    -----------
    G : nxgraph
      A NetworkX nxgraph

    See Also
    --------
    freeze
    """
    try:
        return G.frozen
    except AttributeError:
        return False

def subgraph(G, nbunch):
    """Return the subgraph induced on nodes in nbunch.

    Parameters
    ----------
    G : nxgraph
       A NetworkX nxgraph

    nbunch : list, iterable
       A container of nodes that will be iterated through once (thus
       it should be an iterator or be iterable).  Each element of the
       container should be a valid node type: any hashable type except
       None.  If nbunch is None, return all edges data in the nxgraph.
       Nodes in nbunch that are not in the nxgraph will be (quietly)
       ignored.

    Notes
    -----
    subgraph(G) calls G.subgraph()
    """
    return G.subgraph(nbunch)

def create_empty_copy(G,with_nodes=True):
    """Return a copy of the nxgraph G with all of the edges removed.

    Parameters
    ----------
    G : nxgraph
       A NetworkX nxgraph

    with_nodes :  bool (default=True)
       Include nodes.

    Notes
    -----
    Graph, node, and edge data is not propagated to the new nxgraph.
    """
    H=G.__class__()
    if with_nodes:
        H.add_nodes_from(G)
    return H


def info(G, n=None):
    """Print short summary of information for the nxgraph G or the node n.

    Parameters
    ----------
    G : Networkx nxgraph
       A nxgraph
    n : node (any hashable)
       A node in the nxgraph G
    """
    info='' # append this all to a string
    if n is None:
        info+="Name: %s\n"%G.name
        type_name = [type(G).__name__]
        info+="Type: %s\n"%",".join(type_name)
        info+="Number of nodes: %d\n"%G.number_of_nodes()
        info+="Number of edges: %d\n"%G.number_of_edges()
        nnodes=G.number_of_nodes()
        if len(G) > 0:
            if G.is_directed():
                info+="Average in degree: %8.4f\n"%\
                    (sum(G.in_degree().values())/float(nnodes))
                info+="Average out degree: %8.4f"%\
                    (sum(G.out_degree().values())/float(nnodes))
            else:
                s=sum(G.degree().values())
                info+="Average degree: %8.4f"%\
                    (float(s)/float(nnodes))

    else:
        if n not in G:
            raise nx.NetworkXError("node %s not in nxgraph"%(n,))
        info+="Node % s has the following properties:\n"%n
        info+="Degree: %d\n"%G.degree(n)
        info+="Neighbors: "
        info+=' '.join(str(nbr) for nbr in G.neighbors(n))
    return info

def set_node_attributes(G,name,attributes):
    """Set node attributes from dictionary of nodes and values

    Parameters
    ----------
    G : NetworkX Graph

    name : string
       Attribute name

    attributes: dict
       Dictionary of attributes keyed by node.

    Examples
    --------
    >>> G=nx.path_graph(3)
    >>> bb=nx.betweenness_centrality(G)
    >>> nx.set_node_attributes(G,'betweenness',bb)
    >>> G.node[1]['betweenness']
    1.0
    """
    for node,value in attributes.items():
        G.node[node][name]=value

def get_node_attributes(G,name):
    """Get node attributes from nxgraph

    Parameters
    ----------
    G : NetworkX Graph

    name : string
       Attribute name

    Returns
    -------
    Dictionary of attributes keyed by node.

    Examples
    --------
    >>> G=nx.Graph()
    >>> G.add_nodes_from([1,2,3],color='red')
    >>> color=nx.get_node_attributes(G,'color')
    >>> color[1]
    'red'
    """
    return dict( (n,d[name]) for n,d in G.node.items() if name in d)


def set_edge_attributes(G,name,attributes):
    """Set edge attributes from dictionary of edge tuples and values

    Parameters
    ----------
    G : NetworkX Graph

    name : string
       Attribute name

    attributes: dict
       Dictionary of attributes keyed by edge (tuple).

    Examples
    --------
    >>> G=nx.path_graph(3)
    >>> bb=nx.edge_betweenness_centrality(G, normalized=False)
    >>> nx.set_edge_attributes(G,'betweenness',bb)
    >>> G[1][2]['betweenness']
    2.0
    """
    for (u,v),value in attributes.items():
        G[u][v][name]=value

def get_edge_attributes(G,name):
    """Get edge attributes from nxgraph

    Parameters
    ----------
    G : NetworkX Graph

    name : string
       Attribute name

    Returns
    -------
    Dictionary of attributes keyed by node.

    Examples
    --------
    >>> G=nx.Graph()
    >>> G.add_path([1,2,3],color='red')
    >>> color=nx.get_edge_attributes(G,'color')
    >>> color[(1,2)]
    'red'
    """
    return dict( ((u,v),d[name]) for u,v,d in G.edges(data=True) if name in d)


def all_neighbors(graph, node):
    """ Returns all of the neighbors of a node in the nxgraph.

    If the nxgraph is directed returns predecessors as well as successors.

    Parameters
    ----------
    nxgraph : NetworkX nxgraph
        Graph to find neighbors.

    node : node
        The node whose neighbors will be returned.

    Returns
    -------
    neighbors : iterator
        Iterator of neighbors
    """
    if graph.is_directed():
        values = itertools.chain.from_iterable([graph.predecessors_iter(node),
                                                graph.successors_iter(node)])
    else:
        values = graph.neighbors_iter(node)

    return values

def non_neighbors(graph, node):
    """Returns the non-neighbors of the node in the nxgraph.

    Parameters
    ----------
    nxgraph : NetworkX nxgraph
        Graph to find neighbors.

    node : node
        The node whose neighbors will be returned.

    Returns
    -------
    non_neighbors : iterator
        Iterator of nodes in the nxgraph that are not neighbors of the node.
    """
    nbors = set(neighbors(graph, node)) | set([node])
    return (nnode for nnode in graph if nnode not in nbors)
