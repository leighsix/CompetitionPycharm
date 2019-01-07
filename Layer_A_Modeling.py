import networkx as nx
import numpy as np
import random
import Setting_Simulation_Value


class Layer_A_Modeling:
    def __init__(self):
        # network : 1 = random regular graph   2 = barabasi-albert graph
        self.SS = Setting_Simulation_Value.Setting_Simulation_Value()
        self.A_state = self.SS.A_state     # state = [   ]  kinds of states
        self.A_node = self.SS.A_node
        self.A_edge = self.SS.A_edge
        self.MAX = self.SS.MAX
        self.MIN = self.SS.MIN
        self.network = self.SS.A_network
        self.A = self.A_layer_config()[0]
        self.A_edges = self.A_layer_config()[1]

    def A_layer_config(self):
        # A_layer 구성요소 A_layer_config(state = [1,2], node = 2048, edge = 5, Max = 2, Min = -2)
        self.select_layer_A_model(self.network)
        return self.A, self.A_edges
        # A : A의 각 노드의 상태, A_state : A 노드 상태의 종류(1, 2, -1, -2),
        # A_node : 노드의 수, A_edge : 내부연결선수, A_edges : 내부연결상태(튜플), MAX : 최대상태, MIN : 최소상태

    def select_layer_A_model(self, network):
        if network == 1:
            self.making_layer_A_random_regular()
        elif network == 2:
            self.making_layer_A_barabasi_albert()
        return self.A, self.A_edges


    def making_layer_A_random_regular(self):
        # A_layer random_regular network
        self.A = np.array(self.A_state * int(self.A_node / len(self.A_state)), int)
        random.shuffle(self.A)
        self.A_edges = nx.random_regular_graph(self.A_edge, self.A_node, seed=None)
        return self.A, self.A_edges


    def making_layer_A_barabasi_albert(self):
        # A_layer 바바라시-알버트 네트워크
        self.A = np.array(self.A_state * int(self.A_node / len(self.A_state)), int)
        random.shuffle(self.A)
        self.A_edges = nx.barabasi_albert_graph(self.A_node, self.A_edge, seed=None)
        return self.A, self.A_edges

if __name__ == "__main__" :
    layer_A = Layer_A_Modeling()
    print(layer_A.A)


