import json
import os

import torch
import torch.utils.data
from sklearn.preprocessing import StandardScaler

import gnn.preprocessing.loader
from gnn.evaluation.validation import inference as inference_, custom_inference as custom_inference_
from gnn.preprocessing.loader import load_dataset
from gnn.utils import load_model, denormalized


def future_share_price_performance():
    result_file = os.path.join('output', 'StemGNN', 'invest', 'train')
    data = load_dataset('invest', 6, 2, 2)
    y = data[-1, :]
    forecast = inference(data, 'StemGNN', result_file).detach().cpu().numpy()
    y_hat = forecast.mean(axis=0)
    return classify(y, y_hat)


def inference(data, model_name, result_file):
    with open(os.path.join(result_file, 'norm_stat.json'), 'r') as f:
        normalize_statistic = json.load(f)
    scaler = StandardScaler()
    scaler.fit(data)
    model = load_model(result_file)
    test_set = gnn.preprocessing.loader.ForecastDataset(data, window_size=12, horizon=12,
                                                        normalize_method='z_score',
                                                        norm_statistic=normalize_statistic)
    data_loader = torch.utils.data.DataLoader(test_set, batch_size=32, drop_last=False,
                                              shuffle=False, num_workers=0)
    if model_name == 'StemGNN':
        forecast_norm, target_norm = inference_(model, data_loader, 'cpu',
                                                data.shape[1], 12, 12)
        forecast = denormalized(forecast_norm, 'z_score', normalize_statistic)
        return forecast[-1, :]
    else:
        forecast_norm, target_norm = custom_inference_(model, data_loader)
        forecast = torch.Tensor()
        for i in range(12):
            forecast = torch.Tensor(scaler.inverse_transform(forecast_norm[:, :, i]))

        return forecast[-1, :, :]


def classify(y, y_hat):
    classification = []
    for i in range(len(y)):
        if (y_hat[i] / y[i]) >= 1.02:
            classification.append(1)
        elif 0.98 < (y_hat[i] / y[i]) < 1.02:
            classification.append(0)
        else:
            classification.append(-1)
