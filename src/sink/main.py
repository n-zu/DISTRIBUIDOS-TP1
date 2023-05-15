import logging
import middleware
from common.config import setup
from common.receive_stats import receive_stats, stats
from common.process_stats import process_stats
from common.communication import send_to_client
from common.static.static_data import receive_static_data


def main():
  receive_static_data()
  receive_stats()

  final_stats = process_stats(stats)
  send_to_client(final_stats)


if __name__ == "__main__":
  try:
    setup()
    main()
    middleware.close()
  except middleware.MiddlewareClosed:
    logging.warning("Program Terminated")
