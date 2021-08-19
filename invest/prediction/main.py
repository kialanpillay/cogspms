import json
import os

import numpy as np
import pandas as pd
import torch
import torch.utils.data

from gnn.evaluation.validation import inference as inference_, custom_inference as custom_inference_
from gnn.preprocessing.loader import CustomStandardScaler, ForecastDataset, CustomSimpleDataLoader
from gnn.preprocessing.utils import process_data
from gnn.utils import load_model, inverse_transform_


def future_share_price_performance(year, model_name="GWN", dataset="INVEST_GNN_clean", horizon=10):
    result_file = os.path.join('output', model_name, dataset, 'train')
    ub = ((year - 2009) * 365)
    df = pd.read_csv(os.path.join('data', dataset + '.csv'))
    data = df.values
    y = data[ub - 1, :]

    forecast = inference(data[0:ub, :], model_name, result_file, horizon=horizon).detach().cpu().numpy()
    y_hat = forecast.mean(axis=1)
    classification = classify(y, y_hat)

    d = {}
    for i, c in enumerate(df.columns):
        d[c] = [classification[i]]
    return pd.DataFrame(d, columns=df.columns)


def inference(data, model_name, result_file, window_size=40, horizon=10):
    with open(os.path.join(result_file, 'norm_stat.json'), 'r') as f:
        normalize_statistic = json.load(f)
    model = load_model(result_file)
    if model_name == 'StemGNN':
        data_set = ForecastDataset(data, window_size=window_size, horizon=horizon,
                                   normalize_method='z_score',
                                   norm_statistic=normalize_statistic)
        data_loader = torch.utils.data.DataLoader(data_set, batch_size=32, drop_last=False,
                                                  shuffle=False, num_workers=0)
        forecast_norm, target_norm = inference_(model, data_loader, 'cpu',
                                                data.shape[1], window_size, horizon)
        forecast = inverse_transform_(forecast_norm, 'z_score', normalize_statistic)
        # N x H
        return np.swapaxes(forecast[-1, :], 0, 1)
    else:
        x, y = process_data(data, window_size, horizon)
        scaler = CustomStandardScaler(mean=x.mean(), std=x.std())
        data_loader = CustomSimpleDataLoader(scaler.transform(x), scaler.transform(y), 32)
        forecast_norm, target_norm = custom_inference_(model, data_loader)
        # N x H
        return scaler.inverse_transform(forecast_norm[-1, :, :])


def classify(y, y_hat):
    classification = []
    for i in range(len(y)):
        if (y_hat[i] / y[i]) >= 1.02:
            classification.append(1)
        elif 0.98 < (y_hat[i] / y[i]) < 1.02:
            classification.append(0)
        else:
            classification.append(-1)
    return classification
