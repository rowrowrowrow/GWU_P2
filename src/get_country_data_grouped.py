# Imports
import pandas as pd
from pathlib import Path
import numpy as np
from src.read_data import read_data

grouped = None

def get_country_data_grouped():
    global grouped
    
    if grouped is not None:
        return grouped
    else:
        data_df = read_data()

        data_df = data_df.drop(columns=['Country Name','Series Name']).copy()

        data_df = data_df.groupby([
            'Country Code',
            'Series Code'
            ])

        # We want to return all the data for the aggregation so just return the data during aggregation
        data_df = data_df.agg(lambda x: x)

        # Replace the default missing data value with NaN
        data_df = data_df.replace('..', np.nan)

        grouped = data_df.T
        
        return grouped