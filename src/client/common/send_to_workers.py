from .config import config


def publish_to_workers(data):
  config.pub_socket.send_string(data)


def send_to_all_workers(data):
  for i in range(config.workers_amount):
    config.push_socket.send_string(data)
