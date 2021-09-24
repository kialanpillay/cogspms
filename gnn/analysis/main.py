import argparse
import os

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import seaborn as sn
from matplotlib import cm

from cluster import spectral_bicluster
from network import build_network, generate_network_metrics, build_hierarchical_network, generate_adjacency_network


def run():
    df = pd.read_csv(args.raw, delimiter=',')
    corr = df.corr()
    df_cluster = pd.DataFrame()
    graph = None

    if args.cluster:
        df_cluster = spectral_bicluster(corr, 2)

    if args.network:
        if args.hierarchical:
            graph = build_hierarchical_network(df, args.n)
            df_metrics = generate_network_metrics(df, args.n, True)
        else:
            graph = build_network(df, args.n)
            df_metrics = generate_network_metrics(df, args.n)
        if args.save:
            df_metrics.to_csv('network_metrics.csv', index=False)

    if args.adj_data:
        df_ = pd.read_csv(args.adj_data, index_col=0)
        # sn.set(font_scale=0.5)
        # sn.heatmap(df_, annot=False, center=0, cmap='coolwarm', square=True, vmax=0.2)
        # plt.savefig(os.path.join('img', 'StemGNN_corr.png'), dpi=300, bbox_inches='tight')
        graph = generate_adjacency_network(df_)

    if not df_cluster.empty:
        sn.set(font_scale=0.5)
        sn.heatmap(df_cluster, annot=False, center=0, cmap='coolwarm', square=True)
        if args.plot:
            plt.show()
        if args.save:
            if not os.path.exists('img'):
                os.makedirs('img')
            plt.savefig(os.path.join('img', 'bicluster_n_2.png'), dpi=300, bbox_inches='tight')
    if graph:
        pos = nx.spring_layout(graph, seed=args.seed)
        betweenness_dict = nx.betweenness_centrality(graph, normalized=True, endpoints=True)
        node_color = [20000 * v for v in betweenness_dict.values()]
        node_size = [200 * graph.degree(v) for v in graph]
        edge_widths = [abs(w) for (*edge, w) in graph.edges.data('weight')]
        plt.figure(figsize=(12, 7))
        if args.adj_data:
            nx.draw_networkx(graph, pos=pos, with_labels=True, node_color=node_color, cmap='coolwarm',
                             node_size=node_size, font_size=8, font_color='black', edge_color=edge_widths,
                             edge_cmap=cm.get_cmap('Greys'), edge_vmin=0, edge_vmax=1)
        else:
            nx.draw_networkx(graph, pos=pos, with_labels=True, node_color=node_color, cmap='coolwarm',
                             node_size=node_size, font_size=8, font_color='black', edge_color='silver')
        # for node, (x, y) in pos.items():
        #     text(x, y, node, fontsize=dict(graph.degree)[node], ha='center', va='center')
        plt.axis('off')
        if args.plot:
            plt.show()
        if args.save:
            if not os.path.exists('img'):
                os.makedirs('img')
            plt.savefig(os.path.join('img', 'network.png'), dpi=300, bbox_inches='tight')


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw', type=str, default='data/JSE_clean_truncated.csv')
    parser.add_argument('--adj_data', type=str, default=None)
    parser.add_argument('--plot', type=str2bool, default=False)
    parser.add_argument('--cluster', type=str2bool, default=False)
    parser.add_argument('--network', type=str2bool, default=False)
    parser.add_argument('--hierarchical', type=str2bool, default=False)
    parser.add_argument('--n', type=int, default=5)
    parser.add_argument('--seed', type=int, default=3)
    parser.add_argument('--save', type=str2bool, default=True)
    args = parser.parse_args()
    run()
