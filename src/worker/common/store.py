CITIES = ["montreal", "toronto", "washington"]

weather = {}
stations = {}
trips_data = {}

for city in CITIES:
  weather[city] = {}
  stations[city] = {}


def store_weather(city, date, precipitation):
  weather[city][date] = precipitation


def store_station(city, id, lat, lng):
  stations[city][id] = (lat, lng)
