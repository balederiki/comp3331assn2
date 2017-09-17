from collections import defaultdict
from Node import DNode


class Graph(object):
  """a class that represents a discreet graph using a dictionary with nodes
     as keys and adjacent nodes as a list of items attached to the keys.

     Attributes:
      _graph (dict(set)): keys in the dictionary are the individual nodes
                          values in the set are AdjNodes
    
  """
  def __init__(self):
    self._graph = defaultdict(set)

  def update(self, node, aNodes):
    """updates a node with the most current information
       checks if a node needs to be removed
    """
    try:
      del self._graph[node]
    except:
      pass
    for aNode in aNodes:
      if aNode.alive == False:
        self.removeNode(aNode.name)
      self._graph[node].add(aNode)

  def removeNode(self, node):
    """removes all references to a node from the graph"""
    justRemoved = self._graph.pop(node, None)
    if justRemoved:
      for n, aNodes in self._graph.items():
        aNodes = [a for a in aNodes if a.name != node]

  def printAllPaths(self, startN):
    """print out the paths and their costs to all other nodes in the graph from
      the start node
    """
    nodes = self.calcLeastCostPaths(startN)
    for n in nodes:
      if n.name == startN:
        continue
      path = self.getPathStr(nodes, n)
      print("least-cost path to node {!s}: {!s}".format(n.name, path)
            + "and the cost is {:.1f}".format(n.dist))

  def calcLeastCostPaths(self, startN):
    """calculates the cost of all paths to nodes in the graph
       from the start node
    """
    nodes = []
    for n in self._graph.keys():
      dN = DNode(n)
      if n == startN:
        dN.dist = 0
      nodes.append(dN)

    unvisited = list(nodes)
    unvisited.sort(key = lambda x: x.dist)

    while unvisited:
      curr = unvisited[0]
      unvisited.remove(curr)
      for adjN in self._graph[curr.name]:
        try:
          adjDnode = next(n for n in unvisited if n.name == adjN.name)
        except:
          continue
        newD = curr.dist + adjN.cost
        if newD < adjDnode.dist:
          adjDnode.dist = newD
          adjDnode.parent = curr
          unvisited.sort(key = lambda x: x.dist)

    return nodes

  def getPathStr(self, nodes, end):
    """ gets the string representation of the least-cost path 
        that needs to be taken 
    """ 
    pathStr = ""
    n = end
    while not n == None:
      pathStr = n.name + pathStr
      n = n.parent
    return pathStr


