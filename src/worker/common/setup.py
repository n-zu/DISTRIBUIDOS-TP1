import zmq
import logging

SUB_ADDR = "client:5556"


class Config:
  def __init__(self):
    self.context = None
    self.sub_socket = None


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
  config.sub_socket = config.context.socket(zmq.SUB)

  config.sub_socket.connect(f'tcp://{SUB_ADDR}')
  config.sub_socket.setsockopt_string(zmq.SUBSCRIBE, "weather")
  config.sub_socket.setsockopt_string(zmq.SUBSCRIBE, "stations")
  config.sub_socket.setsockopt_string(zmq.SUBSCRIBE, "finish_upload")


def setup():
  loggingSetup()
  zmqSetup()
