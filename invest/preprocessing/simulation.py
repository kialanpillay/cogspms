import random


def simulate(df, frac=0.3, scale=1, method='std'):
    idx = df.sample(frac=frac).index
    if method == 'std':
        for col in df.columns:
            if col == "Name" or col == "Date":
                continue
            uniform = random.uniform(0, 1)
            if uniform >= 0.5:
                df.loc[idx, col] += df[col].std() * scale
            else:
                df.loc[idx, col] -= df[col].std() * scale
    if method == 'zero':
        for col in df.columns:
            if col == "Name" or col == "Date":
                continue
            df.loc[idx, col] = 0
    if method == 'mean':
        for col in df.columns:
            if col == "Name" or col == "Date":
                continue
            df.loc[idx, col] = df[col].mean() * scale
    return df
