from .config import config
import middleware


def send_to_all_workers(data):
  for i in range(config.workers_amount):
    middleware.push(data)
