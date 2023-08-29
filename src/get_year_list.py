from src.read_data import read_data

def get_year_list():
    """Retrieves a list of years from which to query.

    Returns:
        A list of years available from the data.
    """
    
    data_df = read_data()

    years = data_df.drop(columns=[
        'Country Name',
        'Country Code',
        'Series Name',
        'Series Code',
        ]).columns
    
    return years


