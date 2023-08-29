from src.read_data import read_data

def get_series_list():
    """Retrieves a list of the series from which to query.

    Returns:
        A list of tuples in the format ('Series Name', 'Series Code'), where 'Series Code' is the unique country or categorical Series Code used by world bank for identifying the Series Name.
    """
    
    data_df = read_data()

    names = data_df[['Series Name','Series Code']].drop_duplicates()

    names = names[names['Series Code'].notna()]

    series = list(names.itertuples(index=False, name=None))
    
    series.sort()
    
    return series


