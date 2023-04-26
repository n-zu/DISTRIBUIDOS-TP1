import logging
from ..setup import config


class Trip:
  def __init__(self, city, start_date, start_station_code, end_date, end_station_code, duration_sec, is_member, yearid):
    self.city = city
    self.start_date = start_date
    self.end_date = end_date
    self.start_station_code = yearid + "-" + start_station_code
    self.end_station_code = yearid + "-" + end_station_code
    self.duration_sec = duration_sec

  def enrich(get_weather, get_station):
    pass


def process_trip(trip: Trip):

  # trip.enrich( get_weather, get_station )
  pass


def process_trips_batch(city, batch):
  for row in batch:
    # start_date,start_station_code,end_date,end_station_code,duration_sec,is_member,yearid
    args = row.split(',')
    trip = Trip(city, *args)
    process_trip(trip)


def process_trips():
  """Process trips data"""

  while True:
    data = config.pull_socket.recv_string()

    if data == 'finish':
      break

    rows = data.split(';')
    header = rows[0].split(',')
    logging.info(f"Received: {header}")
    logging.debug(rows)  # TODO: delete this line

    if header[0] != 'trips':
      logging.error(f"Expected 'trips', received {header[0]}")
      continue

    process_trips_batch(header[1], rows[1:])

    config.push_socket.send_string(rows[0])  # TODO: delete this line

  # config.pull_socket.close()
  config.push_socket.send_string('finish')
