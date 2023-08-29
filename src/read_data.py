# Imports
import pandas as pd
from pathlib import Path

data = None

def read_data():
    global data
    
    if data is not None:
        return data
    else:
        data = pd.read_csv(
            Path("./Resources/03c00fd0-1cf9-46e8-aa22-40e2b0adbc27_Data.csv"), 
        )
        
        return data