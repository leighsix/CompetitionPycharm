import numpy as np
import math
import random


class Setting_Simulation_Value():
    def __init__(self):
        self.database = 'finding_keynode'  # 'competition  renew_competition'
        self.table = 'keynode_table_for_100steps'
        self.MODEL = 'LM(8)'
        self.Structure = 'BA-BA'

        self.Limited_step = 100
        self.Repeating_number = 10

        self.A_state = [1, 2]
        self.A_node = 512
        self.A_edge = 5
        self.A_inter_edges = 1
        self.A_array_choice = 1
        self.MAX = 2
        self.MIN = -2

        self.B_state = [-1]
        self.B_node = 64
        self.B_edge = 5
        self.B_inter_edges = int(self.A_node / self.B_node)
        self.B_array_choice = 1

        A_array = self.making_A_array_choice(self.A_array_choice)
        self.A = A_array[0]
        self.average_initial_A = A_array[1]
        self.dev_A = A_array[2]
        self.positive_ratio_A = A_array[3]

        B_array = self.making_B_array_choice(self.B_array_choice)
        self.B = B_array[0]
        self.average_initial_B = B_array[1]
        self.dev_B = B_array[2]
        self.positive_ratio_B = B_array[3]


        self.drawing_graph = False
        self.DB = 'MySQL'
        self.gap = 30
        simulation_condition = self.simulation_condition(self.gap)
        self.R = simulation_condition[0]
        self.D = simulation_condition[1]
        self.variable_list = self.gamma_and_beta_list(self.R, self.D)
        self.NodeColorDict = {1: 'hotpink', 2: 'red', -1: 'skyblue', -2: 'blue'}
        self.EdgeColorDict = {1: 'green', 2: 'hotpink', 4: 'red',  -1: 'skyblue', -2: 'blue', -4 : 'darkblue'}
        self.workers = 4

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

    def making_A_array_choice(self, a):
        if a == 1:
            self.static_making_A_array()
        elif a == 2:
            self.random_making_A_array()
        return self.A, self.average_initial_A, self.dev_A, self.positive_ratio_A

    def static_making_A_array(self):
        values = self.A_state
        nodes = int(self.A_node / len(values))
        self.A = np.array(values * nodes)
        random.shuffle(self.A)
        self.average_initial_A = sum(self.A) / self.A_node
        self.dev_A = math.sqrt(Setting_Simulation_Value.cal_variance(self.A, self.average_initial_A))
        self.positive_ratio_A = sum(self.A > 0) / self.A_node
        return self.A, self.average_initial_A, self.dev_A, self.positive_ratio_A

    def random_making_A_array(self):
        values = self.A_state
        layer_A = []
        for i in range(self.A_node):
            v = random.choice(values)
            layer_A.append(v)
        self.A = np.array(layer_A, int)
        random.shuffle(self.A)
        self.average_initial_A = sum(self.A) / self.A_node
        self.dev_A = math.sqrt(Setting_Simulation_Value.cal_variance(self.A, self.average_initial_A))
        self.positive_ratio_A = sum(self.A > 0) / self.A_node
        return self.A, self.average_initial_A, self.dev_A, self.positive_ratio_A

    def making_B_array_choice(self, b):
        if b == 1:
            self.static_making_B_array()
        elif b == 2:
            self.random_making_B_array()
        return self.B, self.average_initial_B, self.dev_B, self.positive_ratio_B

    def static_making_B_array(self):
        values = self.B_state
        nodes = int(self.B_node / len(values))
        self.B = np.array(values * nodes)
        random.shuffle(self.B)
        self.average_initial_B = sum(self.B) / self.B_node
        self.dev_B = math.sqrt(Setting_Simulation_Value.cal_variance(self.B, self.average_initial_B))
        self.positive_ratio_B = sum(self.B > 0) / self.B_node
        return self.B, self.average_initial_B, self.dev_B, self.positive_ratio_B

    def random_making_B_array(self):
        values = self.B_state
        layer_B = []
        for i in range(self.B_node):
            v = random.choice(values)
            layer_B.append(v)
        self.B = np.array(layer_B, int)
        random.shuffle(self.B)
        self.average_initial_B = sum(self.B) / self.B_node
        self.dev_B = math.sqrt(Setting_Simulation_Value.cal_variance(self.B, self.average_initial_B))
        self.positive_ratio_B = sum(self.B > 0) / self.B_node
        return self.B, self.average_initial_B, self.dev_B, self.positive_ratio_B


    @staticmethod
    def cal_variance(layer, mean):
        vsum = 0
        for x in layer:
            vsum = vsum + (x - mean) ** 2
        var = vsum / len(layer)
        return var

if __name__ == "__main__":
    SS = Setting_Simulation_Value()
    #layer_A1 = Layer_A_Modeling.Layer_A_Modeling(SS)
    print(SS.A_node)
    #print(len(layer_A1.A))
    #layer_A2 = Layer_A_Modeling.Layer_A_Modeling(SS)
    print(SS.B_node)
    print(SS.A)
    print(SS.B)
    #print(len(layer_A2.A))
