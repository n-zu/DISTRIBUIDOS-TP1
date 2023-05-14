import json
from .config import config
from middleware import push


def send_to_client(msg):

  if isinstance(msg, str):
    push(msg)
  else:
    str_msg = json.dumps(msg)
    push(str_msg)
