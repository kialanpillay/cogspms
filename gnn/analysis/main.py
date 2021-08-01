import argparse

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import seaborn as sn

from cluster import spectral_bicluster
from network import build_network


def run():
    df = pd.read_csv(args.raw, delimiter=',')
    corr = df.corr()

    df_cluster = spectral_bicluster(corr, 3)
    graph = None
    if args.network:
        graph = build_network(df)

    if args.plot:
        sn.set(font_scale=0.5)
        sn.heatmap(df_cluster, annot=False, center=0, cmap='coolwarm', square=True)

        if graph:
            pos = nx.spring_layout(graph)
            betweenness_dict = nx.betweenness_centrality(graph, normalized=True, endpoints=True)
            node_color = [2000 * graph.degree(v) for v in graph]
            node_size = [20000 * v for v in betweenness_dict.values()]
            plt.figure(figsize=(12, 7))
            nx.draw_networkx(graph, pos=pos, with_labels=True,
                             node_color=node_color,
                             node_size=node_size, font_size=8)
            # for node, (x, y) in pos.items():
            #     text(x, y, node, fontsize=dict(graph.degree)[node], ha='center', va='center')
            plt.axis('off')

        plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw', type=str, default='data/JSE_clean_truncated.csv')
    parser.add_argument('--plot', type=bool, default=False)
    parser.add_argument('--network', type=bool, default=False)
    args = parser.parse_args()
    run()
