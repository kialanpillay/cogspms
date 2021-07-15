import json
import os
import time

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data
from sklearn.preprocessing import StandardScaler

import gnn.preprocessing.loader
from gnn.evaluation.validation import validate
from gnn.models.gwnet import GraphWaveNet
from gnn.models.mtgnn import MTGNN
from gnn.models.stemgnn import Model
from gnn.preprocessing.process import transform
from gnn.training.engine import Engine
from gnn.utils import save_model


def init_model(model_name, args):
    if model_name == 'StemGNN':
        return Model(args.node_cnt, 2, args.window_size, args.multi_layer, horizon=args.horizon)
    elif model_name == 'GWN':
        return GraphWaveNet(device=args.device, node_cnt=args.node_cnt, dropout=args.dropout_rate,
                            supports=args.supports, gcn_bool=args.gcn_bool, adapt_adj=args.adapt_adj,
                            adj_init=args.adj_init, in_dim=args.in_dim, out_dim=args.horizon,
                            residual_channels=args.channels, dilation_channels=args.channels,
                            skip_channels=args.channels * 8, end_channels=args.channels * 16)
    else:
        return MTGNN(args.gcn_true, args.buildA_true, args.gcn_depth, args.num_nodes,
                     device=args.device,
                     dropout=args.dropout, subgraph_size=args.subgraph_size,
                     node_dim=args.node_dim,
                     dilation_exponential=args.dilation_exponential,
                     conv_channels=args.conv_channels, residual_channels=args.residual_channels,
                     skip_channels=args.skip_channels, end_channels=args.end_channels,
                     seq_length=args.window_size, in_dim=args.in_dim, out_dim=args.horizon,
                     layers=args.layers, propalpha=args.propalpha, tanhalpha=args.tanhalpha,
                     layer_norm_affline=args.multi_step)


def get_iterable_loader(model_name, loader):
    if model_name == 'StemGNN':
        return loader
    else:
        return loader.get_iterator()


def train(train_data, valid_data, args, result_file):
    model_name = args.model
    model = init_model(model_name, args)
    model.to(args.device)
    if len(train_data) == 0:
        raise Exception('Cannot organize enough training data')
    if len(valid_data) == 0:
        raise Exception('Cannot organize enough validation data')

    if args.norm_method == 'z_score':
        train_mean = np.mean(train_data, axis=0)
        train_std = np.std(train_data, axis=0)
        norm_statistic = {"mean": train_mean.tolist(), "std": train_std.tolist()}

    elif args.norm_method == 'min_max':
        train_min = np.min(train_data, axis=0)
        train_max = np.max(train_data, axis=0)
        norm_statistic = {"min": train_min.tolist(), "max": train_max.tolist()}
    else:
        norm_statistic = None
    if norm_statistic is not None:
        with open(os.path.join(result_file, 'norm_stat.json'), 'w') as f:
            json.dump(norm_statistic, f)

    if args.optim == 'RMSProp':
        optim = torch.optim.RMSprop(params=model.parameters(), lr=args.lr, eps=1e-08)
    elif args.optim == 'SGD':
        optim = torch.optim.SGD(params=model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
    elif args.optim == 'Adagrad':
        optim = torch.optim.Adagrad(params=model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
    elif args.optim == 'Adadelta':
        optim = torch.optim.Adadelta(params=model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
    else:
        optim = torch.optim.Adam(params=model.parameters(), lr=args.lr, betas=(0.9, 0.999))

    my_lr_scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer=optim, gamma=args.decay_rate)

    if model_name == 'StemGNN':

        train_set = gnn.preprocessing.loader.ForecastDataset(train_data, window_size=args.window_size,
                                                             horizon=args.horizon,
                                                             normalise_method=args.norm_method,
                                                             norm_statistic=norm_statistic)
        valid_set = gnn.preprocessing.loader.ForecastDataset(valid_data, window_size=args.window_size,
                                                             horizon=args.horizon,
                                                             normalise_method=args.norm_method,
                                                             norm_statistic=norm_statistic)

        train_loader = torch.utils.data.DataLoader(train_set, batch_size=args.batch_size, drop_last=False, shuffle=True,
                                                   num_workers=0)
        valid_loader = torch.utils.data.DataLoader(valid_set, batch_size=args.batch_size, shuffle=False, num_workers=0)
    else:
        x_train, y_train = transform(train_data, args.window_size, args.horizon)
        x_valid, y_valid = transform(valid_data, args.window_size, args.horizon)
        train_loader = gnn.preprocessing.loader.CustomSimpleDataLoader(x_train, y_train, args.batch_size)
        valid_loader = gnn.preprocessing.loader.CustomSimpleDataLoader(x_valid, y_valid, args.batch_size)

    train_loader = get_iterable_loader(model_name, train_loader)

    forecast_loss = nn.MSELoss(reduction='mean').to(args.device)

    scaler = StandardScaler().fit(train_data)
    if model_name == 'MTGNN':
        engine = Engine(model, forecast_loss, optim, args.clip, args.step_size1, args.horizon, scaler,
                        args.device, args.cl)

    total_params = 0
    for name, parameter in model.named_parameters():
        if not parameter.requires_grad:
            continue
        param = parameter.numel()
        total_params += param
    print(f"Total Trainable Params: {total_params}")
    print(model_name)
    print(train_data.shape)
    best_validate_mae = np.inf
    validate_score_non_decrease_count = 0
    performance_metrics = {}
    for epoch in range(args.epoch):
        epoch_start_time = time.time()
        model.train()
        loss_total = 0
        samples = 0
        cnt = 0
        for i, (inputs, target) in enumerate(train_loader):
            if model_name == 'MTGNN':
                inputs = torch.Tensor(inputs).to(args.device).transpose(1, 3)
                target = torch.Tensor(target).to(args.device).transpose(1, 3)
                if i % args.step_size2 == 0:
                    perm = np.random.permutation(range(args.node_cnt))
                sub = int(args.node_cnt / args.splits)
                for j in range(args.splits):
                    if j != args.splits - 1:
                        idx = perm[j * sub:(j + 1) * sub]
                    else:
                        idx = perm[j * sub:]

                    if args.multi_step:
                        idx = torch.tensor(idx).to(args.device)
                        x = inputs[:, :, idx, :]
                        y = target[:, :, idx, :]
                        loss = engine.train(x, y[:, 0, :, :], idx)
                        cnt += 1
                        loss_total += float(loss)
                    else:
                        idx = torch.tensor(idx).to(args.device)
                        x = inputs[:, :, idx, :]
                        y = target[:, idx]
                        forecast = torch.squeeze(model(x, idx))
                        scale = inputs.scale.expand(forecast.size(0), inputs.shape[1])
                        scale = scale[:, idx]
                        loss = forecast_loss(forecast * scale, y * scale)
                        cnt += 1
                        loss.backward()
                        loss_total += loss.item()
                        samples += (forecast.size() * inputs.shape[1])
                        loss_total += float(loss.item())

            elif model_name == 'GWN':
                inputs = torch.Tensor(inputs).to(args.device).transpose(1, 3)
                target = torch.Tensor(target).to(args.device).transpose(1, 3)
                inputs = F.pad(inputs, (1, 0, 0, 0))
                model.zero_grad()
                forecast = model(inputs).transpose(1, 3)
                target = torch.unsqueeze(target[:, 0, :, :], dim=1)
                loss = forecast_loss(forecast, target)
                cnt += 1
                loss.backward()
                optim.step()
                loss_total += float(loss)
            else:
                inputs = inputs.to(args.device)
                target = target.to(args.device)
                model.zero_grad()
                forecast, _ = model(inputs)
                loss = forecast_loss(forecast, target)
                cnt += 1
                loss.backward()
                optim.step()
                loss_total += float(loss)
        print('| end of epoch {:3d} | time: {:5.2f}s | train_total_loss {:5.4f}'.format(epoch, (
                time.time() - epoch_start_time), loss_total / cnt))
        save_model(model, result_file, epoch)
        if (epoch + 1) % args.exponential_decay_step == 0:
            my_lr_scheduler.step()
        if (epoch + 1) % args.validate_freq == 0:
            is_best = False
            print('------ VALIDATE ------')
            performance_metrics = \
                validate(model, model_name, valid_loader, args.device, args.norm_method, norm_statistic,
                         args.node_cnt, args.window_size, args.horizon,
                         result_file=result_file, scaler=scaler)
            if best_validate_mae > performance_metrics['mae']:
                best_validate_mae = performance_metrics['mae']
                is_best = True
                validate_score_non_decrease_count = 0
            else:
                validate_score_non_decrease_count += 1
            if is_best:
                save_model(model, result_file)
        if args.early_stop and validate_score_non_decrease_count >= args.early_stop_step:
            break
    return performance_metrics, norm_statistic
