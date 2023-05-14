import os
import logging
from signal import signal, SIGINT, SIGTERM
from .middleware import init, close, subscribe_all, push, pull

PULL_PORT = 5558
PUSH_TO_CLIENT_PORT = 5557
SUB_ADDR = "client:5556"


class Config:
  def __init__(self):
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


def middleware_setup():
  init(
    sub_addr=SUB_ADDR,
    push_addr=(None,PUSH_TO_CLIENT_PORT),
    pull_addr=(None,PULL_PORT)
  )

  topics = ["stations","finish_upload"] #permutate cities

  subscribe_all(topics)



def envSetup():
  config.workers_amount = int(os.environ['WORKERS_AMOUNT'])
  logging.debug(f"Workers amount: {config.workers_amount}")


def sync():
  for i in range(config.workers_amount):
    s = pull()
    logging.debug(f"Received [{s}] from worker {i}")

  push("System Up")


def signalHandler(signum, frame):
  logging.info(f"Received signal: {signum}")
  close()
  exit(0)


def setup():
  loggingSetup()
  middleware_setup()
  envSetup()
  sync()

  TERM_SIGNALS = [SIGINT, SIGTERM]
  for sig in TERM_SIGNALS:
    signal(sig, signalHandler)
