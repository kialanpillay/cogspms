import numpy as np
import torch


def masked_metric(mask, metric, axis=None):
    if np.any(mask):
        masked_array = np.ma.masked_array(metric, mask=mask)
        result = masked_array.mean(axis=axis)
        if isinstance(result, np.ma.MaskedArray):
            return result.filled(np.nan)
        else:
            return result
    return np.mean(metric, axis).astype(np.float64)


def masked_mae(v, v_, axis=None):
    mask = (v == 0)
    metric = np.abs(v_ - v)
    return masked_metric(mask, metric, axis)


def masked_mape(v, v_, axis=None):
    mask = (v == 0)
    metric = np.abs(v_ - v) / np.abs(v)
    return masked_metric(mask, metric, axis)


def masked_rmse(v, v_, axis=None):
    mask = (v == 0)
    metric = np.mean((v_ - v) ** 2)
    return masked_metric(mask, metric, axis)


def mae(v, v_, axis=None):
    return np.mean(np.abs(v_ - v), axis).astype(np.float64)


def mape(v, v_, axis=None):
    metric = (np.abs(v_ - v) / np.abs(v) + 1e-5).astype(np.float64)
    return np.mean(metric, axis)


def mse(v, v_, axis=None):
    return np.mean((v_ - v) ** 2, axis).astype(np.float64)


def rmse(v, v_, axis=None):
    return np.sqrt(np.mean((v_ - v) ** 2, axis)).astype(np.float64)


def evaluate(y, y_hat, by_step=False, by_node=False):
    if not by_step and not by_node:
        return mape(y, y_hat), mae(y, y_hat), rmse(y, y_hat)
    if by_step and by_node:
        return mape(y, y_hat, axis=0), mae(y, y_hat, axis=0), rmse(y, y_hat, axis=0)
    if by_step:
        return mape(y, y_hat, axis=(0, 2)), mae(y, y_hat, axis=(0, 2)), rmse(y, y_hat, axis=(0, 2))
    if by_node:
        return mape(y, y_hat, axis=(0, 1)), mae(y, y_hat, axis=(0, 1)), rmse(y, y_hat, axis=(0, 1))


def evaluate_multiple(ys, ys_hat, by_node=False):
    if not by_node:
        return masked_mape_(ys, ys_hat), masked_mae_(ys, ys_hat), masked_rmse_(ys, ys_hat)
    else:
        return masked_mape_(ys, ys_hat), masked_mae_(ys, ys_hat), masked_rmse_(ys, ys_hat)


def get_mask(v, null_val):
    if np.isnan(null_val):
        mask = ~torch.isnan(v)
    else:
        mask = (v != null_val)
    mask = mask.float()
    mask /= torch.mean(mask)
    return torch.where(torch.isnan(mask), torch.zeros_like(mask), mask)


def masked_mse_(v, v_, null_val=np.nan):
    mask = get_mask(v, null_val)
    metric = ((v_ - v) ** 2) * mask
    metric = torch.where(torch.isnan(metric), torch.zeros_like(metric), metric)
    return torch.mean(metric)


def masked_rmse_(v, v_, null_val=np.nan):
    return torch.sqrt(masked_mse_(v, v_, null_val=null_val)).item()


def masked_mae_(v, v_, null_val=np.nan):
    mask = get_mask(v, null_val)
    metric = torch.abs(v_ - v) * mask
    metric = torch.where(torch.isnan(metric), torch.zeros_like(metric), metric)
    return torch.mean(metric).item()


def masked_mape_(v, v_, null_val=np.nan):
    mask = get_mask(v, null_val)
    metric = (torch.abs(v_ - v) * mask / v) * mask
    metric = metric * mask
    metric = torch.where(torch.isnan(metric), torch.zeros_like(metric), metric)
    return torch.mean(metric)
