import json
import os
import time

import numpy as np
import torch
import torch.nn as nn
import torch.utils.data

import gnn.preprocessing.loader
from gnn.evaluation.validation import validate_baseline
from gnn.models.lstm import LSTM
from gnn.utils import save_model


def train(train_data, valid_data, args, result_file):
    """
    Trains a LSTM model and returns a set of validation performance metrics

    Parameters
    ----------
    train_data : numpy.ndarray
        Train set
    valid_data : numpy.ndarray
        Validation set
    args : argparse.Namespace
        Command line arguments
    result_file : str
        Directory to store trained model parameter files

    Returns
    -------
    dict
    """
    model = LSTM(input_size=args.window_size, hidden_layers=args.lstm_hidden_layers, hidden_size=args.lstm_hidden_size,
                 output_size=args.horizon)
    model.to(args.device)
    if len(train_data) == 0:
        raise Exception('Cannot organize enough training data')
    if len(valid_data) == 0:
        raise Exception('Cannot organize enough validation data')

    if args.norm_method == 'z_score':
        train_mean = np.mean(train_data[:, args.lstm_node], axis=0)
        train_std = np.std(train_data[:, args.lstm_node], axis=0)
        norm_statistic = {"mean": [train_mean], "std": [train_std]}

    elif args.norm_method == 'min_max':
        train_min = np.min(train_data[:, args.lstm_node], axis=0)
        train_max = np.max(train_data[:, args.lstm_node], axis=0)
        norm_statistic = {"min": [train_min], "max": [train_max]}
    else:
        norm_statistic = None
    if norm_statistic is not None:
        with open(os.path.join(result_file, 'norm_stat.json'), 'w') as f:
            json.dump(norm_statistic, f)

    if args.optimizer == 'RMSProp':
        optimizer = torch.optim.RMSprop(params=model.parameters(), lr=args.lr)
    elif args.optimizer == 'SGD':
        optimizer = torch.optim.SGD(params=model.parameters(), lr=args.lr)
    elif args.optimizer == 'Adagrad':
        optimizer = torch.optim.Adagrad(params=model.parameters(), lr=args.lr)
    elif args.optimizer == 'Adadelta':
        optimizer = torch.optim.Adadelta(params=model.parameters(), lr=args.lr)
    else:
        optimizer = torch.optim.Adam(params=model.parameters(), lr=args.lr, betas=(0.9, 0.999))

    lr_scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer=optimizer, gamma=args.decay_rate)

    train_set = gnn.preprocessing.loader.ForecastDataset(train_data, window_size=args.window_size,
                                                         horizon=args.horizon, normalize_method=args.norm_method,
                                                         norm_statistic=norm_statistic)
    valid_set = gnn.preprocessing.loader.ForecastDataset(valid_data, window_size=args.window_size,
                                                         horizon=args.horizon, normalize_method=args.norm_method,
                                                         norm_statistic=norm_statistic)

    train_loader = torch.utils.data.DataLoader(train_set, batch_size=args.batch_size, drop_last=False, shuffle=True,
                                               num_workers=0)
    valid_loader = torch.utils.data.DataLoader(valid_set, batch_size=args.batch_size, shuffle=False, num_workers=0)

    criterion = nn.MSELoss(reduction='mean').to(args.device)

    total_params = 0
    for name, parameter in model.named_parameters():
        if not parameter.requires_grad:
            continue
        param = parameter.numel()
        total_params += param
    if args.verbose:
        print(f"Total Trainable Params: {total_params}")
        print("LSTM")
        print()

    best_validate_mae = np.inf
    validate_score_non_decrease_count = 0
    performance_metrics = {}
    for epoch in range(50):
        epoch_start_time = time.time()
        model.train()
        loss_total = 0
        cnt = 0
        for i, (inputs, target) in enumerate(train_loader):
            optimizer.zero_grad()
            model.hidden_cell = (torch.zeros(model.hidden_layers, 1, model.hidden_size),
                                 torch.zeros(model.hidden_layers, 1, model.hidden_size))
            forecast = model(inputs[:, :, args.lstm_node])
            loss = criterion(forecast, target[:, :, args.lstm_node])
            loss.backward()
            cnt += 1
            optimizer.step()
            loss_total += float(loss)
        if args.verbose:
            print('Epoch {:2d} | Time: {:4.2f}s | Total Loss: {:5.4f}'.format(epoch + 1, (
                     time.time() - epoch_start_time), loss_total / cnt))
        save_model(model, result_file, epoch)
        if (epoch + 1) % args.exponential_decay_step == 0:
            lr_scheduler.step()
        if (epoch + 1) % args.validate_freq == 0:
            is_best = False
            if args.verbose:
                print('------ VALIDATE ------')
            performance_metrics = \
                validate_baseline(model, args.lstm_node, valid_loader, args.device, args.norm_method, norm_statistic)
            if args.horizon == 1:
                validate_baseline(model, args.lstm_node, valid_loader, args.device, args.norm_method, norm_statistic,
                                  True)
            if np.abs(best_validate_mae) > np.abs(performance_metrics['mae']):
                best_validate_mae = performance_metrics['mae']
                is_best = True
                validate_score_non_decrease_count = 0
            else:
                validate_score_non_decrease_count += 1
            if is_best:
                save_model(model, result_file)
        if args.early_stop and validate_score_non_decrease_count >= args.early_stop_step:
            break
    return performance_metrics
