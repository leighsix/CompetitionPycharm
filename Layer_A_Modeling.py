import networkx as nx
import numpy as np
import pandas as pd
import random
import Setting_Simulation_Value
## A layer Modeling : A, A_edges, AB_edges, AB_neighbor


class Layer_A_Modeling:
    def __init__(self):
        # network : 1 = random regular graph   2 = barabasi-albert graph
        self.SS = Setting_Simulation_Value.Setting_Simulation_Value()
        self.A = self.A_layer_config()[0]
        self.A_edges = self.A_layer_config()[1]
        self.AB_edges = self.A_layer_config()[2]
        self.AB_neighbor = self.A_layer_config()[3]
        self.A_node_info = self.making_node_info()
        self.layer_A_internal_edge_dic = self.making_layer_A_internal_edge()
        self.external_edge_dic = self.making_external_edge()

    def A_layer_config(self):
        # A_layer 구성요소 A_layer_config(state = [1,2], node = 2048, edge = 5, Max = 2, Min = -2)
        self.select_layer_A_model(self.SS.A_network)
        self.making_interconnected_edges()
        return self.A, self.A_edges, self.AB_edges, self.AB_neighbor
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
        self.A = np.array(self.SS.A_state * int(self.SS.A_node / len(self.SS.A_state)), int)
        random.shuffle(self.A)
        self.A_edges = nx.random_regular_graph(self.SS.A_edge, self.SS.A_node, seed=None)
        return self.A, self.A_edges


    def making_layer_A_barabasi_albert(self):
        # A_layer 바바라시-알버트 네트워크
        self.A = np.array(self.SS.A_state * int(self.SS.A_node / len(self.SS.A_state)), int)
        random.shuffle(self.A)
        self.A_edges = nx.barabasi_albert_graph(self.SS.A_node, self.SS.A_edge, seed=None)
        return self.A, self.A_edges

    def making_interconnected_edges(self):
        self.AB_edges = []
        self.AB_neighbor = []
        for i in range(int(self.SS.A_node / self.SS.B_inter_edges)):
            for j in range(self.SS.B_inter_edges):
                connected_A_node = np.array(self.A_edges.nodes).reshape(-1, self.SS.B_inter_edges)[i][j]
                self.AB_neighbor.append(connected_A_node)
                self.AB_edges.append((i, connected_A_node))
        self.AB_neighbor = np.array(self.AB_neighbor).reshape(-1, self.SS.B_inter_edges)
        return self.AB_edges, self.AB_neighbor
        # AB_neighbor은 B노드번호 기준으로 연결된 A노드번호  ex) AB_neighbor[0]= array([0, 1])
        # B 노드 0에 A노드 0번, 1번이 연결되어 있다는 뜻
        # AB_edges는 (0, 1)은 B 노드 0번과 A 노드 1번이 연결되어 있다는 뜻

    def making_node_info(self):  # layer, node_number, location
        node_info = [{'node_number': i, 'layer': 'A', 'location': (random.random(), random.random())}
                     for i in sorted(self.A_edges.nodes)]
        node_info = pd.DataFrame(node_info, columns=['node_number', 'layer', 'location'])
        return node_info


if __name__ == "__main__" :
    Layer_A = Layer_A_Modeling()
    print(Layer_A.A)
    print(Layer_A.A_edges.edges)
    print(Layer_A.AB_edges)
    print(Layer_A.AB_neighbor)



