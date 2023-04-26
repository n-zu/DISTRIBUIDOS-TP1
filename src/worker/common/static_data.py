import logging
from .setup import config
from .util import parse_float
from .store import store_weather, store_station


def parse_weather(row):
  # date, prectot
  return row.split(",")


def parse_station(row):
  # code, lat, lng, year
  return row.split(",")


def handle_static_data(data_type, city, rows):
  if data_type == "weather":
    for row in rows:
      [date, precipitation] = parse_weather(row)
      store_weather(city, date, parse_float(precipitation))

  elif data_type == "stations":
    for row in rows:
      [year, code, lat, lng] = parse_station(row)
      store_station(city, year+"-"+code, parse_float(lat), parse_float(lng))

  else:
    logging.error(f"Received unknown data type {data_type}")


def receive_static_data():
  """Receive static data from the client and store it"""

  while True:
    string = config.sub_socket.recv_string()
    rows = string.split(";")
    header = rows[0]

    logging.debug(f"Received static data: {header} ({len(rows)-1})")

    if header == "finish_upload":
      break

    [data_type, city] = header.split(",")

    handle_static_data(data_type, city, rows[1:])

  config.sub_socket.close()
  logging.info("Finished receiving static data")
