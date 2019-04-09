import numpy as np
import networkx as nx
import Setting_Simulation_Value
import KFOpinionDynamics
import KFDecisionDynamics
import MakingPandas
import InterconnectedLayerModeling
import matplotlib
import Interconnected_Network_Visualization
matplotlib.use("Agg")


class KFInterconnectedDynamics:
    def __init__(self):
        self.kfopinion = KFOpinionDynamics.KFOpinionDynamics()
        self.kfdecision = KFDecisionDynamics.KFDecisionDynamics()
        self.mp = MakingPandas.MakingPandas()
        self.network = Interconnected_Network_Visualization.Interconnected_Network_Visualization()
        self.total_value = np.zeros(15)

    def interconnected_dynamics(self, setting, inter_layer, prob_p, beta, node_i_name):
        ims = []
        step_number = 0
        while True:
            time_count = self.kfopinion.A_COUNT + self.kfdecision.B_COUNT
            if step_number == 0:
                if setting.drawing_graph == 1:
                    im = self.network.draw_interconnected_network(setting, inter_layer, 'result.png')[0]
                    ims.append(im)
                prob_beta_mean = self.calculate_initial_prob_beta_mean(setting, inter_layer, beta)
                layer_state_mean = self.mp.layer_state_mean(setting, inter_layer)
                different_state_ratio = self.mp.different_state_ratio(setting, inter_layer)
                fraction_plus = self.mp.calculate_fraction_plus(setting, inter_layer)
                initial_value = np.array([layer_state_mean[0], layer_state_mean[1],
                                          fraction_plus[0], fraction_plus[1],
                                          prob_p, prob_beta_mean, different_state_ratio[0],
                                          different_state_ratio[1], different_state_ratio[2],
                                          len(sorted(inter_layer.A_edges.edges)), len(inter_layer.B_edges),
                                          self.mp.judging_consensus(setting, inter_layer),
                                          self.mp.counting_negative_node(setting, inter_layer),
                                          self.mp.counting_positive_node(setting, inter_layer), time_count])
                self.total_value = initial_value
            inter_layer = self.kfopinion.A_layer_dynamics(setting, inter_layer, prob_p, node_i_name)
            decision = self.kfdecision.B_layer_dynamics(setting, inter_layer, beta, node_i_name)
            inter_layer = decision[0]
            prob_beta_mean = decision[1]
            if setting.drawing_graph == 1:
                im = self.network.draw_interconnected_network(setting, inter_layer, 'result.png')[0]
                ims.append(im)
                judge_A = []
                judge_B = []
                for i in range(setting.A_node):
                    judge_A.append(inter_layer.two_layer_graph.nodes[i]['state'])
                for i in range(setting.A_node, setting.A_node + setting.B_node):
                    judge_B.append(inter_layer.two_layer_graph.nodes[i]['state'])
                judge_A = np.array(judge_A)
                judge_B = np.array(judge_B)
                if (np.all(judge_A > 0) == 1 and np.all(judge_B > 0) == 1) or \
                        (np.all(judge_A < 0) == 1 and np.all(judge_B < 0) == 1):
                    print('Consensus')
                    break
            step_number += 1
            layer_state_mean = self.mp.layer_state_mean(setting, inter_layer)
            different_state_ratio = self.mp.different_state_ratio(setting, inter_layer)
            fraction_plus = self.mp.calculate_fraction_plus(setting, inter_layer)
            array_value = np.array([layer_state_mean[0], layer_state_mean[1],
                                    fraction_plus[0], fraction_plus[1],
                                    prob_p, prob_beta_mean, different_state_ratio[0],
                                    different_state_ratio[1], different_state_ratio[2],
                                    len(sorted(inter_layer.A_edges.edges)), len(inter_layer.B_edges),
                                    self.mp.judging_consensus(setting, inter_layer),
                                    self.mp.counting_negative_node(setting, inter_layer),
                                    self.mp.counting_positive_node(setting, inter_layer), time_count])
            if step_number >= 1:
                self.total_value = np.vstack([self.total_value, array_value])
            self.kfopinion.A_COUNT = 0
            self.kfdecision.B_COUNT = 0
            if step_number >= setting.Limited_step:
                break
        ims = np.array(ims)
        if setting.drawing_graph == 1:
            self.network.making_movie_for_dynamics(ims)
        return inter_layer, self.total_value

    def calculate_initial_prob_beta_mean(self, setting, inter_layer, beta):
        prob_beta_list = []
        for i in range(setting.B_node):
            opposite = []
            external_edge_number = len(inter_layer.AB_neighbor[i])
            internal_edge_number \
                = len(sorted(nx.all_neighbors(inter_layer.two_layer_graph, i+setting.A_node))) - external_edge_number
            for j in range(internal_edge_number):
                a = inter_layer.two_layer_graph.nodes[i + setting.A_node]['state']
                b = inter_layer.two_layer_graph.nodes[sorted(nx.all_neighbors(inter_layer.two_layer_graph, i+setting.A_node), reverse=True)[j]]['state']
                if a * b < 0:
                    opposite.append(1)
            for j in range(external_edge_number):
                a = inter_layer.two_layer_graph.nodes[i + setting.A_node]['state']
                b = inter_layer.two_layer_graph.nodes[sorted(nx.all_neighbors(inter_layer.two_layer_graph, i+setting.A_node), reverse=False)[j]]['state']
                if a * b < 0:
                    opposite.append(1)
            prob_beta = ((sum(opposite))/((external_edge_number)+(internal_edge_number)))**beta
            prob_beta_list.append(prob_beta)
        prob_beta_mean = sum(prob_beta_list) / setting.B_node
        return prob_beta_mean

if __name__ == "__main__":
    print("InterconnectedDynamics")
    setting = Setting_Simulation_Value.Setting_Simulation_Value()
    inter_layer = InterconnectedLayerModeling.InterconnectedLayerModeling(setting)
    prob_p = 0.3
    beta = 10
    state = 0
    for i in range(setting.A_node):
        state += inter_layer.two_layer_graph.nodes[i]['state']
    print(state)
    state = 0
    for i in range(setting.A_node, setting.A_node + setting.B_node):
        state += inter_layer.two_layer_graph.nodes[i]['state']
    print(state)
    inter_dynamics = KFInterconnectedDynamics()
    prob_beta_mean = inter_dynamics.calculate_initial_prob_beta_mean(setting, inter_layer, beta)
    print(prob_beta_mean)
    for i in range(10):
        inter_layer = inter_dynamics.interconnected_dynamics(setting, inter_layer, prob_p, beta, 'A_0')[0]
        print(inter_layer.two_layer_graph.node[0]['state'])
    state = 0
    for i in range(setting.A_node):
        state += inter_layer.two_layer_graph.nodes[i]['state']
    print(state)
    state = 0
    for i in range(setting.A_node, setting.A_node + setting.B_node):
        state += inter_layer.two_layer_graph.nodes[i]['state']
    print(state)











