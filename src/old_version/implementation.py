"""
This is an old version, manually implemented version of Girvan-Newman.
I didn't want to use the preset module in Snap in the beginning,
but I found it is probably going to have some flaws if I implement manually.
It might have some bugs.
"""

class Node:
    """
    One Node in a graph
    
    Arguments:
    id (integer): node id as well as user id
    
    Attirbutes:
    id (integer): node id as well as user id
    neighbors (list of integer): a list of Node id which connect to current node
    """

    def __init__(self, id):
        self.id = id
        neighbors = []

    def addNeighbor(self, neighbor_id):
        neighbors.append(neighbor_id)


class Graph:
    """
        The graph constructed by text file
        
        Arguments:
        filename (string): text file, one edge per line, format: user1 user2, no repeat edge
        
        Attributes:
        Nodes (Dictionary): key(id)-value(Node object) pairs of Nodes in the graph
        """
    
    def __init__(self, filename):
        Nodes = {}
        text_file = open(filename, 'r')
        for line in text_file:
            pair = line.split()
            id_1 = int(pair[0])
            id_2 = int(pair[1])
            if id_1 not in Nodes:
                node_1 = Node(id_1)
                Nodes[id_1] = node_1
            if id_2 not in Nodes:
                node_2 = Node(id_2)
                Nodes[id_2] = node_2
            Node[id_1].addNeighbor(id_2)
            Node[id_2].addNeighbor(id_1)


def BFS(graph, root_id):
    """
    Breath First Search Algorithm
    
    :param graph: (Graph) the graph
    :param root_id: (integer) id of the root node
    
    :return: (Dictionary) pairs of Node id and the len of shortest path
    """
    i = 0
    discoverd = []
    discoverd.append(root_id)
    path = {}
    path[root_id] = i
    nodes = graph.Nodes
    current_id = root_id
    while not len(discoverd) == len(nodes):
        i = i + 1
        for neighbor in nodes[current_id].neighbors:
            if neighbor not in discoverd:
                if neighbor in path:
                    if i < path[neighbor]:
                        path[neighbor] = i
                else:
                    path[neighbor] = i
                discoverd.append(neighbor)
    return path


def GirvanNewman(graph):
    """
    Manual implementation of Girvan-Newman Algorithm
    
    :param: (Graph) the graph
    
    :return: (Dictionary) betweeness
    """
    btwness = {}
    for key in graph.Nodes:
        # process the result from BFS
        path = BFS(graph, key) # path: {node_id: len_of_shortest_path}
        bottom_node = key
        for node in path:
            if path[node] > path[bottom_node]
            bottom_node = node
        # compute betweenness algorithm
        parents = [bottom_node:0]
        while not len(parents) == len(path):
            for node in path:
                if path[node] == path[bottom_node]-1 :
                    parents.append(node)
            for parent in parents:
                btwness[parent] = (btwness[bottom_node]+1) / len(parents)
                bottom_node = parent
