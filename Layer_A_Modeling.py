import networkx as nx
import numpy as np
import pandas as pd
import random
import Setting_Revised_Value
## A layer Modeling : A, A_edges, AB_edges, AB_neighbor


class Layer_A_Modeling():
    def __init__(self, setting):
        # network : 1 = random regular graph   2 = barabasi-albert graph
        self.A = self.A_layer_config(setting)[0]
        self.A_edges = self.A_layer_config(setting)[1]
        self.AB_edges = self.A_layer_config(setting)[2]
        self.AB_neighbor = self.A_layer_config(setting)[3]
        self.AB_edges_reverse = self.A_layer_config(setting)[4]
        self.A_node_info = self.making_node_info()

    def A_layer_config(self, setting):
        # A_layer 구성요소 A_layer_config(state = [1,2], node = 2048, edge = 5, Max = 2, Min = -2)
        self.select_layer_A_model(setting)
        self.making_interconnected_edges(setting)
        return self.A, self.A_edges, self.AB_edges, self.AB_neighbor, self.AB_edges_reverse
        # A : A의 각 노드의 상태, A_state : A 노드 상태의 종류(1, 2, -1, -2),
        # A_node : 노드의 수, A_edge : 내부연결선수, A_edges : 내부연결상태(튜플), MAX : 최대상태, MIN : 최소상태

    def select_layer_A_model(self, setting):
        if setting.Structure.split('-')[0] == 'RR':
            self.making_layer_A_random_regular(setting)
        elif setting.Structure.split('-')[0] == 'BA':
            self.making_layer_A_barabasi_albert(setting)
        return self.A, self.A_edges

    def making_layer_A_random_regular(self, setting):
        # A_layer random_regular network
        self.A = np.array(setting.A_state * int(setting.A_node / len(setting.A_state)), int)
        random.shuffle(self.A)
        self.A_edges = nx.random_regular_graph(setting.A_edge, setting.A_node, seed=None)
        return self.A, self.A_edges


    def making_layer_A_random_regular(self, setting):
        # A_layer random_regular network
        self.A = np.array(setting.A_state * int(setting.A_node / len(setting.A_state)), int)
        random.shuffle(self.A)
        self.A_edges = nx.random_regular_graph(setting.A_edge, setting.A_node, seed=None)
        return self.A, self.A_edges

    def making_layer_A_barabasi_albert(self, setting):
        # A_layer 바바라시-알버트 네트워크
        self.A = np.array(setting.A_state * int(setting.A_node / len(setting.A_state)), int)
        random.shuffle(self.A)
        self.A_edges = nx.barabasi_albert_graph(setting.A_node, setting.A_edge, seed=None)
        return self.A, self.A_edges

    def making_interconnected_edges(self, setting):
        self.AB_edges = []
        self.AB_edges_reverse = []
        self.AB_neighbor = []
        for i in range(int(setting.A_node / setting.B_inter_edges)):
            for j in range(setting.B_inter_edges):
                connected_A_node = np.array(self.A_edges.nodes).reshape(-1, setting.B_inter_edges)[i][j]
                self.AB_neighbor.append(connected_A_node)
                self.AB_edges.append((i, connected_A_node))
                self.AB_edges_reverse.append((connected_A_node, i))
        self.AB_neighbor = np.array(self.AB_neighbor).reshape(-1, setting.B_inter_edges)
        self.AB_edges_reverse = sorted(self.AB_edges_reverse)
        return self.AB_edges, self.AB_neighbor, self.AB_edges_reverse
        # AB_neighbor은 B노드번호 기준으로 연결된 A노드번호  ex) AB_neighbor[0]= array([0, 1])
        # B 노드 0에 A노드 0번, 1번이 연결되어 있다는 뜻
        # AB_edges는 (0, 1)은 B 노드 0번과 A 노드 1번이 연결되어 있다는 뜻
        # AB_edges_reverse는 (0, 1)은 A노드 0번과 B노드 1번이 연결되어 있다는 뜻

    def making_node_info(self):  # layer, node_number, location
        node_info = [{'node_number': i, 'layer': 'A', 'location': (random.random(), random.random())}
                     for i in sorted(self.A_edges.nodes)]
        node_info = pd.DataFrame(node_info, columns=['node_number', 'layer', 'location'])
        return node_info


if __name__ == "__main__" :
    print("layer_A")
    setting = Setting_Revised_Value.Setting_Revised_Value()
    Layer_A = Layer_A_Modeling(setting)
    #print('---------------------')
    #print(Layer_A.A)
    #print('---------------------')
    print(Layer_A.AB_neighbor)
    #print(Layer_A.AB_edges)
    #print(Layer_A.AB_edges_reverse)
    print(Layer_A.AB_edges_reverse)
    #print('---------------------')
    #print(Layer_A.AB_edges)
    #print('---------------------A_edges')
    #print(sorted(Layer_A.A_edges))
    #print(Layer_A.A_edges.edges)
    #print(Layer_A.AB_edges)
    #print(Layer_A.AB_neighbor)
    #print(Layer_A.SS.A_node)



