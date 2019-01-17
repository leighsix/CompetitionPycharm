import numpy as np
import networkx as nx
import Setting_Simulation_Value
import OpinionDynamics
import DecisionDynamics
import MakingPandas
import Interconnected_Layer_Modeling
import Layer_A_Modeling
import Layer_B_Modeling


class InterconnectedDynamics:
    def __init__(self):
        self.SS = Setting_Simulation_Value.Setting_Simulation_Value()
        self.opinion = OpinionDynamics.OpinionDynamics()
        self.decision = DecisionDynamics.DecisionDynamics()
        self.mp = MakingPandas.MakingPandas()
        self.network = Interconnected_Layer_Modeling.Interconnected_Layer_Modeling()
        self.total_value = np.zeros(11)

    def interconnected_dynamics(self, layer_A, layer_B, prob_p, beta):
        step_number = 0
        ims = []
        while True:
            self.opinion.A_layer_dynamics(layer_A, layer_B, prob_p)
            self.calculate_prob_beta_mean(layer_A, layer_B, beta)
            self.decision.B_layer_dynamics(layer_A, layer_B, beta)
            if self.SS.drawing_graph == 0:
                im = self.network.draw_interconnected_network(layer_A, layer_B, 'result.png')
                ims.append([im])
                if (np.all(layer_A.A > 0) == 1 and np.all(layer_B.B > 0) == 1) or \
                        (np.all(layer_A.A < 0) == 1 and np.all(layer_B.B < 0) == 1):
                    print('Consensus :' + step_number+1)
                    break
            step_number += 1
            print(step_number)
            time_count = self.opinion.A_COUNT + self.decision.B_COUNT
            array_value = np.array([self.mp.layer_state_mean(layer_A, layer_B)[0],
                                    self.mp.layer_state_mean(layer_A, layer_B)[1], prob_p, prob_beta_mean,
                                    self.mp.different_state_ratio(layer_A, layer_B)[0],
                                    self.mp.different_state_ratio(layer_A, layer_B)[1],
                                    self.mp.different_state_ratio(layer_A, layer_B)[2],
                                    self.mp.judging_consensus(layer_A, layer_B),
                                    self.mp.counting_negative_node(layer_A, layer_B),
                                    self.mp.counting_positive_node(layer_A, layer_B), time_count])
            if step_number == 1:
                self.total_value = array_value
            elif step_number > 1:
                self.total_value = np.vstack([self.total_value, array_value])
            self.opinion.A_COUNT = 0
            self.decision.B_COUNT = 0
            if step_number >= self.SS.Limited_step:
                break
        self.network.making_movie_for_dynamics(ims)
        return layer_A, layer_B, self.total_value

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
    print("Operating finished")








