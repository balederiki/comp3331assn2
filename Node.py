class AdjNode(object):  
  """ a class that holds information about a node and link that is 
      adjacent to this node. This is packaged in the link state messages.
  Args:
    name (str): the name of the adjacent node
    cost (float): the cost to reach that node 
    port (int): the port on which this node can be reached
  Attributes:
    name (str): the name of the adjacent node
    cost (float): the cost to reach that node 
    port (int): the port on which this node can be reached
    alive (bool): indicated whether the node is still active or not
  """
  def __init__(self, name, cost, port):
    self.name = name
    self.cost = cost
    self.port = port
    self.alive = True

  def __repr__(self):
    return "n:{}, c:{}, p:{}".format(self.name, self.cost, self.port)

class DNode():
  """used by graph.py to calculate the minimum distances to other nodes
  Args:
    name: the name to give the node
  Attributes:
    name (str): The name of the node (singular uppercase letter)
    dist (float): the distance to that node
    visited (bool): whether the node has been visited or not
    parent (DNode): the parent of the node in Dijkstra's algorithm
  """
  def __init__(self, name):
    self.name = name
    self.dist = float("inf")
    self.visited = False
    self.parent = None

  def __cmp__(self, other):
    """compares nodes based on their """
    return self.dist.__cmp__(other.dist)