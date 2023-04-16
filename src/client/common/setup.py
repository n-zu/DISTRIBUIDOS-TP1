import zmq
import logging

PUB_PORT = 5556


class Config:
    def __init__(self):
        self.context = None
        self.pub_socket = None


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


def setup():
    loggingSetup()
    zmqSetup()
