import snap

class Graph:
    """
    The graph constructed by text file
    
    Arguments:
    filename (string): text file, one edge per line, format: user1 user2, no repeat edge
    
    Attributes:
    graph (snap.TUNGraph): undirected graph consists of the users & edges from file
    betweenness (Dictionary): hash table that mapped edges with their betweenness
    """

    def __init__(self, filename):
        self.graph = snap.TUNGraph.New()
        text_file = open(filename, 'r')
        for line in text_file:
            pair = line.split()
            id_1 = int(pair[0])
            id_2 = int(pair[1])
            # generate nodes if they have not been added
            if not self.graph.IsNode(id_1):
                self.graph.AddNode(id_1)
            if not self.graph.IsNode(id_2):
                self.graph.AddNode(id_2)
            self.graph.AddEdge(id_1, id_2)
        text_file.close()
        self.betweenness = self.EdgeBetweenness(self.graph)

    def EdgeBetweenness(self, graph):
        """
        Get the table of edge betweenness.
        
        :param graph: (TUNGraph) a undirected graph
        
        :return: (Dictionary) hash table that mapped edges with their betweenness
        """
        result = {}
        # Compute betweeness
        # nodes_btwn: output as key-value pairs: key-node id, value-btwness
        # edges_btwn: output as key-value pairs: key-(nid1, nid2), value-btwness
        nodes_btwn = snap.TIntFltH()
        edges_btwn = snap.TIntPrFltH()
        snap.GetBetweennessCentr(graph, nodes_btwn, edges_btwn)
        for edge in edges_btwn:
            pair = (edge.GetVal1(), edge.GetVal2())
            result[pair] = edges_btwn[edge]
        return result


def SnapGirvanNewman(G1):
    """
    Call the Stanford Snap method for Girvan-Newman Algorithm.
    This method only gives the final result, does not remember the process.
    
    The code is modified from Snap users manual.
    
    :param G1: (TUNGraph) a undirected graph
    
    :return: (list) list of lists (as communities) of node id
    """
    CmtyV = snap.TCnComV()
    modularity = snap.CommunityGirvanNewman(G1, CmtyV)
    communities = []
    for Cmty in CmtyV1:
        commu = [] # use a list instead of TCnComV
        for NI in Cmty:
            # NI - Node Id, an integer
            commu.append(NI)
        communities.append(commu)

