import numpy as np
import Setting_Simulation_Value
import KFInterconnectedDynamics
import KFMakingPandas
import CalculatingProperty
import InterconnectedLayerModeling


class KFRepeatDynamics:
    def __init__(self, setting):
        self.kfinter_dynamics = KFInterconnectedDynamics.KFInterconnectedDynamics()
        self.kfmp = KFMakingPandas.KFMakingPandas()
        self.cal_property = CalculatingProperty.CalculatingProperty()
        self.num_data = np.zeros([setting.Limited_step+1, 15])
        self.Num_Data = np.zeros([setting.Limited_step+1, 15])

    def repeat_dynamics(self, setting, prob_p, beta, node_i_name):
        time = 0
        inter_layer = InterconnectedLayerModeling.InterconnectedLayerModeling(setting)

        for i in range(setting.Repeating_number):
            time += 1
            print(time)
            self.kfinter_dynamics.interconnected_dynamics(setting, inter_layer, prob_p, beta, node_i_name)
            # print(sorted(inter_layer.two_layer_graph.neighbors(0)))
            total_array = self.kfinter_dynamics.total_value
            self.num_data = self.num_data + total_array
            self.kfinter_dynamics.total_value = np.zeros(15)
        Num_Data = self.num_data / setting.Repeating_number
        panda_db = self.kfmp.making_dataframe_per_step(setting, Num_Data, node_i_name)
        self.num_data = np.zeros([setting.Limited_step + 1, 15])
        self.Num_Data = np.zeros([setting.Limited_step + 1, 15])
        number = node_i_name.split('_')[1]
        panda_db = self.cal_property.making_df_for_property(panda_db, inter_layer, number)
        return panda_db


if __name__ == "__main__":
    print("RepeatDynamics")
    setting = Setting_Simulation_Value.Setting_Simulation_Value()
    prob_p = 0.2
    beta = 1.5
    node_i_name = 'A_0'
    repeat = KFRepeatDynamics(setting)
    result = repeat.repeat_dynamics(setting, prob_p, beta, node_i_name)
    print(result)
