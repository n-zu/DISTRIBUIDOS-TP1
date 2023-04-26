import logging
import zmq

WORKERS_AMOUNT = 2


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


loggingSetup()
context = zmq.Context()

# Socket to receive messages on
receiver = context.socket(zmq.PULL)
receiver.bind("tcp://*:5558")

# Wait for start of batch
s = receiver.recv_string()

finished_workers = 0

while True:
  s = receiver.recv_string()
  logging.info(f"Received: {s}")

  if s == 'finish':
    finished_workers += 1
  if finished_workers == WORKERS_AMOUNT:
    break

logging.info("Finished")
