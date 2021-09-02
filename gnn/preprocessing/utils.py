import numpy as np

from gnn.utils import calculate_scaled_laplacian, symmetric_adjacency, asymmetric_adjacency, \
    calculate_normalized_laplacian, correlation_adjacency_matrix


def process_data(data, window_size, horizon):
    """
    Transforms a two-dimensional input (N x T) into a four-dimensional dataset,
    where N is the number of nodes and T is the steps.

    Yaguang Li, Rose Yu, Cyrus Shahabi, and Yan Liu. 2018.
    Diffusion Convolutional Recurrent Neural Network: Data-Driven Traffic Forecasting.

    Parameters
    ----------
    data : numpy.ndarray
        Input dataset
    window_size : int
        Input sequence length
    horizon : int
        Output sequence length

    Returns
    -------
    numpy.ndarray
    """
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


def process_adjacency_matrix(adj_data, adj_type):
    """
    Preprocesses a Graph WaveNet adjacency matrix

    Parameters
    ----------
    adj_data : numpy.ndarray
        Graph adjacency matrix
    adj_type : str
        Adjacency matrix transformation type

    Returns
    -------
    [numpy.ndarray]
    """
    adj = correlation_adjacency_matrix(adj_data)
    if adj_type == "scaled_laplacian":
        adj = [calculate_scaled_laplacian(adj)]
    elif adj_type == "normalized_laplacian":
        adj = [calculate_normalized_laplacian(adj).astype(np.float32).todense()]
    elif adj_type == "symmetric_adjacency" or adj_type == "transition":
        adj = [symmetric_adjacency(adj)]
    elif adj_type == "double_transition":
        adj = [asymmetric_adjacency(adj), asymmetric_adjacency(np.transpose(adj))]
    elif adj_type == "identity":
        adj = [np.diag(np.ones(adj.shape[0])).astype(np.float32)]
    else:
        error = 0
        assert error
    return adj
