import os
import logging
from signal import signal, SIGINT, SIGTERM
import middleware

CITIES = ["montreal", "toronto", "washington"]
STATIC_DATA = ["stations"]


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
  PULL_PORT = int(os.environ['PULL_PORT'])
  PUSH_TO_CLIENT_PORT = int(os.environ['PUSH_TO_CLIENT_PORT'])
  SUB_ADDR = os.environ['SUB_ADDR']
  middleware.init(
    sub_addr=SUB_ADDR,
    push_addr=(None,PUSH_TO_CLIENT_PORT),
    pull_addr=(None,PULL_PORT)
  )

  for data in STATIC_DATA:
    for city in CITIES:
      middleware.subscribe(f"{data},{city}")
  middleware.subscribe("finish_upload")



def envSetup():
  config.workers_amount = int(os.environ['WORKERS_AMOUNT'])
  logging.debug(f"Workers amount: {config.workers_amount}")


def sync():
  for i in range(config.workers_amount):
    s = middleware.pull()
    logging.debug(f"Received [{s}] from worker {i}")

  middleware.push("System Up")


def signalHandler(signum, frame):
  logging.info(f"Received signal: {signum}")
  middleware.close()


def setup():
  loggingSetup()
  middleware_setup()
  envSetup()
  sync()

  TERM_SIGNALS = [SIGINT, SIGTERM]
  for sig in TERM_SIGNALS:
    signal(sig, signalHandler)
