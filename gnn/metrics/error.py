import numpy as np


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
