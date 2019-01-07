import networkx as nx
import numpy as np
import random
import Setting_Simulation_Value


class Layer_B_Modeling:
    def __init__(self):
        # network : 1 = random regular graph   2 = barabasi-albert graph
        self.SS = Setting_Simulation_Value.Setting_Simulation_Value()
        self.B_state = self.SS.B_state    # state = [   ]  kinds of states
        self.B_node = self.SS.B_node
        self.B_edge = self.SS.B_edge
        self.inter_edges = self.SS.inter_edges
        self.network = self.SS.B_network
        self.B_layer_config()
        self.B = self.B_layer_config()[0]
        self.B_edges = self.B_layer_config()[1]

    def B_layer_config(self):  # B_layer 구성요소 B_layer_config(state = [-1], node = 2048, edge = 5, inter_edge= 1)
        self.select_layer_B_model(self.network)
        return B, B_edges

    def select_layer_B_model(self, network):
        if network == 1:
            self.making_layer_B_random_regular()
        elif network == 2:
            self.making_layer_B_barabasi_albert()
        return B, B_edges

    def making_layer_B_random_regular(self):  # B_layer random_regular network
        global B, B_edges
        B = np.array(self.B_state * int(self.B_node / len(self.B_state)), int)
        random.shuffle(B)
        B_edges = nx.random_regular_graph(self.B_edge, self.B_node, seed=None)
        return B, B_edges

    def making_layer_B_barabasi_albert(self):  # B_layer 바바라시-알버트 네트워크
        global B, B_edges
        B = np.array(self.B_state * int(self.B_node / len(self.B_state)), int)
        random.shuffle(B)
        B_edges = nx.barabasi_albert_graph(self.B_node, self.B_edge, seed=None)
        return B, B_edges

if __name__ == "__main__" :
    Layer_B = Layer_B_Modeling()
    print(Layer_B.B)