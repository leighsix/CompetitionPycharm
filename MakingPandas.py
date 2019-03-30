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

    def layer_state_mean(self, setting):
        layer_A_mean = sum(setting.A) / setting.A_node
        layer_B_mean = sum(setting.B) / setting.B_node
        return layer_A_mean, layer_B_mean

    def counting_positive_node(self, setting):
        return sum(setting.A > 0) + sum(setting.B > 0)

    def counting_negative_node(self, setting):
        return sum(setting.A < 0) + sum(setting.B < 0)

    def different_state_ratio(self, setting):
        global A_ratio, B_ratio
        A_plus = sum(setting.A > 0)
        A_minus = sum(setting.A < 0)
        if A_plus >= A_minus:
            A_ratio = min(A_plus, A_minus) / setting.A_node
        elif A_plus < A_minus:
            A_ratio = -(min(A_plus, A_minus)) / setting.A_node
        B_plus = sum(setting.B > 0)
        B_minus = sum(setting.B < 0)
        if B_plus >= B_minus:
            B_ratio = min(B_plus, B_minus) / setting.B_node
        elif B_plus < B_minus:
            B_ratio = -(min(B_plus, B_minus)) / setting.B_node
        return A_ratio, B_ratio, A_ratio*B_ratio

    def judging_consensus(self, setting):
        if (((np.all(setting.A > 0) == 1) and (np.all(setting.B > 0) == 1)) or
                ((np.all(setting.A < 0) == 1) and (np.all(setting.B < 0) == 1))):
                return True
        else:
            return False


if __name__ == "__main__":
    print("MakingPandas")
    setting = Setting_Simulation_Value.Setting_Simulation_Value()
    layer_A = Layer_A_Modeling.Layer_A_Modeling(setting)
    layer_B = Layer_B_Modeling.Layer_B_Modeling(setting)
    mp = MakingPandas()
    result = mp.judging_consensus(setting)
    print(result)
