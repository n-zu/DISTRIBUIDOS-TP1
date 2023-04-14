#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
import zmq
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

logging.debug("Server started")

while True:
    #  Wait for next request from client
    message = socket.recv()
    logging.debug("Received request: %s" % message)

    #  Do some 'work'
    time.sleep(1)

    #  Send reply back to client
    socket.send(b"World")
