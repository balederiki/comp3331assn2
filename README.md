COMP3331 Assignment 2
James Nicol

==========================================
Python 3 should be used to execute Lsr.py
usage
$./startNetwork.sh
==========================================

Discussion of features
Features implemented
This program simulates a small network of interconnected routers (or nodes) that can each
determine the shortest path to all other routers in the network given information about the routers
that are adjacent to them.
Each node knows the names and ports of the nodes it is connected to as well as the ‘cost’ of the link
to them, the node then shares this information periodically with the network by ‘flooding’ a UDP
message containing that information as well as the node that this information is coming from to all
of its neighbours. The neighbours then send that message to all of their neighbours, and so on until
all nodes in the network have received messages from all other nodes. By collecting the information
in these messages, each node can gain a full picture of the topology of the network, and create a
graph from it. The node can then use Dijkstra’s algorithm on the graph to determine the shortest
path to all nodes in the graph.

Network topology data structure
The network (or Graph) use a dictionary to keep track of the topology of the network. In this
dictionary, the keys are the names of the nodes of the network and the values associated with each
key is the list of the nodes adjacent to them using the class adjNode. When a node update message
is received which contains information about a node and the nodes adjacent to it, the
Graph.update() function is called; This deletes the previous record of that node and replaces it with
the more up to date information. This may seem like a poor performance choice, however if this
were not done, each adjacent node in the message would have to be checked against every adjacent
node in the graph, which has O(n 2 ) complexity and deleting the existing entries and replacing them
with the new ones only has O(n) complexity. So that is why the entries are deleted.
Link state packet format
The link state packet is made up of a tuple of the node that the packet originated from, and a list of
nodes adjacent to it in the form of a list of adjNode objects. The adjNode object holds the name of
the adjacent node, its UDP port, the ‘cost’ to get to it from the original node and whether the node
is still ‘Alive’ or not. In this format, the link state packet can very quickly be added to each nodes
network graph.

Link state broadcasting
Each node broadcasts its own link-state packets from a separate thread, and are sent every
UPDATE_INTERVAL. The bytes data for the packet is created by pickling the objects that are to be
sent, and then when they are received they are unpickled.
When a link-state packet is received, it checks the time that the last update packet for that node was
received, if this packet arrives before the UPDATE_INTERVAL then the message will be ignored, as
forwarding this packet would cause an infinite loop of update packets and the network would
breakdown. If a link-state packet arrives after the UPDATE_INTERVAL then this message will beforwarded to all other adjacent nodes (apart from the one it received it from and the original node)
and then the current time is noted so that it can reject duplicate messages in the interval.

Failed Nodes
On top of sending link-state packets, each node sends heartbeat messages to all of its adjacent
nodes, the format of which is a tuple of the node name and an empty list indicating that this is a
heartbeat message. This is handled in the same thread that handles the sending of the link-state
packets. A number of heart beat messages per link-state update can be chosen.
When checking for incoming packets, a node will check for this heartbeat message and record the
time it arrives. If a node detects it has missed 3 heartbeat messages, this indicates that the node has
‘gone down’ and can no longer be used to send messages through. The removeNode function is then
called, this removes the dead node from the network graph and the node is marked as dead in its
adjNodes list by setting its adjNode.alive attribute to False. This is done so that when a link state
packet is sent from this node to other nodes, it can indicate that that node is dead and all nodes can
update their graphs.

Improvements
Despite having a heartbeat message, it is a little bit useless as only the nodes adjacent to the node
that has failed will know about this quickly whereas other nodes in the graph will have to wait until
the next update interval to update their graphs, additionally graphs are only updated on the receipt
of a new link-state message anyway. Unfortunately the way that flooding was set up meant that
updates arriving before the UPDATE_INTERVAL are ignored meaning that even if a node indicated to
another node that a separate node had failed early, this message would be ignored. So to improve
this, either heart beat messages could be flooded to the network as well, but this would take a lot of
overhead, or the way the update packets are flooded could be changed.
An extension to the program could be for nodes that have been declared dead to be reconnected to
the graph upon restarting them. (After some investigation I found that this extension had been
unintentionally included in the program and nodes may be restarted and added back into the
network after a failure)


Borrowed or inspired code
The Graph class in graph.py was inspired by the Graph class in the response on this stack overflow
page. The key concept that was borrowed was using a dictionary to represent the graph.
<http://stackoverflow.com/questions/19472530/representing-graphs-data-structure-in-python>
The calcLeastCostPaths function was adapted from the pseudo code for using a priority queue to
perform Dijkstra’s algorithm from this wiki article
<https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm>
