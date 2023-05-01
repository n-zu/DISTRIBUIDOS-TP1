import logging
from common.setup import setup
from common.static_data import receive_static_data
from common.trips.process_trips import process_trips


def main():
  setup()
  logging.info("Worker Started")

  receive_static_data()

  process_trips()


if __name__ == "__main__":
  main()
