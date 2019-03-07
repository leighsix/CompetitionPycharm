import numpy as np
import Setting_Simulation_Value
import MakingPandas
import RevisedRepeatDynamics
import sqlalchemy
from multiprocessing import Pool
from numba import jit


class Revised_Variable:
    def __init__(self, setting):
        self.mp = MakingPandas.MakingPandas()
        self.repeat_dynamics = RevisedRepeatDynamics.RevisedRepeatDynamics(setting)

    def calculate_and_input_database(self, setting_variable_tuple):
        gamma = setting_variable_tuple[1][0]
        beta = setting_variable_tuple[1][1]
        print(gamma, beta)  # 프로그램 잘 실행되고 있는지 확인을 위해서 프린트 실시
        prob_p = gamma / (gamma + 1)
        self.repeat_dynamics.repeat_dynamics(setting_variable_tuple[0], prob_p, beta)
        panda_db = self.mp.making_dataframe_per_step(setting_variable_tuple[0], self.repeat_dynamics.Num_Data)
        print(panda_db.loc[0])
        panda_db['gamma'] = gamma
        panda_db['beta'] = beta
        engine = sqlalchemy.create_engine('mysql+pymysql://root:2853@localhost:3306/renew_competition')
        panda_db.to_sql(name='average_layer_state', con=engine, index=False, if_exists='append')
        print(panda_db.loc[0])  # 프로그램 잘 실행되고 있는지 확인을 위해서 프린트 실시
        self.repeat_dynamics.num_data = np.zeros([setting_variable_tuple[0].Limited_step+1, 11])
        self.repeat_dynamics.Num_Data = np.zeros([setting_variable_tuple[0].Limited_step+1, 11])

    def paralleled_work(self, setting):
        workers = setting.workers
        setting_variable_list = []
        for i in setting.variable_list:
            setting_variable_list.append((setting, i))
        with Pool(workers) as p:
            p.map(self.calculate_and_input_database, setting_variable_list)

if __name__ == "__main__":
    print("Changing_Variable")
    setting = Setting_Simulation_Value.Setting_Simulation_Value()
    changing_variable = Revised_Variable(setting)
    changing_variable.paralleled_work(setting)
    print("Operating end")



    #def paralleled_work(self):
    #    workers = self.SS.workers
    #    variable_list = self.SS.variable_list
    #    with concurrent.futures.ProcessPoolExecutor(workers) as executor:
    #          executor.map(self.calculate_and_input_database, variable_list)
