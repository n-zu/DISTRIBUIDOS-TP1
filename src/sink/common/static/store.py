import logging
CITIES = ["montreal", "toronto", "washington"]

weather = {}
stations = {}

for city in CITIES:
  weather[city] = {}
  stations[city] = {}


def store_station(city, id, name):
  stations[city][id] = name


def get_station(city, id):
  try:
    return stations[city][id]
  except KeyError:
    logging.warning(f"Could not find station {id} in {city}")
    return None  # We asume no data means unknown location
