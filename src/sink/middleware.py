import zmq

middleware = {}

def init( pub_port = None, sub_addr = None, push_addr = None, pull_addr = None, hwm = None ):
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
      middleware["push_socket"].bind(f'tcp://{ip}:{port}')
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

def subscribe( topic ):
  if middleware["sub_socket"]:
    middleware["sub_socket"].setsockopt_string(zmq.SUBSCRIBE, topic)
  else:
    raise Exception("No sub socket")
  
def subscribe_all( topics ):
  for topic in topics:
    subscribe(topic)
  
def publish( topic, message ):
  if middleware["pub_socket"]:
    middleware["pub_socket"].send_string(f"{topic};{message}")
  else:
    raise Exception("No pub socket")
  
def recv_sub_msg():
  if middleware["sub_socket"]:
    return middleware["sub_socket"].recv_string()
  else:
    raise Exception("No sub socket")
  
def push( message ):
  if middleware["push_socket"]:
    middleware["push_socket"].send_string(message)
  else:
    raise Exception("No push socket")
  
def pull():
  if middleware["pull_socket"]:
    return middleware["pull_socket"].recv_string()
  else:
    raise Exception("No pull socket")
  
def close():
  if middleware["context"]:
    middleware["context"].term()
  else:
    raise Exception("Not initialized")