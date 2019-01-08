import Setting_Simulation_Value
import InterconnectedDynamics
import Layer_A_Modeling
import Layer_B_Modeling


class RepeatDynamics:
    def __init__(self):
        self.SS = Setting_Simulation_Value.Setting_Simulation_Value()
        self.inter_dynamics = InterconnectedDynamics.InterconnectedDynamics()

    def repeat_dynamics(self, prob_p, beta):
        for i in range(self.SS.Repeating_number):
            layer_A = Layer_A_Modeling.Layer_A_Modeling()
            layer_B = Layer_B_Modeling.Layer_B_Modeling()
            self.inter_dynamics.interconnected_dynamics(layer_A, layer_B, prob_p, beta)
            # 데이터 베이스 저장 함수 들어가기(평균내는 함수)


if __name__ == "__main__":
    print("RepeatDynamics")
    prob_p = 0.1
    beta = 1.5
    repeat = RepeatDynamics()
    repeat.repeat_dynamics(prob_p, beta)
    # print(sum(result[0])/2048, sum(result[1])/2048)
    print("Operating end")
