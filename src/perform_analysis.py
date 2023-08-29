import tensorflow as tf
import pandas as pd
import numpy as np
from pathlib import Path
from joblib import load

model_path = Path("./WorldBankFertilityModel.h5")
scaler_path = Path("./scaler.joblib")
onehotencoder_path = Path("./onehotencoder.joblib")

model = tf.keras.models.load_model(model_path)

def perform_analysis(country_code, series, years, value):
    return country_code, series, years, value