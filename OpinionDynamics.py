import random
import Setting_Simulation_Value
import InterconnectedLayerModeling
import time


class OpinionDynamics:
    def __init__(self):
        self.A_COUNT = 0

    def A_layer_simultaneous_dynamics(self, setting, inter_layer, prob_p):
        temp_inter_layer = inter_layer
        for i, j in sorted(temp_inter_layer.A_edges.edges()):
            a = temp_inter_layer.two_layer_graph.nodes[i]['state']
            b = temp_inter_layer.two_layer_graph.nodes[j]['state']
            if a * b > 0:
                persuasion = self.A_layer_persuasion_function(setting, temp_inter_layer.two_layer_graph.nodes[i],
                                                              temp_inter_layer.two_layer_graph.nodes[j], prob_p)
                inter_layer.two_layer_graph.nodes[i]['state'] = persuasion[0]
                inter_layer.two_layer_graph.nodes[j]['state'] = persuasion[1]
            elif a * b < 0:
                compromise = self.A_layer_compromise_function(setting, temp_inter_layer.two_layer_graph.nodes[i],
                                                              temp_inter_layer.two_layer_graph.nodes[j], prob_p)
                inter_layer.two_layer_graph.nodes[i]['state'] = compromise[0]
                inter_layer.two_layer_graph.nodes[j]['state'] = compromise[1]
        for i, j in sorted(temp_inter_layer.AB_edges):
            a = temp_inter_layer.two_layer_graph.nodes[j]['state']
            b = temp_inter_layer.two_layer_graph.nodes[i]['state']
            if a * b > 0:
                inter_layer.two_layer_graph.nodes[j]['state'] \
                    = self.AB_layer_persuasion_function(setting, temp_inter_layer.two_layer_graph.nodes[j], prob_p)
            elif a * b < 0:
                inter_layer.two_layer_graph.nodes[j]['state'] \
                    = self.AB_layer_compromise_function(setting, temp_inter_layer.two_layer_graph.nodes[j], prob_p)
        return inter_layer


    def A_layer_dynamics(self, setting, inter_layer, prob_p):  # A_layer 다이내믹스, 감마 적용 및 설득/타협 알고리즘 적용
        for i, j in sorted(inter_layer.A_edges.edges()):
            a = inter_layer.two_layer_graph.nodes[i]['state']
            b = inter_layer.two_layer_graph.nodes[j]['state']
            if a * b > 0:
                persuasion = self.A_layer_persuasion_function(setting, inter_layer.two_layer_graph.nodes[i],
                                                              inter_layer.two_layer_graph.nodes[j], prob_p)
                inter_layer.two_layer_graph.nodes[i]['state'] = persuasion[0]
                inter_layer.two_layer_graph.nodes[j]['state'] = persuasion[1]
            elif a * b < 0:
                compromise = self.A_layer_compromise_function(setting, inter_layer.two_layer_graph.nodes[i],
                                                              inter_layer.two_layer_graph.nodes[j], prob_p)
                inter_layer.two_layer_graph.nodes[i]['state'] = compromise[0]
                inter_layer.two_layer_graph.nodes[j]['state'] = compromise[1]
        for i, j in sorted(inter_layer.AB_edges):
            a = inter_layer.two_layer_graph.nodes[j]['state']
            b = inter_layer.two_layer_graph.nodes[i]['state']

            if a * b > 0:
                inter_layer.two_layer_graph.nodes[j]['state'] \
                    = self.AB_layer_persuasion_function(setting, inter_layer.two_layer_graph.nodes[j], prob_p)
            elif a * b < 0:
                inter_layer.two_layer_graph.nodes[j]['state'] \
                    = self.AB_layer_compromise_function(setting, inter_layer.two_layer_graph.nodes[j], prob_p)
        return inter_layer


    def A_layer_persuasion_function(self, setting, a, b, prob_p):  # A layer 중에서 same orientation 에서 일어나는  변동 현상
        z = random.random()
        if z < prob_p:
            if (a['state']) > 0 and (b['state']) > 0:
                a['state'] = self.A_layer_node_right(a, setting.MAX)
                b['state'] = self.A_layer_node_right(b, setting.MAX)
            elif (a['state']) < 0 and (b['state']) < 0:
                a['state'] = self.A_layer_node_left(a, setting.MIN)
                b['state'] = self.A_layer_node_left(b, setting.MIN)
        return a['state'], b['state']

    def A_layer_compromise_function(self, setting, a, b, prob_p):  # A layer  중에서 opposite orientation 에서 일어나는 변동 현상
        z = random.random()
        if z < (1 - prob_p):
            if (a['state']) * (b['state']) == -1:
                if z < ((1 - prob_p) / 2):
                    (a['state']) = 1
                    (b['state']) = 1
                elif z > ((1 - prob_p) / 2):
                    a['state'] = -1
                    b['state'] = -1
            elif (a['state']) > 0:
                a['state'] = self.A_layer_node_left(a, setting.MIN)
                b['state'] = self.A_layer_node_right(b, setting.MAX)
            elif (a['state']) < 0:
                a['state'] = self.A_layer_node_right(a, setting.MAX)
                b['state'] = self.A_layer_node_left(b, setting.MIN)
        return a['state'], b['state']

    def AB_layer_persuasion_function(self, setting, a, prob_p):  # A-B layer 중에서 same orientation 에서 일어나는  변동 현상
        z = random.random()
        if z < prob_p:
            if (a['state']) > 0:
                a['state'] = self.A_layer_node_right(a, setting.MAX)
            elif (a['state']) < 0:
                a['state'] = self.A_layer_node_left(a, setting.MIN)
        return a['state']

    def AB_layer_compromise_function(self, setting, a, prob_p):  # A-B layer  중에서 opposite orientation 에서 일어나는 변동 현상
        z = random.random()
        if z < (1 - prob_p):
            if (a['state']) > 0:
                a['state'] = self.A_layer_node_left(a, setting.MIN)
            elif (a['state']) < 0:
                a['state'] = self.A_layer_node_right(a, setting.MAX)
        elif z > (1 - prob_p):
            a['state'] = a['state']
        return a['state']

    def A_layer_node_left(self, a, Min):
        if (a['state']) > Min:
            if (a['state']) < 0 or (a['state']) > 1:
                (a['state']) = (a['state']) - 1
                self.A_COUNT += 1
            elif (a['state']) == 1:
                a['state'] = -1
                self.A_COUNT += 1
        elif (a['state']) <= Min:
            (a['state']) = Min
        return a['state']

    def A_layer_node_right(self, a, Max):
        if (a['state']) < Max:
            if (a['state']) > 0 or (a['state']) < -1:
                a['state'] = (a['state']) + 1
                self.A_COUNT += 1
            elif (a['state']) == -1:
                a['state'] = 1
                self.A_COUNT += 1
        elif (a['state']) >= Max:
            a['state'] = Max
        return a['state']


if __name__ == "__main__":
    print("OpinionDynamics")
    setting = Setting_Simulation_Value.Setting_Simulation_Value()
    inter_layer = InterconnectedLayerModeling.InterconnectedLayerModeling(setting)
    state = 0
    for i in range(setting.A_node):
        state += inter_layer.two_layer_graph.nodes[i]['state']
    print(state)
    opinion = OpinionDynamics()
    start = time.time()
    for i in range(100):
        inter_layer = opinion.A_layer_dynamics(setting, inter_layer, 0.3)
    state = 0
    for i in range(setting.A_node):
        state += inter_layer.two_layer_graph.nodes[i]['state']
    print(state)
    end = time.time()
    print(end - start)

