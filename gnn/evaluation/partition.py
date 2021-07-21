from sklearn.model_selection import TimeSeriesSplit


def partition(data, n_splits=5, valid_ratio=0.1):
    time_series_split = TimeSeriesSplit(n_splits=n_splits)
    for train_validation, test in time_series_split.split(data):
        train_end = int((1.0 - valid_ratio) * len(train_validation))
        train = train_validation[:train_end]
        validation = train_validation[train_end:]
        yield train, validation, test


def train_validation_(partitions):
    for train, val, _ in partitions:
        yield train, val
