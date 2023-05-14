import logging
import json
from .join_stats import join_stats
from .config import config
from middleware import pull
stats = {}


def receive_stats_message():
  s = pull()
  # logging.debug(f"Received: {s}")

  recv_stats = json.loads(s)
  join_stats(stats, recv_stats)


def receive_stats():

  logging.info("Receiving stats")

  finished_workers = 0

  while True:
    receive_stats_message()

    finished_workers += 1
    if finished_workers == config.workers_amount:
      break

  logging.info("Finished receiving stats")
  # logging.debug(f"Stats: {stats}")
