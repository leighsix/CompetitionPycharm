import numpy as np
import math


class Setting_Simulation_Value :
    def __init__(self):
        self.Structure = "RR-RR"
        self.A_state = [1, 2]
        self.A_node = 2048
        self.A_edge = 5
        self.MAX = 2
        self.MIN = -2
        self.A_network = 1
        self.B_state = [-1]
        self.B_node = 2048
        self.B_edge = 5
        self.B_inter_edges = 1
        self.A_inter_edges = 1
        self.B_network = 1        # network : 1 = random regular graph   2 = barabasi-albert graph
        self.gap = 30
        self.Repeating_number = 100
        self.Limited_step = 30
        self.R = self.simulation_condition(self.gap)[0]
        self.D = self.simulation_condition(self.gap)[1]
        self.variable_list = self.gamma_and_beta_list(self.R, self.D)
        self.NodeColorDict = {1: 'hotpink', 2: 'red', -1: 'skyblue', -2: 'blue'}
        self.EdgeColorDict = {1: 'yellow', 2: 'hotpink', 4: 'red',  -1: 'skyblue', -2: 'blue', -4 : 'darkblue'}
        self.database = 'renew_competition'   #'competition'
        self.drawing_graph = False
        self.workers = 4

    def simulation_condition(self, gap):
        self.R = np.linspace(1, 1.5, gap)
        self.D = np.linspace(self.making_beta_scale(gap)[0], self.making_beta_scale(gap)[1], gap)
        return self.R, self.D

    def gamma_and_beta_list(self, gamma_list, beta_list):
        variable_list = []
        for gamma in gamma_list:
            for beta in beta_list:
                variable_list.append((gamma, beta))
        return variable_list

    def making_beta_scale(self, a):
        scale = math.log((1 / (self.B_edge + 1)) ** 3)\
                / math.log(self.B_inter_edges / (self.B_edge + self.B_inter_edges))
        return 0, scale, a


if __name__ == "__main__":
    SS = Setting_Simulation_Value()
    print(SS.R)
    print(SS.D)
