import numpy as np
import Setting_Simulation_Value
import InterconnectedDynamics
import Layer_A_Modeling
import Layer_B_Modeling
from numba import jit


class RepeatDynamics:
    def __init__(self, setting):
        self.inter_dynamics = InterconnectedDynamics.InterconnectedDynamics()
        self.num_data = np.zeros([setting.Limited_step+1, 11])
        self.Num_Data = np.zeros([setting.Limited_step+1, 11])

    def repeat_dynamics(self, setting, prob_p, beta):
        time = 0
        for i in range(setting.Repeating_number):
            time += 1
            print(time)
            layer_A = Layer_A_Modeling.Layer_A_Modeling(setting)
            layer_B = Layer_B_Modeling.Layer_B_Modeling(setting)
            self.inter_dynamics.interconnected_dynamics(setting, layer_A, layer_B, prob_p, beta)
            total_array = self.inter_dynamics.total_value
            self.num_data = self.num_data + total_array
            self.inter_dynamics.total_value = np.zeros(11)
        self.Num_Data = self.num_data / setting.Repeating_number
        return self.Num_Data


if __name__ == "__main__":
    print("RepeatDynamics")
    setting = Setting_Simulation_Value.Setting_Simulation_Value()
    prob_p = 0.1
    beta = 1.5
    repeat = RepeatDynamics(setting)
    result = repeat.repeat_dynamics(setting, prob_p, beta)
    print(result)
