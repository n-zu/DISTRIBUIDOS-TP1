# Middleware for communication between processes
# 
# - An agent could do all actions, subscribe, publish, pull and push
# - Pub/Sub:
#   - One publisher may have multiple subscribers
#   - There cant be multiple publishers for one subscriber
#   - There cant be many to many communication
# - Pull/Push
#   - There can be one puller/many pushers or one pusher/many pullers
#   - The "many" have to specify the (ip,port) of the "one",
#     while the one specifies which port it uses to communicate.
#   - There cant be many to many communication

import zmq

middleware = {"on": False}

class MiddlewareClosed(Exception):
  def __init__(self, message):
    super().__init__(message)

def fail_if_closed(func):
  '''
  Decorator to check if middleware is initialized
  '''
  def wrapper(*args, **kwargs):
    if middleware["on"]:
      try:
        return func(*args, **kwargs)
      except Exception as e:
        if not middleware["on"]:
          raise MiddlewareClosed("Middleware closed or not initialized")
        raise e
    else:
      raise MiddlewareClosed("Middleware closed or not initialized")
  return wrapper
    

def init(
    pub_port = None,
    sub_addr = None,
    push_addr = None,
    pull_addr = None,
    hwm = None,
    timeout_ms = None
  ):
  '''
  Initialize the middleware
  - pub_port: port from which to publish messages
  - sub_addr: address to which to subscribe
  - push_addr: address to which to push messages in a (ip, port) tuple
    - if ip is None, this process may push to multiple processes from it's defined port
    - if ip is not None, this process may only push to the process with the specified ip and port
  - pull_addr: address from which to pull messages in a (ip, port) tuple
    - if ip is None, this process may pull from multiple processes from it's defined port
    - if ip is not None, this process may only pull from the process with the specified ip and port
  - hwm: high water mark for push/pull sockets (how many messages can be queued before blocking push)
  - timeout_ms: timeout for pull socket in milliseconds
  '''
  middleware["on"] = True
  middleware["context"] = zmq.Context()

  if pub_port:
    middleware["pub_socket"] = middleware["context"].socket(zmq.PUB)
    middleware["pub_socket"].bind(f'tcp://*:{pub_port}')

  if sub_addr:
    middleware["sub_socket"] = middleware["context"].socket(zmq.SUB)
    middleware["sub_socket"].connect(f'tcp://{sub_addr}')

  if push_addr:
    ip, port = push_addr
    middleware["push_socket"] = middleware["context"].socket(zmq.PUSH)
    if ip:
      middleware["push_socket"].connect(f'tcp://{ip}:{port}')
    else:
      middleware["push_socket"].bind(f'tcp://*:{port}')
      if hwm:
        middleware["push_socket"].set_hwm(hwm)
  
  if pull_addr:
    ip, port = pull_addr
    middleware["pull_socket"] = middleware["context"].socket(zmq.PULL)
    if ip:
      middleware["pull_socket"].connect(f'tcp://{ip}:{port}')
    else:
      middleware["pull_socket"].bind(f'tcp://*:{port}')
      if hwm:
        middleware["pull_socket"].set_sockopt(zmq.RCVHWM, hwm)
    if timeout_ms:
      middleware["pull_socket"].setsockopt(zmq.RCVTIMEO, timeout_ms)

@fail_if_closed
def subscribe( topic ):
  '''
  Subscribe to a topic
  '''
  if middleware["sub_socket"]:
    middleware["sub_socket"].setsockopt_string(zmq.SUBSCRIBE, topic)
  else:
    raise Exception("No sub socket")

@fail_if_closed
def subscribe_all( topics ):
  '''
  Subscribe to all topics in a list
  '''
  for topic in topics:
    subscribe(topic)
  
@fail_if_closed
def publish( topic, message ):
  '''
  Publish a message to a topic
  '''
  if middleware["pub_socket"]:
    middleware["pub_socket"].send_string(f"{topic};{message}")
  else:
    raise Exception("No pub socket")

@fail_if_closed
def recv_sub_msg():
  '''
  Receive a message from a subscribed topic
  returns (topic, data)
  '''
  if middleware["sub_socket"]:
    msg = middleware["sub_socket"].recv_string()
    [topic, data] = msg.split(";", 1)
    return topic, data
  else:
    raise Exception("No sub socket")

@fail_if_closed
def push( message ):
  '''
  Push a message to a puller
  '''
  if middleware["push_socket"]:
    middleware["push_socket"].send_string(message)
  else:
    raise Exception("No push socket")
  
@fail_if_closed
def pull():
  '''
  Pull a message from a pusher
  '''
  if middleware["pull_socket"]:
    return middleware["pull_socket"].recv_string()
  else:
    raise Exception("No pull socket")
  
@fail_if_closed
def close():
  '''
  Close all sockets/file descriptors and clean up
  '''
    
  if "pub_socket" in middleware:
    middleware["pub_socket"].close()
  if "sub_socket" in middleware:
    middleware["sub_socket"].close()
  if "push_socket" in middleware:
    middleware["push_socket"].close()
  if "pull_socket" in middleware:
    middleware["pull_socket"].close()
  if "context" in middleware:
    middleware["context"].term()
  
  middleware["on"] = False