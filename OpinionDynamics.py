import random
import Modeling
import Setting_Simulation_Value
import Layer_A_Modeling
import Layer_B_Modeling


class OpinionDynamics:
    def __init__(self):
        self.SS = Setting_Simulation_Value.Setting_Simulation_Value()
        self.A = Layer_A_Modeling.Layer_A_Modeling()
        self.B = Layer_B_Modeling.Layer_B_Modeling()
        self.SS = Setting_Simulation_Value.Setting_Simulation_Value()
        self.M = Modeling.Modeling()
        self.A_layer_dynamics()

    def A_layer_dynamics(self):  # A_layer 다이내믹스, 감마 적용 및 설득/타협 알고리즘 적용
        for i, j in sorted(self.A.A_edges.edges()):
            if self.A.A[i] * self.A.A[j] > 0:
                self.A.A[i] = self.A_layer_persuasion_function(self.A.A[i], self.A.A[j])[0]
                self.A.A[j] = self.A_layer_persuasion_function(self.A.A[i], self.A.A[j])[1]
            elif self.A.A[i] * self.A.A[j] < 0:
                self.A.A[i] = self.A_layer_compromise_function(self.A.A[i], self.A.A[j])[0]
                self.A.A[j] = self.A_layer_compromise_function(self.A.A[i], self.A.A[j])[1]
        for i, j in sorted(self.M.AB_edges):
            if self.A.A[j] * self.B.B[i] > 0:
                self.A.A[j] = self.AB_layer_persuasion_function(self.A.A[j], self.B.B[i])[0]
                self.B.B[i] = self.AB_layer_persuasion_function(self.A.A[j], self.B.B[i])[1]
            elif self.A.A[j] * self.B.B[i] < 0:
                self.A.A[j] = self.AB_layer_compromise_function(self.A.A[j], self.B.B[i])[0]
                self.B.B[i] = self.AB_layer_compromise_function(self.A.A[j], self.B.B[i])[1]
        return self.A.A


    def A_layer_persuasion_function(self, a, b):  # A layer 중에서 same orientation 에서 일어나는  변동 현상
        z = random.random()
        if z < prob_p:
            if a > 0:
                a = A_layer_node_right(a, MAX)
                b = A_layer_node_right(b, MAX)
            elif a < 0:
                a = A_layer_node_left(a, MIN)
                b = A_layer_node_left(b, MIN)
        elif z > prob_p:
            a = a
            b = b
        return a, b

    def A_layer_compromise_function(self, a, b):  # A layer  중에서 opposite orientation 에서 일어나는 변동 현상
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
                a = A_layer_node_left(a, MIN)
                b = A_layer_node_right(b, MAX)
            elif a < b:
                a = A_layer_node_right(a, MAX)
                b = A_layer_node_left(b, MIN)
        elif z > (1 - prob_p):
            a = a
            b = b
        return a, b

    def AB_layer_persuasion_function(self, a, b):  # A-B layer 중에서 same orientation 에서 일어나는  변동 현상
        z = random.random()
        if z < prob_p:
            if a > 0:
                a = A_layer_node_right(a, MAX)
                b = b
            elif a < 0:
                a = A_layer_node_left(a, MIN)
                b = b
        elif z > prob_p:
            a = a
            b = b
        return a, b

    def AB_layer_compromise_function(self, a, b):  # A-B layer  중에서 opposite orientation 에서 일어나는 변동 현상
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
                a = A_layer_node_left(self, a, MIN)
                b = b
            elif a < b:
                a = A_layer_node_right(self, a, MAX)
                b = b
        elif z > (1 - prob_p):
            a = a
            b = b
        return a, b

    def A_layer_node_left(self, a, MIN):
        if a >= MIN:
            if a == MIN:
                a = a
            elif a < 0 or a > 1:
                a = a - 1
            elif a == 1:
                a = -1
        elif a < MIN:
            a = MIN
        return a

    def A_layer_node_right(self, a, MAX):
        if a <= MAX:
            if a == MAX:
                a = a
            elif a > 0 or a < -1:
                a = a + 1
            elif a == -1:
                a = 1
        elif a > MAX:
            a = MAX
        return a

if __name__ == "__main__":
    opinion_dynamics = OpinionDynamics()