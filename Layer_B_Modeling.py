import networkx as nx
import numpy as np
import random

class Layer_B_Modeling():
    def __init__(self, state=[], node=0, edge=0, inter_edges=0, network=0):
        # network : 1 = random regular graph   2 = barabasi-albert graph
        self.B_state = state    # state = [   ]  kinds of states
        self.B_node = node
        self.B_edge = edge
        self.inter_edges = inter_edges
        self.network = network
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
    Layer_B = Layer_B_Modeling([-1, 1], 2048, 5, 1, 1)
    print(Layer_B.B)
