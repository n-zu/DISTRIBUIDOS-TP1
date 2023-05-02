import logging
from ..config import config
from .store import store_station, stations


def parse_station(row):
  # code, lat, lng, year, name
  return row.split(",")


def handle_static_data(data_type, city, rows):

  if data_type == "stations":
    for row in rows:
      [year, code, lat, lng, name] = parse_station(row)
      store_station(city, year+"-"+code, name)

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

  for city in stations:
    logging.info(f"Stations - {city}: {len(stations[city])}")
