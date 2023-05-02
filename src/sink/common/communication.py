import json
from .config import config


def send_to_client(msg):

  if isinstance(msg, str):
    config.client_socket.send_string(msg)
  else:
    str_msg = json.dumps(msg)
    config.client_socket.send_string(str_msg)
