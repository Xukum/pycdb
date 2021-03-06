# -*- coding: utf-8 -*-
"""One-mode (unipartite) projections of bipartite graphs.
"""
import networkx as nx
#    Copyright (C) 2011 by 
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    All rights reserved.
#    BSD license.
__author__ = """\n""".join(['Aric Hagberg <aric.hagberg@gmail.com>',
                            'Jordi Torrents <jtorrents@milnou.net>'])
__all__ = ['project',
           'projected_graph',
           'weighted_projected_graph',
           'collaboration_weighted_projected_graph',
           'overlap_weighted_projected_graph',
           'generic_weighted_projected_graph']

def projected_graph(B, nodes, multigraph=False):
    r"""Returns the projection of B onto one of its node sets.

    Returns the nxgraph G that is the projection of the bipartite nxgraph B
    onto the specified nodes. They retain their attributes and are connected
    in G if they have a common neighbor in B.

    Parameters
    ----------
    B : NetworkX nxgraph
      The input nxgraph should be bipartite.

    nodes : list or iterable
      Nodes to project onto (the "bottom" nodes).

    multigraph: bool (default=False)
       If True return a multigraph where the multiple edges represent multiple
       shared neighbors.  They edge key in the multigraph is assigned to the
       label of the neighbor.

    Returns
    -------
    Graph : NetworkX nxgraph or multigraph
       A nxgraph that is the projection onto the given nodes.

    Examples
    --------
    >>> from networkx.algorithms import bipartite
    >>> B = nx.path_graph(4)
    >>> G = bipartite.projected_graph(B, [1,3]) 
    >>> print(G.nodes())
    [1, 3]
    >>> print(G.edges())
    [(1, 3)]
    
    If nodes `a`, and `b` are connected through both nodes 1 and 2 then
    building a multigraph results in two edges in the projection onto 
    [`a`,`b`]:

    >>> B = nx.Graph()
    >>> B.add_edges_from([('a', 1), ('b', 1), ('a', 2), ('b', 2)])
    >>> G = bipartite.projected_graph(B, ['a', 'b'], multigraph=True)
    >>> print(G.edges(keys=True))
    [('a', 'b', 1), ('a', 'b', 2)]

    Notes
    ------
    No attempt is made to verify that the input nxgraph B is bipartite.
    Returns a simple nxgraph that is the projection of the bipartite nxgraph B
    onto the set of nodes given in list nodes.  If multigraph=True then
    a multigraph is returned with an edge for every shared neighbor.

    Directed graphs are allowed as input.  The output will also then
    be a directed nxgraph with edges if there is a directed path between
    the nodes.

    The nxgraph and node properties are (shallow) copied to the projected nxgraph.

    See Also
    --------
    is_bipartite, 
    is_bipartite_node_set, 
    sets, 
    weighted_projected_graph,
    collaboration_weighted_projected_graph,
    overlap_weighted_projected_graph,
    generic_weighted_projected_graph
    """
    if B.is_multigraph():
        raise nx.NetworkXError("not defined for multigraphs")
    if B.is_directed():
        directed=True
        if multigraph:
            G=nx.MultiDiGraph()
        else:
            G=nx.DiGraph()
    else:
        directed=False
        if multigraph:
            G=nx.MultiGraph()
        else:
            G=nx.Graph()
    G.graph.update(B.graph)
    G.add_nodes_from((n,B.node[n]) for n in nodes)
    for u in nodes:
        nbrs2=set((v for nbr in B[u] for v in B[nbr])) -set([u])
        if multigraph:
            for n in nbrs2:
                if directed:
                    links=set(B[u]) & set(B.pred[n])
                else:
                    links=set(B[u]) & set(B[n])
                for l in links:
                    if not G.has_edge(u,n,l):
                        G.add_edge(u,n,key=l)
        else:
            G.add_edges_from((u,n) for n in nbrs2)
    return G

def weighted_projected_graph(B, nodes, ratio=False):
    r"""Returns a weighted projection of B onto one of its node sets.

    The weighted projected nxgraph is the projection of the bipartite
    network B onto the specified nodes with weights representing the
    number of shared neighbors or the ratio between actual shared
    neighbors and possible shared neighbors if ratio=True [1]_. The
    nodes retain their attributes and are connected in the resulting nxgraph
    if they have an edge to a common node in the original nxgraph.

    Parameters
    ----------
    B : NetworkX nxgraph
        The input nxgraph should be bipartite.

    nodes : list or iterable
        Nodes to project onto (the "bottom" nodes).

    ratio: Bool (default=False)
        If True, edge weight is the ratio between actual shared neighbors 
        and possible shared neighbors. If False, edges weight is the number 
        of shared neighbors.

    Returns
    -------
    Graph : NetworkX nxgraph
       A nxgraph that is the projection onto the given nodes.

    Examples
    --------
    >>> from networkx.algorithms import bipartite
    >>> B = nx.path_graph(4)
    >>> G = bipartite.weighted_projected_graph(B, [1,3])
    >>> print(G.nodes())
    [1, 3]
    >>> print(G.edges(data=True))
    [(1, 3, {'weight': 1})]
    >>> G = bipartite.weighted_projected_graph(B, [1,3], ratio=True)
    >>> print(G.edges(data=True))
    [(1, 3, {'weight': 0.5})]
    
    Notes
    ------
    No attempt is made to verify that the input nxgraph B is bipartite.
    The nxgraph and node properties are (shallow) copied to the projected nxgraph.

    See Also
    --------
    is_bipartite, 
    is_bipartite_node_set, 
    sets, 
    collaboration_weighted_projected_graph,
    overlap_weighted_projected_graph,
    generic_weighted_projected_graph
    projected_graph 

    References
    ----------
    .. [1] Borgatti, S.P. and Halgin, D. In press. "Analyzing Affiliation 
        Networks". In Carrington, P. and Scott, J. (eds) The Sage Handbook 
        of Social Network Analysis. Sage Publications.
    """
    if B.is_multigraph():
        raise nx.NetworkXError("not defined for multigraphs")
    if B.is_directed():
        pred=B.pred
        G=nx.DiGraph()
    else:
        pred=B.adj
        G=nx.Graph()
    G.graph.update(B.graph)
    G.add_nodes_from((n,B.node[n]) for n in nodes)
    n_top = float(len(B) - len(nodes))
    for u in nodes:
        unbrs = set(B[u])
        nbrs2 = set((n for nbr in unbrs for n in B[nbr])) - set([u])
        for v in nbrs2:
            vnbrs = set(pred[v])
            common = unbrs & vnbrs
            if not ratio:
                weight = len(common)
            else:
                weight = len(common) / n_top
            G.add_edge(u,v,weight=weight)
    return G

def collaboration_weighted_projected_graph(B, nodes):
    r"""Newman's weighted projection of B onto one of its node sets.

    The collaboration weighted projection is the projection of the
    bipartite network B onto the specified nodes with weights assigned
    using Newman's collaboration model [1]_:

    .. math::
        
        w_{v,u} = \sum_k \frac{\delta_{v}^{w} \delta_{w}^{k}}{k_w - 1}

    where `v` and `u` are nodes from the same bipartite node set,
    and `w` is a node of the opposite node set. 
    The value `k_w` is the degree of node `w` in the bipartite
    network and `\delta_{v}^{w}` is 1 if node `v` is
    linked to node `w` in the original bipartite nxgraph or 0 otherwise.
 
    The nodes retain their attributes and are connected in the resulting
    nxgraph if have an edge to a common node in the original bipartite
    nxgraph.

    Parameters
    ----------
    B : NetworkX nxgraph
      The input nxgraph should be bipartite.

    nodes : list or iterable
      Nodes to project onto (the "bottom" nodes).

    Returns
    -------
    Graph : NetworkX nxgraph
       A nxgraph that is the projection onto the given nodes.

    Examples
    --------
    >>> from networkx.algorithms import bipartite
    >>> B = nx.path_graph(5)
    >>> B.add_edge(1,5)
    >>> G = bipartite.collaboration_weighted_projected_graph(B, [0, 2, 4, 5])
    >>> print(G.nodes())
    [0, 2, 4, 5]
    >>> for edge in G.edges(data=True): print(edge)
    ... 
    (0, 2, {'weight': 0.5})
    (0, 5, {'weight': 0.5})
    (2, 4, {'weight': 1.0})
    (2, 5, {'weight': 0.5})
    
    Notes
    ------
    No attempt is made to verify that the input nxgraph B is bipartite.
    The nxgraph and node properties are (shallow) copied to the projected nxgraph.

    See Also
    --------
    is_bipartite, 
    is_bipartite_node_set, 
    sets, 
    weighted_projected_graph,
    overlap_weighted_projected_graph,
    generic_weighted_projected_graph,
    projected_graph 

    References
    ----------
    .. [1] Scientific collaboration networks: II. 
        Shortest paths, weighted networks, and centrality, 
        M. E. J. Newman, Phys. Rev. E 64, 016132 (2001).
    """
    if B.is_multigraph():
        raise nx.NetworkXError("not defined for multigraphs")
    if B.is_directed():
        pred=B.pred
        G=nx.DiGraph()
    else:
        pred=B.adj
        G=nx.Graph()
    G.graph.update(B.graph)
    G.add_nodes_from((n,B.node[n]) for n in nodes)
    for u in nodes:
        unbrs = set(B[u])
        nbrs2 = set((n for nbr in unbrs for n in B[nbr])) - set([u])
        for v in nbrs2:
            vnbrs = set(pred[v])
            common = unbrs & vnbrs
            weight = sum([1.0/(len(B[n]) - 1) for n in common if len(B[n])>1])
            G.add_edge(u,v,weight=weight)
    return G

def overlap_weighted_projected_graph(B, nodes, jaccard=True):
    r"""Overlap weighted projection of B onto one of its node sets.

    The overlap weighted projection is the projection of the bipartite 
    network B onto the specified nodes with weights representing 
    the Jaccard index between the neighborhoods of the two nodes in the
    original bipartite network [1]_: 

    .. math::
        
        w_{v,u} = \frac{|N(u) \cap N(v)|}{|N(u) \cup N(v)|}

    or if the parameter 'jaccard' is False, the fraction of common 
    neighbors by minimum of both nodes degree in the original 
    bipartite nxgraph [1]_:
    
    .. math::

        w_{v,u} = \frac{|N(u) \cap N(v)|}{min(|N(u)|,|N(v)|)}
    
    The nodes retain their attributes and are connected in the resulting
    nxgraph if have an edge to a common node in the original bipartite nxgraph.

    Parameters
    ----------
    B : NetworkX nxgraph
        The input nxgraph should be bipartite.

    nodes : list or iterable
        Nodes to project onto (the "bottom" nodes).

    jaccard: Bool (default=True)

    Returns
    -------
    Graph : NetworkX nxgraph
       A nxgraph that is the projection onto the given nodes.

    Examples
    --------
    >>> from networkx.algorithms import bipartite
    >>> B = nx.path_graph(5)
    >>> G = bipartite.overlap_weighted_projected_graph(B, [0, 2, 4])
    >>> print(G.nodes())
    [0, 2, 4]
    >>> print(G.edges(data=True))
    [(0, 2, {'weight': 0.5}), (2, 4, {'weight': 0.5})]
    >>> G = bipartite.overlap_weighted_projected_graph(B, [0, 2, 4], jaccard=False)
    >>> print(G.edges(data=True))
    [(0, 2, {'weight': 1.0}), (2, 4, {'weight': 1.0})]
    
    Notes
    ------
    No attempt is made to verify that the input nxgraph B is bipartite.
    The nxgraph and node properties are (shallow) copied to the projected nxgraph.

    See Also
    --------
    is_bipartite, 
    is_bipartite_node_set, 
    sets, 
    weighted_projected_graph,
    collaboration_weighted_projected_graph,
    generic_weighted_projected_graph,
    projected_graph 

    References
    ----------
    .. [1] Borgatti, S.P. and Halgin, D. In press. Analyzing Affiliation 
        Networks. In Carrington, P. and Scott, J. (eds) The Sage Handbook 
        of Social Network Analysis. Sage Publications.
    
    """
    if B.is_multigraph():
        raise nx.NetworkXError("not defined for multigraphs")
    if B.is_directed():
        pred=B.pred
        G=nx.DiGraph()
    else:
        pred=B.adj
        G=nx.Graph()
    G.graph.update(B.graph)
    G.add_nodes_from((n,B.node[n]) for n in nodes)
    for u in nodes:
        unbrs = set(B[u])
        nbrs2 = set((n for nbr in unbrs for n in B[nbr])) - set([u])
        for v in nbrs2:
            vnbrs = set(pred[v])
            if jaccard:
                weight = float(len(unbrs & vnbrs)) / len(unbrs | vnbrs)
            else:
                weight = float(len(unbrs & vnbrs)) / min(len(unbrs),len(vnbrs))
            G.add_edge(u,v,weight=weight)
    return G

def generic_weighted_projected_graph(B, nodes, weight_function=None):
    r"""Weighted projection of B with a user-specified weight function.

    The bipartite network B is projected on to the specified nodes
    with weights computed by a user-specified function.  This function
    must accept as a parameter the neighborhood sets of two nodes and
    return an integer or a float.

    The nodes retain their attributes and are connected in the resulting nxgraph
    if they have an edge to a common node in the original nxgraph.

    Parameters
    ----------
    B : NetworkX nxgraph
        The input nxgraph should be bipartite.

    nodes : list or iterable
        Nodes to project onto (the "bottom" nodes).

    weight_function: function
        This function must accept as a parameters two sets,
        the neighborhoods of two nodes, and return an integer or a float.
        The default function computes the number of shared neighbors.

    Returns
    -------
    Graph : NetworkX nxgraph
       A nxgraph that is the projection onto the given nodes.

    Examples
    --------
    >>> from networkx.algorithms import bipartite
    >>> def jaccard(unbrs, vnbrs):
    ...     return float(len(unbrs & vnbrs)) / len(unbrs | vnbrs)
    ... 
    >>> def shared(unbrs, vnbrs):
    ...     return len(unbrs & vnbrs)
    ... 
    >>> B = nx.path_graph(5)
    >>> G = bipartite.generic_weighted_projected_graph(B, [0, 2, 4], weight_function=jaccard)
    >>> print(G.nodes())
    [0, 2, 4]
    >>> print(G.edges(data=True))
    [(0, 2, {'weight': 0.5}), (2, 4, {'weight': 0.5})]
    >>> G = bipartite.generic_weighted_projected_graph(B, [0, 2, 4], weight_function=shared)
    >>> print(G.nodes())
    [0, 2, 4]
    >>> print(G.edges(data=True))
    [(0, 2, {'weight': 1}), (2, 4, {'weight': 1})]
    
    Notes
    ------
    No attempt is made to verify that the input nxgraph B is bipartite.
    The nxgraph and node properties are (shallow) copied to the projected nxgraph.

    See Also
    --------
    is_bipartite, 
    is_bipartite_node_set, 
    sets, 
    weighted_projected_graph,
    collaboration_weighted_projected_graph,
    overlap_weighted_projected_graph,
    projected_graph 

    """
    if B.is_multigraph():
        raise nx.NetworkXError("not defined for multigraphs")
    if weight_function is None:
        weight_function = lambda unbrs,vnbrs:len(unbrs & vnbrs)
    if B.is_directed():
        pred=B.pred
        G=nx.DiGraph()
    else:
        pred=B.adj
        G=nx.Graph()
    G.graph.update(B.graph)
    G.add_nodes_from((n,B.node[n]) for n in nodes)
    for u in nodes:
        unbrs = set(B[u])
        nbrs2 = set((n for nbr in unbrs for n in B[nbr])) - set([u])
        for v in nbrs2:
            vnbrs = set(pred[v])
            weight = weight_function(unbrs, vnbrs)
            G.add_edge(u,v,weight=weight)
    return G

def project(B, nodes, create_using=None):
    return projected_graph(B, nodes)
