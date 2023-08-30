from src.get_series_list import get_series_list

def get_series_name(series_code):
    series_options = get_series_list()
    return [item[0] for item in series_options if item[1] == series_code][0]


