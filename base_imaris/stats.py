import pandas as pd
import numpy as np
from objects import GetSurpassObjects


def get_statistics_cell(vImaris , object_type , object_name):

    """

    :param vImaris: imaris instance
    :param object_type: imaris object type
    :param object_name: imaris object name
    :return: cell level statistics

    """

    objects = GetSurpassObjects(vImaris=vImaris, search=object_type)
    object_cells = objects[object_name]
    object_cell_stats = object_cells.GetStatistics()

    # Get individual cell IDs and track IDs to create set of edges which form a track

    cells = object_cells.GetIds()
    tracks = object_cells.GetTrackIds()
    edges_indices = object_cells.GetTrackEdges()
    edges = [[str(cells[start]),str(cells[stop])] for [start, stop] in edges_indices]

    track_cell_mapping = {}
    for trackID, (start, stop) in zip(tracks, edges_indices):

        start = cells[start]
        stop = cells[stop]

        track_cell_mapping[str(start)] = str(trackID)
        track_cell_mapping[str(stop)] = str(trackID)

    track_cell_mapping_df = pd.DataFrame.from_dict(track_cell_mapping, orient='index')
    track_cell_mapping_df.reset_index(inplace=True)
    track_cell_mapping_df.columns = ['objectID', 'trackID']

    stats_df = pd.DataFrame({'objectID': [str(objectID) for objectID in object_cell_stats.mIds],
                             'names': object_cell_stats.mNames,
                             'values': object_cell_stats.mValues})

    stats_track_df = pd.merge(left=track_cell_mapping_df,
                              right=stats_df,
                              how='inner')

    stats_pivot = stats_track_df.pivot_table(index=['trackID', 'objectID'],
                                             columns='names',
                                             values='values')
    stats_pivot_df = stats_pivot.reset_index()
    stats_pivot_df['time'] = stats_pivot_df.loc[:, 'Time Index'].values
    stats_pivot_df['track_time'] = stats_pivot_df.loc[:, 'Time Since Track Start'].values

    return(stats_pivot_df)



def get_statistics_track(vImaris , object_type , object_name):

    """

    :param vImaris: imaris instance
    :param object_type: imaris object type
    :param object_name: imaris object name
    :return: track level statistics
    """

    objects = GetSurpassObjects(vImaris=vImaris, search=object_type)
    object_cells = objects[object_name]
    object_cell_stats = object_cells.GetStatistics()

    data_list = [[objectID,name,unit,value] for objectID,name,unit,value in zip(object_cell_stats.mIds,
                                                                                object_cell_stats.mNames,
                                                                                object_cell_stats.mUnits,
                                                                                object_cell_stats.mValues) if (objectID>100000)]
    data_df_long = pd.DataFrame(data_list,columns=['trackID','colname','unit','values'])
    data_df_wide = data_df_long.pivot_table(index='trackID',columns='colname').loc[:,'values'].reset_index(col_level=1)

    return(data_df_wide)