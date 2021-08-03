import matplotlib.pyplot as plt
from matplotlib.pyplot import text
import networkx as nx
import numpy as np


def build_network(df):
    corr = df.corr()
    v_corr = corr.values
    graph = nx.Graph()
    edges = {}

    for i, a in enumerate(v_corr):
        idx = np.argpartition(np.delete(a, i), -5)[-5:]
        edges[corr.columns[i]] = \
            np.delete(corr.columns[idx].values, np.where(corr.columns[idx].values == corr.columns[i]))

    for k, v in edges.items():
        print(k, v)
        for n in v:
            graph.add_edge(k, n)

    density = nx.density(graph)
    print("Network density:", density)

    return graph
