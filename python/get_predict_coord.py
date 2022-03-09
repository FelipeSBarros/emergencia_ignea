import geopy
from geopy.distance import VincentyDistance
# from geopy import distance


def predict_fire_geopy():
    # todo ver solucao https://geopy.readthedocs.io/en/latest/#geopy.distance.Distance.destination
    # given: lat1, lon1, b = bearing in degrees, d = distance in kilometers

    # origin = geopy.Point(lat1, lon1)
    # destination = VincentyDistance(kilometers=d).destination(origin, b)

    lat2, lon2 = destination.latitude, destination.longitude

    # TODO outr possibilidade

    # # distance.distance(unit=15).destination((lat,lon),bering)
    # # Exemples
    # distance.distance(nautical=15).destination((-24, -42), 90)
    # distance.distance(miles=15).destination((-24, -42), 90)
    # distance.distance(kilometers=15).destination((-24, -42), 90)

def prodict_fire_math():
    import math

    R = 6378.1  # Radius of the Earth
    brng = 1.57  # Bearing is 90 degrees converted to radians.
    d = 15  # Distance in km

    # lat2  52.20444 - the lat result I'm hoping for
    # lon2  0.36056 - the long result I'm hoping for.

    lat1 = math.radians(52.20472)  # Current lat point converted to radians
    lon1 = math.radians(0.14056)  # Current long point converted to radians

    lat2 = math.asin(math.sin(lat1) * math.cos(d / R) +
                     math.cos(lat1) * math.sin(d / R) * math.cos(brng))

    lon2 = lon1 + math.atan2(math.sin(brng) * math.sin(d / R) * math.cos(lat1),
                             math.cos(d / R) - math.sin(lat1) * math.sin(lat2))

    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)

    print(lat2)
    print(lon2)
