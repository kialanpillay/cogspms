import networkx as nx
import numpy as np
import pandas as pd
from networkx.algorithms import community


def build_network(df, n=5):
    """
    Builds a correlation network using correlation matrix data. The maximal n correlations for each share
    specify the edges between nodes in the network.

    Parameters
    ----------
    df : pandas.DataFrame
        Correlation matrix data to cluster.
    n : int, optional
        Number of maximal correlations

    Returns
    -------
    graph : networkx.Graph
    """
    corr = df.corr()
    v_corr = corr.values
    graph = nx.Graph()
    edges = {}

    for i, a in enumerate(v_corr):
        idx = np.argpartition(np.delete(a, i), -n)[-n:]
        edges[corr.columns[i]] = \
            (np.delete(corr.columns[idx].values, np.where(corr.columns[idx].values == corr.columns[i])),
             np.delete(a[idx], np.where(corr.columns[idx].values == corr.columns[i])))

    for k, v in edges.items():
        for i in range(len(v[0])):
            graph.add_edge(k, v[0][i], weight=v[1][i])

    return graph


def build_hierarchical_network(df, n=5):
    """
    Builds a hierarchical correlation network using correlation matrix data. The maximal n correlations for each share
    specify the edges between nodes in the network. For each share, for each maximally correlated share,
    an edge is inserted for each indirectly correlated share.

    Parameters
    ----------
    df : pandas.DataFrame
        Correlation matrix data to cluster.
    n : int, optional
        Number of maximal correlations

    Returns
    -------
    graph : networkx.Graph
    """
    corr = df.corr()
    v_corr = corr.values
    graph = nx.Graph()
    edges = {}

    for i, a in enumerate(v_corr):
        idx = np.argpartition(np.delete(a, i), -n)[-n:]
        edges[corr.columns[i]] = \
            np.delete(corr.columns[idx].values, np.where(corr.columns[idx].values == corr.columns[i]))

    for k, v in edges.items():
        for n_ in v:
            graph.add_edge(k, n_)
            for e in edges[n_]:
                if graph.has_edge(k, e) or k == e:
                    continue
                graph.add_edge(k, e)

    # print(dict(reversed(sorted(nx.betweenness_centrality(graph).items(), key=lambda item: item[1]))))
    # print(dict(reversed(sorted(nx.degree_centrality(graph).items(), key=lambda item: item[1]))))
    return graph


def generate_network_metrics(df, n=10, hierarchical=False):
    """
    Builds successively denser correlation networks and computes and returns core network metrics

    Parameters
    ----------
    df : pandas.DataFrame
        Correlation matrix data to cluster.
    n : int, optional
        Number of maximal correlations
    hierarchical: bool, optional
        Build a hierarchical correlation network

    Returns
    -------
    df : pandas.DataFrame
    """
    corr = df.corr()
    v_corr = corr.values

    df = pd.DataFrame(columns=['Edges', 'Network Density', 'Betweenness Centrality', 'Degree Centrality',
                               'Closeness Centrality', '# Correlations', 'Top Level Communities',
                               'Next Level Communities', 'Transitivity'])

    for i in range(1, n + 1):
        graph = nx.Graph()
        edges = {}
        for j, a in enumerate(v_corr):
            idx = np.argpartition(np.delete(a, j), -i)[-i:]
            edges[corr.columns[j]] = \
                np.delete(corr.columns[idx].values, np.where(corr.columns[idx].values == corr.columns[j]))

        for k, v in edges.items():
            for n_ in v:
                graph.add_edge(k, n_)
                if hierarchical:
                    for e in edges[n_]:
                        if graph.has_edge(k, e):
                            continue
                        graph.add_edge(k, e)

        degree_dict = nx.degree_centrality(graph)
        betweenness_dict = nx.betweenness_centrality(graph, normalized=True, endpoints=True)
        closeness_dict = nx.closeness_centrality(graph)
        communities_generator = community.girvan_newman(graph)
        top_level_communities = next(communities_generator)
        next_level_communities = next(communities_generator)

        df = df.append({'Edges': graph.number_of_edges(), 'Network Density': round(nx.density(graph), 2),
                        'Betweenness Centrality': round(np.mean(list(betweenness_dict.values())), 2),
                        'Degree Centrality': round(np.mean(list(degree_dict.values())), 2), 'Closeness Centrality':
                            round(np.mean(list(closeness_dict.values())), 2), 'Correlations': i,
                        'Top Level Communities': len(sorted(map(sorted, top_level_communities))),
                        'Next Level Communities': len(sorted(map(sorted, next_level_communities))),
                        'Transitivity': round(nx.transitivity(graph), 2)}, ignore_index=True)

    d = nx.coloring.greedy_color(graph, strategy="largest_first")
    d_ = {}
    for k, v in d.items():
        if v not in d_:
            d_[v] = [k]
        else:
            d_[v].append(k)
    return df


def generate_adjacency_network(df):
    """
    Generates a network representation of a graph adjacency matrix

    Parameters
    ----------
    df : pandas.DataFrame
        Adjacency matrix data.

    Returns
    -------
    graph : networkx.Graph
    """
    v_corr = df.values
    graph = nx.Graph()
    edges = {}

    for i, a in enumerate(v_corr):
        idx = np.nonzero(np.abs(a) > 0.01)
        edges[df.columns[i]] = (df.columns[idx].values, a[idx])

    for k, v in edges.items():
        for i in range(len(v[0])):
            graph.add_edge(k, v[0][i], weight=v[1][i])

    return graph
