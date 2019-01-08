import random
import Setting_Simulation_Value
import Layer_A_Modeling
import Layer_B_Modeling


class OpinionDynamics:
    def __init__(self):
        self.SS = Setting_Simulation_Value.Setting_Simulation_Value()

    def A_layer_dynamics(self, layer_A, layer_B, prob_p):  # A_layer 다이내믹스, 감마 적용 및 설득/타협 알고리즘 적용
        for i, j in sorted(layer_A.A_edges.edges()):
            if layer_A.A[i] * layer_A.A[j] > 0:
                layer_A.A[i] = self.A_layer_persuasion_function(layer_A.A[i], layer_A.A[j], prob_p)[0]
                layer_A.A[j] = self.A_layer_persuasion_function(layer_A.A[i], layer_A.A[j], prob_p)[1]
            elif layer_A.A[i] * layer_A.A[j] < 0:
                layer_A.A[i] = self.A_layer_compromise_function(layer_A.A[i], layer_A.A[j], prob_p)[0]
                layer_A.A[j] = self.A_layer_compromise_function(layer_A.A[i], layer_A.A[j], prob_p)[1]
        for i, j in sorted(layer_A.AB_edges):
            if layer_A.A[j] * layer_B.B[i] > 0:
                layer_A.A[j] = self.AB_layer_persuasion_function(layer_A.A[j], layer_B.B[i], prob_p)[0]
            elif layer_A.A[j] * layer_B.B[i] < 0:
                layer_A.A[j] = self.AB_layer_compromise_function(layer_A.A[j], layer_B.B[i], prob_p)[0]
        return layer_A, layer_B

    def A_layer_persuasion_function(self, a, b, prob_p):  # A layer 중에서 same orientation 에서 일어나는  변동 현상
        z = random.random()
        if z < prob_p:
            if a > 0:
                a = self.A_layer_node_right(a, self.SS.MAX)
                b = self.A_layer_node_right(b, self.SS.MAX)
            elif a < 0:
                a = self.A_layer_node_left(a, self.SS.MIN)
                b = self.A_layer_node_left(b, self.SS.MIN)
        elif z > prob_p:
            a = a
            b = b
        return a, b

    def A_layer_compromise_function(self, a, b, prob_p):  # A layer  중에서 opposite orientation 에서 일어나는 변동 현상
        z = random.random()
        if z < (1 - prob_p):
            if a * b == -1:
                if z < ((1 - prob_p) / 2):
                    a = 1
                    b = 1
                elif z > ((1 - prob_p) / 2):
                    a = -1
                    b = -1
            elif a > b:
                a = self.A_layer_node_left(a, self.SS.MIN)
                b = self.A_layer_node_right(b, self.SS.MAX)
            elif a < b:
                a = self.A_layer_node_right(a, self.SS.MAX)
                b = self.A_layer_node_left(b, self.SS.MIN)
        elif z > (1 - prob_p):
            a = a
            b = b
        return a, b

    def AB_layer_persuasion_function(self, a, b, prob_p):  # A-B layer 중에서 same orientation 에서 일어나는  변동 현상
        z = random.random()
        if z < prob_p:
            if a > 0:
                a = self.A_layer_node_right(a, self.SS.MAX)
                b = b
            elif a < 0:
                a = self.A_layer_node_left(a, self.SS.MIN)
                b = b
        elif z > prob_p:
            a = a
            b = b
        return a, b

    def AB_layer_compromise_function(self, a, b, prob_p):  # A-B layer  중에서 opposite orientation 에서 일어나는 변동 현상
        z = random.random()
        if z < (1 - prob_p):
            if a * b == -1:
                if z < ((1 - prob_p) / 2):
                    a = 1
                    b = b
                elif z > ((1 - prob_p) / 2):
                    a = -1
                    b = b
            elif a > b:
                a = self.A_layer_node_left(a, self.SS.MIN)
                b = b
            elif a < b:
                a = self.A_layer_node_right(a, self.SS.MAX)
                b = b
        elif z > (1 - prob_p):
            a = a
            b = b
        return a, b

    def A_layer_node_left(self, a, Min):
        if a >= Min:
            if a == Min:
                a = a
            elif a < 0 or a > 1:
                a = a - 1
            elif a == 1:
                a = -1
        elif a < Min:
            a = Min
        return a

    def A_layer_node_right(self, a, Max):
        if a <= Max:
            if a == Max:
                a = a
            elif a > 0 or a < -1:
                a = a + 1
            elif a == -1:
                a = 1
        elif a > Max:
            a = Max
        return a

if __name__ == "__main__":
    print("OpinionDynamics")
    Layer_A = Layer_A_Modeling.Layer_A_Modeling()
    Layer_B = Layer_B_Modeling.Layer_B_Modeling()
    opinion = OpinionDynamics()
    opinion.A_layer_dynamics(Layer_A, Layer_B, 1)
    print(Layer_A.A, Layer_B.B)
