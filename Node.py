# a class that holds information about a node and link that is 
# adjacent to this node 
class AdjNode(object):
  def __init__(self, name, cost, port):
    self.name = name
    self.cost = cost
    self.port = port
    self.alive = True

  def __repr__(self):
    return "n:{}, c:{}, p:{}".format(self.name, self.cost, self.port)

# used by graph.py to calculate the minimum distances to 
# other nodes
class DNode():
  def __init__(self, name):
    self.name = name
    self.dist = float("inf")
    self.visited = False
    self.parent = None

  def __cmp__(self, other):
    return self.dist.__cmp__(other.dist)