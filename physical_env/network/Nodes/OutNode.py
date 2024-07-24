from Node import Node
from scipy.spatial.distance import euclidean

class OutNode(Node):
    def __init__(self, location ,id , phy):
       super().__init__(location , phy)
       self.location = location 
       self.id = id
       self.cluster_id = 0

    def find_receiver(self): # define outnode
        for node in self.neighbors:
            if(node.__class__.__name__ == "RelayNode" and node.start.id == self.cluster_id): 
                    return node
        pass

    def probe_neighbors(self):
        self.neighbors.clear()
        self.potentialSender.clear()
        for node in self.net.listNodes:
            if self != node and euclidean(node.location, self.location) <= self.com_range:
                self.neighbors.append(node)
                if(node.__class__.__name__ == "InNode"):
                    if(self.cluster_id == node.cluster_id):
                        self.potentialSender.append(node)
                if(node.__class__.__name__ == "SensorNode"):
                    if(self.cluster_id == node.cluster_id):
                        self.potentialSender.append(node)
                if(node.__class__.__name__ == "ConnectorNode"):
                    if(self.cluster_id == node.cluster_id):
                        self.potentialSender.append(node)