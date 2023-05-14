import json
import logging
from .config import config
import middleware


def get_stats():
  """Get stats from the sink"""

  stats = middleware.pull()
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
