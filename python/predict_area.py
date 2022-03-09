from datetime import datetime
from glob import glob

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import requests
from decouple import config

OWM_KEY = config('OWM_KEY')
incendios = glob('./datos/*.geojson')


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
    # weather_data = data
    for index, hora in enumerate(weather_data.get("hourly")[0:24]):  # 24 horas de previsao
        # hora = data.get("hourly")[0]
        # incendios_pred_df.loc[ind, ['temp']] = round(hora.get('temp') - 273.15, 2)
        weather_df = weather_df.append({  # TODO uodate removing warning
            'fecha': datetime.utcfromtimestamp(hora.get('dt')).strftime('%Y-%m-%d'),
            'hora': datetime.utcfromtimestamp(hora.get('dt')).strftime('%H:%M:%S'),
            'viento_dir': hora.get('deg'),
            'viento_vel': hora.get('wind_speed') * 3600,  # todo considerar desplazamiento a cada hora/itercao
            'viento_rafaga': hora.get('wind_gust') * 3600,  # todo idem
            'humedad': hora.get('humidity'),
            'lon': data['lon'],
            'lat': data['lat'],
        }, ignore_index=True)
    weather_gdf = gpd.GeoDataFrame(weather_df,
                                   geometry=gpd.points_from_xy(weather_df['lon'], weather_df['lat'], crs="EPSG:4326"))
    weather_gdf['geometry_buffer'] = weather_gdf.to_crs("EPSG:5349").buffer(
        distance=weather_gdf['viento_vel'].astype(float), resolution=16).to_crs("EPSG:4326")
    # single feature with multipart geometries
    return gpd.tools.collect(weather_gdf['geometry_buffer'])


for incendio in incendios:
    # incendio = incendios[0]
    incendios_df = gpd.read_file(incendio)  # todo pensar em fazer append dos dfs
    incendios_pred_df = incendios_df.copy()
    incendios_pred_df['buffer_pred'] = None
    for ind in incendios_pred_df.index:
        # ind = incendios_pred_df.index[0]
        lat = incendios_df['latitude'][ind]
        lon = incendios_df['longitude'][ind]
        url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&mode=metric&exclude=[current, minutely, daily, alerts]&lang=es&appid={OWM_KEY}'
        resp = requests.get(url=url)
        data = resp.json()
        incendios_pred_df['buffer_pred'][ind] = pred_incendio(data)

incendios_pred_df = incendios_pred_df.set_geometry('buffer_pred')
for geometry in incendios_pred_df.geometry:
    print(geometry)
# incendios_pred_df.to_file('./datos/incendios_pred.shp')  # todo solve this problem
fig, ax = plt.subplots()
incendios_pred_df.plot(ax=ax, facecolor=None, edgecolor="black")
incendios_pred_df['geometry'].plot(ax=ax, markersize=.5, color='black')
plt.show();

fig, ax = plt.subplots()
incendios_pred_df.loc[[ind]].plot(ax=ax, edgecolor="black")
incendios_pred_df.loc[[ind], 'geometry'].plot(ax=ax, color='black')
plt.show();
