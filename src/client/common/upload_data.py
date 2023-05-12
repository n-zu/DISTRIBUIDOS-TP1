import logging
from .config import config
from .process_files import process_csv, join_batch
from .send_to_workers import publish_to_workers

CITIES = ["montreal", "toronto", "washington"]


def upload(file, upload_batch_fn):
  for city in CITIES:
    logging.info(f'uploading {city}/{file} data')

    def _upload_batch_fn(batch):
      upload_batch_fn(batch, city)

    try:
      process_csv(f'{config.data_path}/{city}/{file}', _upload_batch_fn)
    except FileNotFoundError:
      logging.error(f'could not find {config.data_path}/{city}/{file}')
      continue
    except Exception as e:
      logging.error(f'error uploading {config.data_path}/{city}/{file}: {e}')
      continue


def upload_weather_batch(batch, city):
  data = "weather,"+city + ";"
  data += join_batch(batch)
  publish_to_workers(data)


def upload_weather():
  upload('weather.csv', upload_weather_batch)


def upload_stations_batch(batch, city):
  data = "stations,"+city + ";"
  data += join_batch(batch)
  publish_to_workers(data)


def upload_stations():
  upload('stations.csv', upload_stations_batch)


def finish_upload():
  publish_to_workers("finish_upload")
  logging.info("Finished uploading static data")
