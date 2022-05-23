import time
import time
import overpy
from overpy.exception import OverpassTooManyRequests

overpass_api = overpy.Overpass()


def has_indigenous_population(row, overpass_api, buffer_distance):
    # row.geometry.y = -27.094
    # row.geometry.x = -54.9722
    # buffer_distance = 10000

    RiskFactor = 0
    query = f"node(around:{buffer_distance},{row.geometry.y},{row.geometry.x})[place=hamlet][name~'Comunidad Aborigen']; out meta;"
    try:
        indigenous_population = overpass_api.query(query)
        time.sleep(30)
    except OverpassTooManyRequests:
        time.sleep(30)
        indigenous_population = overpass_api.query(query)

    if indigenous_population.nodes or indigenous_population.ways:
        RiskFactor = 10

    return RiskFactor


def has_gas_station(row, overpass_api, buffer_distance):
    # buffer_distance = 500
    # row.geometry.y = -26.9912
    # row.geometry.x = -54.4885
    RiskFactor = 0

    query = f"node(around:{buffer_distance},{row.geometry.y},{row.geometry.x})[amenity=fuel];out meta;"
    try:
        gas_stations = overpass_api.query(query)
        time.sleep(30)
    except OverpassTooManyRequests:
        time.sleep(30)
        gas_stations = overpass_api.query(query)

    if gas_stations.nodes or gas_stations.ways:
        RiskFactor = 9

    return RiskFactor


def has_inflamable_gas(row, overpass_api, buffer_distance):
    # row.geometry.y = -27.44457;
    # row.geometry.x = -55.87458;
    RiskFactor = 0

    query = f"node(around:{buffer_distance},{row.geometry.y},{row.geometry.x})[shop=gas];out meta;"
    try:
        gas = overpass_api.query(query)
        time.sleep(30)
    except OverpassTooManyRequests:
        time.sleep(30)
        gas = overpass_api.query(query)

    if gas.nodes or gas.ways:
        RiskFactor = 9

    return RiskFactor


def gas_supply(row, overpass_api, buffer_distance):
    # row.geometry.y = -27.44457
    # row.geometry.x = -55.87458
    RiskFactor = 0

    query = f"way(around:{buffer_distance},{row.geometry.y},{row.geometry.x})[man_made=storage_tank][substation=gas];out meta;"
    try:
        gas_suppply = overpass_api.query(query)
        time.sleep(30)
    except OverpassTooManyRequests:
        time.sleep(30)
        gas_suppply = overpass_api.query(query)

    if gas_suppply.nodes or gas_suppply.ways:
        RiskFactor = 9
    return RiskFactor


def has_schools(row, overpass_api, buffer_distance):
    # row.geometry.y = -27.42830
    # row.geometry.x = -55.89126
    RiskFactor = 0
    query = f"node(around:{buffer_distance},{row.geometry.y},{row.geometry.x})[amenity=school];out meta;"
    try:
        schools = overpass_api.query(query)
        time.sleep(30)
    except OverpassTooManyRequests:
        time.sleep(30)
        schools = overpass_api.query(query)

    if schools.nodes or schools.ways:
        RiskFactor = 8
    return RiskFactor


def timber_supply(row, overpass_api, buffer_distance):
    # row.geometry.y = -27.47436
    # row.geometry.x = -55.15989
    RiskFactor = 0
    query = f"node(around:{buffer_distance},{row.geometry.y},{row.geometry.x})[craft=sawmill];out meta;"
    try:
        timber = overpass_api.query(query)
        time.sleep(30)
    except OverpassTooManyRequests:
        time.sleep(30)
        timber = overpass_api.query(query)

    if timber.nodes or timber.ways:

        RiskFactor = 7
    return RiskFactor


def power_line(row, overpass_api, buffer_distance):
    # row.geometry.y = -27.47611;
    # row.geometry.x = -55.15734;
    RiskFactor = 0
    query = f"way(around:{buffer_distance},{row.geometry.y},{row.geometry.x})[power=line];out meta;"
    try:
        power_line = overpass_api.query(query)
        time.sleep(30)
    except OverpassTooManyRequests:
        time.sleep(30)
        power_line = overpass_api.query(query)

    if power_line.nodes or power_line.ways:
        RiskFactor = 5
    return RiskFactor


def urban_areas(row, overpass_api, buffer_distance):
    # row.geometry.y = -26.69454
    # row.geometry.x = -54.20307
    RiskFactor = 0
    query = f"relation(around:{buffer_distance},{row.geometry.y},{row.geometry.x})[landuse=residential];out meta;"
    try:
        urban_areas = overpass_api.query(query)
        time.sleep(30)
    except OverpassTooManyRequests:
        time.sleep(30)
        urban_areas = overpass_api.query(query)

    if urban_areas.relations or urban_areas.nodes or urban_areas.ways:
        RiskFactor = 5
    return RiskFactor
