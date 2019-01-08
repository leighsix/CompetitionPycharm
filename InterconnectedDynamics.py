import numpy as np
import networkx as nx
import Setting_Simulation_Value
import OpinionDynamics
import DecisionDynamics
import Layer_A_Modeling
import Layer_B_Modeling
import MakingDB


class InterconnectedDynamics:
    def __init__(self):
        self.SS = Setting_Simulation_Value.Setting_Simulation_Value()
        self.opinion = OpinionDynamics.OpinionDynamics()
        self.decision = DecisionDynamics.DecisionDynamics()
        self.making_db = MakingDB.MakingDB()

    def interconnected_dynamics(self, layer_A, layer_B, prob_p, beta):
        step_number = 0
        while True:
            self.opinion.A_layer_dynamics(layer_A, layer_B, prob_p)
            self.calculate_prob_beta_mean(layer_A, layer_B, beta)
            self.decision.B_layer_dynamics(layer_A, layer_B, beta)
            step_number += 1
            time_count = self.opinion.A_COUNT + self.decision.B_COUNT
            self.opinion.A_COUNT = 0
            self.decision.A_COUNT = 0
            gamma = prob_p/(1-prob_p)
            self.making_db.setting_value_saving(layer_A, layer_B, step_number, beta, gamma, prob_beta_mean, time_count)

            if (((np.all(layer_A.A > 0) == 1) and (np.all(layer_B.B > 0) == 1)) or
                    ((np.all(layer_A.A < 0) == 1) and (np.all(layer_B.B < 0) == 1)) or
                    (step_number >= self.SS.Limited_step)):
                break
        return layer_A, layer_B

    def calculate_prob_beta_mean(self, layer_A, layer_B, beta):
        global prob_beta_mean
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
        prob_beta_mean = sum(prob_beta_list) / self.SS.B_node
        return prob_beta_mean


if __name__ == "__main__" :
    print("InterconnectedDynamics")
    Layer_A = Layer_A_Modeling.Layer_A_Modeling()
    Layer_B = Layer_B_Modeling.Layer_B_Modeling()
    prob_p = 0.5
    beta = 1.5
    inter_dynamics = InterconnectedDynamics()
    inter_dynamics.interconnected_dynamics(Layer_A, Layer_B, prob_p, beta)
    print(sum(Layer_A.A)/2048, sum(Layer_B.B)/2048)








