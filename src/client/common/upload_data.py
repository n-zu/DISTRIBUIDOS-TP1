import logging
from .process_files import process_csv, parse_weather_batch
from .setup import config

CITIES = ["montreal", "toronto", "washington"]


def upload(file, upload_batch_fn):
    for city in CITIES:
        logging.info(f'uploading weather data for {city}')

        def _upload_batch_fn(batch):
            upload_batch_fn(batch, city)

        try:
            process_csv(f'data/{city}/{file}', _upload_batch_fn)
        except FileNotFoundError:
            logging.error(f'could not find weather data for {city}')
            continue
        except Exception as e:
            logging.error(f'error uploading weather data for {city}: {e}')
            continue


def upload_weather_batch(batch, city):
    data = "weather,"+city + ";"
    data += parse_weather_batch(batch)
    config.pub_socket.send_string(data)
    logging.debug('sent weather data '+data[:20])


def upload_weather():
    upload('weather.csv', upload_weather_batch)
