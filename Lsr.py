#!/usr/bin/python3
import sys
import socket
import threading
import time
import pickle
from threading import Thread
from Node import AdjNode
from Graph import Graph

# constants
ROUTE_UPDATE_INTERVAL = 5 
UPDATE_INTERVAL = 1.0
HB_PER_UPDATE = 5 # must be >0
HOST = ''

def main():
  # check the number of sysargs, if correct then capture them
  if len(sys.argv) == 4:
    nodeName = sys.argv[1]
    nodePort = int(sys.argv[2])
    configFile = sys.argv[3]
  else:
    print("incorrect argruments, Name, Port, config")
    return

  adjNodes = getNodesFromFile(configFile)

  # create an empty graph that will represent the network
  network = Graph()

  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.bind((HOST, nodePort))

  # create a lock for the list of adjacent nodes 
  # as it is used by both threads
  adjLock = threading.RLock()
  # create and start the thread that sends periodic updates
  # to the other nodes
  updateT = UpdateThread(sock, adjNodes, adjLock, nodeName)
  updateT.start()

  network.update(nodeName, adjNodes)

  refT = time.time()
  while True:
    adjData = recvFromAll(sock, adjNodes)
    # if any data was received, update the graph
    if adjData:
      node, nAdj = adjData
      # if nAdj is None this indicates this node has gone down
      # and should be removed from the graph
      if nAdj == None:
        removeNode(node, adjNodes, network, adjLock)
      else:
        network.update(node, nAdj)

    # check if it is time to recalculate the graph and 
    # print the statistics about it
    if time.time() > refT + ROUTE_UPDATE_INTERVAL:
      print("="*51)
      refT = time.time()
      network.printAllPaths(nodeName)

def removeNode(node, aNodes, network, aLock):
  """removes a node from both the adjacent nodes list
     and this nodes picture of the network  aLock.acquire()
  """
  aNode = next(n for n in aNodes if n.name == node)
  aNode.alive = False
  aLock.release()

  network.removeNode(node)

def getNodesFromFile(file):
  """exctract a list of adjacent nodes from the text 
     file that is given
  """

  fh = open(file, encoding='ascii', newline="")
  fLines = fh.readlines()
  numNodes = int(fLines.pop(0))
  adjNodes = []
  for x in range(numNodes):
    name, cost, port = fLines[x].split()
    n = AdjNode(name, float(cost), int(port))
    adjNodes.append(n)
  return adjNodes

def recvFromAll(sock, adjNodes):
  """checks if there are any packets to be read, checks the type of packet and 
     floods the message if it is an update or take note of the time of a heartbeat
     if it misses 3 heartbeats it will indicate this by returning 'None' in the second 
     field of the tuple and the node that it missed it from in the first
  """
  sock.setblocking(0)
  try:
    data, addr = sock.recvfrom(1024)
    rName, rAdjNodes = pickle.loads(data)

    # check if the message is a heartbeat, and mark 
    # the time that it arrived if it is
    if rAdjNodes == []: 
      tPair = next((x for x in recvFromAll.lHBtime if x[0] == rName), None)
      try:
        recvFromAll.lHBtime.remove(tPair)
      except:
        pass
      recvFromAll.lHBtime.append((rName, time.time()))
      return None

    # calculate the time that would indicate a timeout
    hbTimeout = (UPDATE_INTERVAL/HB_PER_UPDATE)*3
    # check to see if 3 heartbeats in a row have been missed
    for a in recvFromAll.lHBtime:
      if time.time() > a[1] + hbTimeout:
        fNode = a[0]
        recvFromAll.lHBtime.remove(a)
        return (fNode, None)

    # mark the time that the update packet arrived for a node,
    # so that additional update packets from that node are not forwarded 
    # the next update interval
    try:
      tPair = next((x for x in recvFromAll.lUtime if x[0] == rName))
      if time.time() > tPair[1] + UPDATE_INTERVAL*0.99:
        recvFromAll.lUtime.remove(tPair)
        recvFromAll.lUtime.append((rName, time.time()))
      else:
        # packet arrived before the next update interval
        # do not flood this packet
        return None
    except:
      recvFromAll.lUtime.append((rName, time.time()))

    # flood the packet to the network on all adjacent ports
    for node in [n for n in adjNodes if n.port != addr[1] and n.port != rName]:
      sock.sendto(data, ('127.0.0.1', node.port))
    return (rName, rAdjNodes)
  except socket.error:
    pass
  return None
recvFromAll.lUtime = []
recvFromAll.lHBtime = []

class UpdateThread(Thread):
  def __init__(self, sock, adjNodes, adjLock, name):
    Thread.__init__(self)
    self.adjNodes = adjNodes
    self.sock = sock
    self.adjLock = adjLock
    self.nName = name

# starts the thread and sends periodic pulses and updates
  def run(self):
    while True:
      for x in range(HB_PER_UPDATE):
        self.sndHB()
        time.sleep(UPDATE_INTERVAL/HB_PER_UPDATE)
      self.sndUpdate()

# send a heart beat, denoted by 'None' in adjNodes field
  def sndHB(self):
    for node in self.adjNodes:
      msg = pickle.dumps((self.nName, []))
      addr = ('127.0.0.1', node.port)
      try:
        self.sock.sendto(msg, addr)
      except socket.error:
        pass

# send info about this nodes adjacent nodes
  def sndUpdate(self):
    for node in self.adjNodes:
      self.adjLock.acquire()
      msg = pickle.dumps((self.nName, self.adjNodes))
      self.adjLock.release()
      addr = ('127.0.0.1', node.port)
      try:
        self.sock.sendto(msg, addr)
      except socket.error:
        pass

if __name__ == "__main__" : main()
