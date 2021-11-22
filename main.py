import datetime
import os
import sched
import time
import pandas
import requests
from bs4 import BeautifulSoup


def to_int(n, start, end):
    x = []
    for i in range(len(n)):
        x.append(n[i])
    return "".join(x[start:end])


def get_data():
    url = 'https://weather.com/ru-RU/weather/today/l/614b2d6e7bb8acb0f0506eeb7eec1d37515e02a3e33012e0d32ff7dc3f9ff3b3'
    r = requests.get(url)
    x = open('parse.html', 'w')
    x.write(r.text)
    x.close()
    soup = BeautifulSoup(r.text)  # Отправляем полученную страницу в библиотеку для парсинга

    now_datetime = datetime.datetime.now().strftime("%Y-%m-%d-%H.%M.%S")

    now_temp = soup.find_all('span', {'data-testid': 'TemperatureValue'})[0].text
    feels_like_temp = soup.find('span', {'class': 'TodayDetailsCard--feelsLikeTempValue--Cf9Sl'}).text
    highest_temp = soup.find_all('span', {'data-testid': 'TemperatureValue'})[1].text
    lowest_temp = soup.find_all('span', {'data-testid': 'TemperatureValue'})[2].text
    w_condition = soup.find('div', {'class': 'CurrentConditions--phraseValue--2Z18W'}).text
    humidity = soup.find('span', {'data-testid': 'PercentageValue'}).text
    visibility = to_int(soup.find('span', {'data-testid': 'VisibilityValue'}).text, 0, 4)
    pressure = to_int(soup.find('span', {'data-testid': 'PressureValue'}).text, 8, 14)
    wind_speed = to_int(soup.find('span', {'data-testid': 'Wind'}).text.split()[1], 9, 11)
    dew_point = soup.find_all('div', {'data-testid': 'wxData'})[3].text
    uv_index = soup.find('span', {'data-testid': 'UVIndexValue'}).text.split()[0]
    moon_phase = soup.find_all('div', {'data-testid': 'wxData'})[7].text
    sunrise_time = soup.find_all('p', {'class': 'SunriseSunset--dateValue--N2p5B'})[0].text
    sunset_time = soup.find_all('p', {'class': 'SunriseSunset--dateValue--N2p5B'})[1].text
    """print("now_temp", now_temp)
    print("feels_like_temp", feels_like_temp)
    print("highest_temp", highest_temp)
    print("lowest_temp", lowest_temp)
    print("w_condition", w_condition)
    print("humidity", humidity)
    print("visibility", visibility)
    print("pressure", pressure)
    print("wind_speed", wind_speed)
    print("dew_point", dew_point)
    print("uv_index", uv_index)
    print("moon_phase", moon_phase)
    print("sunset_time", sunset_time)
    print("sunrise_time", sunrise_time)"""
    if os.stat("date.json").st_size == 0:
        df = pandas.DataFrame([[now_temp, feels_like_temp, highest_temp, lowest_temp, w_condition, humidity, visibility, pressure, wind_speed, dew_point, uv_index, moon_phase, sunset_time, sunrise_time]],
                              columns=["now_temp", "feels_like_temp", "highest_temp", "lowest_temp", "w_condition", "humidity", "visibility", "pressure", "wind_speed", "dew_point", "uv_index", "moon_phase", "sunset_time", "sunrise_time"])
    else:
        df = pandas.read_json('date.json')
        df.loc[str(now_datetime)] = [now_temp, feels_like_temp, highest_temp, lowest_temp, w_condition, humidity, visibility, pressure, wind_speed, dew_point, uv_index, moon_phase, sunset_time, sunrise_time]
    df.to_json('date.json')
    df.to_csv('date.csv')


def do_something(sc):
    get_data()
    s.enter(15, 1, do_something, (sc,))


s = sched.scheduler(time.time, time.sleep)
s.enter(15, 1, do_something, (s,))
s.run()
