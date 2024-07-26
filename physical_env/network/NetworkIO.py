import copy
import simpy
import yaml
import random
import numpy as np
import sys
import os
import json
sys.path.append(os.path.dirname(__file__))
from BaseStation import BaseStation
from Network import Network
from physical_env.network.Nodes.Node import Node
from Target import Target


class NetworkIO:
    def __init__(self, file_data):
        with open(file_data, 'r') as file:
            self.net_argc = yaml.safe_load(file)

    def makeNetwork(self):
        net_argc = copy.deepcopy(self.net_argc)
        self.node_phy_spe = net_argc["node_phy_spe"]
        self.seed = net_argc["seed"]
        np.random.seed(self.seed)
        random.seed(self.seed)
        listNodes = []
        listTargets = []
        for tmp in net_argc["nodes"]:
            listNodes.append(Node(location=tmp, phy_spe=copy.deepcopy(self.node_phy_spe)))
        
        target_id = -1 # khởi tạo id của target
        for target_location in self.net_argc["targets"]:
            target_id += 1
            listTargets.append(Target(location = target_location, id = target_id))

        baseStation = BaseStation(location=net_argc["base_station"])
        env = simpy.Environment()
        #net = Network(env, baseStation, listTargets, net_argc["max_time"],phy=copy.deepcopy(self.node_phy_spe)) 

        return env, Network(env, baseStation, listTargets, net_argc["max_time"],phy=copy.deepcopy(self.node_phy_spe)) 

