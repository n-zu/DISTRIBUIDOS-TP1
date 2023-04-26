import logging
from .setup import config
from .process_files import process_csv, parse_trips_batch
from .send_to_workers import send_to_all_workers

CITIES = ["montreal", "toronto", "washington"]


def send_trips_batch(batch, city):
  data = f"trips,{city};"
  data += parse_trips_batch(batch)
  config.push_socket.send_string(data)
  logging.debug(f"Sent: trips,{city};")


def stream_trips():
  """Stream trips to the workers"""

  config.sink_socket.send_string("start_streaming")

  for city in CITIES:

    def _send_trips_batch(batch):
      send_trips_batch(batch, city)

    process_csv(f'data/{city}/trips.csv', _send_trips_batch, 10, 10)

  send_to_all_workers('finish')
