#!/usr/bin/python
# CS4032 - Lab02
# Michael Daly/Mc Andrew

import logging, socket, sys
import Queue
from time import sleep
from threading import Thread
from multiprocessing import Value

msg = "IP:%s\nPort:%d\nStudentID:19665f8aea13911e4746d7527c5e69121f7154c9907b0aabc27640dd03b5e91b"

def run_server(port, maxThreads=8, maxQueue=100):
  host = 'localhost'
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  q = Queue.Queue(maxsize=maxQueue)
  threads = []
  isRunning = Value('i', 1)
  
  # connection handler
  def connection_handler(isRunning, queue):
    BUFFER_SIZE = 8096

    while isRunning.value:
      conn, addr = queue.get()

      logging.info("Thread recieved connection from queue from address %s:%d" % (addr[0], addr[1]))

      data = conn.recv(BUFFER_SIZE) # doesn't handle messages longer than BUFFER_SIZE

      if data == "KILL_SERVICE\n":
        logging.info("Server shutting down.")
        isRunning.value = 0
        conn.sendall("SHUTTING_DOWN")
        conn.close()
        raise SystemExit("Received shutdown command.")

      elif data[:4] == 'HELO':
        logging.info("Echoing message back")
        conn.sendall(data + (msg % (host, port)))

      else:
        logging.info("Unknown Request.")
        conn.sendall("UNRECOGNISED_COMMAND")

      conn.close()

    raise SystemExit("Noticed shutdown. Shutting down thread")

  try:
    # setup thread pool
    for i in xrange(maxThreads):
      thread = Thread(target=connection_handler, args=(isRunning, q))
      thread.daemon = True # daemonise so that KeyboardInterupt on main thread kills these threads too
      thread.start()
      
      threads.append(thread)

    # listen for connections and hand them off to a thread in the pool
    s.bind((host, port))
    s.listen(1)
    logging.info("Server has bound to socket on host '%s' and port '%d'" % (host, port))
    while isRunning.value:
      # accept connections
      conn, addr = s.accept()
      logging.info("Accepting connection from address '%s'" % addr[0])
      try:
        q.put((conn, addr), False) # do not block if queue is full - reject connection
      except Queue.Full:
        logging.info("Server overloaded cannot accept anymore connections")

    s.close()

  except (KeyboardInterrupt, SystemExit):
    logging.info("END: Shutting down service")
    sys.exit(0)

if __name__ == "__main__":
  if len(sys.argv) is not 3:
    raise Exception("Usage: ./server.py << port >> << maxThreads >>")
  port = int(sys.argv[1])
  maxThreads = int(sys.argv[2])

  # logging
  FORMAT = "%(asctime)s %(process)s %(thread)s: %(message)s"
  logging.basicConfig(format=FORMAT, level=logging.INFO)

  run_server(port, maxThreads)
