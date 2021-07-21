import json
import os

import torch
import torch.utils.data
from sklearn.preprocessing import StandardScaler

import gnn.preprocessing.loader
from gnn.evaluation.validation import validate
from gnn.preprocessing.process import transform
from gnn.utils import load_model


def test(test_data, args, result_train_file, result_test_file):
    with open(os.path.join(result_train_file, 'norm_stat.json'), 'r') as f:
        normalize_statistic = json.load(f)
    model = load_model(result_train_file)
    node_cnt = test_data.shape[1]
    test_set = gnn.preprocessing.loader.ForecastDataset(test_data, window_size=args.window_size, horizon=args.horizon,
                                                        normalize_method=args.norm_method,
                                                        norm_statistic=normalize_statistic)
    test_loader = torch.utils.data.DataLoader(test_set, batch_size=args.batch_size, drop_last=False,
                                              shuffle=False, num_workers=0)
    performance_metrics = validate(model, args.model, test_loader, args.device, args.norm_method, normalize_statistic,
                                   node_cnt, args.window_size, args.horizon,
                                   result_file=result_test_file)
    mae, mape, rmse = performance_metrics['mae'], performance_metrics['mape'], performance_metrics['rmse']
    print('Performance on test set: MAPE: {:5.2f} | MAE: {:5.2f} | RMSE: {:5.4f}'.format(mape, mae, rmse))


def custom_test(test_data, args, result_train_file, result_test_file):
    with open(os.path.join(result_train_file, 'norm_stat.json'), 'r') as f:
        normalize_statistic = json.load(f)
    model = load_model(result_train_file)
    scaler = StandardScaler()
    scaler.fit(test_data)
    x, y = transform(test_data, args.window_size, args.horizon)
    test_loader = gnn.preprocessing.loader.CustomSimpleDataLoader(x, y, args.batch_size)
    performance_metrics = validate(model, args.model, test_loader, args.device, args.norm_method, normalize_statistic,
                                   args.node_cnt, args.window_size, args.horizon,
                                   result_file=result_test_file, scaler=scaler)
    mae, mape, rmse = performance_metrics['mae'], performance_metrics['mape'], performance_metrics['rmse']
    print('Performance on test set: MAPE: {:5.2f} | MAE: {:5.2f} | RMSE: {:5.4f}'.format(mape, mae, rmse))
