import numpy as np
import Setting_Simulation_Value
import InterconnectedDynamics
import InterconnectedLayerModeling
import time


class RepeatDynamics:
    def __init__(self):
        self.inter_dynamics = InterconnectedDynamics.InterconnectedDynamics()

    def repeat_simultaneous_dynamics(self, setting, gamma, beta):
        num_data = np.zeros([setting.Limited_step + 1, 13])
        for i in range(setting.Repeating_number):
            inter_layer = InterconnectedLayerModeling.InterconnectedLayerModeling(setting)
            total_array = self.inter_dynamics.interconnected_simultaneous_dynamics(setting, inter_layer, gamma, beta)
            num_data = num_data + total_array
        Num_Data = num_data / setting.Repeating_number
        return Num_Data

    def repeat_dynamics(self, setting, gamma, beta):
        num_data = np.zeros([setting.Limited_step + 1, 13])
        for i in range(setting.Repeating_number):
            inter_layer = InterconnectedLayerModeling.InterconnectedLayerModeling(setting)
            total_array = self.inter_dynamics.interconnected_dynamics(setting, inter_layer, gamma, beta)
            num_data = num_data + total_array
        Num_Data = num_data / setting.Repeating_number
        return Num_Data


if __name__ == "__main__":
    print("RepeatDynamics")
    start = time.time()
    setting = Setting_Simulation_Value.Setting_Simulation_Value()
    gamma = 0.2
    beta = 1.5
    repeat = RepeatDynamics()
    result = repeat.repeat_dynamics(setting, gamma, beta)
    print(result)
    end = time.time()
    print(end - start)
