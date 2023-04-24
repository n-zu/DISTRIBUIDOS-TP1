from common.setup import setup
from common.upload_data import upload_weather, upload_stations, finish_upload
from time import sleep


def main():
  setup()
  sleep(5)  # TODO: Replace with a proper synchronization mechanism

  upload_weather()
  upload_stations()
  finish_upload()

  sleep(5)  # TODO: Remove this, when stream_trips() is implemented

  # stream_trips()

  # get_stats()


if __name__ == "__main__":
  main()
