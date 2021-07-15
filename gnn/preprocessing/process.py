import numpy as np


def transform(data, window_size, horizon):
    x_offsets = np.sort(np.concatenate((np.arange(-(window_size - 1), 1, 1),)))
    y_offsets = np.sort(np.arange(1, (horizon + 1), 1))
    samples, nodes = data.shape[0], data.shape[1]
    data = np.expand_dims(data, axis=-1)
    data = np.concatenate([data], axis=-1)
    x, y = [], []
    min_t = abs(min(x_offsets))
    max_t = abs(samples - abs(max(y_offsets)))
    for t in range(min_t, max_t):
        x.append(data[t + x_offsets, ...])
        y.append(data[t + y_offsets, ...])
    x = np.stack(x, axis=0)
    y = np.stack(y, axis=0)
    return x, y
