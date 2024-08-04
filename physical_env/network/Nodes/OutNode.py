from Node import Node
from scipy.spatial.distance import euclidean
import math

class OutNode(Node):
    def __init__(self, location ,id , phy):
       super().__init__(location , phy)
       self.location = location 
       self.id = id
       self.cluster_id = 0

    def find_receiver(self): # define outnode
        nearest_node = None
        min_distance = math.inf
        for node in self.neighbors:
            if(node.__class__.__name__ == "RelayNode" and node.send_cluster_id.id == self.cluster_id): 
                if euclidean(node.location, self.location) < min_distance:
                    nearest_node = node
                    min_distance = euclidean(node.location, self.location)
        if (nearest_node != None):
            return nearest_node

        # nếu không tìm được relay node, tìm cho in node gần nhất nếu có
        # for node in self.neighbors:
        #     if(node.__class__.__name__ == "InNode"):
        #         if euclidean(node.location, self.location) < min_distance:
        #             nearest_node = node
        #             min_distance = euclidean(node.location, self.location)
        # return nearest_node

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