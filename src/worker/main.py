#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

context = zmq.Context()

#  Socket to talk to server
logging.debug("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://client:5555")

#  Do 10 requests, waiting each time for a response
for request in range(10):
    logging.debug("Sending request %s …" % request)
    socket.send(b"Hello")

    #  Get the reply.
    message = socket.recv()
    logging.debug("Received reply %s [ %s ]" % (request, message))
