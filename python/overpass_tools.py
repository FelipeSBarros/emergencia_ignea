import overpy

overpass_api = overpy.Overpass()

def has_indigenous_population(overpass_api, buffer_distance, Longitud, Latitud):
    # Latitud = -27.094
    # Longitud = -54.9722
    # buffer_distance = 10000

    RiskFactor = 0
    query = f"node(around:{buffer_distance},{Latitud},{Longitud})[place=hamlet][name~'Comunidad Aborigen']; out meta;"
    indigenous_population = overpass_api.query(query)

    if (
        indigenous_population.nodes
        or indigenous_population.ways
    ):
        RiskFactor = 10

    return RiskFactor

def has_gas_station(overpass_api, buffer_distance, Longitud, Latitud):
    # buffer_distance = 500
    # Latitud = -26.9912
    # Longitud = -54.4885
    RiskFactor = 0

    query = f"node(around:{buffer_distance},{Latitud},{Longitud})[amenity=fuel];out meta;"
    gas_stations = overpass_api.query(query)

    if (
            gas_stations.nodes
            or gas_stations.ways
    ):
        RiskFactor = 9

    return RiskFactor

def has_inflamable_gas(overpass_api, buffer_distance, Longitud, Latitud):
    # Latitud = -27.44457;
    # Longitud = -55.87458;
    RiskFactor = 0

    query = f"node(around:{buffer_distance},{Latitud},{Longitud})[shop=gas];out meta;"
    gas = overpass_api.query(query)

    if (
            gas.nodes
            or gas.ways
    ):
        RiskFactor = 9

    return RiskFactor


def gas_supply(overpass_api, buffer_distance, Longitud, Latitud):
    # Latitud = -27.44457
    # Longitud = -55.87458
    RiskFactor = 0

    query = f'way(around:{buffer_distance},{Latitud},{Longitud})[man_made=storage_tank][substation=gas];out meta;'
    gas_suppply = overpass_api.query(query)
    if (
            gas_suppply.nodes or
            gas_suppply.ways
    ):
        RiskFactor = 9
    return RiskFactor


def gas_supply(overpass_api, buffer_distance, Longitud, Latitud):
    # Latitud = -27.42830
    # Longitud = -55.89126

    query = f'node(around:{buffer_distance},{Latitud},{Longitud})[amenity=school];out meta;'
    schools = overpass_api.query(query)

    if (
            schools.nodes or schools.ways
    ):
        RiskFactor = 8
    return RiskFactor


def timber_supply(overpass_api, buffer_distance, Longitud, Latitud):
    # Latitud = -27.47436
    # Longitud = -55.15989
    RiskFactor = 0
    query = f'node(around:{buffer_distance},{Latitud},{Longitud})[craft=sawmill];out meta;'
    timber = overpass_api.query(query)
    if( timber.nodes or timber.ways ):

        RiskFactor = 7;
    return RiskFactor

def power_line(overpass_api, buffer_distance, Longitud, Latitud):
    # Latitud = -27.47611;
    # Longitud = -55.15734;

    query = f'way(around:{buffer_distance},{Latitud},{Longitud})[power=line];out meta;'
    power_line = overpass_api.query(query)
    if (
        power_line.nodes or
        power_line.ways
    ):
        RiskFactor = 5;
    return RiskFactor

def urban_areas(overpass_api, buffer_distance, Longitud, Latitud):
    # Latitud = -26.69454
    # Longitud = -54.20307
    query = f'relation(around:{buffer_distance},{Latitud},{Longitud})[landuse=residential];out meta;'
    urban_areas = overpass_api.query(query)
    if (urban_areas.relations or urban_areas.nodes or urban_areas.ways):
        RiskFactor = 5;
    return RiskFactor
