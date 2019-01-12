import networkx as nx
import numpy as np
import pandas as pd
import random
import Setting_Simulation_Value
## B layer : B, B_edges


class Layer_B_Modeling:
    def __init__(self):
        self.SS = Setting_Simulation_Value.Setting_Simulation_Value()
        self.B_layer_config()
        self.B = self.B_layer_config()[0]
        self.B_edges = self.B_layer_config()[1]
        self.B_node_info = self.making_node_info()
        self.layer_B_internal_edge_dic = self.making_layer_B_internal_edge()

    def B_layer_config(self):  # B_layer 구성요소 B_layer_config(state = [-1], node = 2048, edge = 5, inter_edge= 1)
        self.select_layer_B_model(self.SS.B_network)
        return B, B_edges

    def select_layer_B_model(self, network):
        if network == 1:
            self.making_layer_B_random_regular()
        elif network == 2:
            self.making_layer_B_barabasi_albert()
        return B, B_edges

    def making_layer_B_random_regular(self):  # B_layer random_regular network
        global B, B_edges
        B = np.array(self.SS.B_state * int(self.SS.B_node / len(self.SS.B_state)), int)
        random.shuffle(B)
        B_edges = nx.random_regular_graph(self.SS.B_edge, self.SS.B_node, seed=None)
        return B, B_edges

    def making_layer_B_barabasi_albert(self):  # B_layer 바바라시-알버트 네트워크
        global B, B_edges
        B = np.array(self.SS.B_state * int(self.SS.B_node / len(self.SS.B_state)), int)
        random.shuffle(B)
        B_edges = nx.barabasi_albert_graph(self.SS.B_node, self.SS.B_edge, seed=None)
        return B, B_edges

    def making_node_info(self):  # layer, node_number, location
        node_info = [{'node_number': i, 'layer': 'B', 'location': (random.random(), random.random())}
                    for i in sorted(self.B_edges.nodes)]
        node_info = pd.DataFrame(node_info, columns=['node_number', 'layer', 'location'])
        return node_info

    def making_layer_B_internal_edge(self):
        layer_B_internal_edge_dic ={}
        for i, j in sorted(self.B_edges.edges):
            layer_B_internal_edge_dic[((i, 'layer_B'), (j, 'layer_B'))] = 1
        return layer_B_internal_edge_dic


if __name__ == "__main__":
    Layer_B = Layer_B_Modeling()
    B = Layer_B.B
    B_edges = Layer_B.B_edges
    print(B)
    print(B_edges.edges)
