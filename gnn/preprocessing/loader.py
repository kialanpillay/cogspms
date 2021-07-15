import os
import pickle

import numpy as np
import pandas as pd
import torch
import torch.utils.data as torch_data
from torch.autograd import Variable

from gnn.utils import calculate_scaled_laplacian, symmetric_adjacency, asymmetric_adjacency, \
    calculate_normalized_laplacian, normalized


class CustomDataLoader(object):
    def __init__(self, file_name, train, valid, device, window_size, horizon, normalize=2):
        self.P = window_size
        self.h = horizon
        self.raw_dat = np.loadtxt(file_name, delimiter=',')
        self.dat = np.zeros(self.raw_dat.shape)
        self.n, self.m = self.dat.shape
        self.normalise = 2
        self._normalized(normalize)
        self._split(int(train * self.n), int((train + valid) * self.n))
        self.scale = Variable(self.scale.to(torch.from_numpy(np.ones(self.m).astype(np.float64))))
        self.device = device

    def _normalized(self, normalize):
        if normalize == 0:
            self.dat = self.raw_dat

        if normalize == 1:
            self.dat = self.raw_dat / np.max(self.raw_dat)

        if normalize == 2:
            for i in range(self.m):
                self.scale[i] = np.max(np.abs(self.raw_dat[:, i]))
                self.dat[:, i] = self.raw_dat[:, i] / np.max(np.abs(self.raw_dat[:, i]))

    def _split(self, train, valid):

        train_set = range(self.P + self.h - 1, train)
        valid_set = range(train, valid)
        test_set = range(valid, self.n)
        self.train = self._batchify(train_set)
        self.valid = self._batchify(valid_set)
        self.test = self._batchify(test_set)

    def _batchify(self, idx_set):
        n = len(idx_set)
        X = torch.zeros((n, self.P, self.m))
        Y = torch.zeros((n, self.m))
        for i in range(n):
            end = idx_set[i] - self.h + 1
            start = end - self.P
            X[i, :, :] = torch.from_numpy(self.dat[start:end, :])
            Y[i, :] = torch.from_numpy(self.dat[idx_set[i], :])
        return [X, Y]

    def get_batches(self, inputs, targets, batch_size, shuffle=True):
        length = len(inputs)
        if shuffle:
            index = torch.randperm(length)
        else:
            index = torch.LongTensor(range(length))
        start_idx = 0
        while start_idx < length:
            end_idx = min(length, start_idx + batch_size)
            excerpt = index[start_idx:end_idx]
            X = inputs[excerpt]
            Y = targets[excerpt]
            X = X.to(self.device)
            Y = Y.to(self.device)
            yield Variable(X), Variable(Y)
            start_idx += batch_size


class CustomSimpleDataLoader(object):
    def __init__(self, xs, ys, batch_size, pad_with_last_sample=True):
        self.batch_size = batch_size
        self.current_ind = 0
        if pad_with_last_sample:
            num_padding = (batch_size - (len(xs) % batch_size)) % batch_size
            x_padding = np.repeat(xs[-1:], num_padding, axis=0)
            y_padding = np.repeat(ys[-1:], num_padding, axis=0)
            xs = np.concatenate([xs, x_padding], axis=0)
            ys = np.concatenate([ys, y_padding], axis=0)
        self.size = len(xs)
        self.num_batch = int(self.size // self.batch_size)
        self.xs = xs
        self.ys = ys

    def shuffle(self):
        permutation = np.random.permutation(self.size)
        xs, ys = self.xs[permutation], self.ys[permutation]
        self.xs = xs
        self.ys = ys

    def get_iterator(self):
        self.current_ind = 0

        def wrapper():
            while self.current_ind < self.num_batch:
                start_ind = self.batch_size * self.current_ind
                end_ind = min(self.size, self.batch_size * (self.current_ind + 1))
                x_i = self.xs[start_ind: end_ind, ...]
                y_i = self.ys[start_ind: end_ind, ...]
                yield x_i, y_i
                self.current_ind += 1

        return wrapper()


class ForecastDataset(torch_data.Dataset):
    def __init__(self, df, window_size, horizon, normalise_method=None, norm_statistic=None, interval=1):
        self.window_size = window_size
        self.interval = interval
        self.horizon = horizon
        self.normalize_method = normalise_method
        self.norm_statistic = norm_statistic
        df = pd.DataFrame(df)
        df = df.fillna(method='ffill', limit=len(df)).fillna(method='bfill', limit=len(df)).values
        self.data = df
        self.df_length = len(df)
        self.x_end_idx = self.get_x_end_idx()
        if normalise_method:
            self.data, _ = normalized(self.data, normalise_method, norm_statistic)

    def __getitem__(self, index):
        hi = self.x_end_idx[index]
        lo = hi - self.window_size
        train_data = self.data[lo: hi]
        target_data = self.data[hi:hi + self.horizon]
        x = torch.from_numpy(train_data).type(torch.float)
        y = torch.from_numpy(target_data).type(torch.float)
        return x, y

    def __len__(self):
        return len(self.x_end_idx)

    def get_x_end_idx(self):
        x_index_set = range(self.window_size, self.df_length - self.horizon + 1)
        x_end_idx = [x_index_set[j * self.interval] for j in range((len(x_index_set)) // self.interval)]
        return x_end_idx


def load_pickle(pickle_file):
    try:
        with open(pickle_file, 'rb') as f:
            pickle_data = pickle.load(f)
    except UnicodeDecodeError:
        with open(pickle_file, 'rb') as f:
            pickle_data = pickle.load(f, encoding='latin1')
    except Exception as e:
        print('Unable to load data ', pickle_file, ':', e)
        raise
    return pickle_data


def load_adj(pkl_filename, adj_type):
    _, _, adj = load_pickle(pkl_filename)
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
        assert error, "Adjacency matrix type not defined"
    return adj


def load(dataset, train_length, valid_length, test_length):
    data_file = os.path.join('data', dataset + '.csv')
    data = pd.read_csv(data_file).values

    train_ratio = train_length / (train_length + valid_length + test_length)
    valid_ratio = valid_length / (train_length + valid_length + test_length)
    train_data = data[:int(train_ratio * len(data))]
    valid_data = data[int(train_ratio * len(data)):int((train_ratio + valid_ratio) * len(data))]
    test_data = data[int((train_ratio + valid_ratio) * len(data)):]
    return train_data, valid_data, test_data
