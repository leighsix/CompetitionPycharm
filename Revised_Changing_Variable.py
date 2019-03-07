import numpy as np
import Setting_Revised_Value
import MakingPandas
import RevisedRepeatDynamics
import sqlalchemy
from multiprocessing import Pool


class Revised_Changing_Variable:
    def __init__(self, setting):
        self.mp = MakingPandas.MakingPandas()
        self.revised_repeat_dynamics = RevisedRepeatDynamics.RevisedRepeatDynamics(setting)

    def calculate_and_input_database(self, setting_variable_tuple):
        self.revised_repeat_dynamics.repeat_dynamics(setting_variable_tuple[0], setting_variable_tuple[1])
        panda_db = self.mp.making_dataframe_per_step(setting_variable_tuple[0], self.revised_repeat_dynamics.Num_Data)
        print(panda_db.loc[0])
        panda_db['beta'] = setting_variable_tuple[1]
        engine = sqlalchemy.create_engine('mysql+pymysql://root:2853@localhost:3306/renew_competition')
        panda_db.to_sql(name='revised_initial_state', con=engine, index=False, if_exists='append')
        print(panda_db.loc[0])  # 프로그램 잘 실행되고 있는지 확인을 위해서 프린트 실시
        self.revised_repeat_dynamics.num_data = np.zeros([setting_variable_tuple[0].Limited_step+1, 11])
        self.revised_repeat_dynamics.Num_Data = np.zeros([setting_variable_tuple[0].Limited_step+1, 11])

    def paralleled_work(self, setting):
        workers = setting.workers
        setting_variable_list = []
        for i in setting.D:
            setting_variable_list.append((setting, i))
        with Pool(workers) as p:
            p.map(self.calculate_and_input_database, setting_variable_list)

if __name__ == "__main__":
    print("Changing_Variable")
    setting = Setting_Revised_Value.Setting_Revised_Value()
    revised_changing_variable = Revised_Changing_Variable(setting)
    revised_changing_variable.paralleled_work(setting)
    print("Operating end")



    #def paralleled_work(self):
    #    workers = self.SS.workers
    #    variable_list = self.SS.variable_list
    #    with concurrent.futures.ProcessPoolExecutor(workers) as executor:
    #          executor.map(self.calculate_and_input_database, variable_list)
