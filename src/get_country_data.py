from src.get_country_data_grouped import get_country_data_grouped

def get_country_data(country_code, series, year):
    grouped = get_country_data_grouped()
    return grouped[country_code, series].loc[year]


