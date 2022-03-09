import io
from datetime import datetime

import geopandas as gpd
import pandas as pd
# from decouple import config
import requests
from geopandas import GeoDataFrame
from geopandas import read_file  # todo confirmar se precisa importar

# NASA_KEY = config('NASA_KEY', default='')

urls = ['https://firms.modaps.eosdis.nasa.gov/data/active_fire/modis-c6.1/csv/MODIS_C6_1_South_America_24h.csv',
        'https://firms.modaps.eosdis.nasa.gov/data/active_fire/suomi-npp-viirs-c2/csv/SUOMI_VIIRS_C2_South_America_24h.csv',
        'https://firms.modaps.eosdis.nasa.gov/data/active_fire/noaa-20-viirs-c2/csv/J1_VIIRS_C2_South_America_24h.csv']


def get_data(url):
    """
    Request data from fire database, select few columns and return as DataFrame
    :param url:
    :return: pd.DataFrame
    """
    url_content = requests.get(url)
    file_name = url.split('/')[5]
    url_data = url_content.content
    raw_data = pd.read_csv(io.StringIO(url_data.decode('utf-8')))
    raw_data[['latitude', 'longitude', 'acq_date', 'acq_time', 'satellite', 'confidence']]
    raw_data['source'] = file_name
    return raw_data


def filter_misiones(to_filter):
    misiones = read_file("./datos/misiones.geojson")
    data_misiones = to_filter.sjoin(misiones)
    return data_misiones


def clean_data(incendios_df):
    incendios_df = GeoDataFrame(data=incendios_df,
                                geometry=gpd.points_from_xy(
                                    incendios_df.longitude,
                                    incendios_df.latitude),
                                crs=4326)
    incendios_cleaned = filter_misiones(incendios_df)
    incendios_cleaned = incendios_cleaned.reset_index()
    return incendios_cleaned


def get_misiones_data():
    df = pd.concat([get_data(i) for i in urls])
    df_cleaned = clean_data(df)
    if not df_cleaned.empty:
        df_cleaned.to_file(f'./datos/incendios_misiones_{datetime.today().date()}.geojson')


if __name__ == '__main__':
    get_misiones_data()
