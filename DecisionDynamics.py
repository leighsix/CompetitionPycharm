import random
import time
import numpy as np
import Setting_Simulation_Value
import InterconnectedLayerModeling
import networkx as nx

class DecisionDynamics:
    def __init__(self):
        self.B_COUNT = 0

    def B_layer_dynamics(self, setting, inter_layer, beta):  # B_layer 다이내믹스, 베타 적용 및 언어데스 알고리즘 적용
        prob_beta_list = []
        for node_i in range(setting.A_node, setting.A_node+setting.B_node):
            neighbors = np.array(sorted(nx.neighbors(inter_layer.two_layer_graph, node_i)))
            neighbor_state = []
            for neighbor in neighbors:
                neighbor_state.append(inter_layer.two_layer_graph.nodes[neighbor]['state'])
            neighbor_array = np.array(neighbor_state)
            same_orientation = int(np.sum(neighbor_array * inter_layer.two_layer_graph.nodes[node_i]['state'] > 0))
            opposite_orientation = len(neighbors) - same_orientation
            prob_beta = (opposite_orientation / len(neighbors)) ** beta
            z = random.random()
            if z < prob_beta:
                inter_layer.two_layer_graph.nodes[node_i]['state'] = \
                    -(inter_layer.two_layer_graph.nodes[node_i]['state'])
                self.B_COUNT += 1
            prob_beta_list.append(prob_beta)
        prob_beta_array = np.array(prob_beta_list)
        prob_beta_mean = np.sum(prob_beta_array) / len(prob_beta_array)
        return inter_layer, prob_beta_mean

    def B_state_change_probability_cal(self, setting, inter_layer, beta):
        prob_beta_list = []
        for node_i in range(setting.A_node, setting.A_node+setting.B_node):
            neighbors = np.array(sorted(nx.neighbors(inter_layer.two_layer_graph, node_i)))
            neighbor_state = []
            for neighbor in neighbors:
                neighbor_state.append(inter_layer.two_layer_graph.nodes[neighbor]['state'])
            neighbor_array = np.array(neighbor_state)
            same_orientation = int(np.sum(neighbor_array * inter_layer.two_layer_graph.nodes[node_i]['state'] > 0))
            opposite_orientation = len(neighbors) - same_orientation
            prob_beta = (opposite_orientation / len(neighbors)) ** beta
            prob_beta_list.append(prob_beta)
        prob_beta_array = np.array(prob_beta_list)
        prob_beta_mean = np.sum(prob_beta_array) / len(prob_beta_array)
        return prob_beta_array, prob_beta_mean


if __name__ == "__main__" :
    print("DecisionDynamics")
    setting = Setting_Simulation_Value.Setting_Simulation_Value()
    inter_layer = InterconnectedLayerModeling.InterconnectedLayerModeling(setting)
    state = 0
    for i in range(setting.A_node, setting.A_node+setting.B_node):
        state += inter_layer.two_layer_graph.nodes[i]['state']
    print(state)
    start = time.time()
    decision = DecisionDynamics()
    inter_layer = decision.B_layer_dynamics(setting, inter_layer, 1.5)[0]
    state = 0
    for i in range(setting.A_node, setting.A_node+setting.B_node):
        state += inter_layer.two_layer_graph.nodes[i]['state']
    print(state)
    end = time.time()
    print(end-start)



