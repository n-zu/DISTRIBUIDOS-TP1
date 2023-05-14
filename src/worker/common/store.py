import logging
CITIES = ["montreal", "toronto", "washington"]

weather = {}
stations = {}

for city in CITIES:
  weather[city] = {}
  stations[city] = {}


def store_weather(city, date, precipitation):
  weather[city][date] = precipitation


def store_station(city, id, lat, lng):
  stations[city][id] = (lat, lng)


def get_weather(city, date):
  try:
    return weather[city][date]
  except KeyError:
    logging.warning(f"Could not find weather for {city} on {date}")
    return 0  # We asume no data means no precipitation


def get_station(city, id):
  try:
    return stations[city][id]
  except KeyError:
    logging.warning(f"Could not find station {id} in {city}")
    return (None, None)  # We asume no data means unknown location
