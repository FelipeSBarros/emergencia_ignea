import csv
from datetime import datetime
from glob import glob
import requests
import geopandas as gpd
import pandas as pd
from decouple import config

OWM_KEY = config('OWM_KEY')
incendios = glob('./datos/*.geojson')


# incendios = incendios[0]
incendios_df = gpd.read_file(incendios)
incendios_pred_df = incendios_df.copy()

def pred_incendio(weather_data):
    """
    Recorre las 24 horas de las condiciones ambientales para:
    - converter fecha,
    - converter hora,
    - acceder a direccion, velocidad, rafaga del viento y humedad
    convirte el df en gdf y transforma en buffer considerando velocidad de viento; # todo cambiar para velocidad + hora transcurrida
   retorna
    """
    weather_df = pd.DataFrame(
        columns=['fecha', 'hora', 'viento_dir', 'viento_vel', 'viento_rafaga', 'humedad'])
    for hora in weather_data.get("hourly")[0:24]:
        # hora = data.get("hourly")[0]
        # incendios_pred_df.loc[ind, ['temp']] = round(hora.get('temp') - 273.15, 2)
        weather_df = weather_df.append({
            'fecha': datetime.utcfromtimestamp(hora.get('dt')).strftime('%Y-%m-%d'),
            'hora': datetime.utcfromtimestamp(hora.get('dt')).strftime('%H:%M:%S'),
            'viento_dir': hora.get('deg'),
            'viento_vel': hora.get('wind_speed'),
            'viento_rafaga': hora.get('wind_gust'),
            'humedad': hora.get('humidity'),
            'lon': data['lon'],
            'lat': data['lat'],
        }, ignore_index=True)
    weather_gdf = gpd.GeoDataFrame(weather_df, geometry=gpd.points_from_xy(weather_df['lon'], weather_df['lat']))
    weather_gdf['geometry_buffer'] = weather_gdf.buffer(distance=weather_gdf['viento_vel'].astype(float), resolution=16)
    # single feature with multipart geometries
    df = {
        # 'id': [0],
    'geometry': [gpd.tools.collect(weather_gdf['geometry_buffer'])]}
    weather_pred = gpd.GeoDataFrame(df, crs="EPSG:4326")
    return weather_pred
    # return gpd.tools.collect(weather_gdf['geometry_buffer'])

incendios_pred_df['buffer_pred'] = None
for ind in incendios_pred_df.index:
    # ind = incendios_pred_df.index[0]
    lat = incendios_df['latitude'][ind]
    lon = incendios_df['longitude'][ind]
    url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&mode=metric&exclude=[current, minutely, daily, alerts]&lang=es&appid={OWM_KEY}'
    resp = requests.get(url=url)
    data = resp.json()

    incendios_pred_df.loc[[ind],['buffer_pred']] = gpd.GeoSeries([pred_incendio(data)['geometry']])







print(df.apply(lambda row: row["Name"] + " " + str(row["Percentage"]), axis = 1))
