import os
import zmq
import logging

PULL_PORT = 5558
PUSH_TO_CLIENT_PORT = 5557


class Config:
  def __init__(self):
    self.context = None
    self.pull_socket = None
    self.client_socket = None
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
  context = zmq.Context()

  config.pull_socket = context.socket(zmq.PULL)
  config.pull_socket.bind(f"tcp://*:{PULL_PORT}")

  config.client_socket = context.socket(zmq.PUSH)
  config.client_socket.bind(f"tcp://*:{PUSH_TO_CLIENT_PORT}")


def envSetup():
  config.workers_amount = int(os.environ['WORKERS_AMOUNT'])
  logging.debug(f"Workers amount: {config.workers_amount}")


def setup():
  loggingSetup()
  zmqSetup()
  envSetup()
