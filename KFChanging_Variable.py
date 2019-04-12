import numpy as np
import Setting_Simulation_Value
import KFRepeatDynamics
import sqlalchemy
from multiprocessing import Pool


class KFChanging_Variable:
    def __init__(self, setting):
        self.kfrepeat_dynamics = KFRepeatDynamics.KFRepeatDynamics(setting)

    def calculate_and_input_database(self, setting_variable_tuple):
        gamma = setting_variable_tuple[1][0]
        beta = setting_variable_tuple[1][1]
        print(gamma, beta)  # 프로그램 잘 실행되고 있는지 확인을 위해서 프린트 실시
        prob_p = gamma / (gamma + 1)
        node_list_A = self.making_node_list_A(setting)
        for i in node_list_A:
            panda_db = self.kfrepeat_dynamics.repeat_dynamics(setting_variable_tuple[0], prob_p, beta, i)
            panda_db['gamma'] = gamma
            panda_db['beta'] = beta
            print(panda_db.loc[0])
            engine = sqlalchemy.create_engine('mysql+pymysql://root:2853@localhost:3306/%s' % setting_variable_tuple[0].database)
            panda_db.to_sql(name='%s' % setting_variable_tuple[0].table, con=engine, index=False, if_exists='append')
            print(panda_db.loc[0])  # 프로그램 잘 실행되고 있는지 확인을 위해서 프린트 실시

    def paralleled_work(self, setting):
        workers = setting.workers
        setting_variable_list = []
        for i in setting.variable_list:
            setting_variable_list.append((setting, i))
        with Pool(workers) as p:
            p.map(self.calculate_and_input_database, setting_variable_list)


    def making_node_list_A(self, setting):
        node_list = [0]
        for i in range(setting.A_node):
            node_i_name = 'A_%s' %i
            node_list.append(node_i_name)
        return node_list

    def making_node_list_B(self, setting):
        node_list = [0]
        for i in range(setting.B_node):
            node_i_name = 'B_%s' %i
            node_list.append(node_i_name)
        return node_list






if __name__ == "__main__":
    print("Changing_Variable")
    setting = Setting_Simulation_Value.Setting_Simulation_Value()
    changing_variable = KFChanging_Variable(setting)
    print(changing_variable.making_node_list_A(setting))
    #changing_variable.paralleled_work(setting)
    print("Operating end")



    #def paralleled_work(self):
    #    workers = self.SS.workers
    #    variable_list = self.SS.variable_list
    #    with concurrent.futures.ProcessPoolExecutor(workers) as executor:
    #          executor.map(self.calculate_and_input_database, variable_list)
