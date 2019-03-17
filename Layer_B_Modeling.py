import networkx as nx
import numpy as np
import pandas as pd
import Setting_Revised_Value
import random
## B layer : B, B_edges


class Layer_B_Modeling:
    def __init__(self, setting):
        self.B = setting.B
        self.B_edges = self.B_layer_config(setting)
        self.B_node_info = self.making_node_info()

    def B_layer_config(self, setting):  # B_layer 구성요소 B_layer_config(state = [-1], node = 2048, edge = 5, inter_edge= 1)
        self.B_edges = self.select_layer_B_model(setting)
        return self.B_edges

    def select_layer_B_model(self, setting):
        if setting.Structure.split('-')[1] == 'RR':
            self.making_layer_B_random_regular(setting)
        elif setting.Structure.split('-')[1] == 'BA':
            self.making_layer_B_barabasi_albert(setting)
        return self.B_edges

    def making_layer_B_random_regular(self, setting):  # B_layer random_regular network
        self.B_edges = nx.random_regular_graph(setting.B_edge, setting.B_node, seed=None)
        return self.B_edges

    def making_layer_B_barabasi_albert(self, setting):  # B_layer 바바라시-알버트 네트워크
        self.B_edges = nx.barabasi_albert_graph(setting.B_node, setting.B_edge, seed=None)
        return self.B_edges

    def making_node_info(self):  # layer, node_number, location
        node_info = [{'node_number': i, 'layer': 'B', 'location': (random.random(), random.random())}
                    for i in sorted(self.B_edges.nodes)]
        node_info = pd.DataFrame(node_info, columns=['node_number', 'layer', 'location'])
        return node_info


if __name__ == "__main__":
    print("layer_B")
    setting = Setting_Revised_Value.Setting_Revised_Value()
    Layer_B = Layer_B_Modeling(setting)
    print(Layer_B.B)
    print(sum(Layer_B.B))
    print(sorted(Layer_B.B_edges))