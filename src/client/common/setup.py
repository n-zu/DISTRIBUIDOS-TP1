import zmq
import logging


def loggingSetup():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')


def zmqSetup():
    global context
    context = zmq.Context()


def setup():
    loggingSetup()
    zmqSetup()
