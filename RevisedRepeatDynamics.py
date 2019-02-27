import numpy as np
import Setting_Revised_Value
import RevisedInterconnectedDynamics
import Layer_A_Modeling
import Layer_B_Modeling
from numba import jit


class RevisedRepeatDynamics:
    def __init__(self, setting):
        self.revised_inter_dynamics = RevisedInterconnectedDynamics.RevisedInterconnectedDynamics()
        self.num_data = np.zeros([setting.Limited_step+1, 11])
        self.Num_Data = np.zeros([setting.Limited_step+1, 11])

    def repeat_dynamics(self, setting, beta):
        time = 0
        for i in range(setting.Repeating_number):
            time += 1
            print(time)
            layer_A = Layer_A_Modeling.Layer_A_Modeling(setting)
            layer_B = Layer_B_Modeling.Layer_B_Modeling(setting)
            self.revised_inter_dynamics.revised_interconnected_dynamics(setting, layer_A, layer_B, beta)
            print(sum(layer_A.A), sum(layer_B.B))
            total_array = self.revised_inter_dynamics.total_value
            self.num_data = self.num_data + total_array
            self.revised_inter_dynamics.total_value = np.zeros(11)
        self.Num_Data = self.num_data / setting.Repeating_number
        return self.Num_Data


if __name__ == "__main__":
    print("RepeatDynamics")
    setting = Setting_Revised_Value.Setting_Revised_Value()
    beta = 2.8
    repeat = RevisedRepeatDynamics(setting)
    result = repeat.repeat_dynamics(setting, beta)
    print(result)
