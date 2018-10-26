import numpy as np
import pandas as pd

def get_imaris_statistics(object_type, name):

    ## Get object connection for cell collection in Imaris

    object_cells = object_type[name]
    object_cell_stats = object_cells.GetStatistics()

    ## Get individual cell IDs and track IDs to create set of edges which form a track

    cells = object_cells.GetIds()
    tracks = object_cells.GetTrackIds()
    edges_indices = object_cells.GetTrackEdges()
    edges = [ [str(cells[start]),str(cells[stop])] for [start,stop] in edges_indices]

    track_cell_mapping = {}
    for trackID,(start,stop) in zip(tracks,edges_indices):

        start = cells[start]
        stop  = cells[stop]

        track_cell_mapping[str(start)] = str(trackID)
        track_cell_mapping[str(stop)]  = str(trackID)

    track_cell_mapping_df = pd.DataFrame.from_dict(track_cell_mapping,orient='index')
    track_cell_mapping_df.reset_index(inplace=True)
    track_cell_mapping_df.columns = ['objectID','trackID']

    stats_df = pd.DataFrame({'objectID':[str(objid) for objid in object_cell_stats.mIds],
                             'names':object_cell_stats.mNames,
                             'values':object_cell_stats.mValues})

    stats_track_df = pd.merge(left=track_cell_mapping_df,
                              right=stats_df,
                              how='inner')

    stats_pivot = stats_track_df.pivot_table(index=['trackID','objectID'],
                                             columns='names',
                                             values='values')
    stats_pivot_df = stats_pivot.reset_index()
    stats_pivot_df['time'] = stats_pivot_df.loc[:,'Time Index']

    return(stats_pivot_df)
