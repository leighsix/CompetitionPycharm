import numpy as np
import Setting_Simulation_Value
import OpinionDynamics
import DecisionDynamics
import Layer_A_Modeling
import Layer_B_Modeling


class InterconnectedDynamics:
    def __init__(self):
        self.SS = Setting_Simulation_Value.Setting_Simulation_Value()
        self.opinion = OpinionDynamics.OpinionDynamics()
        self.decision = DecisionDynamics.DecisionDynamics()

    def interconnected_dynamics(self, layer_A, layer_B, prob_p, beta):
        step_number = 0
        while True:
            self.opinion.A_layer_dynamics(layer_A, layer_B, prob_p)
            self.decision.B_layer_dynamics(layer_A, layer_B, beta)
            step_number += 1
            if (((np.all(layer_A.A > 0) == 1) and (np.all(layer_B.B > 0) == 1)) or
                    ((np.all(layer_A.A < 0) == 1) and (np.all(layer_B.B < 0) == 1)) or
                    (step_number >= self.SS.Limited_step)):
                break
        return layer_A, layer_B


if __name__ == "__main__" :
    print("InterconnectedDynamics")
    Layer_A = Layer_A_Modeling.Layer_A_Modeling()
    Layer_B = Layer_B_Modeling.Layer_B_Modeling()
    prob_p = 0.5
    beta = 1.5
    inter_dynamics = InterconnectedDynamics()
    inter_dynamics.interconnected_dynamics(Layer_A, Layer_B, prob_p, beta)
    print(sum(Layer_A.A)/2048, sum(Layer_B.B)/2048)








