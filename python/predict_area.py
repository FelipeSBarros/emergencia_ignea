import logging
from datetime import datetime
from glob import glob

import geopandas as gpd
import pandas as pd
import requests
from decouple import config

OWM_KEY = config('OWM_KEY')


def pred_new_coords(lat, lon, d, wind_deg):
    """

    """
    import math
    R = 6378.1  # Radius of the Earth
    # d = 15  # Distance in km  # todo confirmar isso
    lat1 = math.radians(lat)  # Current lat point converted to radians
    lon1 = math.radians(lon)  # Current long point converted to radians
    lat2 = math.asin(math.sin(lat1) * math.cos(d / R) +
                     math.cos(lat1) * math.sin(d / R) * math.cos(wind_deg))

    lon2 = lon1 + math.atan2(math.sin(wind_deg) * math.sin(d / R) * math.cos(lat1),
                             math.cos(d / R) - math.sin(lat1) * math.sin(lat2))

    return {'lat': math.degrees(lat2), 'lon': math.degrees(lon2)}


def pred_incendio(weather_data):
    """
    Recorre las 24 horas de las condiciones ambientales para:
    - converter fecha,
    - converter hora,
    - acceder a direccion, velocidad, rafaga del viento y humedad
    convirte el df en gdf y transforma en buffer considerando velocidad de viento;
   retorna
    """

    weather_df = pd.DataFrame(
        columns=['fecha', 'hora', 'viento_dir', 'viento_vel', 'viento_rafaga', 'humedad'])
    # weather_data = data
    for index, hora in enumerate(weather_data.get("hourly")[0:24]):  # 24 horas de previsao
        # hora = data.get("hourly")[0]
        # index = 0
        # incendios_pred_df.loc[ind, ['temp']] = round(hora.get('temp') - 273.15, 2)
        if index > 0:
            weather_data.update(
                pred_new_coords(
                    lon=weather_data.get('lon'),
                    lat=weather_data.get('lat'),
                    d=3.600,
                    wind_deg=hora.get('wind_deg')
                ))

        weather_df = pd.concat(
            [
                weather_df,
                pd.DataFrame([
                    {
                        'fecha': datetime.utcfromtimestamp(hora.get('dt')).strftime('%Y-%m-%d'),
                        'hora': datetime.utcfromtimestamp(hora.get('dt')).strftime('%H:%M:%S'),
                        'viento_dir': hora.get('wind_deg'),
                        'viento_vel': hora.get('wind_speed') * 3600,
                        'viento_rafaga': hora.get('wind_gust') * 3600,
                        'humedad': hora.get('humidity'),
                        'lon': weather_data['lon'],
                        'lat': weather_data['lat'],
                    }
                ])
            ]
        )

    weather_gdf = gpd.GeoDataFrame(weather_df,
                                   geometry=gpd.points_from_xy(
                                       weather_df['lon'],
                                       weather_df['lat'],
                                       crs="EPSG:4326"))
    weather_gdf['geometry_buffer'] = weather_gdf.to_crs("EPSG:5349").buffer(
        distance=weather_gdf['viento_vel'].astype(float),
        resolution=16).to_crs("EPSG:4326")
    return gpd.tools.collect(weather_gdf['geometry_buffer'])


def predict_area():
    try:
        incendios = glob(f'./datos/incendios_misiones.geojson')[0]
        incendios_df = gpd.read_file(incendios)
    except IndexError:
        logging.warning("incendios_misiones.geojson no existente. Probablemente no haya incendios en Misiones")
    else:
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
        incendios_pred_df = incendios_pred_df.drop('geometry', 1)
        incendios_pred_df = incendios_pred_df.dissolve('index')
        incendios_pred_df.to_file(f'./datos/prediccion_incendios.geojson')


if __name__ == '__main__':
    predict_area()
