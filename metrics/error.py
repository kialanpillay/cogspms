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


def rmse(v, v_, axis=None):
    return np.sqrt(np.mean((v_ - v) ** 2, axis)).astype(np.float64)
