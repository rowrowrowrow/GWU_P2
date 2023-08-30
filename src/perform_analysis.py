import tensorflow as tf
import pandas as pd
import numpy as np
from pathlib import Path
from joblib import load
from src.get_country_data_grouped import get_country_data_grouped
from IPython.display import HTML

model_path = Path("./WorldBankFertilityModel.h5")
scaler_path = Path("./scaler.joblib")
onehotencoder_path = Path("./onehotencoder.joblib")

model = tf.keras.models.load_model(model_path)
scaler = load(scaler_path)
onehotencoder = load(onehotencoder_path)
series_code_total_fertility_rate = 'SP.DYN.TFRT.IN'

def perform_analysis(country_code, series, year, value):
    original_data = get_country_data_grouped()[country_code].loc[year]

    real_y = original_data.loc[series_code_total_fertility_rate]
    new_data = original_data.copy()
    new_data.loc[series] = float(value)
    
    columns = onehotencoder.get_feature_names_out(['country_code'])

    data = {}

    for column in columns:
        if column.endswith(country_code):
            data[column] = [1]
        else:
            data[column] = [0]
    
    df_country_code = pd.DataFrame(data=data, columns=columns)

    df_original = original_data.to_frame().T.reset_index(drop=True)
    df_new = new_data.to_frame().T.reset_index(drop=True)

    df_original_scaled_data = scaler.transform(df_original)
    df_new_scaled_data = scaler.transform(df_new)

    df_original_scaled = pd.DataFrame(data=df_original_scaled_data, columns=df_original.columns)
    df_new_scaled = pd.DataFrame(data=df_new_scaled_data, columns=df_new.columns)

    df_final_original = pd.concat([df_original_scaled.drop(columns=series_code_total_fertility_rate), df_country_code], axis=1)
    df_final_new = pd.concat([df_new_scaled.drop(columns=series_code_total_fertility_rate), df_country_code], axis=1)

    df_final_original = df_final_original.fillna(0).reset_index(drop=True)
    df_final_new = df_final_new.fillna(0).reset_index(drop=True)
    
    
    original_prediction = model.predict(df_final_original)
    new_prediction = model.predict(df_final_new)

    df_original_scaled[series_code_total_fertility_rate] = original_prediction[0][0]
    df_new_scaled[series_code_total_fertility_rate] = new_prediction[0][0]

    series_index_original = df_original_scaled.columns.get_loc(series_code_total_fertility_rate)
    series_index_new = df_new_scaled.columns.get_loc(series_code_total_fertility_rate)

    df_final_original_unscaled_prediction = scaler.inverse_transform(df_original_scaled)[0][series_index_original]
    df_final_new_unscaled_prediction = scaler.inverse_transform(df_new_scaled)[0][series_index_new]
    
    
    html = '<ul>'
    html += f"<li>The real fertility rate: <strong>{real_y}</strong></li>"
    html += f"<li>The model's predicted rate with real data: <strong>{df_final_original_unscaled_prediction}</strong></li>"
    html += f"<li>The model's predicted rate given a value of {value} for series code {series}: <strong>{df_final_new_unscaled_prediction}</strong></li>"
    html += "</ul>"
    html = HTML(html)
    return html