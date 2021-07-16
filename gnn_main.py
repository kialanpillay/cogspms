import argparse
import os
from datetime import datetime

import torch

import gnn.evaluation.test_
import gnn.train
from gnn.preprocessing.loader import load_dataset, load_adj
from gnn.preprocessing.process import process_adjacency_matrix

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, default='StemGNN')
# StemGNN arguments
parser.add_argument('--train', type=bool, default=True)
parser.add_argument('--evaluate', type=bool, default=True)
parser.add_argument('--dataset', type=str, default='ECG_data')
parser.add_argument('--window_size', type=int, default=12)
parser.add_argument('--horizon', type=int, default=12)
parser.add_argument('--train_length', type=float, default=6)
parser.add_argument('--valid_length', type=float, default=2)
parser.add_argument('--test_length', type=float, default=2)
parser.add_argument('--epoch', type=int, default=5)
parser.add_argument('--lr', type=float, default=1e-4)
parser.add_argument('--multi_layer', type=int, default=5)
parser.add_argument('--device', type=str, default='cpu')
parser.add_argument('--validate_freq', type=int, default=1)
parser.add_argument('--batch_size', type=int, default=32)
parser.add_argument('--norm_method', type=str, default='z_score')
parser.add_argument('--optim', type=str, default='RMSProp')
parser.add_argument('--early_stop', type=bool, default=False)
parser.add_argument('--exponential_decay_step', type=int, default=5)
parser.add_argument('--decay_rate', type=float, default=0.5)
parser.add_argument('--dropout_rate', type=float, default=0.5)
parser.add_argument('--leakyrelu_rate', type=int, default=0.2)

# GWN arguments
parser.add_argument('--adj_data', type=str, default=None)
parser.add_argument('--adj_type', type=str, default='double_transition')
parser.add_argument('--gcn_bool', type=bool, default=True)
parser.add_argument('--apt_only', type=bool, default=True)
parser.add_argument('--adapt_adj', type=bool, default=False)
parser.add_argument('--random_adj', type=bool, default=True)
parser.add_argument('--channels', type=int, default=32)
parser.add_argument('--in_dim', type=int, default=1)
parser.add_argument('--weight_decay', type=float, default=0.0001)

# MTGNN arguments

parser.add_argument('--build_adj', type=bool, default=True)
parser.add_argument('--load_static_feature', type=bool, default=False)
parser.add_argument('--cl', type=bool, default=True)
parser.add_argument('--gcn_depth', type=int, default=2)
parser.add_argument('--subgraph_size', type=int, default=20)
parser.add_argument('--node_dim', type=int, default=40)
parser.add_argument('--dilation_exponential', type=int, default=1)
parser.add_argument('--conv_channels', type=int, default=32)
parser.add_argument('--residual_channels', type=int, default=32)
parser.add_argument('--skip_channels', type=int, default=64)
parser.add_argument('--end_channels', type=int, default=128)
parser.add_argument('--layers', type=int, default=3)
parser.add_argument('--clip', type=int, default=5)
parser.add_argument('--step_size1', type=int, default=2500)
parser.add_argument('--step_size2', type=int, default=100)
parser.add_argument('--seed', type=int, default=101)
parser.add_argument('--prop_alpha', type=float, default=0.05)
parser.add_argument('--tanh_alpha', type=float, default=3)
parser.add_argument('--splits', type=int, default=1)
parser.add_argument('--runs', type=int, default=10)
parser.add_argument('--multi_step', type=bool, default=True)

args = parser.parse_args()
print(f'Training configs: {args}')
result_train_file = os.path.join('output', args.model, args.dataset, 'train')
result_test_file = os.path.join('output', args.model, args.dataset, 'test')
if not os.path.exists(result_train_file):
    os.makedirs(result_train_file)
if not os.path.exists(result_test_file):
    os.makedirs(result_test_file)

train_data, valid_data, test_data = load_dataset(args.dataset, args.train_length, args.valid_length, args.test_length)
args.node_cnt = train_data.shape[1]

if args.adj_data:
    adj_matrix = process_adjacency_matrix(load_adj(args.adj_data), args.adj_type)
    args.supports = [torch.tensor(i).to(args.device) for i in adj_matrix]

    if args.model == 'GWN':
        if args.apt_only:
            args.supports = None
            args.adj_init = None
        else:
            if args.random_adj:
                args.adj_init = None
            else:
                adj_init = args.supports[0]

    if args.model == 'MTGNN':
        adj_matrix = torch.tensor(adj_matrix) - torch.eye(args.node_cnt)
        args.adj_matrix = adj_matrix.to(args.device)
else:
    args.adj_matrix = None
    args.adj_init = None
    args.supports = None

torch.manual_seed(0)
if __name__ == '__main__':
    if args.train:
        try:
            before_train = datetime.now().timestamp()
            _, normalize_statistic = gnn.train.train(train_data, valid_data, args, result_train_file)
            after_train = datetime.now().timestamp()
            print(f'Training took {(after_train - before_train) / 60} minutes')
        except KeyboardInterrupt:
            print('-' * 99)
            print('Exiting from training early')
    if args.evaluate:
        before_evaluation = datetime.now().timestamp()
        if args.model == 'StemGNN':
            gnn.evaluation.test_.test(test_data, args, result_train_file, result_test_file)
        else:
            gnn.evaluation.test_.custom_test(test_data, args, result_train_file, result_test_file)
        after_evaluation = datetime.now().timestamp()
        print(f'Evaluation took {(after_evaluation - before_evaluation) / 60} minutes')
    print('done')
