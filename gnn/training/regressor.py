import argparse
import json
import os

import numpy as np
import torch
from sklearn.linear_model import HuberRegressor, Ridge
from sklearn.svm import SVR

from gnn.evaluation.test_ import regressor_test
from gnn.preprocessing.loader import ForecastDataset, load_dataset


def train(args):
    result_train_file = os.path.join('output', args.model, args.dataset, str(args.window_size), str(args.horizon),
                                     'train')
    if not os.path.exists(result_train_file):
        os.makedirs(result_train_file)
    train_data, valid_data, test_data = load_dataset(args.dataset, args.train_length, args.valid_length,
                                                     args.test_length)

    if args.norm_method == 'z_score':
        train_mean = np.mean(train_data[:, args.node], axis=0)
        train_std = np.std(train_data[:, args.node], axis=0)
        norm_statistic = {"mean": [train_mean], "std": [train_std]}
    else:
        norm_statistic = None
    if norm_statistic is not None:
        with open(os.path.join(result_train_file, 'norm_stat.json'), 'w') as f:
            json.dump(norm_statistic, f)

    train_set = ForecastDataset(train_data, window_size=args.window_size,
                                horizon=args.horizon, normalize_method=args.norm_method,
                                norm_statistic=norm_statistic)
    train_loader = torch.utils.data.DataLoader(train_set, batch_size=args.batch_size, drop_last=False, shuffle=True,
                                               num_workers=0)

    inputs_set = []
    target_set = []
    for i, (inputs, target) in enumerate(train_loader):
        inputs_set.append(inputs[:, :, args.node])
        target_set.append(target[:, :, args.node])

    X = np.concatenate(inputs_set, axis=0)[:np.concatenate(target_set, axis=0).shape[0], ...]
    y = np.ravel(np.concatenate(target_set, axis=0))
    if args.model == "huber":
        regressor = HuberRegressor().fit(X, y)
    elif args.model == "ridge":
        regressor = Ridge().fit(X, y)
    else:
        regressor = SVR(C=10, epsilon=0.003).fit(X, y)
    regressor_test(regressor, test_data, args, result_train_file)
