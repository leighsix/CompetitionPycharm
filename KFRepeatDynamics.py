import numpy as np
import Setting_Simulation_Value
import InterconnectedLayerModeling
import KFInterconnectedDynamics
import MakingPandas
import CalculatingProperty

class KFRepeatDynamics:
    def __init__(self):
        self.kfinter_dynamics = KFInterconnectedDynamics.KFInterconnectedDynamics()
        self.mp = MakingPandas.MakingPandas()
        self.cal_property = CalculatingProperty.CalculatingProperty()

    def repeat_dynamics_for_only_100steps(self, setting, inter_layer, node_i_name, fixed_node_state):
        total_data = np.zeros(0)
        node_number = node_i_name.split('_')[1]
        if node_number != 'N':
            node_number = int(node_number)
            inter_layer.two_layer_graph.node[node_number]['state'] = fixed_node_state
        line = 0
        for gamma in setting.R:
            for beta in setting.D:
                print(gamma, beta)
                line +=1
                num_data_for_100steps = np.zeros(15)
                prob_p = gamma / (gamma + 1)
                for i in range(setting.Repeating_number):
                    dynamics_result = self.kfinter_dynamics.interconnected_dynamics_100steps_result_only(setting, inter_layer, prob_p, beta, node_i_name)
                    result_array = dynamics_result[1]
                    num_data_for_100steps = num_data_for_100steps + result_array
                Num_Data = num_data_for_100steps / setting.Repeating_number
                additional_array = self.mp.making_array_for_100steps(setting, Num_Data, gamma, beta)
                final_array = self.cal_property.making_array_for_property(additional_array, inter_layer, node_i_name)
                if line == 1:
                    total_data = final_array
                elif line > 1:
                    total_data = np.vstack([total_data, final_array])
        return total_data


    def repeat_dynamics(self, setting, inter_layer, prob_p, beta, node_i_name, fixed_node_state):
        num_data = np.zeros([setting.Limited_step + 1, 15])
        time = 0
        node_number = node_i_name.split('_')[1]
        if node_number != 'N':
            node_number = int(node_number)
            inter_layer.two_layer_graph.node[node_number]['state'] = fixed_node_state
        for i in range(setting.Repeating_number):
            time += 1
            dynamics_result = self.kfinter_dynamics.interconnected_dynamics(setting, inter_layer, prob_p, beta, node_i_name)
            # print(sorted(inter_layer.two_layer_graph.neighbors(0)))
            total_array = dynamics_result[1]
            num_data = num_data + total_array
        Num_Data = num_data / setting.Repeating_number
        panda_db = self.mp.making_dataframe_per_step(setting, Num_Data)
        panda_db = self.cal_property.making_df_for_property(panda_db, inter_layer, node_i_name)
        return panda_db


if __name__ == "__main__":
    print("RepeatDynamics")
    setting = Setting_Simulation_Value.Setting_Simulation_Value()
    print(setting.R, setting.D)
    inter_layer = InterconnectedLayerModeling.InterconnectedLayerModeling(setting)
    node_i_name = 'A_0'
    fixed_node_state = 1
    repeat = KFRepeatDynamics()
    result = repeat.repeat_dynamics_for_only_100steps(setting, inter_layer, node_i_name, fixed_node_state)
    print(result)
