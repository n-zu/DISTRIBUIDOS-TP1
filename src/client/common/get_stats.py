import json
import logging
from .config import config


def get_stats():
  """Get stats from the sink"""

  stats = config.sink_socket.recv_string()
  try:
    stats = json.loads(stats)
  except json.decoder.JSONDecodeError:
    logging.error(f"Received invalid stats: {stats}")
    return

  logging.info(f"Received stats: {stats}")
  save_stats(stats)


def save_stats(stats):
  """Save stats to a file"""

  with open(f'{config.data_path}/stats.json', 'w') as f:
    json.dump(stats, f, indent=2)
