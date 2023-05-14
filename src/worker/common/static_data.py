import logging
import middleware
from .util import parse_float
from .store import store_weather, store_station, weather, stations


def parse_weather(row):
  # in: "date,prectot,qv2m,rh2m,ps,t2m_range,ts,t2mdew,t2mwet,t2m_max,t2m_min,t2m,ws50m_range,ws10m_range,ws50m_min,ws10m_min,ws50m_max,ws10m_max,ws50m,ws10m,yearid"
  # out: ["date", "prectot"]
  return row.split(",")[0:2]


def parse_station(row):
  # in: "code,name,latitude,longitude,yearid"
  # out: ["code", "name", "lat", "lng", "yearid"]
  return row.split(",")


def handle_static_data(data_type, city, rows):
  if data_type == "weather":
    for row in rows:
      [date, precipitation] = parse_weather(row)
      store_weather(city, date, parse_float(precipitation))

  elif data_type == "stations":
    for row in rows:
      [code, _name, lat, lng, year] = parse_station(row)
      store_station(city, year+"-"+code, parse_float(lat), parse_float(lng))

  else:
    logging.error(f"Received unknown data type {data_type}")


def receive_static_data():
  """Receive static data from the client and store it"""

  while True:
    string = middleware.recv_sub_msg()
    rows = string.split(";")
    header = rows[0]

    logging.debug(f"Received static data: {header} ({len(rows)-1})")

    if header == "finish_upload":
      break

    [data_type, city] = header.split(",")

    handle_static_data(data_type, city, rows[1:])

  logging.info("Finished receiving static data")
  for city in weather:
    logging.info(f"Weather - {city}: {len(weather[city])}")
  for city in stations:
    logging.info(f"Stations - {city}: {len(stations[city])}")
