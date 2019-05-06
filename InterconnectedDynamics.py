import numpy as np
import networkx as nx
import Setting_Simulation_Value
import OpinionDynamics
import DecisionDynamics
import MakingPandas
import InterconnectedLayerModeling
import matplotlib
import time
matplotlib.use("Agg")


class InterconnectedDynamics:
    def __init__(self):
        self.opinion = OpinionDynamics.OpinionDynamics()
        self.decision = DecisionDynamics.DecisionDynamics()
        self.mp = MakingPandas.MakingPandas()

    def interconnected_dynamics(self, setting, inter_layer, gamma, beta):
        total_value = np.zeros(15)
        for step_number in range(setting.Limited_step+1):
            if step_number == 0:
                decision_prob = self.decision.B_state_change_probability_cal(setting, inter_layer, beta)
                opinion_prob = self.opinion.A_state_change_probability_cal(inter_layer, gamma)
                initial_value = self.making_properties_array(setting, inter_layer, gamma, beta, opinion_prob[1],
                                                             opinion_prob[2], decision_prob[1])
                total_value = total_value + initial_value
            elif step_number >= 1:
                opinion_result = self.opinion.A_layer_dynamics(setting, inter_layer, gamma)
                decision_result = self.decision.B_layer_dynamics(setting, opinion_result[0], beta)
                array_value = self.making_properties_array(setting, decision_result[0], gamma, beta, opinion_result[1],
                                                           opinion_result[2], decision_result[1])
                total_value = np.vstack([total_value, array_value])
        self.opinion.A_COUNT = 0
        self.decision.B_COUNT = 0
        return total_value

    def making_properties_array(self, setting, inter_layer, gamma, beta, persuasion_prob, compromise_prob, prob_beta_mean):
        interacting_properties = self.mp.interacting_property(setting, inter_layer)
        change_count = self.opinion.A_COUNT + self.decision.B_COUNT
        array_value = np.array([gamma, beta, prob_beta_mean, persuasion_prob, compromise_prob,
                                interacting_properties[0], interacting_properties[1],
                                interacting_properties[2], interacting_properties[3],
                                interacting_properties[4], interacting_properties[5],
                                interacting_properties[6],
                                len(sorted(inter_layer.A_edges.edges)), len(inter_layer.B_edges),
                                change_count])
        return array_value


if __name__ == "__main__":
    print("InterconnectedDynamics")
    start = time.time()
    setting = Setting_Simulation_Value.Setting_Simulation_Value()
    inter_layer = InterconnectedLayerModeling.InterconnectedLayerModeling(setting)
    gamma = 0.5
    beta = 1.5
    state = 0
    for i in range(setting.A_node):
        state += inter_layer.two_layer_graph.nodes[i]['state']
    print(state)
    inter_dynamics = InterconnectedDynamics()
    array = inter_dynamics.interconnected_dynamics(setting, inter_layer, gamma, beta)
    print(array)
    state = 0
    for i in range(setting.A_node):
        state += inter_layer.two_layer_graph.nodes[i]['state']
    print(state)
    end = time.time()
    print(end-start)











