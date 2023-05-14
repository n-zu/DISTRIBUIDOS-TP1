import middleware
import logging
from signal import signal, SIGINT, SIGTERM

SUB_ADDR = "client:5556" # client pub addr (static data)
PULL_ADDR = ("client",5557) # client push addr (trips)
PUSH_ADDR = ("sink", 5558) # sink pull addr (sync/stats)


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
  middleware.init(
    sub_addr=SUB_ADDR,
    pull_addr=PULL_ADDR,
    push_addr=PUSH_ADDR,
    hwm=1,
    timeout_ms=1000,
  )

  topics = ["weather", "stations", "finish_upload"] # TODO: Expand cities
  middleware.subscribe_all(topics)


def sync():
  logging.debug("Sending ready to sink")
  middleware.push("ready")


def signalHandler(signum, frame):
  logging.info(f"Received signal: {signum}")
  middleware.close()


def setup():
  loggingSetup()
  middleware_setup()
  sync()

  TERM_SIGNALS = [SIGINT, SIGTERM]
  for sig in TERM_SIGNALS:
    signal(sig, signalHandler)
