import logging
import middleware
from .config import config, CITIES
from .process_files import process_csv, join_batch


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
  topic = "weather,"+city
  data = join_batch(batch)
  middleware.publish(topic,data)


def upload_weather():
  upload('weather.csv', upload_weather_batch)


def upload_stations_batch(batch, city):
  topic = "stations,"+city
  data = join_batch(batch)
  middleware.publish(topic,data)


def upload_stations():
  upload('stations.csv', upload_stations_batch)


def finish_upload():
  msg="finish_upload"
  middleware.publish(msg,msg)
  logging.info("Finished uploading static data")
