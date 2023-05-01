import os
import zmq
import logging

PUB_PORT = 5556
PUSH_PORT = 5557
PULL_FROM_SINK_ADDR = "sink:5557"


class Config:
  def __init__(self):
    self.context = None
    self.pub_socket = None
    self.push_socket = None
    self.sink_socket = None
    self.workers_amount = 0


config = Config()


def loggingSetup():
  logging.addLevelName(
      logging.DEBUG, "\033[1;32m%s\033[1;0m" % logging.getLevelName(logging.DEBUG))
  logging.addLevelName(
      logging.INFO, "\033[1;34m%s\033[1;0m" % logging.getLevelName(logging.INFO))
  logging.addLevelName(
      logging.WARNING, "\033[1;33m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
  logging.addLevelName(
      logging.ERROR, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.ERROR))
  logging.addLevelName(
      logging.CRITICAL, "\033[1;41m%s\033[1;0m" % logging.getLevelName(logging.CRITICAL))

  logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',
                      datefmt='%H:%M:%S')


def zmqSetup():
  config.context = zmq.Context()

  config.pub_socket = config.context.socket(zmq.PUB)
  config.pub_socket.bind(f'tcp://*:{PUB_PORT}')

  config.push_socket = config.context.socket(zmq.PUSH)
  config.push_socket.bind(f'tcp://*:{PUSH_PORT}')

  config.sink_socket = config.context.socket(zmq.PULL)
  config.sink_socket.connect(f'tcp://{PULL_FROM_SINK_ADDR}')


def envSetup():
  config.workers_amount = int(os.environ['WORKERS_AMOUNT'])
  logging.debug(f"Workers amount: {config.workers_amount}")


def sync():
  s = config.sink_socket.recv_string()
  logging.debug(f"Received sync: {s}")


def setup():
  loggingSetup()
  zmqSetup()
  envSetup()
  sync()
