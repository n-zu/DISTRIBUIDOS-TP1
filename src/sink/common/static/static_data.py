import logging
from middleware import recv_sub_msg
from .store import store_station, stations


def parse_station(row):
  # in: "code,name,latitude,longitude,yearid"
  # out: ["code", "name", "lat", "lng", "yearid"]
  return row.split(",")


def handle_static_data(data_type, city, rows):

  if data_type == "stations":
    for row in rows:
      [code, name, _lat, _lng, year] = parse_station(row)
      store_station(city, year+"-"+code, name)

  else:
    logging.error(f"Received unknown data type {data_type}")


def receive_static_data():
  """Receive static data from the client and store it"""

  while True:
    header,data = recv_sub_msg()
    rows = data.split(";")

    logging.debug(f"Received static data: {header} ({len(rows)})")

    if header == "finish_upload":
      break

    [data_type, city] = header.split(",")

    handle_static_data(data_type, city, rows)

  logging.info("Finished receiving static data")

  for city in stations:
    logging.info(f"Stations - {city}: {len(stations[city])}")
