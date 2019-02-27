import numpy as np
import networkx as nx
import Setting_Revised_Value
import RevisedOpinionDynamics
import RevisedDecisionDynamics
import MakingPandas
import Revised_Interconnected_Layer_Modeling
import Layer_A_Modeling
import Layer_B_Modeling
import matplotlib
matplotlib.use("Agg")


class RevisedInterconnectedDynamics:
    def __init__(self):
        self.revised_opinion = RevisedOpinionDynamics.RevisedOpinionDynamics()
        self.revised_decision = RevisedDecisionDynamics.RevisedDecisionDynamics()
        self.mp = MakingPandas.MakingPandas()
        self.revised_network = Revised_Interconnected_Layer_Modeling.Revised_Interconnected_Layer_Modeling()
        self.total_value = np.zeros(11)

    def revised_interconnected_dynamics(self, setting, layer_A, layer_B, beta):
        ims = []
        step_number = 0
        while True:
            time_count = self.revised_opinion.A_COUNT + self.revised_decision.B_COUNT
            if step_number == 0:
                prob_beta_mean = self.calculate_initial_prob_beta_mean(setting, layer_A, layer_B, beta)
                prob_p_mean = self.calculate_initial_prob_p_mean(setting, layer_A, layer_B, beta)
                initial_value = np.array([self.mp.layer_state_mean(setting, layer_A, layer_B)[0],
                                          self.mp.layer_state_mean(setting, layer_A, layer_B)[1],
                                          prob_p_mean, prob_beta_mean,
                                          self.mp.different_state_ratio(setting, layer_A, layer_B)[0],
                                          self.mp.different_state_ratio(setting, layer_A, layer_B)[1],
                                          self.mp.different_state_ratio(setting, layer_A, layer_B)[2],
                                          self.mp.judging_consensus(layer_A, layer_B),
                                          self.mp.counting_negative_node(layer_A, layer_B),
                                          self.mp.counting_positive_node(layer_A, layer_B), time_count])
                self.total_value = initial_value
            layer_A = self.revised_opinion.A_layer_dynamics(setting, layer_A, layer_B, beta)[0]
            layer_B = self.revised_opinion.A_layer_dynamics(setting, layer_A, layer_B, beta)[1]
            prob_p_mean = self.revised_opinion.A_layer_dynamics(setting, layer_A, layer_B, beta)[2]
            layer_A = self.revised_decision.B_layer_dynamics(layer_A, layer_B, beta)[0]
            layer_B = self.revised_decision.B_layer_dynamics(layer_A, layer_B, beta)[1]
            prob_beta_mean = self.revised_decision.B_layer_dynamics(layer_A, layer_B, beta)[2]
            if setting.drawing_graph == 1:
                im = self.revised_network.draw_interconnected_network(layer_A, layer_B, 'result.png')[0]
                ims.append(im)
                if (np.all(layer_A.A > 0) == 1 and np.all(layer_B.B > 0) == 1) or \
                        (np.all(layer_A.A < 0) == 1 and np.all(layer_B.B < 0) == 1):
                    print('Consensus')
                    break
            step_number += 1
            array_value = np.array([self.mp.layer_state_mean(setting, layer_A, layer_B)[0],
                                    self.mp.layer_state_mean(setting, layer_A, layer_B)[1],
                                    prob_p_mean, prob_beta_mean,
                                    self.mp.different_state_ratio(setting, layer_A, layer_B)[0],
                                    self.mp.different_state_ratio(setting, layer_A, layer_B)[1],
                                    self.mp.different_state_ratio(setting, layer_A, layer_B)[2],
                                    self.mp.judging_consensus(layer_A, layer_B),
                                    self.mp.counting_negative_node(layer_A, layer_B),
                                    self.mp.counting_positive_node(layer_A, layer_B), time_count])
            if step_number >= 1:
                self.total_value = np.vstack([self.total_value, array_value])
            self.revised_opinion.A_COUNT = 0
            self.revised_decision.B_COUNT = 0
            if step_number >= setting.Limited_step:
                break
        ims = np.array(ims)
        if setting.drawing_graph == 1:
            self.revised_network.making_movie_for_dynamics(ims, beta)
        return layer_A, layer_B, self.total_value

    def calculate_initial_prob_beta_mean(self, setting, layer_A, layer_B, beta):
        prob_beta_list = []
        for i in sorted(layer_B.B_edges.nodes):
            opposite = []
            internal_edge_number = len(sorted(nx.all_neighbors(layer_B.B_edges, i)))
            external_edge_number = len(layer_A.AB_neighbor[i])
            for j in range(internal_edge_number):
                if (layer_B.B[i]) * (layer_B.B[sorted(nx.all_neighbors(layer_B.B_edges, i))[j]]) < 0:
                    opposite.append(1)
            for j in range(external_edge_number):
                if (layer_B.B[i]) * (layer_A.A[layer_A.AB_neighbor[i][j]]) < 0:
                    opposite.append(1)
            prob_beta = (sum(opposite) / (external_edge_number+internal_edge_number))**beta
            prob_beta_list.append(prob_beta)
        prob_beta_mean = sum(prob_beta_list) / setting.B_node
        return prob_beta_mean

    def calculate_initial_prob_p_mean(self, setting, layer_A, layer_B, beta):
        prob_p_list = []
        for i in sorted(layer_A.A_edges.nodes):
            opposite = []
            internal_edge_number = len(sorted(nx.all_neighbors(layer_A.A_edges, i)))
            external_edge_number = 1
            for j in range(internal_edge_number):
                if (layer_A.A[i]) * (layer_A.A[sorted(nx.all_neighbors(layer_A.A_edges, i))[j]]) < 0:
                    opposite.append(1)
            for j in range(external_edge_number):
                if (layer_B.B[i]) * (layer_A.A[layer_A.AB_neighbor[i][j]]) < 0:
                    opposite.append(1)
            prob_q = (sum(opposite) / (external_edge_number+internal_edge_number))**beta
            prob_p = 1 - prob_q
            prob_p_list.append(prob_p)
        prob_p_mean = sum(prob_p_list) / setting.A_node
        return prob_p_mean

if __name__ == "__main__":
    print("InterconnectedDynamics")
    setting = Setting_Revised_Value.Setting_Revised_Value()
    Layer_A = Layer_A_Modeling.Layer_A_Modeling(setting)
    Layer_B = Layer_B_Modeling.Layer_B_Modeling(setting)
    beta = 0.5
    revised_inter_dynamics = RevisedInterconnectedDynamics()
    prob_beta_mean = revised_inter_dynamics.calculate_initial_prob_beta_mean(setting, Layer_A, Layer_B, beta)
    print(prob_beta_mean)
    array_list = revised_inter_dynamics.revised_interconnected_dynamics(setting, Layer_A, Layer_B, beta)
    print(Layer_A.A)
    print(array_list)
    print(len(array_list))
    print(sum(Layer_A.A)/2048, sum(Layer_B.B)/2048)
    print("Operating finished")








