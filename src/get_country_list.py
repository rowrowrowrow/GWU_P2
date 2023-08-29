from src.read_data import read_data

def get_country_list():
    """Retrieves a list of categories from which to query.

    Returns:
        A list of tuples in the format ('Category', 'Code'), where 'Code' is the unique country or categorical code used by world bank for identifying the category.
    """
    
    data_df = read_data()

    names = data_df[['Country Name','Country Code']].drop_duplicates()

    names = names[names['Country Code'].notna()]

    options = list(names.itertuples(index=False, name=None))
    
    options.sort()
    
    return options


