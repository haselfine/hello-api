import requests
import os
from pprint import pprint
from datetime import datetime
import logging

key = os.environ.get('WEATHER_KEY')
url = f'http://openweathermap.org/data/2.5/forecast'
error_message = 'An error occurred. Please make sure you enter a valid US city.'
logging.basicConfig(level=logging.DEBUG)


class API_Error(Exception):
    pass

def main():
    if key is None:
        print('Error. Need valid API key.')
    else:
        get_location()
        
def get_location():
    while True:
        user_city = input('What city would you like the forecast for? (Or type q to quit) ')
        if user_city.upper() == 'Q':
            break
        user_city_country = f'{user_city.lower()},us'
        
        call_api(user_city_country)

def call_api(user_city_country):
    try:
        query = {'q': user_city_country, 'units':'imperial', 'appid': key}
        
        response = requests.get(url, params=query).json()
        if response['cod'] == '200':
            configure_data(response)
        elif response['cod'] == '401':
            raise API_Error(response['message'])
        elif response['cod'] == '404':
            raise API_Error(error_message)
        elif response['cod'] == '500':
            raise API_Error('A server error occurred. Feel free to quit the program. ')
    except API_Error:
        print(response['message'])
        pass
    except TypeError as te:
        print('Make sure you enter only the city. No nonalphabetic characters please.')
        print(te)
    except Exception as e:
        print(error_message)
        logging.debug(e)
    
        

def configure_data(data):
    list_of_forecasts = data['list']
    user_friendly_forecasts = []
    for forecast in list_of_forecasts:
        temp = forecast['main']['temp']
        description = forecast['weather']['description']
        windspeed = forecast['wind']['speed']
        timestamp = forecast['dt']
        date_format = datetime.fromtimestamp(timestamp) #I'm choosing to do local time because that's when the weather should happen at that location.
        date = datetime.date(date_format)
        hour = date_format.hour
        am = True
        if hour > 12:
            hour = hour-12
            am = False
        if am:
            am_pm = 'am'
        else:
            am_pm = 'pm'
        user_friendly_forecasts.append(f'On {date} at {hour}:00{am_pm}, the temperature will be {temp}°F. The weather will be {description} and the wind will be {windspeed} mph.')
    print_data(user_friendly_forecasts)

def print_data(user_friendly_forecasts):
    for forecast in user_friendly_forecasts:
        print(forecast)

if __name__ == '__main__':
    main()
