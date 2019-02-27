import random
import networkx as nx
import Layer_A_Modeling
import Layer_B_Modeling
import Setting_Revised_Value


class RevisedOpinionDynamics:
    def __init__(self):
        self.A_COUNT = 0

    def A_layer_dynamics(self, setting, layer_A, layer_B, beta):  # A_layer 다이내믹스, 감마 적용 및 설득/타협 알고리즘 적용
        prob_p_list = []
        for i, j in sorted(layer_A.A_edges.edges()):
            if layer_A.A[i] * layer_A.A[j] > 0:
                prob_p = RevisedOpinionDynamics.calculate_prob_p(layer_A, layer_B, beta, i)
                layer_A.A[i] = self.A_layer_persuasion_function(setting, layer_A.A[i], layer_A.A[j], prob_p)[0]
                prob_p_list.append(prob_p)
                prob_p = RevisedOpinionDynamics.calculate_prob_p(layer_A, layer_B, beta, j)
                layer_A.A[j] = self.A_layer_persuasion_function(setting, layer_A.A[i], layer_A.A[j], prob_p)[1]
                prob_p_list.append(prob_p)
            elif layer_A.A[i] * layer_A.A[j] < 0:
                prob_p = RevisedOpinionDynamics.calculate_prob_p(layer_A, layer_B, beta, i)
                layer_A.A[i] = self.A_layer_compromise_function(setting, layer_A.A[i], layer_A.A[j], prob_p)[0]
                prob_p_list.append(prob_p)
                prob_p = RevisedOpinionDynamics.calculate_prob_p(layer_A, layer_B, beta, j)
                layer_A.A[j] = self.A_layer_compromise_function(setting, layer_A.A[i], layer_A.A[j], prob_p)[1]
                prob_p_list.append(prob_p)
        for i, j in sorted(layer_A.AB_edges):
            if layer_A.A[j] * layer_B.B[i] > 0:
                prob_p = RevisedOpinionDynamics.calculate_prob_p(layer_A, layer_B, beta, j)
                layer_A.A[j] = self.AB_layer_persuasion_function(setting, layer_A.A[j], prob_p)
                prob_p_list.append(prob_p)
            elif layer_A.A[j] * layer_B.B[i] < 0:
                prob_p = RevisedOpinionDynamics.calculate_prob_p(layer_A, layer_B, beta, j)
                layer_A.A[j] = self.AB_layer_compromise_function(setting, layer_A.A[j], layer_B.B[i], prob_p)
                prob_p_list.append(prob_p)
        prob_p_mean = sum(prob_p_list) / len(prob_p_list)
        return layer_A, layer_B, prob_p_mean

    def A_layer_persuasion_function(self, setting, a, b, prob_p):  # A layer 중에서 same orientation 에서 일어나는  변동 현상
        z = random.random()
        if z < prob_p:
            if a > 0 and b > 0:
                a = self.A_layer_node_right(a, setting.MAX)
                b = self.A_layer_node_right(b, setting.MAX)
            elif a < 0 and b < 0:
                a = self.A_layer_node_left(a, setting.MIN)
                b = self.A_layer_node_left(b, setting.MIN)
        return a, b

    def A_layer_compromise_function(self, setting, a, b, prob_p):  # A layer  중에서 opposite orientation 에서 일어나는 변동 현상
        z = random.random()
        if z < (1 - prob_p):
            if a * b == -1:
                if z < ((1 - prob_p) / 2):
                    a = 1
                    b = 1
                elif z > ((1 - prob_p) / 2):
                    a = -1
                    b = -1
            elif a > 0:
                a = self.A_layer_node_left(a, setting.MIN)
                b = self.A_layer_node_right(b, setting.MAX)
            elif a < 0:
                a = self.A_layer_node_right(a, setting.MAX)
                b = self.A_layer_node_left(b, setting.MIN)
        return a, b

    def AB_layer_persuasion_function(self, setting, a, prob_p):  # A-B layer 중에서 same orientation 에서 일어나는  변동 현상
        z = random.random()
        if z < prob_p:
            if a > 0:
                a = self.A_layer_node_right(a, setting.MAX)
            elif a < 0:
                a = self.A_layer_node_left(a, setting.MIN)
        return a

    def AB_layer_compromise_function(self, setting, a, b, prob_p):  # A-B layer  중에서 opposite orientation 에서 일어나는 변동 현상
        z = random.random()
        if z < (1 - prob_p):
            if a * b == -1:
                if z < ((1 - prob_p) / 2):
                    a = 1
                elif z > ((1 - prob_p) / 2):
                    a = -1
            elif a > 0:
                a = self.A_layer_node_left(a, setting.MIN)
            elif a < 0:
                a = self.A_layer_node_right(a, setting.MAX)
        elif z > (1 - prob_p):
            a = a
        return a

    def A_layer_node_left(self, a, Min):
        if a > Min:
            if a < 0 or a > 1:
                a = a - 1
                self.A_COUNT += 1
            elif a == 1:
                a = -1
                self.A_COUNT += 1
        elif a <= Min:
            a = Min
        return a

    def A_layer_node_right(self, a, Max):
        if a < Max:
            if a > 0 or a < -1:
                a = a + 1
                self.A_COUNT += 1
            elif a == -1:
                a = 1
                self.A_COUNT += 1
        elif a >= Max:
            a = Max
        return a

    @staticmethod
    def calculate_prob_p(layer_A, layer_B, beta, i):
        opposite = []
        internal_edge_number = len(sorted(nx.all_neighbors(layer_A.A_edges, i)))
        external_edge_number = 1
        for j in range(internal_edge_number):
            if (layer_A.A[i]) * (layer_A.A[sorted(nx.all_neighbors(layer_A.A_edges, i))[j]]) < 0:
                opposite.append(1)
        if (layer_A.A[i]) * (layer_B.B[layer_A.AB_edges_reverse[i][1]]) < 0:
            opposite.append(1)
        prob_q = (sum(opposite) / (external_edge_number+internal_edge_number))**beta
        prob_p = 1 - prob_q
        return prob_p


if __name__ == "__main__":
    print("RevisedOpinionDynamics")
    setting = Setting_Revised_Value.Setting_Revised_Value()
    Layer_A = Layer_A_Modeling.Layer_A_Modeling(setting)
    Layer_B = Layer_B_Modeling.Layer_B_Modeling(setting)
    print(Layer_A.A, Layer_B.B)
    revised_opinion = RevisedOpinionDynamics()
    revised_opinion.A_layer_dynamics(setting, Layer_A, Layer_B, 1)
    print(Layer_A.A, Layer_B.B)
    print(revised_opinion.A_layer_dynamics(setting, Layer_A, Layer_B, 1)[2])
