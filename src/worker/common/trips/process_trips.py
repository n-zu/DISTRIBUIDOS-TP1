import logging
from .trip import Trip
import middleware
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


def log_received_trips(header, amount, count):
  PARTIAL_COUNT_LIM = 50000

  count["total"] += amount
  count["partial"] += amount

  if count["partial"] >= PARTIAL_COUNT_LIM:
    logging.info(
        f"Received {header} | {amount}/{count['partial']}/{count['total']}")
    count["partial"] = 0


def process_trips():
  """Process trips data"""

  count = {
      "total": 0,
      "partial": 0,
  }

  while True:
    try:
      data = middleware.pull()
    except middleware.MiddlewareClosed as e:
      raise e
    except Exception as e:
      logging.error(f"Error receiving data: {e}")
      break

    if data == 'finish':
      break

    rows = data.split(';')
    header = rows[0].split(',')
    log_received_trips(header, len(rows)-1, count)

    if header[0] != 'trips':
      logging.error(f"Expected 'trips', received {header[0]}")
      continue

    process_trips_batch(header[1], rows[1:])

  logging.info("Finished processing trips")
  upload_stats()
