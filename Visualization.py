import SelectDB
import Setting_Simulation_Value
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sympy import *
from mpl_toolkits.mplot3d.axes3d import *


class Visualization:
    def __init__(self):
        self.select_db = SelectDB.SelectDB()
        self.SS = Setting_Simulation_Value.Setting_Simulation_Value()

    def plot_2D_gamma_for_average_state(self, table, beta_value):
        df = self.select_db.select_data_from_DB(table)
        beta_list = self.select_db.making_select_list(table, 'beta')
        temp_value = Visualization.covert_to_select_list_value(beta_list, beta_value)
        df = df[df.Steps == self.SS.Limited_step]
        df = df[df.beta == temp_value]
        plt.figure()
        sns.set_style("whitegrid")
        plt.plot(df['gamma'], (df['LAYER_A_MEAN'] + df['LAYER_B_MEAN']), '-', label='beta=%s' % temp_value)
        plt.legend(framealpha=1, frameon=True)
        plt.ylim(-3.3, 3.3)
        plt.xlabel('gamma')
        plt.ylabel('Average States')
        plt.show()

    def plot_2D_beta_for_average_state(self, table, gamma_value):
        df = self.select_db.select_data_from_DB(table)
        gamma_list = self.select_db.making_select_list(table, 'gamma')
        temp_value = Visualization.covert_to_select_list_value(gamma_list, gamma_value)
        df = df[df.Steps == self.SS.Limited_step]
        df = df[df.gamma == temp_value]
        plt.figure()
        sns.set_style("whitegrid")
        plt.plot(df['beta'], (df['LAYER_A_MEAN'] + df['LAYER_B_MEAN']), '-', label='gamma=%s' % temp_value)
        plt.legend(framealpha=1, frameon=True)
        plt.ylim(-3.3, 3.3)
        plt.xlabel('beta')
        plt.ylabel('Average States')
        plt.show()

    def plot_3D_trisurf_for_average_state(self, table):
        df = self.select_db.select_data_from_DB(table)
        df2 = df[df.Steps == self.SS.Limited_step]
        sns.set_style("whitegrid")
        plt.figure()
        ax = plt.axes(projection='3d')
        ax.plot_trisurf(df2['beta'], df2['gamma'], (df2['LAYER_A_MEAN'] + df2['LAYER_B_MEAN']),
                        cmap='RdBu', edgecolor='none')
        ax.set_xlabel('beta')
        ax.set_ylabel('gamma')
        ax.set_zlabel('Average States')
        ax.set_title('beta-gamma-States')
        ax.view_init(45, 45)
        plt.show()


    def plot_3D_scatter_for_average_state(self, table):
        df = self.select_db.select_data_from_DB(table)
        df2 = df[df.Steps == self.SS.Limited_step]
        sns.set_style("whitegrid")
        plt.figure()
        ax = plt.axes(projection='3d')
        ax.scatter(df2['beta'], df2['gamma'], (df2['LAYER_A_MEAN'] + df2['LAYER_B_MEAN']),
                        c =(df2['LAYER_A_MEAN'] + df2['LAYER_B_MEAN']), cmap='RdBu', linewidth = 0.2)
        ax.set_xlabel('beta')
        ax.set_ylabel('gamma')
        ax.set_zlabel('Average States')
        ax.set_title('beta-gamma-States')
        ax.view_init(45, 45)
        plt.show()

    def plot_3D_contour_for_average_state(self, table):
        df = self.select_db.select_data_from_DB(table)
        df = df[df.Steps == self.SS.Limited_step]
        sns.set_style("whitegrid")
        beta_list = list(self.select_db.making_select_list(table, 'beta'))  # list이지만 실제로는 array
        gamma_list = list(self.select_db.making_select_list(table, 'gamma'))
        state_list = np.array(df['LAYER_A_MEAN'] + df['LAYER_B_MEAN'])
        result_beta = sorted(beta_list * len(gamma_list))
        result_gamma = sorted(gamma_list * len(beta_list))
        X, Y = np.meshgrid(result_beta, result_gamma)
        Z = Visualization.contour_Z_function(beta_list, gamma_list, state_list)
        plt.figure()
        ax = plt.axes(projection='3d')
        ax.contour3D(X, Y, Z, 50, cmap='RdBu')
        ax.set_xlabel('beta')
        ax.set_ylabel('gamma')
        ax.set_zlabel('Average States')
        ax.set_title('beta-gamma-States')
        ax.view_init(45, 45)
        plt.show()

    def plot_3D_to_2D_contour_for_average_state(self, table):
        df = self.select_db.select_data_from_DB(table)
        df = df[df.Steps == self.SS.Limited_step]
        sns.set_style("whitegrid")
        beta_list = list(self.select_db.making_select_list(table, 'beta'))  # list이지만 실제로는 array
        gamma_list = list(self.select_db.making_select_list(table, 'gamma'))
        state_list = np.array(df['LAYER_A_MEAN'] + df['LAYER_B_MEAN'])
        result_beta = sorted(beta_list * len(gamma_list))
        result_gamma = sorted(gamma_list * len(beta_list))
        X, Y = np.meshgrid(result_beta, result_gamma)
        Z = Visualization.contour_Z_function(beta_list, gamma_list, state_list)
        plt.figure()
        sns.set()
        plt.contourf(X, Y, Z, 50, cmap='RdBu')
        plt.xlabel('beta')
        plt.ylabel('gamma')
        plt.colorbar(label='Average states')
        plt.show()

    def flow_prob_beta_chart(self, table, beta_value, gamma_value):
        #beta_value = [min, max], #gamma_value =[min, max]
        df = self.select_db.select_data_from_DB(table)
        beta_list = self.select_db.making_select_list(table, 'beta')  # 이름은 list이지만 실제로는 array
        gamma_list = self.select_db.making_select_list(table, 'gamma') # 이름은 list이지만 실제로는 array
        beta_min = Visualization.covert_to_select_list_value(beta_list, beta_value[0])
        beta_max = Visualization.covert_to_select_list_value(beta_list, beta_value[1])
        gamma_min = Visualization.covert_to_select_list_value(gamma_list, gamma_value[0])
        gamma_max = Visualization.covert_to_select_list_value(gamma_list, gamma_value[1])
        df = df[df.beta >= beta_min]
        df = df[df.beta <= beta_max]
        df = df[df.gamma >= gamma_min]
        df = df[df.beta <= gamma_max]
        plt.figure()
        sns.set()
        for i in range(0, self.SS.Limited_step):
            df1 = df.loc[0 + (self.SS.Limited_step*i): (self.SS.Limited_step-1) + (self.SS.Limited_step*i)]
            plt.plot(df1['Steps'], df1['PROB_BETA'], linewidth=0.7)
        plt.ylabel('probability for layer B')
        plt.xlabel('time(step)')
        plt.show()

    def different_state_ratio_chart(self, table, beta_value, gamma_value, select_layer):
        df = self.select_db.select_data_from_DB(table)
        beta_list = self.select_db.making_select_list(table, 'beta')    # 이름은 list이지만 실제로는 array
        gamma_list = self.select_db.making_select_list(table, 'gamma')  # 이름은 list이지만 실제로는 array
        beta_min = Visualization.covert_to_select_list_value(beta_list, beta_value[0])
        beta_max = Visualization.covert_to_select_list_value(beta_list, beta_value[1])
        gamma_min = Visualization.covert_to_select_list_value(gamma_list, gamma_value[0])
        gamma_max = Visualization.covert_to_select_list_value(gamma_list, gamma_value[1])
        df = df[df.beta >= beta_min]
        df = df[df.beta <= beta_max]
        df = df[df.gamma >= gamma_min]
        df = df[df.beta <= gamma_max]
        plt.figure()
        sns.set()
        for i in range(0, self.SS.Limited_step):
            df1 = df.loc[0 + (self.SS.Limited_step*i): (self.SS.Limited_step-1) + (self.SS.Limited_step*i)]
            plt.plot(df1['Steps'], df1['%s_DIFFERENT_STATE_RATIO'%select_layer], linewidth=0.7)
        plt.ylabel('different state ratio for layer %s'%select_layer)
        plt.xlabel('time(step)')
        plt.show()

    @staticmethod
    def contour_Z_function(beta_list, gamma_list, state_list ):
        if len(state_list) == len(gamma_list) * len(beta_list):
            state_list = state_list.reshape(len(gamma_list), len(beta_list))
        elif len(state_list) != len(gamma_list) * len(beta_list):
            state_list = list(state_list)
            for i in range((len(gamma_list) * len(beta_list)) - len(state_list)):
                state_list.append(0*i)
            state_list = np.array(state_list)
            state_list = state_list.reshape(len(gamma_list), len(beta_list))
        Z = np.zeros([len(beta_list) * len(gamma_list), len(beta_list) * len(gamma_list)])
        for i in range(0, len(gamma_list)):
            for j in range(0, len(beta_list)):
                for k in range(0, len(beta_list)):
                    for l in range(0, len(gamma_list)):
                        Z[(i * len(beta_list)) + k][(j * len(gamma_list)) + l] = state_list[i][j]
        return Z

    @staticmethod
    def covert_to_select_list_value(select_list, input_value):  # list가 만들어져 있는 곳에 사용
        loc = sum(select_list <= input_value)  # select_list는 making_select_list를 사용, array로 만들어져 있음
        temp_value = select_list[loc - 1][0]
        return temp_value[0]

if __name__ == "__main__":
    print("Visualization")
    visualization = Visualization()
    visualization.plot_3D_to_2D_contour_for_average_state('average_layer_state')
    #visualization.plot_3D_contour_for_average_state('average_layer_state')
    #visualization.plot_3D_scatter_for_average_state('average_layer_state')    #previous_research
    #visualization.plot_3D_trisurf_for_average_state('previous_research')
    #visualization.plot_2D_beta_for_average_state('previous_research', 0.2)
    #visualization.plot_2D_beta_for_average_state('previous_research', 0.4)
    #visualization.plot_2D_beta_for_average_state('previous_research', 0.6)

    print("paint finished")
