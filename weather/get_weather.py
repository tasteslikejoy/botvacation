import datetime

import requests
import pprint


api_weather = '9276dd599bc62a4e345acc27daa81cf3'

def get_weather(api_weather, city):
    try:
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_weather}&units=metric'
        )
        data = r.json()

        city = data['name']
        cur_weather = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])

        print(f'Город: {city}'
              f'Температура: {cur_weather}'
              f'Влажность: {humidity}'
              f'Давление: {pressure}'
              f'Скорость ветра: {wind}'
              f'Восход: {sunrise_timestamp}')


        pprint.pprint(data)

    except Exception as e:
        print(e)

def main():
    city = input('City:')
    get_weather(city, api_weather)

if __name__ == '__main__':
    main()