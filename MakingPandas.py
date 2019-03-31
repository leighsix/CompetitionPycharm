import pandas as pd
import numpy as np
import Layer_A_Modeling
import Layer_B_Modeling
import Setting_Simulation_Value


class MakingPandas:
    def making_dataframe_per_step(self, setting, value_array):
        columns = ['LAYER_A_MEAN', 'LAYER_B_MEAN', 'PROB_P', 'PROB_BETA', 'A_DIFFERENT_STATE_RATIO',
                   'B_DIFFERENT_STATE_RATIO', 'CONSENSUS_INDEX', 'CONSENSUS', 'NEGATIVE_STATE_NUMBER',
                   'POSITIVE_STATE_NUMBER', 'TIME_COUNT']
        df = pd.DataFrame(value_array, columns=columns)
        step = [i for i in range(0, setting.Limited_step+1)]
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

    def layer_state_mean(self, layer_A, layer_B):
        judge_A = []
        judge_B = []
        for i in range(len(layer_A.G_A.nodes)):
            judge_A.append(layer_A.G_A.nodes[i]['state'])
        for i in range(len(layer_B.G_B.nodes)):
            judge_B.append(layer_B.G_B.nodes[i]['state'])
        layer_A_mean = sum(judge_A) / len(layer_A.G_A.nodes)
        layer_B_mean = sum(judge_B) / len(layer_B.G_B.nodes)
        return layer_A_mean, layer_B_mean

    def counting_positive_node(self, layer_A, layer_B):
        judge_A = []
        judge_B = []
        for i in range(len(layer_A.G_A.nodes)):
            judge_A.append(layer_A.G_A.nodes[i]['state'])
        for i in range(len(layer_B.G_B.nodes)):
            judge_B.append(layer_B.G_B.nodes[i]['state'])
        judge_A = np.array(judge_A)
        judge_B = np.array(judge_B)
        return sum(judge_A > 0) + sum(judge_B > 0)

    def counting_negative_node(self, layer_A, layer_B):
        judge_A = []
        judge_B = []
        for i in range(len(layer_A.G_A.nodes)):
            judge_A.append(layer_A.G_A.nodes[i]['state'])
        for i in range(len(layer_B.G_B.nodes)):
            judge_B.append(layer_B.G_B.nodes[i]['state'])
        judge_A = np.array(judge_A)
        judge_B = np.array(judge_B)
        return sum(judge_A < 0) + sum(judge_B < 0)

    def different_state_ratio(self, layer_A, layer_B):
        global A_ratio, B_ratio
        judge_A = []
        judge_B = []
        for i in range(len(layer_A.G_A.nodes)):
            judge_A.append(layer_A.G_A.nodes[i]['state'])
        for i in range(len(layer_B.G_B.nodes)):
            judge_B.append(layer_B.G_B.nodes[i]['state'])
        judge_A = np.array(judge_A)
        judge_B = np.array(judge_B)
        A_plus = sum(judge_A > 0)
        A_minus = sum(judge_A < 0)
        if A_plus >= A_minus:
            A_ratio = min(A_plus, A_minus) / len(layer_A.G_A.nodes)
        elif A_plus < A_minus:
            A_ratio = -(min(A_plus, A_minus)) / len(layer_B.G_B.nodes)
        B_plus = sum(judge_B > 0)
        B_minus = sum(judge_B < 0)
        if B_plus >= B_minus:
            B_ratio = min(B_plus, B_minus) / len(layer_B.G_B.nodes)
        elif B_plus < B_minus:
            B_ratio = -(min(B_plus, B_minus)) / len(layer_B.G_B.nodes)
        return A_ratio, B_ratio, A_ratio*B_ratio

    def judging_consensus(self, layer_A, layer_B):
        judge_A = []
        judge_B = []
        for i in range(len(layer_A.G_A.nodes)):
            judge_A.append(layer_A.G_A.nodes[i]['state'])
        for i in range(len(layer_B.G_B.nodes)):
            judge_B.append(layer_B.G_B.nodes[i]['state'])
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
    layer_A = Layer_A_Modeling.Layer_A_Modeling(setting)
    layer_B = Layer_B_Modeling.Layer_B_Modeling(setting)
    mp = MakingPandas()
    result1 = mp.judging_consensus(layer_A, layer_B)
    result2 = mp.different_state_ratio(layer_A, layer_B)
    result3 = mp.layer_state_mean(layer_A, layer_B)
    result4 = mp.counting_positive_node(layer_A, layer_B)
    result5 = mp.counting_negative_node(layer_A, layer_B)
    print(result1)
    print(result2)
    print(result3)
    print(result4)
    print(result5)
