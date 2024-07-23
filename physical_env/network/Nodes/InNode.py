import random
from .Node import Node

class InNode(Node):
    def __init__(self, location ,id , phy):
        super().__init__(location , phy)
        self.location = location 
        self.id = id
        self.cluster_id = 0

        self.out_node_list = []
        self.out_node_number = 1

        self.chosen_out_node_index = self.chosen_random_index()


        self.rr_current_unit = 0 # số lần liên tiếp gửi gói tin cho outnode trước khi chuyển sang node khác
        self.package_index = 0

        self.rr_max_unit = 2
        self.rr_max_cycle = 5
        self.max_package_index = self.out_node_number * self.rr_max_unit * self.rr_max_cycle


    # def find_receiver(self): # define outnode
    #     for node in self.neighbors: 
    #         # if(node.__class__.__name__ == "OutNode") and self.level > node.level:
    #         if(node.__class__.__name__ == "OutNode") and self.cluster_id == node.cluster_id:
    #             return node
    #     pass

    def find_receiver(self):
        
        # ROUND-ROBIN ALGORITHM

        self.get_out_node_list()

        if(self.package_index == self.max_package_index):
            self.package_index = 0
            self.rr_current_unit = 0 
            self.chosen_out_node_index = self.chosen_random_index()

        if(self.rr_current_unit == self.rr_max_unit):
            self.rr_current_unit = 0 
            self.chosen_out_node_index = (self.chosen_out_node_index + 1) % self.out_node_number

        self.rr_current_unit = self.rr_current_unit + 1
        self.package_index = self.package_index + 1

        return self.out_node_list[self.chosen_out_node_index] 

    def chosen_random_index(self):
        if(self.out_node_number == 1):
            return 0
        index = random.randint(0, self.out_node_number - 1)
        return index
    
    def get_out_node_list(self):
        for node in self.neighbors:
            if(node.__class__.__name__ == "OutNode" and self.cluster_id == node.cluster_id):
                self.out_node_list.append(node)
        self.out_node_number = len(self.out_node_list)

        