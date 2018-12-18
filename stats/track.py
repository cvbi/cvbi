# Get parameters related to a single track

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


def get_motility(data_cell, time_limit=600):
    """

    :param data_cell: pandas dataframe,  Imaris statistics dataset obtained using base_imaris.stats.get_imaris_statistics
    :param time_limit : Int64, time limit(in seconds) up to which track data is used,  default is 600s (10 minutes)
    :return: Retruns a wide-format pandas dataframe containing
    """

    columns_use = ['trackID', 'Time Since Track Start', 'Displacement^2']
    data_use = data_cell.loc[:, columns_use].copy()
    data_use.sort_values(by=['trackID', 'Time Since Track Start'], inplace=True)
    data_use = data_use.loc[data_use.loc[:, 'Time Since Track Start'].lt(time_limit).values, :].copy()
    data_use['t_since_start'] = data_use.loc[:, 'Time Since Track Start'].lt(time_limit).values.cumsum()

    data_use_long = data_use.loc[:, ['trackID', 't_since_start', 'Displacement^2']].copy()
    data_use_wide = data_use_long.pivot_table(values='Displacement^2',
                                              index='trackID',
                                              columns='t_since_start', )

    X = data_use_wide.columns.values.reshape(-1, 1)
    y = data_use_wide.iloc[0].values.reshape(-1, 1)

    model = LinearRegression(normalize=True)
    model.fit(X=X, y=y)
    beta = model.coef_[0][0]
    c = model.intercept_[0]
    r2 = r2_score(y, model.predict(X))

    data_use_wide['motility'] = beta
    data_use_wide['beta'] = beta
    data_use_wide['c'] = c
    data_use_wide['r2'] = r2
    data_use_wide.reset_index(drop=False, inplace=True)

    return(data_use_wide)