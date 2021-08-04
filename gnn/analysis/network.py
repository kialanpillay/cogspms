import networkx as nx
import numpy as np
import pandas as pd
from networkx.algorithms import community


def build_network(df, n=5):
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

    return graph


def build_hierarchical_network(df, n=5):
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
