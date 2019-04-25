import SelectDB
import numpy as np
import Setting_Simulation_Value
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import pandas as pd
from sympy import *
from mpl_toolkits.mplot3d.axes3d import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from numba import jit
matplotlib.use("TkAgg")


class Visualization:

    def plot_2D_gamma_for_average_state(self, setting, df, beta_value, marker):
        beta_list = Visualization.making_select_list(df, 'beta')
        temp_value = Visualization.covert_to_select_list_value(beta_list, beta_value)
        df = df[df.Steps == setting.Limited_step]
        df = df[df.beta == temp_value]
        plt.plot(df['gamma'], ((df['LAYER_A_MEAN']/setting.MAX) + df['LAYER_B_MEAN']) / 2, marker,
                 label=r'$\beta$=%.2f' % temp_value,
                 markersize=6, linewidth=1.5, markeredgewidth=1)

    def plot_2D_beta_for_average_state(self, setting, df, gamma_value, marker):
        gamma_list = Visualization.making_select_list(df, 'gamma')
        temp_value = Visualization.covert_to_select_list_value(gamma_list, gamma_value)
        df = df[df.Steps == setting.Limited_step]
        df = df[df.gamma == temp_value]
        plt.style.use('seaborn-whitegrid')
        plt.plot(df['beta'], ((df['LAYER_A_MEAN']/setting.MAX) + df['LAYER_B_MEAN']) / 2, marker,
                 label=r'$\gamma$=%.2f' % temp_value,
                 markersize=6, linewidth=1.5, markeredgewidth=1)

    def plot_3D_scatter_for_average_state(self, df):
        ax = plt.axes(projection='3d')
        ax.scatter(df['beta'], df['gamma'], ((df['LAYER_A_MEAN']/setting.MAX) + df['LAYER_B_MEAN']) / 2,
                   c=((df['LAYER_A_MEAN']/setting.MAX) + df['LAYER_B_MEAN']) / 2, cmap='RdBu', linewidth=0.2)
        ax.set_xlabel(r'$\beta$', fontsize=18, labelpad=8)
        ax.set_ylabel(r'$\gamma$', fontsize=18, labelpad=8)
        ax.set_zlabel('AS', fontsize=18, labelpad=8)
        ax.set_title(r'$\beta$-$\gamma$-AS', fontsize=18)
        ax.tick_params(axis='both', labelsize=14)
        ax.view_init(45, 45)


    def plot_3D_trisurf_for_average_state(self, df):
        ax = plt.axes(projection='3d')
        ax.plot_trisurf(df['beta'], df['gamma'], ((df['LAYER_A_MEAN']/setting.MAX) + df['LAYER_B_MEAN']) / 2,
                        cmap='RdBu', edgecolor='none')
        ax.set_xlabel(r'$\beta$', fontsize=18, labelpad=8)
        ax.set_ylabel(r'$\gamma$', fontsize=18, labelpad=8)
        ax.set_zlabel('AS', fontsize=18, labelpad=8)
        ax.set_title(r'$\beta$-$\gamma$-AS', fontsize=18)
        ax.tick_params(axis='both', labelsize=14)
        ax.view_init(45, 45)

    def plot_3D_contour_for_average_state(self, setting, df):
        beta_list = Visualization.making_select_list(df, 'beta')  # list이지만 실제로는 array
        gamma_list = Visualization.making_select_list(df, 'gamma')
        X, Y = np.meshgrid(beta_list, gamma_list)
        Z = Visualization.state_list_function(setting, df, gamma_list, beta_list)
        ax = plt.axes(projection='3d')
        ax.contour3D(X, Y, Z, 50, cmap='RdBu')
        ax.set_xlabel(r'$\beta$', fontsize=18, labelpad=6)
        ax.set_ylabel(r'$\gamma$', fontsize=18, labelpad=6)
        ax.set_zlabel('AS', fontsize=18, labelpad=6)
        ax.set_title(r'$\beta$-$\gamma$-AS', fontsize=18)
        ax.view_init(45, 45)

    def plot_3D_to_2D_contour_for_average_state(self, setting, df):
        # df = df[df.Steps == setting.Limited_step]
        beta_list = Visualization.making_select_list(df, 'beta')  # list이지만 실제로는 array
        gamma_list = Visualization.making_select_list(df, 'gamma')
        X, Y = np.meshgrid(beta_list, gamma_list)
        Z = Visualization.state_list_function(setting, df, gamma_list, beta_list)
        plt.contourf(X, Y, Z, 50, cmap='RdBu')
        #plt.clabel(contours, inline=True, fontsize=8)


    def average_state_for_steps(self, setting, df, beta_value, gamma_value):
        beta_list = Visualization.making_select_list(df, 'beta')    # 이름은 list이지만 실제로는 array
        gamma_list = Visualization.making_select_list(df, 'gamma')  # 이름은 list이지만 실제로는 array
        beta_min = Visualization.covert_to_select_list_value(beta_list, beta_value[0])
        beta_max = Visualization.covert_to_select_list_value(beta_list, beta_value[1])
        gamma_min = Visualization.covert_to_select_list_value(gamma_list, gamma_value[0])
        gamma_max = Visualization.covert_to_select_list_value(gamma_list, gamma_value[1])
        df = df[df.gamma >= gamma_min]
        df = df[df.gamma <= gamma_max]
        df = df[df.beta >= beta_min]
        df = df[df.beta <= beta_max]
        gamma_array = pd.DataFrame(df['gamma'])
        gamma_array = np.array(gamma_array.drop_duplicates())
        beta_array = pd.DataFrame(df['beta'])
        beta_array = np.array(beta_array.drop_duplicates())
        for i in sorted(gamma_array):
            for j in beta_array:
                df1 = df[df.gamma == i[0]]
                df2 = df1[df1.beta == j[0]]
                if len(df2) >= setting.Limited_step:
                    plt.plot(df['Steps'], ((df['LAYER_A_MEAN']/setting.MAX) + df['LAYER_B_MEAN']) / 2, linewidth=0.3)



    def flow_prob_beta_chart(self, setting, df, beta_value, gamma_value):
        # beta_value = [min, max], #gamma_value =[min, max]
        # df = df[df.Steps <= setting.Limited_step]
        beta_list = Visualization.making_select_list(df, 'beta')  # 이름은 list이지만 실제로는 array
        gamma_list = Visualization.making_select_list(df, 'gamma')  # 이름은 list이지만 실제로는 array
        beta_min = Visualization.covert_to_select_list_value(beta_list, beta_value[0])
        beta_max = Visualization.covert_to_select_list_value(beta_list, beta_value[1])
        gamma_min = Visualization.covert_to_select_list_value(gamma_list, gamma_value[0])
        gamma_max = Visualization.covert_to_select_list_value(gamma_list, gamma_value[1])
        df = df[df.gamma >= gamma_min]
        df = df[df.gamma <= gamma_max]
        df = df[df.beta >= beta_min]
        df = df[df.beta <= beta_max]
        gamma_array = pd.DataFrame(df['gamma'])
        gamma_array = np.array(gamma_array.drop_duplicates())
        beta_array = pd.DataFrame(df['beta'])
        beta_array = np.array(beta_array.drop_duplicates())
        for i in sorted(gamma_array):
            for j in beta_array:
                df1 = df[df.gamma == i[0]]
                df2 = df1[df1.beta == j[0]]
                if len(df2) >= setting.Limited_step :
                    plt.plot(df2['Steps'], df2['PROB_BETA'], linewidth=0.3)

    def different_state_ratio_chart(self, setting, df, beta_value, gamma_value, select_layer):
        # df = df[df.Steps <= setting.Limited_step]
        beta_list = Visualization.making_select_list(df, 'beta')    # 이름은 list이지만 실제로는 array
        gamma_list = Visualization.making_select_list(df, 'gamma')  # 이름은 list이지만 실제로는 array
        beta_min = Visualization.covert_to_select_list_value(beta_list, beta_value[0])
        beta_max = Visualization.covert_to_select_list_value(beta_list, beta_value[1])
        gamma_min = Visualization.covert_to_select_list_value(gamma_list, gamma_value[0])
        gamma_max = Visualization.covert_to_select_list_value(gamma_list, gamma_value[1])
        df = df[df.gamma >= gamma_min]
        df = df[df.gamma <= gamma_max]
        df = df[df.beta >= beta_min]
        df = df[df.beta <= beta_max]
        gamma_array = pd.DataFrame(df['gamma'])
        gamma_array = np.array(gamma_array.drop_duplicates())
        beta_array = pd.DataFrame(df['beta'])
        beta_array = np.array(beta_array.drop_duplicates())
        for i in sorted(gamma_array):
            for j in beta_array:
                df1 = df[df.gamma == i[0]]
                df2 = df1[df1.beta == j[0]]
                if len(df2) >= setting.Limited_step:
                    plt.plot(df2['Steps'], df2['%s_DIFFERENT_STATE_RATIO' % select_layer], linewidth=0.7)

    @staticmethod
    def state_list_function(setting, df, gamma_list, beta_list):
        Z = np.zeros([len(gamma_list), len(beta_list)])
        for i, gamma in enumerate(gamma_list):
            for j, beta in enumerate(beta_list):
                df1 = df[df.gamma == gamma]
                df2 = df1[df1.beta == beta]
                if len(df2) == 0:
                     Z[i][j] = 0
                else:
                    Z[i][j] = ((df2['LAYER_A_MEAN'].iloc[0]/setting.MAX) + df2['LAYER_B_MEAN'].iloc[0]) / 2
        return Z

    @staticmethod
    def covert_to_select_list_value(select_list, input_value):  # list가 만들어져 있는 곳에 사용
        loc = sum(select_list <= input_value)  # select_list는 making_select_list를 사용, array로 만들어져 있음
        temp_value = select_list[loc - 1]
        return temp_value

    @staticmethod
    def making_select_list(df, list_name):
        list = []
        df = pd.DataFrame(df[list_name])
        select_list = np.array(df.drop_duplicates())
        for i in range(len(select_list)):
            list.append(select_list[i][0])
        return np.array(sorted(list))

if __name__ == "__main__":
    print("Visualization")
    setting = Setting_Simulation_Value.Setting_Simulation_Value()
    setting.database = 'paper_revised_data'
    setting.table = 'simulation_table2'
    select_db = SelectDB.SelectDB()
    df = select_db.select_data_from_DB(setting)
    print(len(df))
    # df = df[df.Unchanged_A_Node == 'A_95']
    df = df[df.Steps == 100]
    print(len(df))
    df = df[df.MODEL == 'RR(5)-RR(2)']
    print(len(df))
    # df = df[df.Unchanged_A_Node == 'A_N']
    visualization = Visualization()
    fig = plt.figure()
    visualization.plot_3D_trisurf_for_average_state(df)
    plt.show()
    plt.close()
    #visualization.plot_3D_to_2D_contour_for_average_state(setting, df)
    #visualization.plot_3D_to_2D_contour_for_average_state()
    #visualization.plot_3D_contour_for_average_state('previous_research')
    #visualization.plot_3D_scatter_for_average_state('average_layer_state')    #previous_research
    # fig = visualization.flow_prob_beta_chart([0, 3], [0, 2])
    # fig = visualization.different_state_ratio_chart([0, 3], [0, 2], 'B')
    # visualization.plot_2D_beta_for_average_state(0.2)
    # visualization.plot_2D_beta_for_average_state(0.4)

    #visualization.plot_2D_beta_for_average_state('previous_research', 0.4)
    #visualization.plot_2D_beta_for_average_state('previous_research', 0.6)
    print("paint finished")