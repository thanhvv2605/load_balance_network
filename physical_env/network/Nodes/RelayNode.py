from Node import Node
from scipy.spatial.distance import euclidean
import math
class RelayNode(Node):
    def __init__(self, location ,id , phy,start,end):
       super().__init__(location , phy)
       self.location = location 
       self.id = id
       self.start = start
       self.end = end
    def find_receiver(self): # define outnode
        for node in self.neighbors:

            nearest_node = None
            min_distance = math.inf

            if(node.__class__.__name__ == "RelayNode") :
            # if(node.__class__.__name__ == "RelayNode"):

              if(self.start.id == node.start.id and self.end.id == node.end.id):
                Location_end = self.net.baseStation.location
                if self.end.__class__.__name__ == "BaseStation":
                       Location_end = self.end.location
                else: Location_end = self.end.centroid
                
                distance_1 =  euclidean(node.location, Location_end)
                distance_2 =  euclidean(self.location, Location_end)
                if distance_1 < distance_2:
                    if (euclidean(node.location, self.location) < min_distance):
                        nearest_node = node
                        min_distance = euclidean(node.location, self.location)
                
                return nearest_node
        for node in self.neighbors:
            # if(node.__class__.__name__ == "InNode") and self.level > node.level:
            if(node.__class__.__name__ == "InNode"):

                if(node.cluster_id == self.end.id):
                 return node
        pass

    def probe_neighbors(self):
        self.neighbors.clear()
        self.potentialSender.clear()

        for node in self.net.listNodes:
            if self != node and euclidean(node.location, self.location) <= self.com_range:
                self.neighbors.append(node)
                if(node.__class__.__name__ == "RelayNode"):
                    if(self.start.id == node.start.id and self.end.id == node.end.id):
                        self.potentialSender.append(node)
                if(node.__class__.__name__ == "OutNode"):
                    if(node.cluster_id == self.start.id):
                        self.potentialSender.append(node)
                
