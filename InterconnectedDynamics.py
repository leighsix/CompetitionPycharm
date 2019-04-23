import numpy as np
import networkx as nx
import Setting_Simulation_Value
import OpinionDynamics
import DecisionDynamics
import MakingPandas
import InterconnectedLayerModeling
import matplotlib
import Interconnected_Network_Visualization
import time
matplotlib.use("Agg")


class InterconnectedDynamics:
    def __init__(self):
        self.opinion = OpinionDynamics.OpinionDynamics()
        self.decision = DecisionDynamics.DecisionDynamics()
        self.mp = MakingPandas.MakingPandas()
        self.network = Interconnected_Network_Visualization.Interconnected_Network_Visualization()

    def interconnected_simultaneous_dynamics(self, setting, inter_layer, gamma, beta):
        total_value = np.zeros(13)
        ims = []
        step_number = 0
        prob_p = gamma / (gamma + 1)
        while True:
            temp_inter_layer = inter_layer
            if step_number == 0:
                if setting.drawing_graph == 1:
                    im = self.network.draw_interconnected_network(setting, inter_layer, 'result.png')[0]
                    ims.append(im)
                probability = self.decision.B_state_change_probability_cal(setting, temp_inter_layer, beta)
                prob_beta_mean = np.sum(probability) / len(probability)
                interacting_properties = self.mp.interacting_property(setting, temp_inter_layer)
                change_count = self.opinion.A_COUNT + self.decision.B_COUNT
                initial_value = np.array([gamma, beta, prob_beta_mean,
                                          interacting_properties[0], interacting_properties[1],
                                          interacting_properties[2], interacting_properties[3],
                                          interacting_properties[4], interacting_properties[5],
                                          interacting_properties[6],
                                          len(sorted(temp_inter_layer.A_edges.edges)), len(temp_inter_layer.B_edges),
                                          change_count])
                total_value = total_value + initial_value
            opinion_result = self.opinion.A_layer_simultaneous_dynamics(setting, temp_inter_layer, prob_p)
            decision_result = self.decision.B_layer_simultaneous_dynamics(setting, temp_inter_layer, beta)
            decision_layer = decision_result[0]
            prob_beta_mean = decision_result[1]
            for node_A in range(setting.A_node):
                inter_layer.two_layer_graph.nodes[node_A]['state'] = opinion_result.two_layer_graph.nodes[node_A]['state']
            for node_B in range(setting.A_node, setting.A_node+setting.B_node):
                inter_layer.two_layer_graph.nodes[node_B]['state'] = decision_layer.two_layer_graph.nodes[node_B]['state']
            if setting.drawing_graph == 1:
                im = self.network.draw_interconnected_network(setting, inter_layer, 'result.png')[0]
                ims.append(im)
                judge_A = []
                judge_B = []
                for i in range(setting.A_node):
                    judge_A.append(inter_layer.two_layer_graph.nodes[i]['state'])
                for i in range(setting.A_node, setting.A_node + setting.B_node):
                    judge_B.append(inter_layer.two_layer_graph.nodes[i]['state'])
                judge_A = np.array(judge_A)
                judge_B = np.array(judge_B)
                if (np.all(judge_A > 0) == 1 and np.all(judge_B > 0) == 1) or \
                        (np.all(judge_A < 0) == 1 and np.all(judge_B < 0) == 1):
                    print('Consensus')
                    break
            step_number += 1
            interacting_properties = self.mp.interacting_property(setting, temp_inter_layer)
            change_count = self.opinion.A_COUNT + self.decision.B_COUNT
            array_value = np.array([gamma, beta, prob_beta_mean,
                                    interacting_properties[0], interacting_properties[1],
                                    interacting_properties[2], interacting_properties[3],
                                    interacting_properties[4], interacting_properties[5],
                                    interacting_properties[6],
                                    len(sorted(temp_inter_layer.A_edges.edges)), len(temp_inter_layer.B_edges),
                                    change_count])
            if step_number >= 1:
                total_value = np.vstack([total_value, array_value])
            if step_number >= setting.Limited_step:
                break
        self.opinion.A_COUNT = 0
        self.decision.B_COUNT = 0
        ims = np.array(ims)
        if setting.drawing_graph == 1:
            self.network.making_movie_for_dynamics(ims)
        return total_value

    def interconnected_dynamics(self, setting, inter_layer, gamma, beta):
        total_value = np.zeros(13)
        ims = []
        step_number = 0
        prob_p = gamma / (gamma + 1)
        while True:
            if step_number == 0:
                if setting.drawing_graph == 1:
                    im = self.network.draw_interconnected_network(setting, inter_layer, 'result.png')[0]
                    ims.append(im)
                probability = self.decision.B_state_change_probability_cal(setting, inter_layer, beta)
                prob_beta_mean = np.sum(probability) / len(probability)
                interacting_properties = self.mp.interacting_property(setting, inter_layer)
                change_count = self.opinion.A_COUNT + self.decision.B_COUNT
                initial_value = np.array([gamma, beta, prob_beta_mean,
                                          interacting_properties[0], interacting_properties[1],
                                          interacting_properties[2], interacting_properties[3],
                                          interacting_properties[4], interacting_properties[5],
                                          interacting_properties[6],
                                          len(sorted(inter_layer.A_edges.edges)), len(inter_layer.B_edges),
                                          change_count])
                total_value = total_value + initial_value
            inter_layer = self.opinion.A_layer_dynamics(setting, inter_layer, prob_p)
            decision = self.decision.B_layer_dynamics(setting, inter_layer, beta)
            inter_layer = decision[0]
            prob_beta_mean = decision[1]
            if setting.drawing_graph == 1:
                im = self.network.draw_interconnected_network(setting, inter_layer, 'result.png')[0]
                ims.append(im)
                judge_A = []
                judge_B = []
                for i in range(setting.A_node):
                    judge_A.append(inter_layer.two_layer_graph.nodes[i]['state'])
                for i in range(setting.A_node, setting.A_node + setting.B_node):
                    judge_B.append(inter_layer.two_layer_graph.nodes[i]['state'])
                judge_A = np.array(judge_A)
                judge_B = np.array(judge_B)
                if (np.all(judge_A > 0) == 1 and np.all(judge_B > 0) == 1) or \
                        (np.all(judge_A < 0) == 1 and np.all(judge_B < 0) == 1):
                    print('Consensus')
                    break
            step_number += 1
            interacting_properties = self.mp.interacting_property(setting, inter_layer)
            change_count = self.opinion.A_COUNT + self.decision.B_COUNT
            array_value = np.array([gamma, beta, prob_beta_mean,
                                    interacting_properties[0], interacting_properties[1],
                                    interacting_properties[2], interacting_properties[3],
                                    interacting_properties[4], interacting_properties[5],
                                    interacting_properties[6],
                                    len(sorted(inter_layer.A_edges.edges)), len(inter_layer.B_edges),
                                    change_count])
            if step_number >= 1:
                total_value = np.vstack([total_value, array_value])
            if step_number >= setting.Limited_step:
                break
        self.opinion.A_COUNT = 0
        self.decision.B_COUNT = 0
        ims = np.array(ims)
        if setting.drawing_graph == 1:
            self.network.making_movie_for_dynamics(ims)
        return total_value

if __name__ == "__main__":
    print("InterconnectedDynamics")
    start = time.time()
    setting = Setting_Simulation_Value.Setting_Simulation_Value()
    inter_layer = InterconnectedLayerModeling.InterconnectedLayerModeling(setting)
    gamma = 0.5
    beta = 8
    state = 0
    for i in range(setting.A_node):
        state += inter_layer.two_layer_graph.nodes[i]['state']
    print(state)
    inter_dynamics = InterconnectedDynamics()
    array = inter_dynamics.interconnected_dynamics(setting, inter_layer, gamma, beta)
    state = 0
    for i in range(setting.A_node):
        state += inter_layer.two_layer_graph.nodes[i]['state']
    print(state)
    end = time.time()
    print(end-start)











