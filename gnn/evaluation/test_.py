import json
import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sn
import torch
import torch.utils.data

import gnn.preprocessing.loader
from gnn.evaluation.validation import validate, validate_baseline, validate_regressor
from gnn.preprocessing.utils import process_data
from gnn.utils import load_model


def test(test_data, args, result_train_file):
    """
    Evaluates a StemGNN model and returns raw and normalized error metrics
    computed on out-of-sample set predictions

    Parameters
    ----------
    test_data : numpy.ndarray
        Test set
    args : argparse.Namespace
        Command line arguments
    result_train_file : str
        Directory to load trained model parameter files
    """
    with open(os.path.join(result_train_file, 'norm_stat.json'), 'r') as f:
        normalize_statistic = json.load(f)
    model = load_model(result_train_file)

    if model.final_adj is not None:
        adj = model.final_adj.detach().cpu().numpy()
        sn.set(font_scale=0.5)
        columns = pd.read_csv('data/' + args.dataset + '.csv').columns
        df = pd.DataFrame(data=adj, columns=columns)
        df.index = columns.values
        df.to_csv(args.model + '_corr.csv')
        sn.heatmap(df, annot=False, center=0, cmap='coolwarm', square=True)
        if 'JSE' in args.dataset:
            if not os.path.exists('img'):
                os.makedirs('img')
            plt.savefig(os.path.join('img', args.model + '_corr.png'), dpi=300, bbox_inches='tight')

    node_cnt = test_data.shape[1]
    test_set = gnn.preprocessing.loader.ForecastDataset(test_data, window_size=args.window_size, horizon=args.horizon,
                                                        normalize_method=args.norm_method,
                                                        norm_statistic=normalize_statistic)
    test_loader = torch.utils.data.DataLoader(test_set, batch_size=args.batch_size, drop_last=False,
                                              shuffle=False, num_workers=0)
    performance_metrics = validate(model, args.model, test_loader, args.device, args.norm_method, normalize_statistic,
                                   node_cnt, args.window_size, args.horizon)
    mae, mape, rmse = performance_metrics['mae'], performance_metrics['mape'], performance_metrics['rmse']
    print('Test Set Performance: MAPE: {:5.2f} | MAE: {:5.2f} | RMSE: {:5.2f}'.format(mape * 100, mae, rmse))


def baseline_test(test_data, args, result_train_file):
    """
    Evaluates a LSTM model and returns raw and normalized error metrics
    computed on out-of-sample set predictions

    Parameters
    ----------
    test_data : numpy.ndarray
        Test set
    args : argparse.Namespace
        Command line arguments
    result_train_file : str
        Directory to load trained model parameter files
    """
    with open(os.path.join(result_train_file, 'norm_stat.json'), 'r') as f:
        normalize_statistic = json.load(f)
    model = load_model(result_train_file)
    test_set = gnn.preprocessing.loader.ForecastDataset(test_data, window_size=args.window_size, horizon=args.horizon,
                                                        normalize_method=args.norm_method)
    test_loader = torch.utils.data.DataLoader(test_set, batch_size=args.batch_size, drop_last=False,
                                              shuffle=False, num_workers=0)
    performance_metrics = validate_baseline(model, args.lstm_node, test_loader, args.device, args.norm_method,
                                            normalize_statistic)
    mae, mape, rmse = performance_metrics['mae'], performance_metrics['mape'], performance_metrics['rmse']
    print('Test Set Performance: MAPE: {:5.2f} | MAE: {:5.2f} | RMSE: {:5.2f}'.format(mape * 100, mae, rmse))

    if args.horizon == 1:
        performance_metrics = validate_baseline(model, args.lstm_node, test_loader, args.device, args.norm_method,
                                                normalize_statistic, True)
        mae, mape, rmse = performance_metrics['mae'], performance_metrics['mape'], performance_metrics['rmse']
        print(
            'Last-Value Test Set Performance: MAPE: {:5.2f} | MAE: {:5.2f} | RMSE: {:5.2f}'.format(mape * 100, mae,
                                                                                                   rmse))


def regressor_test(model, test_data, args, result_train_file):
    with open(os.path.join(result_train_file, 'norm_stat.json'), 'r') as f:
        normalize_statistic = json.load(f)
    test_set = gnn.preprocessing.loader.ForecastDataset(test_data, window_size=args.window_size, horizon=args.horizon,
                                                        normalize_method=args.norm_method)
    test_loader = torch.utils.data.DataLoader(test_set, batch_size=args.batch_size, drop_last=False,
                                              shuffle=False, num_workers=0)
    performance_metrics = validate_regressor(model, args.node, test_loader, args.norm_method,
                                             normalize_statistic)
    mae, mape, rmse = performance_metrics['mae'], performance_metrics['mape'], performance_metrics['rmse']
    print('Test Set Performance: MAPE: {:5.2f} | MAE: {:5.2f} | RMSE: {:5.2f}'.format(mape * 100, mae, rmse))
    print('{:5.2f},{:5.2f},{:5.2f}'.format(mape * 100, mae, rmse))
    if args.horizon == 1:
        performance_metrics = validate_regressor(model, args.node, test_loader, args.norm_method,
                                                 normalize_statistic, True)
        mae, mape, rmse = performance_metrics['mae'], performance_metrics['mape'], performance_metrics['rmse']
        print(
            'Last-Value Test Set Performance: MAPE: {:5.2f} | MAE: {:5.2f} | RMSE: {:5.2f}'.format(mape * 100, mae,
                                                                                                   rmse))


def custom_test(test_data, args, result_train_file):
    """
    Evaluates a GWN or MTGNN model and returns raw and normalized error metrics
    computed on out-of-sample set predictions

    Parameters
    ----------
    test_data : numpy.ndarray
        Test set
    args : argparse.Namespace
        Command line arguments
    result_train_file : str
        Directory to load trained model parameter files
    """
    with open(os.path.join(result_train_file, 'norm_stat.json'), 'r') as f:
        normalize_statistic = json.load(f)
    model = load_model(result_train_file)

    if model.final_adj:
        adj = model.final_adj[0].detach().cpu().numpy()
        sn.set(font_scale=1)
        columns = pd.read_csv('data/' + args.dataset + '.csv').columns
        df = pd.DataFrame(data=adj, columns=columns)
        df.index = columns.values
        df.to_csv(args.model + '_corr.csv')
        sn.heatmap(df, annot=False, center=0, cmap='coolwarm', square=True)
        if 'JSE' in args.dataset:
            if not os.path.exists('img'):
                os.makedirs('img')
            plt.savefig(os.path.join('img', args.model + '_adj.png'), dpi=300, bbox_inches='tight')

    x, y = process_data(test_data, args.window_size, args.horizon)
    scaler = gnn.preprocessing.loader.CustomStandardScaler(mean=x.mean(), std=x.std())
    test_loader = gnn.preprocessing.loader.CustomSimpleDataLoader(scaler.transform(x), scaler.transform(y),
                                                                  args.batch_size)
    performance_metrics = validate(model, args.model, test_loader, args.device, args.norm_method, normalize_statistic,
                                   args.node_cnt, args.window_size, args.horizon, scaler=scaler)
    mae, mape, rmse = performance_metrics['mae'], performance_metrics['mape'], performance_metrics['rmse']
    print('Test Set Performance: MAPE: {:5.2f} | MAE: {:5.2f} | RMSE: {:5.2f}'.format(mape * 100, mae, rmse))
