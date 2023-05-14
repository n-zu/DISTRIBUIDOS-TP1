import logging
from .config import config
from .process_files import process_csv, join_batch
from .send_to_workers import send_to_all_workers
import middleware

CITIES = ["montreal", "toronto", "washington"]


def send_trips_batch(batch, city):
  data = f"trips,{city};"
  data += join_batch(batch)
  middleware.push(data)


def stream_trips():
  """Stream trips to the workers"""

  for city in CITIES:

    def _send_trips_batch(batch):
      send_trips_batch(batch, city)

    def log_send_trips(count):
      logging.debug(
          f"Sent trips, {city} | {count['partial']}/{count['total']}")

    process_csv(f'{config.data_path}/{city}/trips.csv',
                _send_trips_batch, log_func=log_send_trips)

  logging.info("Finished sending trips")
  send_to_all_workers('finish')
