import numpy as np
import Setting_Simulation_Value
import MakingPandas
import RepeatDynamics
import sqlalchemy


class Changing_Variable:
    def __init__(self):
        self.SS = Setting_Simulation_Value.Setting_Simulation_Value()
        self.mp = MakingPandas.MakingPandas()
        self.repeat_dynamics = RepeatDynamics.RepeatDynamics()

    def changing_variable(self):
        for gamma in self.SS.R:
            for beta in self.SS.D:
                prob_p = gamma/(gamma+1)
                self.repeat_dynamics.repeat_dynamics(prob_p, beta)
                panda_db = self.mp.making_dataframe_per_step(self.repeat_dynamics.Num_Data)
                panda_db['gamma'] = gamma
                panda_db['beta'] = beta
                engine = sqlalchemy.create_engine('mysql+pymysql://root:2853@localhost:3306/renew_competition')
                panda_db.to_sql(name='average_layer_state', con=engine, index=False, if_exists='append')
                print(panda_db.loc[0])   # 프로그램 잘 실행되고 있는지 확인을 위해서 프린트 실시
                self.repeat_dynamics.num_data = np.zeros([30, 11])
                self.repeat_dynamics.Num_Data = np.zeros([30, 11])


if __name__ == "__main__":
    print("Changing_Variable")
    changing_variable = Changing_Variable()
    changing_variable.changing_variable()
    print("Operating end")


