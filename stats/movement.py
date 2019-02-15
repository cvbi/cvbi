import numpy as np
import pandas as pd
from cvbi.stats.track import get_motility

def get_metrics_cell(data_cell):
    """

    :param data_cell: A pandas dataframe containing Imaris statistics for a single cell

    :return: Dataframe containing original columns along with additional calculations


    """

    # Get data for a single track
    # Data Munging

    df = data_cell.copy()
    N = df.shape[0]
    Ts = np.arange(start = 1, stop = N + 1, step = 1)
    df.sort_values('time', inplace = True)
    df.reset_index(drop = True, inplace = True)

    df['n_track'] = N
    df['t_track'] = Ts
    df['track_time'] = df.loc[:, 'Time Since Track Start'].values

    # Cluster membership

    X_track = df.loc[:, ['Position X', 'Position Y', 'Position Z']].values
    labels_track = df.cluster_label.values
    df['cluster_id'] = labels_track
    df['cluster_in'] = (df.cluster_id != -1).astype(np.int16).values
    df['cluster_dwell'] = df.cluster_in.cumsum().values
    df['cluster_dwell_time'] = (df.cluster_dwell * 1.0 / df.t_track) * 100

    # Track length, Displacement, mean squared displacement & Meandering index
    try:
        df['track_length'] = df.loc[:, ['Displacement Delta Length']].values.cumsum()
    except:
        df['Displacement Delta Length'] = (df.loc[:, ['Position X', 'Position Y', 'Position Z']].diff() ** 2).sum(1).values
        df['track_length'] = df.loc[:, ['Displacement Delta Length']].values.cumsum()

    df['track_displacement'] = df.loc[:, ['Displacement^2']].pow(0.5).values
    df['velocity'] = (df.track_displacement.values * 1.0 / df.track_time.values)
    df['msd'] = df.loc[:, ['Displacement^2']].values
    df['meandering_index'] = df.track_displacement.divide(df.track_length.values + 1e-15).values

    # Get Arrest Coefficient

    df['arrest_speed_cutoff'] = df.Speed.lt(2.0 / 60).values.astype(np.int)
    df['arrest_cumulative'] = df.arrest_speed_cutoff.cumsum().values
    df['arrest_coefficient'] = df.arrest_cumulative.values * 1.0 / df.t_track.values

    return(df)


def get_metrics_track(df, unit='s'):
    """

    :param df: Dataframe containing cell level metrics, output from `get_metrics_cell`

    :return: Track level aggregates

    """
    if unit=='s':
        m = 60.0
    else:
        m = 1.0

    row = pd.Series(

            data = [df.shape[0],
                    df.track_time.iloc[-1],
                    df.track_length.iloc[-1],
                    df.track_displacement.iloc[-1],
                    df.velocity.iloc[-1] * m,
                    df.track_length.iloc[-1] * m / df.track_time.iloc[-1],
                    df.Speed.iloc[:].mean() * m,
                    df.Speed.iloc[:].std() * m,
                    df.meandering_index.iloc[-1],
                    df.arrest_coefficient.iloc[-1],
                    get_motility(df).loc[:, 'motility'].values[0],
                    df.cluster_in.sum(),
                    df.cluster_in.sum() * 100.0 / df.shape[0],
                    (df.cluster_in.sum() == df.shape[0]).sum(),
                    (df.cluster_in.sum() == 0).sum(),
                    df.cluster_in.iloc[0],
                    df.cluster_in.iloc[-1]
                    ],

            index = ['track_nT',
                     'track_T_delta',
                     'track_distance',
                     'track_displacement',
                     'track_velocity',
                     'track_speed',
                     'track_speed_mu',
                     'track_speed_std',
                     'track_meandering_index',
                     'track_arrest_coeff',
                     'track_motility',
                     'track_dwell_time',
                     'track_dwell_percent',
                     'track_always_in',
                     'track_always_out',
                     'start',
                     'end'
                     ])

    return(row)


def get_metrics_dataset(df, cell_moving = None, t_limit = 60):
    """

    :param df: Track level aggregate dataset
    :param cell_moving: Cell type
    :param t_limit: Total time that calculations were run on

    :return: Data frame collapsed to a dataset, cell type level.

    """
    data_dict = {}

    data_dict['cell_type'] = cell_moving
    data_dict['t_limit'] = t_limit
    data_dict['n_total'] = df.shape[0]

    data_dict['n_start_in'] = (df.start.values == 1).sum()
    data_dict['n_end_in'] = (df.end.values == 1).sum()

    data_dict['n_start_out'] = (df.start.values == 0).sum()
    data_dict['n_end_out'] = (df.end.values == 0).sum()

    data_dict['n_always_in'] = df.track_always_in.values.sum()
    data_dict['n_always_out'] = df.track_always_out.values.sum()

    data_dict['n_out_to_change_state'] = data_dict['n_start_out'] - data_dict['n_always_out']
    data_dict['n_in_to_change_state'] = data_dict['n_start_in'] - data_dict['n_always_in']

    data_dict['n_in_to_in'] = ((df.start.values == 1) & (df.end.values == 1)).sum() - data_dict['n_always_in']
    data_dict['n_in_to_out'] = ((df.start.values == 1) & (df.end.values == 0)).sum()

    data_dict['n_out_to_out'] = ((df.start.values == 0) & (df.end.values == 0)).sum() - data_dict['n_always_out']
    data_dict['n_out_to_in'] = ((df.start.values == 0) & (df.end.values == 1)).sum()

    data_dict['per_out_to_in'] = (data_dict['n_out_to_in'] * 100.0 / data_dict['n_out_to_change_state']).round(2)
    data_dict['per_out_to_out'] = (data_dict['n_out_to_out'] * 100.0 / data_dict['n_out_to_change_state']).round(2)

    data_dict['per_in_to_out'] = (data_dict['n_in_to_out'] * 100.0 / data_dict['n_in_to_change_state']).round(2)
    data_dict['per_in_to_in'] = (data_dict['n_in_to_in'] * 100.0 / data_dict['n_in_to_change_state']).round(2)

    data_dict['per_out_to_in_all'] = (data_dict['n_out_to_in'] * 100.0 / data_dict['n_start_out']).round(2)
    data_dict['per_out_to_out_all'] = (data_dict['n_out_to_out'] * 100.0 / data_dict['n_start_out']).round(2)

    data_dict['per_in_to_out_all'] = (data_dict['n_in_to_out'] * 100.0 / data_dict['n_start_in']).round(2)
    data_dict['per_in_to_in_all'] = (data_dict['n_in_to_in'] * 100.0 / data_dict['n_start_in']).round(2)

    data_out = pd.Series(data_dict)

    return (data_out)


