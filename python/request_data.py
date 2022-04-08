from os import path, remove
import io
import logging
import sys

import geopandas as gpd
import pandas as pd
import requests
from geopandas import GeoDataFrame
from geopandas import read_file  # todo confirmar se precisa importar

urls = [
    "https://firms.modaps.eosdis.nasa.gov/data/active_fire/modis-c6.1/csv/MODIS_C6_1_South_America_24h.csv",
    "https://firms.modaps.eosdis.nasa.gov/data/active_fire/suomi-npp-viirs-c2/csv/SUOMI_VIIRS_C2_South_America_24h.csv",
    "https://firms.modaps.eosdis.nasa.gov/data/active_fire/noaa-20-viirs-c2/csv/J1_VIIRS_C2_South_America_24h.csv",
]


def get_data(url):
    """
    Request data from fire database, select few columns and return as DataFrame
    :param url:
    :return: pd.DataFrame
    """
    logger = logging.getLogger("get_data")
    logger.info("Retrieving data")
    url_content = requests.get(url)
    file_name = url.split("/")[5]
    url_data = url_content.content
    raw_data = pd.read_csv(io.StringIO(url_data.decode("utf-8")))
    raw_data[
        ["latitude", "longitude", "acq_date", "acq_time", "satellite", "confidence"]
    ]
    raw_data["source"] = file_name
    return raw_data


def filter_misiones(to_filter):
    logger = logging.getLogger("filter_misiones")
    logger.info("Filtering fires")
    misiones = read_file("./datos/misiones.geojson")
    data_misiones = to_filter.sjoin(misiones)
    data_misiones.reset_index(inplace=True, drop=True)
    data_misiones["index"] = data_misiones.index
    return data_misiones


def clean_data(incendios_df):
    logger = logging.getLogger("clean_data")
    logger.info("Data cleaning")
    incendios_df = GeoDataFrame(
        data=incendios_df,
        geometry=gpd.points_from_xy(incendios_df.longitude, incendios_df.latitude),
        crs=4326,
    )
    incendios_cleaned = filter_misiones(incendios_df)
    if incendios_cleaned.empty:
        logger.info("Misiones sin incendios activos")
        sys.exit()

    else:
        return incendios_cleaned


def get_misiones_data():
    logger = logging.getLogger("get_misiones_data")
    result = "./datos/incendios_misiones.geojson"
    df = pd.concat([get_data(i) for i in urls])
    df_cleaned = clean_data(df)
    if not df_cleaned.empty:
        if path.exists(result):
            remove(result)
        logger.info("Saving file")
        df_cleaned.to_file(result)


if __name__ == "__main__":
    logging.basicConfig(
        filename="request_data.log",
        level=logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )
    get_misiones_data()
