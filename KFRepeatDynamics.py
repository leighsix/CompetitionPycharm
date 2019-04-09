import numpy as np
import Setting_Simulation_Value
import KFInterconnectedDynamics
import InterconnectedLayerModeling


class KFRepeatDynamics:
    def __init__(self, setting):
        self.kfinter_dynamics = KFInterconnectedDynamics.KFInterconnectedDynamics()
        self.num_data = np.zeros([setting.Limited_step+1, 15])
        self.Num_Data = np.zeros([setting.Limited_step+1, 15])

    def repeat_dynamics(self, setting, prob_p, beta, node_i_name):
        time = 0
        for i in range(setting.Repeating_number):
            time += 1
            print(time)
            inter_layer = InterconnectedLayerModeling.InterconnectedLayerModeling(setting)
            self.kfinter_dynamics.interconnected_dynamics(setting, inter_layer, prob_p, beta, node_i_name)
            total_array = self.kfinter_dynamics.total_value
            self.num_data = self.num_data + total_array
            self.kfinter_dynamics.total_value = np.zeros(15)
        self.Num_Data = self.num_data / setting.Repeating_number
        return self.Num_Data


if __name__ == "__main__":
    print("RepeatDynamics")
    setting = Setting_Simulation_Value.Setting_Simulation_Value()
    prob_p = 0.2
    beta = 1.5
    node_i_name = 'A_0'
    repeat = KFRepeatDynamics(setting)
    result = repeat.repeat_dynamics(setting, prob_p, beta, node_i_name)
    print(result)
