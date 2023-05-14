import os
import logging
from signal import signal, SIGINT, SIGTERM
import middleware

PUB_PORT = 5556
PUSH_PORT = 5557
SINK_IP = "sink"
SINK_PORT = 5557


class Config:
  def __init__(self):
    self.workers_amount = 0
    self.data_path = None


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

def middleware_setup():
  middleware.init(pub_port=PUB_PORT, push_addr=(None, PUSH_PORT), pull_addr=(SINK_IP, SINK_PORT), hwm=config.workers_amount * 2)


def envSetup():
  config.workers_amount = int(os.environ['WORKERS_AMOUNT'])
  logging.debug(f"Workers amount: {config.workers_amount}")
  config.data_path = os.environ['DATA_PATH']
  logging.debug(f"Data path: {config.data_path}")


def sync():
  s = middleware.pull()
  logging.debug(f"Received sync: {s}")


def signalHandler(signum, frame):
  logging.info(f"Received signal: {signum}")
  middleware.close()


def setup():
  loggingSetup()
  envSetup()
  middleware_setup()
  sync()

  TERM_SIGNALS = [SIGINT, SIGTERM]
  for sig in TERM_SIGNALS:
    signal(sig, signalHandler)
