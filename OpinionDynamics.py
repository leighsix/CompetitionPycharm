import random
import Setting_Simulation_Value
import InterconnectedLayerModeling
import time
import math
import networkx as nx
import numpy as np


class OpinionDynamics:
    def __init__(self):
        self.A_COUNT = 0

    def A_layer_dynamics(self, setting, inter_layer, gamma):  # A_layer 다이내믹스, 감마 적용 및 설득/타협 알고리즘 적용
        prob_p = gamma / (1+gamma)
        persuasion_count = 0
        compromise_count = 0
        total_edges_layer_A = len(sorted(inter_layer.A_edges.edges())) + len(sorted(inter_layer.AB_edges))
        for i, j in sorted(inter_layer.A_edges.edges()):
            a = inter_layer.two_layer_graph.nodes[i]['state']
            b = inter_layer.two_layer_graph.nodes[j]['state']
            if a * b > 0:
                z = random.random()
                if z < prob_p:
                    persuasion = self.A_layer_persuasion_function(setting, inter_layer.two_layer_graph.nodes[i],
                                                                  inter_layer.two_layer_graph.nodes[j])
                    inter_layer.two_layer_graph.nodes[i]['state'] = persuasion[0]
                    inter_layer.two_layer_graph.nodes[j]['state'] = persuasion[1]
                    persuasion_count += 1
            elif a * b < 0:
                z = random.random()
                if z < (1 - prob_p):
                    compromise = self.A_layer_compromise_function(setting, inter_layer.two_layer_graph.nodes[i],
                                                                  inter_layer.two_layer_graph.nodes[j], prob_p, z)
                    inter_layer.two_layer_graph.nodes[i]['state'] = compromise[0]
                    inter_layer.two_layer_graph.nodes[j]['state'] = compromise[1]
                    compromise_count += 1
        for i, j in sorted(inter_layer.AB_edges):
            a = inter_layer.two_layer_graph.nodes[j]['state']
            b = inter_layer.two_layer_graph.nodes[i]['state']
            if a * b > 0:
                z = random.random()
                if z < prob_p:
                    inter_layer.two_layer_graph.nodes[j]['state'] \
                        = self.AB_layer_persuasion_function(setting, inter_layer.two_layer_graph.nodes[j])
                    persuasion_count += 1
            elif a * b < 0:
                z = random.random()
                if z < (1 - prob_p):
                    inter_layer.two_layer_graph.nodes[j]['state'] \
                        = self.AB_layer_compromise_function(setting, inter_layer.two_layer_graph.nodes[j])
                    compromise_count += 1
        persuasion_prob = persuasion_count / total_edges_layer_A
        compromise_prob = compromise_count / total_edges_layer_A
        return inter_layer, persuasion_prob, compromise_prob


    def A_layer_persuasion_function(self, setting, a, b):  # A layer 중에서 same orientation 에서 일어나는  변동 현상
        if (a['state']) > 0 and (b['state']) > 0:
            a['state'] = self.A_layer_node_right(a, setting.MAX)
            b['state'] = self.A_layer_node_right(b, setting.MAX)
        elif (a['state']) < 0 and (b['state']) < 0:
            a['state'] = self.A_layer_node_left(a, setting.MIN)
            b['state'] = self.A_layer_node_left(b, setting.MIN)
        return a['state'], b['state']

    def A_layer_compromise_function(self, setting, a, b, prob_p, z):  # A layer  중에서 opposite orientation 에서 일어나는 변동 현상
        if (a['state']) * (b['state']) == -1:
            if z < ((1 - prob_p) / 2):
                (a['state']) = 1
                (b['state']) = 1
            elif z > ((1 - prob_p) / 2):
                a['state'] = -1
                b['state'] = -1
        elif (a['state']) > 0:
            a['state'] = self.A_layer_node_left(a, setting.MIN)
            b['state'] = self.A_layer_node_right(b, setting.MAX)
        elif (a['state']) < 0:
            a['state'] = self.A_layer_node_right(a, setting.MAX)
            b['state'] = self.A_layer_node_left(b, setting.MIN)
        return a['state'], b['state']

    def AB_layer_persuasion_function(self, setting, a):  # A-B layer 중에서 same orientation 에서 일어나는  변동 현상
        if (a['state']) > 0:
            a['state'] = self.A_layer_node_right(a, setting.MAX)
        elif (a['state']) < 0:
            a['state'] = self.A_layer_node_left(a, setting.MIN)
        return a['state']

    def AB_layer_compromise_function(self, setting, a):  # A-B layer  중에서 opposite orientation 에서 일어나는 변동 현상
        if (a['state']) > 0:
            a['state'] = self.A_layer_node_left(a, setting.MIN)
        elif (a['state']) < 0:
            a['state'] = self.A_layer_node_right(a, setting.MAX)
        return a['state']

    def A_layer_node_left(self, a, Min):
        if (a['state']) > Min:
            if (a['state']) < 0 or (a['state']) > 1:
                (a['state']) = (a['state']) - 1
                self.A_COUNT += 1
            elif (a['state']) == 1:
                a['state'] = -1
                self.A_COUNT += 1
        elif (a['state']) <= Min:
            (a['state']) = Min
        return a['state']

    def A_layer_node_right(self, a, Max):
        if (a['state']) < Max:
            if (a['state']) > 0 or (a['state']) < -1:
                a['state'] = (a['state']) + 1
                self.A_COUNT += 1
            elif (a['state']) == -1:
                a['state'] = 1
                self.A_COUNT += 1
        elif (a['state']) >= Max:
            a['state'] = Max
        return a['state']

    def A_state_change_probability_cal(self, inter_layer, gamma):
        prob_p = gamma / (1+gamma)
        prob_list = []
        prob_per_list = []
        prob_com_list = []
        for node_i in sorted(inter_layer.A_edges):
            neighbors = np.array(sorted(nx.neighbors(inter_layer.two_layer_graph, node_i)))
            neighbor_state = []
            for neighbor in neighbors:
                neighbor_state.append(inter_layer.two_layer_graph.nodes[neighbor]['state'])
            neighbor_array = np.array(neighbor_state)
            same_orientation = int(np.sum(neighbor_array * inter_layer.two_layer_graph.nodes[node_i]['state'] > 0))
            opposite_orientation = len(neighbors) - same_orientation
            node_unchanging_prob = 0
            node_persuasion_prob = 0
            node_compromise_prob = 0
            for n in range(0, same_orientation + 1):
                for m in range(0, opposite_orientation + 1):
                    n_combi = self.nCr(same_orientation, n)
                    m_combi = self.nCr(opposite_orientation, m)
                    if n == m:
                        node_unchanging_prob += prob_p ** (n + opposite_orientation - m) * (
                                    (1 - prob_p) ** (same_orientation - n + m)) * n_combi * m_combi
                    elif n > m:
                        node_persuasion_prob += prob_p ** (n + opposite_orientation - m) * (
                                    (1 - prob_p) ** (same_orientation - n + m)) * n_combi * m_combi
                    elif n < m:
                        node_compromise_prob += prob_p ** (n + opposite_orientation - m) * (
                                    (1 - prob_p) ** (same_orientation - n + m)) * n_combi * m_combi
            prob_list.append((node_unchanging_prob, node_unchanging_prob+node_persuasion_prob,
                              node_unchanging_prob+node_persuasion_prob+node_compromise_prob))
            prob_per_list.append(node_persuasion_prob)
            prob_com_list.append(node_compromise_prob)
        prob_array = np.array(prob_list)
        persuasion_prob = sum(prob_per_list) / len(sorted(inter_layer.A_edges))
        compromise_prob = sum(prob_com_list) / len(sorted(inter_layer.A_edges))
        return prob_array, persuasion_prob, compromise_prob

    def nCr(self, n, r):
        f = math.factorial
        return f(n) // f(r) // f(n - r)


if __name__ == "__main__":
    print("OpinionDynamics")
    setting = Setting_Simulation_Value.Setting_Simulation_Value()
    inter_layer = InterconnectedLayerModeling.InterconnectedLayerModeling(setting)
    state = 0
    for i in range(setting.A_node):
        state += inter_layer.two_layer_graph.nodes[i]['state']
    print(state)
    opinion = OpinionDynamics()
    start = time.time()
    prob = opinion.A_state_change_probability_cal(inter_layer, 0.3)
    print(prob[1], prob[2])
    opinion_result = opinion.A_layer_dynamics(setting, inter_layer, 0.3)
    print(opinion_result[1])
    print(opinion_result[2])
    state = 0
    for i in range(setting.A_node):
        state += inter_layer.two_layer_graph.nodes[i]['state']
    print(state)
    end = time.time()
    print(end - start)

