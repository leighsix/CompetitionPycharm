import random
import Setting_Simulation_Value
import Layer_A_Modeling
import Layer_B_Modeling
import networkx as nx


class DecisionDynamics:
    def __init__(self):
        self.B_COUNT = 0

    def B_layer_dynamics(self, layer_A, layer_B, beta):  # B_layer 다이내믹스, 베타 적용 및 언어데스 알고리즘 적용
        prob_beta_list = []
        for i in sorted(layer_B.G_B.nodes):
            opposite = []
            internal_edge_number = len(sorted(nx.all_neighbors(layer_B.B_edges, i)))
            external_edge_number = len(layer_A.AB_neighbor[i])
            for j in range(internal_edge_number):
                a = layer_B.G_B.nodes[i]['state']
                b = layer_B.G_B.nodes[sorted(nx.all_neighbors(layer_B.B_edges, i))[j]]['state']
                if a * b < 0:
                    opposite.append(1)
            for j in range(external_edge_number):
                a = layer_B.G_B.nodes[i]['state']
                b = layer_A.G_A.nodes[layer_A.AB_neighbor[i][j]]['state']
                if a * b < 0:
                    opposite.append(1)
            prob_beta = ((sum(opposite))/((external_edge_number)+(internal_edge_number)))**beta
            prob_beta_list.append(prob_beta)
            z = random.random()
            if z < prob_beta:
                layer_B.G_B.nodes[i]['state'] = -(layer_B.G_B.nodes[i]['state'])
                self.B_COUNT += 1
        prob_beta_mean = sum(prob_beta_list) / len(prob_beta_list)
        return layer_B, prob_beta_mean



if __name__ == "__main__" :
    print("DecisionDynamics")
    setting = Setting_Simulation_Value.Setting_Simulation_Value()
    Layer_A = Layer_A_Modeling.Layer_A_Modeling(setting)
    Layer_B = Layer_B_Modeling.Layer_B_Modeling(setting)
    state = 0
    for i in range(len(Layer_B.G_B.nodes)):
        state += Layer_B.G_B.nodes[i]['state']
    print(state)
    decision = DecisionDynamics()
    value = decision.B_layer_dynamics(Layer_A, Layer_B, 1.5)
    state = 0
    for i in range(len(Layer_B.G_B.nodes)):
        state += Layer_B.G_B.nodes[i]['state']
    print(state)


