import os

import numpy as np
import torch
import torch.utils.data

from gnn.metrics.error import evaluate, evaluate_multiple
from gnn.utils import denormalized


def custom_inference(model, data_loader, device):
    model.eval()
    forecast_set = []
    with torch.no_grad():
        for i, (inputs, target) in enumerate(data_loader.get_iterator()):
            inputs = torch.Tensor(inputs).to(device).transpose(1, 3)
            target = torch.Tensor(target).to(device).transpose(1, 3)[:, 0, :, :]
            forecast_result = model(inputs).transpose(1, 3)
            forecast_set.append(forecast_result.squeeze())

    return torch.cat(forecast_set, dim=0)[:target.size(0), ...], target


def inference(model, data_loader, device, node_cnt, window_size, horizon):
    forecast_set = []
    target_set = []
    model.eval()
    with torch.no_grad():
        for i, (inputs, target) in enumerate(data_loader):
            inputs = inputs.to(device)
            target = target.to(device)
            step = 0
            forecast_steps = np.zeros([inputs.size()[0], horizon, node_cnt], dtype=np.float)
            while step < horizon:
                if model == 'MTGNN' or model == 'GWN':
                    forecast_result = model(inputs)
                    forecast_result = forecast_result.transpose(1, 3)
                else:
                    forecast_result, _ = model(inputs)
                len_model_output = forecast_result.size()[1]
                if len_model_output == 0:
                    raise Exception('Get blank inference result')
                inputs[:, :window_size - len_model_output, :] = inputs[:, len_model_output:window_size,
                                                                :].clone()
                inputs[:, window_size - len_model_output:, :] = forecast_result.clone()
                forecast_steps[:, step:min(horizon - step, len_model_output) + step, :] = \
                    forecast_result[:, :min(horizon - step, len_model_output), :].detach().cpu().numpy()
                step += min(horizon - step, len_model_output)
            forecast_set.append(forecast_steps)
            target_set.append(target.detach().cpu().numpy())
    return np.concatenate(forecast_set, axis=0), np.concatenate(target_set, axis=0)


def validate(model, model_name, data_loader, device, normalise_method, statistic,
             node_cnt, window_size, horizon,
             result_file=None, scaler=None):
    if model_name == 'StemGNN':
        forecast_norm, target_norm = inference(model, data_loader, device,
                                               node_cnt, window_size, horizon)
        print(forecast_norm.shape, target_norm.shape)
    else:
        forecast_norm, target_norm = custom_inference(model, data_loader, device)

    if model_name == 'StemGNN':
        if normalise_method and statistic:
            forecast = denormalized(forecast_norm, normalise_method, statistic)
            target = denormalized(target_norm, normalise_method, statistic)
        else:
            forecast, target = forecast_norm, target_norm
        score = evaluate(target, forecast)
        score_by_node = evaluate(target, forecast, by_node=True)
        score_norm = evaluate(target_norm, forecast_norm)
    else:
        mae = ([], [])
        mape = ([], [])
        rmse = ([], [])
        for i in range(horizon):
            if normalise_method and statistic:
                forecast = torch.Tensor(scaler.inverse_transform(forecast_norm[:, :, i]))
                target = torch.Tensor(scaler.inverse_transform(target_norm[:, :, i]))
            else:
                forecast, target = forecast_norm, target_norm
            score = evaluate_multiple(target, forecast)
            score_norm = evaluate_multiple(target_norm[:, :, i], forecast_norm[:, :, i])

            mae[0].append(score[0])
            mape[0].append(score[1])
            rmse[0].append(score[2])

            mae[1].append(score_norm[0])
            mape[1].append(score_norm[1])
            rmse[1].append(score_norm[2])
        score = (np.mean(mape[0]), np.mean(mae[0]), np.mean(rmse[0]))
        score_norm = (np.mean(mape[1]), np.mean(mae[1]), np.mean(rmse[1]))
    print(f'NORM: MAPE {score_norm[0]:7.9%}; MAE {score_norm[1]:7.9f}; RMSE {score_norm[2]:7.9f}.')
    print(f'RAW : MAPE {score[0]:7.9%}; MAE {score[1]:7.9f}; RMSE {score[2]:7.9f}.')
    if result_file and model_name == 'StemGNN':
        if not os.path.exists(result_file):
            os.makedirs(result_file)
        step_to_print = 0
        forecasting_2d = forecast[:, step_to_print, :]
        forecasting_2d_target = target[:, step_to_print, :]

        np.savetxt(f'{result_file}/target.csv', forecasting_2d_target, delimiter=",")
        np.savetxt(f'{result_file}/predict.csv', forecasting_2d, delimiter=",")
        np.savetxt(f'{result_file}/predict_abs_error.csv',
                   np.abs(forecasting_2d - forecasting_2d_target), delimiter=",")
        np.savetxt(f'{result_file}/predict_ape.csv',
                   np.abs((forecasting_2d - forecasting_2d_target) / forecasting_2d_target), delimiter=",")

    return dict(mae=score[1], mape=score[0], rmse=score[2], )
