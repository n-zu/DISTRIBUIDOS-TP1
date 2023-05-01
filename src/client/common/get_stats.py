import json
import logging
from .setup import config


def get_stats():
  """Get stats from the sink"""

  stats = config.sink_socket.recv_string()
  stats = json.loads(stats)

  logging.info(f"Received stats: {stats}")
