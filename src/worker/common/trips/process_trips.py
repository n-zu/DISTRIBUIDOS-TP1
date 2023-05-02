import logging
from .trip import Trip
from ..config import config
from ..store import get_weather, get_station
from .stats import update_stats, upload_stats


def process_trip(trip: Trip):

  trip.enrich(get_weather, get_station)
  update_stats(trip)


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
    logging.debug(f"Received: {header}")

    if header[0] != 'trips':
      logging.error(f"Expected 'trips', received {header[0]}")
      continue

    process_trips_batch(header[1], rows[1:])

  logging.info("Finished processing trips")
  upload_stats()
