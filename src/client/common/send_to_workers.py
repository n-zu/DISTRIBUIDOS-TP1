from .setup import config


def send_to_all_workers(data):
  config.pub_socket.send_string(data)
