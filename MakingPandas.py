import pandas as pd
import numpy as np
import Setting_Simulation_Value
#import Layer_A_Modeling
#import Layer_B_Modeling


class MakingPandas:
    def __init__(self):
        self.SS = Setting_Simulation_Value.Setting_Simulation_Value()

    def making_dataframe_per_step(self, value_array):
        columns = ['LAYER_A_MEAN', 'LAYER_B_MEAN', 'PROB_P', 'PROB_BETA', 'A_DIFFERENT_STATE_RATIO',
                   'B_DIFFERENT_STATE_RATIO', 'CONSENSUS_INDEX', 'CONSENSUS', 'NEGATIVE_STATE_NUMBER',
                   'POSITIVE_STATE_NUMBER', 'TIME_COUNT']
        df = pd.DataFrame(value_array, columns=columns)
        step = [i for i in range(1, self.SS.Limited_step+1)]
        df['Steps'] = step
        df['Structure'] = self.SS.Structure
        df['A_node_number'] = self.SS.A_node
        df['B_node_number'] = self.SS.B_node
        df['A_internal_edges'] = self.SS.A_edge
        df['B_internal_edges'] = self.SS.B_edge
        df['A_external_edges'] = self.SS.A_inter_edges
        df['B_external_edges'] = self.SS.B_inter_edges
        return df

    def layer_state_mean(self, layer_A, layer_B):
        layer_A_mean = sum(layer_A.A) / self.SS.A_node
        layer_B_mean = sum(layer_B.B) / self.SS.B_node
        return layer_A_mean, layer_B_mean

    def counting_positive_node(self, layer_A, layer_B):
        return sum(layer_A.A > 0) + sum(layer_B.B > 0)

    def counting_negative_node(self, layer_A, layer_B):
        return sum(layer_A.A < 0) + sum(layer_B.B < 0)

    def different_state_ratio(self, layer_A, layer_B):
        global A_ratio, B_ratio
        A_plus = sum(layer_A.A > 0)
        A_minus = sum(layer_A.A < 0)
        if A_plus >= A_minus:
            A_ratio = min(A_plus, A_minus) / self.SS.A_node
        elif A_plus < A_minus:
            A_ratio = -(min(A_plus, A_minus)) / self.SS.A_node
        B_plus = sum(layer_B.B > 0)
        B_minus = sum(layer_B.B < 0)
        if B_plus >= B_minus:
            B_ratio = min(B_plus, B_minus) / self.SS.B_node
        elif B_plus < B_minus:
            B_ratio = -(min(B_plus, B_minus)) / self.SS.B_node
        return A_ratio, B_ratio, A_ratio*B_ratio

    def judging_consensus(self, layer_A, layer_B):
        if (((np.all(layer_A.A > 0) == 1) and (np.all(layer_B.B > 0) == 1)) or
                ((np.all(layer_A.A < 0) == 1) and (np.all(layer_B.B < 0) == 1))):
                return True
        else:
            return False


if __name__ == "__main__":
    print("MakingPandas")
    #layer_A = Layer_A_Modeling.Layer_A_Modeling()
    #layer_B = Layer_B_Modeling.Layer_B_Modeling()
    #mp = MakingPandas()
    #result = mp.judging_consensus(layer_A, layer_B)
    #print(result)