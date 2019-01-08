import Setting_Simulation_Value
import RepeatDynamics

class Changing_Variable:
    def __init__(self):
        self.SS = Setting_Simulation_Value.Setting_Simulation_Value()
        self.repeat_dynamics = RepeatDynamics.RepeatDynamics()

    def changing_variable(self):
        for gamma in self.SS.R:
            for beta in self.SS.D:
                prob_p = gamma/(gamma+1)
                self.repeat_dynamics.repeat_dynamics(prob_p, beta)


if __name__ == "__main__":
    print("Changing_Variable")
    changing_variable = Changing_Variable()
    result = changing_variable.changing_variable()
    print(sum(result[0])/2048, sum(result[1])/2048)


