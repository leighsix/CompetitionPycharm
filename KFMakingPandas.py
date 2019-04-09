import pandas as pd
import numpy as np
import InterconnectedLayerModeling
import Setting_Simulation_Value


class MakingPandas:
    def making_dataframe_per_step(self, setting, value_array):
        columns = ['LAYER_A_MEAN', 'LAYER_B_MEAN', 'FRACTION_A', 'FRACTION_B', 'PROB_P', 'PROB_BETA',
                   'A_DIFFERENT_STATE_RATIO', 'B_DIFFERENT_STATE_RATIO', 'AB_RATIO',
                   'A_total_edges', 'B_total_edges', 'CONSENSUS',
                   'NEGATIVE_STATE_NUMBER', 'POSITIVE_STATE_NUMBER', 'TIME_COUNT']
        df = pd.DataFrame(value_array, columns=columns)
        step = [i for i in range(0, setting.Limited_step+1)]
        df['MODEL'] = setting.MODEL
        df['A_Initial_State'] = setting.average_initial_A
        df['B_Initial_State'] = setting.average_initial_B
        df['A_Initial_Dev'] = setting.dev_A
        df['B_Initial_Dev'] = setting.dev_B
        df['A_Initial_Positive_Ratio'] = setting.positive_ratio_A
        df['B_Initial_Positive_Ratio'] = setting.positive_ratio_B
        df['Steps'] = step
        df['Structure'] = setting.Structure
        df['A_node_number'] = setting.A_node
        df['B_node_number'] = setting.B_node
        df['A_internal_edges'] = setting.A_edge
        df['B_internal_edges'] = setting.B_edge
        df['A_external_edges'] = setting.A_inter_edges
        df['B_external_edges'] = setting.B_inter_edges
        return df

    def layer_state_mean(self, setting, inter_layer):
        judge_A = []
        judge_B = []
        for i in range(setting.A_node):
            judge_A.append(inter_layer.two_layer_graph.nodes[i]['state'])
        for i in range(setting.A_node, setting.A_node + setting.B_node):
            judge_B.append(inter_layer.two_layer_graph.nodes[i]['state'])
        layer_A_mean = sum(judge_A) / setting.A_node
        layer_B_mean = sum(judge_B) / setting.B_node
        return layer_A_mean, layer_B_mean

    def counting_positive_node(self, setting, inter_layer):
        judge_A = []
        judge_B = []
        for i in range(setting.A_node):
            judge_A.append(inter_layer.two_layer_graph.nodes[i]['state'])
        for i in range(setting.A_node, setting.A_node + setting.B_node):
            judge_B.append(inter_layer.two_layer_graph.nodes[i]['state'])
        judge_A = np.array(judge_A)
        judge_B = np.array(judge_B)
        return sum(judge_A > 0) + sum(judge_B > 0)

    def counting_negative_node(self, setting, inter_layer):
        judge_A = []
        judge_B = []
        for i in range(setting.A_node):
            judge_A.append(inter_layer.two_layer_graph.nodes[i]['state'])
        for i in range(setting.A_node, setting.A_node + setting.B_node):
            judge_B.append(inter_layer.two_layer_graph.nodes[i]['state'])
        judge_A = np.array(judge_A)
        judge_B = np.array(judge_B)
        return sum(judge_A < 0) + sum(judge_B < 0)

    def calculate_fraction_plus(self, setting, inter_layer):
        judge_A = []
        judge_B = []
        for i in range(setting.A_node):
            judge_A.append(inter_layer.two_layer_graph.nodes[i]['state'])
        for i in range(setting.A_node, setting.A_node + setting.B_node):
            judge_B.append(inter_layer.two_layer_graph.nodes[i]['state'])
        judge_A = np.array(judge_A)
        judge_B = np.array(judge_B)
        fraction_A = sum(judge_A > 0) / setting.A_node
        fraction_B = sum(judge_B > 0) / setting.B_node
        return fraction_A, fraction_B

    def different_state_ratio(self, setting, inter_layer):
        global A_ratio, B_ratio
        judge_A = []
        judge_B = []
        for i in range(setting.A_node):
            judge_A.append(inter_layer.two_layer_graph.nodes[i]['state'])
        for i in range(setting.A_node, setting.A_node + setting.B_node):
            judge_B.append(inter_layer.two_layer_graph.nodes[i]['state'])
        judge_A = np.array(judge_A)
        judge_B = np.array(judge_B)
        A_plus = sum(judge_A > 0)
        A_minus = sum(judge_A < 0)
        if A_plus >= A_minus:
            A_ratio = min(A_plus, A_minus) / setting.A_node
        elif A_plus < A_minus:
            A_ratio = -(min(A_plus, A_minus)) / setting.B_node
        B_plus = sum(judge_B > 0)
        B_minus = sum(judge_B < 0)
        if B_plus >= B_minus:
            B_ratio = min(B_plus, B_minus) / setting.B_node
        elif B_plus < B_minus:
            B_ratio = -(min(B_plus, B_minus)) / setting.B_node
        return A_ratio, B_ratio, A_ratio*B_ratio

    def judging_consensus(self, setting, inter_layer):
        judge_A = []
        judge_B = []
        for i in range(setting.A_node):
            judge_A.append(inter_layer.two_layer_graph.nodes[i]['state'])
        for i in range(setting.A_node, setting.A_node + setting.B_node):
            judge_B.append(inter_layer.two_layer_graph.nodes[i]['state'])
        judge_A = np.array(judge_A)
        judge_B = np.array(judge_B)
        if ((np.all(judge_A > 0) == 1) and (np.all(judge_B > 0) == 1)) or \
                ((np.all(judge_A < 0) == 1) and (np.all(judge_B < 0) == 1)):
            return True
        else:
            return False

if __name__ == "__main__":
    print("MakingPandas")
    setting = Setting_Simulation_Value.Setting_Simulation_Value()
    inter_layer = InterconnectedLayerModeling.InterconnectedLayerModeling(setting)
    mp = MakingPandas()
    result1 = mp.judging_consensus(setting, inter_layer)
    result2 = mp.different_state_ratio(setting, inter_layer)
    result3 = mp.layer_state_mean(setting, inter_layer)
    result4 = mp.counting_positive_node(setting, inter_layer)
    result5 = mp.counting_negative_node(setting, inter_layer)
    print(result1)
    print(result2)
    print(result3)
    print(result4)
    print(result5)
