import zmq

middleware = {
  "on": False,
}

class MiddlewareClosed(Exception):
  def __init__(self, message):
    super().__init__(message)

def fail_if_closed():
  if not middleware["on"]:
    raise MiddlewareClosed("Middleware is not initialized")
    

def init( pub_port = None, sub_addr = None, push_addr = None, pull_addr = None, hwm = None, timeout_ms = None ):
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
  if middleware["sub_socket"]:
    middleware["sub_socket"].setsockopt_string(zmq.SUBSCRIBE, topic)
  else:
    raise Exception("No sub socket")

@fail_if_closed
def subscribe_all( topics ):
  for topic in topics:
    subscribe(topic)
  
@fail_if_closed
def publish( topic, message ):
  if middleware["pub_socket"]:
    middleware["pub_socket"].send_string(f"{topic};{message}")
  else:
    raise Exception("No pub socket")

@fail_if_closed
def recv_sub_msg():
  if middleware["sub_socket"]:
    return middleware["sub_socket"].recv_string()
  else:
    raise Exception("No sub socket")

@fail_if_closed
def push( message ):
  if middleware["push_socket"]:
    middleware["push_socket"].send_string(message)
  else:
    raise Exception("No push socket")
  
@fail_if_closed
def pull():
  if middleware["pull_socket"]:
    return middleware["pull_socket"].recv_string()
  else:
    raise Exception("No pull socket")
  
@fail_if_closed
def close():
  if middleware["context"]:
    middleware["context"].term()
  else:
    raise Exception("Not initialized")