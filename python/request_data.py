from decouple import config
import requests
import geopandas as gpd


NASA_KEY = config('NASA_KEY')

urls = ['https://firms.modaps.eosdis.nasa.gov/data/active_fire/modis-c6.1/csv/MODIS_C6_1_South_America_24h.csv',
        'https://firms.modaps.eosdis.nasa.gov/data/active_fire/suomi-npp-viirs-c2/csv/SUOMI_VIIRS_C2_South_America_24h.csv',
        'https://firms.modaps.eosdis.nasa.gov/data/active_fire/noaa-20-viirs-c2/csv/J1_VIIRS_C2_South_America_24h.csv']


def get_data(url):
    url_content = requests.get(url)
    # file_name = url.split('/')[-1].split('.')[0]
    file_name = url.split('/')[5]
    data = url_content.content
    csv_file = open(f'./datos/incendios-{file_name}.csv', 'wb')
    csv_file.write(data)
    csv_file.close()  # todo puede retornar el content y ya ir para geodataframe
    return {
        'data': data,
        file_name: file_name
    }


def filter_misiones(to_filter):
    from geopandas import read_file, sjoin
    MISIONES = read_file("./datos/misiones.geojson")
    # incendios_misiones_df = incendios_df.intersects(misiones)
    data_misiones = to_filter.sjoin(MISIONES)
    return data_misiones


def clean_data(content_dict):
    # content_dict = "./incendios-modis-c6.1.csv"
    from pandas import DataFrame, read_csv
    from geopandas import GeoDataFrame
    incendios_df = read_csv(content_dict)
    # incendios_df = DataFrame(content_dict.get('data'))
    incendios_df = GeoDataFrame(data=incendios_df, geometry=gpd.points_from_xy(
        incendios_df.longitude,
        incendios_df.latitude),
                                crs=4326)
    incendios_cleaned = filter_misiones(incendios_df)
    file_name = ''.join(content_dict.split('-')[1:]).split('.')[0]
    incendios_cleaned.to_file(f"./datos/incendios_misiones{file_name}.geojson")


def main():
    from glob import glob
    list(map(get_data, urls))
    results = glob('./datos/*.csv')
    list(map(clean_data, results))


if __name__ == '__main__':
    main()
