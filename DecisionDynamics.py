import random
import Setting_Simulation_Value
import networkx as nx
import Layer_A_Modeling
import Layer_B_Modeling


class DecisionDynamics:
    def __init__(self):
        self.SS = Setting_Simulation_Value.Setting_Simulation_Value()

    def B_layer_dynamics(self, layer_A, layer_B, beta):  # B_layer 다이내믹스, 베타 적용 및 언어데스 알고리즘 적용
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
            prob_beta = (sum(opposite) / ((external_edge_number)+(internal_edge_number)))**beta
            z = random.random()
            if z < prob_beta:
                layer_B.B[i] = -(layer_B.B[i])
        return layer_A, layer_B

if __name__ == "__main__" :
    print("DecisionDynamics")
    Layer_A = Layer_A_Modeling.Layer_A_Modeling()
    Layer_B = Layer_B_Modeling.Layer_B_Modeling()
    decision = DecisionDynamics()
    decision.B_layer_dynamics(Layer_A, Layer_B, 1.5)
    print(sum(Layer_A.A)/2048, sum(Layer_B.B)/2048)

