import logging
import middleware
from common.config import setup
from common.get_stats import get_stats
from common.upload_data import upload_weather, upload_stations, finish_upload
from common.stream_data import stream_trips


def main():
  upload_weather()
  upload_stations()
  finish_upload()

  stream_trips()

  get_stats()


if __name__ == "__main__":
  try:
    setup()
    main()
    middleware.close()
  except middleware.MiddlewareClosed:
    logging.warning("Program Terminated")

