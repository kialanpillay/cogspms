import numpy as np
import pandas as pd
from sklearn.cluster import SpectralCoclustering


def spectral_bicluster(df, n_clusters=5):
    model = SpectralCoclustering(n_clusters=n_clusters, random_state=0)
    model.fit(df.values)

    fit_data = df.values[np.argsort(model.row_labels_)]
    columns = []
    for c in np.argsort(model.row_labels_):
        columns.append(df.columns[c])
    fit_data = fit_data[:, np.argsort(model.column_labels_)]

    df_ = pd.DataFrame(fit_data, columns=columns)
    df_.index = columns
    return df_
