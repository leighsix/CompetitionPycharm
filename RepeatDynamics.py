import pandas as pd
import numpy as np
import Setting_Simulation_Value
import InterconnectedDynamics
import Layer_A_Modeling
import Layer_B_Modeling


class RepeatDynamics:
    def __init__(self):
        self.SS = Setting_Simulation_Value.Setting_Simulation_Value()
        self.inter_dynamics = InterconnectedDynamics.InterconnectedDynamics()
        self.num_data = np.zeros([30, 11])
        self.Num_Data = np.zeros([30, 11])

    def repeat_dynamics(self, prob_p, beta):
        for i in range(self.SS.Repeating_number):
            layer_A = Layer_A_Modeling.Layer_A_Modeling()
            layer_B = Layer_B_Modeling.Layer_B_Modeling()
            self.inter_dynamics.interconnected_dynamics(layer_A, layer_B, prob_p, beta)
            total_array = self.inter_dynamics.total_value
            self.num_data = self.num_data + total_array
            self.inter_dynamics.total_value = np.zeros(11)
        self.Num_Data = self.num_data / self.SS.Repeating_number
        return self.Num_Data

if __name__ == "__main__":
    print("RepeatDynamics")
    prob_p = 0.1
    beta = 1.5
    repeat = RepeatDynamics()
    result = repeat.repeat_dynamics(prob_p, beta)
    print(result)
