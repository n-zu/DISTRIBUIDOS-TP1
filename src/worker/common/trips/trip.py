
def distance(lat1, lon1, lat2, lon2):
  return ((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2) ** 0.5


class Trip:
  def __init__(self, city, start_date, start_station_code, end_date, end_station_code, duration_sec, is_member, yearid):
    self.city = city
    self.start_date = start_date.split(' ')[0]
    self.end_date = end_date.split(' ')[0]
    self.start_station_code = yearid + "-" + start_station_code
    self.end_station_code = yearid + "-" + end_station_code
    self.duration_sec = duration_sec

    self.precipitation = None
    self.distance = None

  def enrich(self, get_weather, get_station):
    weather = get_weather(self.city, self.start_date)
    self.precipitation = weather

    start_station = get_station(self.city, self.start_station_code)
    end_station = get_station(self.city, self.end_station_code)

    self.distance = distance(
        start_station[0], start_station[1], end_station[0], end_station[1])