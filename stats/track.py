# Get parameters related to a single track

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from time import time
import numpy as np
import pandas as pd

def get_motility(data_cell, time_limit=601):
    """

    :param data_cell: pandas dataframe,  Imaris statistics dataset obtained using base_imaris.stats.get_imaris_statistics
    :param time_limit : Int64, time limit(in seconds) up to which track data is used,  default is 601s (10 minutes)
    :return: Retruns a wide-format pandas dataframe containing motility
    """

    columns_use = ['trackID', 'track_time', 'Displacement^2']
    data_use = data_cell.loc[:, columns_use].copy()
    data_use.sort_values(by=['trackID', 'track_time'], inplace=True)
    data_use = data_use.loc[data_use.track_time.lt(time_limit).values, :].copy()
    data_use['t_since_start'] = pd.cut(data_use.track_time.values,
                                       bins=np.arange(start=-1, stop=601, step=60),
                                       labels=np.arange(1, 11))

    data_use_long = data_use.loc[:, ['trackID', 't_since_start', 'Displacement^2']].copy()
    X = data_use_long.t_since_start.ravel().reshape(-1, 1).astype(np.float64)
    y = data_use_long.loc[:, 'Displacement^2'].ravel().reshape(-1, 1).astype(np.float64)

    model = LinearRegression(normalize=True)
    model.fit(X=X, y=y)
    beta = model.coef_[0][0]
    c = model.intercept_[0]
    r2 = r2_score(y, model.predict(X))

    data_out = {}
    for t in range(X.shape[0]):
        t_val = np.int64(t)
        t_name = 't'+str(t_val).zfill(2)
        data_out[t_name] = y.ravel()[t]

    data_out['motility'] = beta
    data_out['beta'] = beta
    data_out['c'] = c
    data_out['r2'] = r2
    data_out['n'] = data_cell.shape[0]

    data_out = pd.DataFrame.from_dict(data_out, orient='index').T
    data_out = data_out.sort_index(axis=1)
    return(data_out)