import csv
from datetime import datetime

import requests
import geopandas as gpd
import pandas as pd

incendios =
# API sin ID!
# url = 'https://api.openweathermap.org/data/2.5/onecall?lat=-27.36649&lon=-55.89411&mode=metric&exclude={current,minutely,daily,alerts}&lang=es&appid='
url = 'https://api.openweathermap.org/data/2.5/onecall?lat=-26.22701&lon=-54.01472&mode=metric&exclude={current,minutely,daily,alerts}&lang=es&appid='

resp = requests.get(url=url)  # , params=params)
data = resp.json()  # Check the JSON Response Content documentation below

# data.keys()

# data.get("hourly")
# len(data.get("hourly"))
for hora in data.get("hourly"):
    to_convert_dt = hora.get('dt')
    converted_dt = datetime.utcfromtimestamp(hora.get('dt')).strftime('%Y-%m-%d %H:%M:%S')
    to_convert_temp = hora.get('temp')
    converted_temp = round(to_convert_temp - 273.15, 2)
    hora.update(dt=converted_dt, temp=converted_temp)

keys = data.get("hourly")[0].keys()

with open('weather.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(data.get("hourly"))
