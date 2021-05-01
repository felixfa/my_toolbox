from my_toolbox.weather import search_city, weather_forecast
import datetime

def test_search_city_for_paris():
    city = search_city('Paris')
    assert city['title'] == 'Paris'

def test_weather_forecast():
    forecast = weather_forecast(44418)
    assert type(forecast) == list
    assert forecast[0]['appicable_date'] == datetime.date.today().strftime('%Y-%m-%d')
