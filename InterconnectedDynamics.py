import numpy as np
import networkx as nx
import Setting_Simulation_Value
import OpinionDynamics
import DecisionDynamics
import MakingPandas
import Layer_A_Modeling
import Layer_B_Modeling
import matplotlib
import Interconnected_Layer_Modeling
from numba import jit
matplotlib.use("Agg")


class InterconnectedDynamics:
    def __init__(self):
        self.opinion = OpinionDynamics.OpinionDynamics()
        self.decision = DecisionDynamics.DecisionDynamics()
        self.mp = MakingPandas.MakingPandas()
        self.network = Interconnected_Layer_Modeling.Interconnected_Layer_Modeling()
        self.total_value = np.zeros(11)

    def interconnected_dynamics(self, setting, layer_A, layer_B, prob_p, beta):
        ims = []
        step_number = 0
        while True:
            time_count = self.opinion.A_COUNT + self.decision.B_COUNT
            if step_number == 0:
                if setting.drawing_graph == 1:
                    im = self.network.draw_interconnected_network(setting, layer_A, layer_B, 'result.png')[0]
                    ims.append(im)
                prob_beta_mean = self.calculate_initial_prob_beta_mean(setting, layer_A, layer_B, beta)
                layer_state_mean = self.mp.layer_state_mean(setting)
                different_state_ratio = self.mp.different_state_ratio(setting)
                initial_value = np.array([layer_state_mean[0], layer_state_mean[1],
                                          prob_p, prob_beta_mean, different_state_ratio[0],
                                          different_state_ratio[1], different_state_ratio[2],
                                          self.mp.judging_consensus(setting),
                                          self.mp.counting_negative_node(setting),
                                          self.mp.counting_positive_node(setting), time_count])
                self.total_value = initial_value
            setting = self.opinion.A_layer_dynamics(setting, layer_A, prob_p)
            decision = self.decision.B_layer_dynamics(setting, layer_A, layer_B, beta)
            setting = decision[0]
            prob_beta_mean = decision[1]
            if setting.drawing_graph == 1:
                im = self.network.draw_interconnected_network(setting, layer_A, layer_B, 'result.png')[0]
                ims.append(im)
                if (np.all(setting.A > 0) == 1 and np.all(setting.B > 0) == 1) or \
                        (np.all(setting.A < 0) == 1 and np.all(setting.B < 0) == 1):
                    print('Consensus')
                    break
            step_number += 1
            layer_state_mean = self.mp.layer_state_mean(setting)
            different_state_ratio = self.mp.different_state_ratio(setting)

            array_value = np.array([layer_state_mean[0], layer_state_mean[1],
                                    prob_p, prob_beta_mean, different_state_ratio[0],
                                    different_state_ratio[1], different_state_ratio[2],
                                    self.mp.judging_consensus(setting),
                                    self.mp.counting_negative_node(setting),
                                    self.mp.counting_positive_node(setting), time_count])
            if step_number >= 1:
                self.total_value = np.vstack([self.total_value, array_value])
            self.opinion.A_COUNT = 0
            self.decision.B_COUNT = 0
            if step_number >= setting.Limited_step:
                break
        ims = np.array(ims)
        if setting.drawing_graph == 1:
            self.network.making_movie_for_dynamics(ims)
        return layer_A, layer_B, self.total_value

    def calculate_initial_prob_beta_mean(self, setting, layer_A, layer_B, beta):
        prob_beta_list = []
        for i in sorted(layer_B.B_edges.nodes):
            opposite = []
            internal_edge_number = len(sorted(nx.all_neighbors(layer_B.B_edges, i)))
            external_edge_number = len(layer_A.AB_neighbor[i])
            for j in range(internal_edge_number):
                if (setting.B[i]) * (setting.B[sorted(nx.all_neighbors(layer_B.B_edges, i))[j]]) < 0:
                    opposite.append(1)
            for j in range(external_edge_number):
                if (setting.B[i]) * (setting.A[layer_A.AB_neighbor[i][j]]) < 0:
                    opposite.append(1)
            prob_beta = (sum(opposite) / (external_edge_number+internal_edge_number))**beta
            prob_beta_list.append(prob_beta)
        prob_beta_mean = sum(prob_beta_list) / setting.B_node
        return prob_beta_mean

if __name__ == "__main__":
    print("InterconnectedDynamics")
    setting = Setting_Simulation_Value.Setting_Simulation_Value()
    Layer_A = Layer_A_Modeling.Layer_A_Modeling(setting)
    Layer_B = Layer_B_Modeling.Layer_B_Modeling(setting)
    prob_p = 0.2
    beta = 10
    inter_dynamics = InterconnectedDynamics()
    prob_beta_mean = inter_dynamics.calculate_initial_prob_beta_mean(setting, Layer_A, Layer_B, beta)
    print(prob_beta_mean)
    inter_dynamics.interconnected_dynamics(setting, Layer_A, Layer_B, prob_p, beta)
    print(setting.A)
    print(setting.B)
    print(sum(setting.A)/2048, sum(setting.B)/256)








