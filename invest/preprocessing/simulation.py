import random

def simulate(df, n=3, scale=1, method='std'):
    idx = df.sample(n).index
    if method == 'std':
        for col in df.columns:
            uniform = random.uniform(0, 1)
            if uniform >= 0.5:
                df.loc[idx, col] += df[col].std() * scale
            else:
                df.loc[idx, col] -= df[col].std() * scale
    if method == 'zero':
        for col in df.columns:
            df.loc[idx, col] = 0
    if method == 'mean':
        for col in df.columns:
            df.loc[idx, col] = df[col].mean() * scale
    return df
