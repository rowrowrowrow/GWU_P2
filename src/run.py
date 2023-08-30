from src.get_country_list import get_country_list
from src.get_series_list import get_series_list
from src.get_year_list import get_year_list
from src.perform_analysis import perform_analysis
from src.get_country_data import get_country_data
from ipywidgets import interact_manual, FloatText, Select

country_code_value = None
series_value = None
years_value = None
    
def run():
    global country_code_value
    global series_value
    global years_value
    """The main function for running the script."""

    category_options = get_country_list()
    
    series_options = get_series_list()
    
    years_options = get_year_list()
    
    country_code = Select(
        value=category_options[0][1],
        options=category_options,
        description='Categories:',
    )
    
    country_code_value = country_code.value
    
    series = Select(
        value=series_options[0][1],
        options=series_options,
        description='Series:',
    )
    
    series_value = series.value
    
    year = Select(
        value=years_options[-1],
        options=years_options,
        description='Year:',
    )
    
    years_value = year.value
    
    initial_value = get_country_data(country_code.value, series.value, year.value)
    
    value = FloatText(
        value=initial_value,
        description=f"{series.value} Value:",
    )
    
    # See the following for an explanation:
    #     https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20Events.html
    def update_value():
        global country_code_value
        global series_value
        global years_value
        
        value.description = f"{series_value} Value:"
        new_value = get_country_data(country_code_value, series_value, years_value)
        value.value = new_value
    
    def update_category(change):
        global country_code_value
        country_code_value = change.new
        update_value()
    
    def update_series(change):
        global series_value
        series_value = change.new
        update_value()
        
    def update_year(change):
        global years_value
        years_value = change.new
        update_value()
        
    country_code.observe(update_category, names='value')
    series.observe(update_series, names='value')
    year.observe(update_year, names='value')

    out = interact_manual(perform_analysis, country_code=country_code, series=series, year=year, value=value)
    
    return out
   
    