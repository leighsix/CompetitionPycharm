import random
import Setting_Simulation_Value
import Layer_A_Modeling
import Layer_B_Modeling


class OpinionDynamics:
    def __init__(self):
        self.A_COUNT = 0

    def A_layer_dynamics(self, setting, layer_A, prob_p):  # A_layer 다이내믹스, 감마 적용 및 설득/타협 알고리즘 적용
        for i, j in sorted(layer_A.A_edges.edges()):
            if setting.A[i] * setting.A[j] > 0:
                setting.A[i] = self.A_layer_persuasion_function(setting, setting.A[i], setting.A[j], prob_p)[0]
                setting.A[j] = self.A_layer_persuasion_function(setting, setting.A[i], setting.A[j], prob_p)[1]
            elif setting.A[i] * setting.A[j] < 0:
                setting.A[i] = self.A_layer_compromise_function(setting, setting.A[i], setting.A[j], prob_p)[0]
                setting.A[j] = self.A_layer_compromise_function(setting, setting.A[i], setting.A[j], prob_p)[1]
        for i, j in sorted(layer_A.AB_edges):
            if setting.A[j] * setting.B[i] > 0:
                setting.A[j] = self.AB_layer_persuasion_function(setting, setting.A[j], prob_p)
            elif setting.A[j] * setting.B[i] < 0:
                setting.A[j] = self.AB_layer_compromise_function(setting, setting.A[j], setting.B[i], prob_p)
        return setting


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


if __name__ == "__main__":
    print("OpinionDynamics")
    setting = Setting_Simulation_Value.Setting_Simulation_Value()
    Layer_A = Layer_A_Modeling.Layer_A_Modeling(setting)
    Layer_B = Layer_B_Modeling.Layer_B_Modeling(setting)
    opinion = OpinionDynamics()
    opinion.A_layer_dynamics(setting, Layer_A, 1)
    print(setting.A, setting.B)
