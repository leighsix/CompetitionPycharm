import numpy as np
import math
import random


class Setting_Simulation_Value:
    def __init__(self):
        self.database = 'paper_revised_data'  # 'competition  renew_competition'
        self.table = 'simulation_table'
        self.MODEL = 'LM(8)'
        self.Structure = 'BA-BA'

        self.Limited_step = 100
        self.Repeating_number = 10

        self.A_state = [1, 2]
        self.A_node = 2048
        self.A_edge = 5
        self.A_inter_edges = 1
        self.A = self.static_making_A_array()
        self.MAX = 2
        self.MIN = -2

        self.B_state = [-1]
        self.B_node = 256
        self.B_edge = 5
        self.B_inter_edges = int(self.A_node / self.B_node)
        self.B = self.static_making_B_array()

        self.drawing_graph = False
        self.DB = 'MySQL'
        self.gap = 40
        simulation_condition = self.simulation_condition(self.gap)
        self.R = simulation_condition[0]
        self.D = simulation_condition[1]
        self.variable_list = self.gamma_and_beta_list(self.R, self.D)
        self.NodeColorDict = {1: 'hotpink', 2: 'red', -1: 'skyblue', -2: 'blue'}
        self.EdgeColorDict = {1: 'green', 2: 'hotpink', 4: 'red',  -1: 'skyblue', -2: 'blue', -4 : 'darkblue'}
        self.workers = 5

    def simulation_condition(self, gap):
        self.R = np.linspace(0, 2, gap)
        self.D = np.linspace(self.making_beta_scale(gap)[0], self.making_beta_scale(gap)[1], gap)
        return self.R, self.D

    def gamma_and_beta_list(self, gamma_list, beta_list):
        self.variable_list = []
        for gamma in gamma_list:
            for beta in beta_list:
                self.variable_list.append((gamma, beta))
        return self.variable_list

    def making_beta_scale(self, a):
        scale = math.log((1 / (self.B_edge + 1)) ** 3)\
                / math.log(self.B_inter_edges / (self.B_edge + self.B_inter_edges))
        return 0, scale, a

    def static_making_A_array(self):
        values = self.A_state * int(self.A_node / len(self.A_state))
        self.A = np.array(values)
        random.shuffle(self.A)
        return self.A

    def static_making_B_array(self):
        values = self.B_state * int(self.B_node / len(self.B_state))
        self.B = np.array(values)
        random.shuffle(self.B)
        return self.B

if __name__ == "__main__":
    SS = Setting_Simulation_Value()
    #layer_A1 = Layer_A_Modeling.Layer_A_Modeling(SS)
    print(SS.A_node)
    #print(len(layer_A1.A))
    #layer_A2 = Layer_A_Modeling.Layer_A_Modeling(SS)
    print(SS.B_node)
    print(SS.A)
    print(SS.variable_list)
    #print(len(layer_A2.A))
