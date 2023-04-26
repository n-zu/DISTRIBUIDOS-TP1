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
    raise Exception(f"Weather KeyError: {city}, {date}")


def get_station(city, id):
  try:
    return stations[city][id]
  except KeyError:
    raise Exception(f"Station KeyError: {city}, {id}")
