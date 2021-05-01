import sys
import requests

BASE_URI = "https://www.metaweather.com"


def search_city(query):
    response=requests.get(BASE_URI + "/api/location/search/?query=" + query).json()

    if len(response) == 0:
        print("This City is not in the list. Try again!")
        return None

    if len(response) == 1:
        city=response[0]['title']
        print(f'Here\'s the weather in {city}')
        return response[0]

    print("Which of these options u want?")
    for index,element in enumerate(response):
        city = element['title']
        print(f'{index+1}: {city}')
    query = input("Number of the City?\n> ")
    query=int(query)-1
    city=response[query]['title']
    print(f'Here\'s the weather in {city}')
    return response[query]


def weather_forecast(woeid):
    response=requests.get(BASE_URI + "/api/location/" + str(woeid)).json()
    #print(response)
    weather5days=[]
    for i in range(5):
        dictweather={}
        dictweather['applicable_date']=response['consolidated_weather'][i]['applicable_date']
        dictweather['weather_state_name']=response['consolidated_weather'][i]['weather_state_name']
        dictweather['the_temp']=response['consolidated_weather'][i]['the_temp']
        weather5days.append(dictweather)
    return weather5days


def weather():

    query = input("City?\n> ")
    city = search_city(query)
    weather_next5days=weather_forecast(city['woeid'])

    for i in range(5):
        date=weather_next5days[i]['applicable_date']
        state=weather_next5days[i]['weather_state_name']
        temp=round(weather_next5days[i]['the_temp'])
        print(f'{date}: {state} {temp}°C')
