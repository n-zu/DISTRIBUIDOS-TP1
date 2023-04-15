import logging
from .process_files import process_csv
from .parse import parse_weather_batch

CITIES = ["montreal", "toronto", "washington"]


def upload(file, upload_batch_fn):
    for city in CITIES:
        logging.info(f'uploading weather data for {city}')
        try:
            process_csv(f'data/{city}/{file}', upload_batch_fn)
        except FileNotFoundError:
            logging.error(f'could not find weather data for {city}')
            continue
        except Exception as e:
            logging.error(f'error uploading weather data for {city}: {e}')
            continue


def upload_weather_batch(batch):
    data = parse_weather_batch(batch)
    logging.info(f'uploading batch of weather data:  {data}')


def upload_weather():
    upload('weather.csv', upload_weather_batch)
