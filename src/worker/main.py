import logging
from common.setup import setup
from common.static_data import receive_static_data
from common.store import weather, stations


def main():
  setup()
  logging.info("Worker Started")

  receive_static_data()

  for city in weather:
    logging.info(f"Weather - {city}: {len(weather[city])}")
  for city in stations:
    logging.info(f"Stations - {city}: {len(stations[city])}")


if __name__ == "__main__":
  main()
