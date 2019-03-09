import numpy as np
import math


class Setting_Revised_Value():
    def __init__(self):
        self.Structure = 'RR-RR'
        self.A_state = [2]
        self.A_node = 2048
        self.A_edge = 5
        self.MAX = 2
        self.MIN = -2
        self.B_state = [-1]
        self.B_node = 2048
        self.B_edge = 5
        self.B_inter_edges = 1
        self.A_inter_edges = 1
        self.Limited_step = 100
        self.drawing_graph = False
        self.database = 'renew_competition'  # 'competition  renew_competition'
        self.table = 'revised_initial_state'
        self.DB = 'MySQL'
        self.A_initial_state = sum(self.A_state) / len(self.A_state)
        self.B_initial_state = sum(self.B_state) / len(self.B_state)
        self.gap = 30
        self.Repeating_number = 100
        self.D = self.simulation_condition(self.gap)
        self.NodeColorDict = {1: 'hotpink', 2: 'red', -1: 'skyblue', -2: 'blue'}
        self.EdgeColorDict = {1: 'yellow', 2: 'hotpink', 4: 'red', -1: 'skyblue', -2: 'blue', -4: 'darkblue'}
        self.workers = 4


    def simulation_condition(self, gap):
        self.D = np.linspace(self.making_beta_scale(gap)[0], self.making_beta_scale(gap)[1], gap)
        return self.D


    def making_beta_scale(self, a):
        scale = math.log((1 / (self.B_edge + 1)) ** 3)\
                / math.log(self.B_inter_edges / (self.B_edge + self.B_inter_edges))
        return 0, scale, a


if __name__ == "__main__":
    SS = Setting_Revised_Value()
    #layer_A1 = Layer_A_Modeling.Layer_A_Modeling(SS)
    print(SS.A_node)
    #print(len(layer_A1.A))
    #layer_A2 = Layer_A_Modeling.Layer_A_Modeling(SS)
    print(SS.A_node)
    print(SS.D)
    #print(len(layer_A2.A))
