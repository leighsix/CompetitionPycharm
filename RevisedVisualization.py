import RevisedSelectDB
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


class RevisedVisualization:
    def plot_2D_beta_for_average_state(self, setting, df):
        df = df[df.Steps == setting.Limited_step]
        plt.style.use('seaborn-whitegrid')
        plt.plot(df['beta'], (df['LAYER_A_MEAN'] + df['LAYER_B_MEAN']), 'o',
                 markersize=5, linewidth=2, markeredgewidth=1)

    def plot_3D_scatter_for_average_state(self, setting, df):
        df = df[df.Steps == setting.Limited_step]
        ax = plt.axes(projection='3d')
        ax.scatter(df['beta'], df['PROB_P'], (df['LAYER_A_MEAN'] + df['LAYER_B_MEAN']),
                   c=(df['LAYER_A_MEAN'] + df['LAYER_B_MEAN']), cmap='RdBu', linewidth=0.2)
        ax.set_xlabel(r'$\beta$', fontsize=18, labelpad=8)
        ax.set_ylabel('PROB_P', fontsize=18, labelpad=8)
        ax.set_zlabel('Average States', fontsize=18, labelpad=8)
        ax.set_title(r'$\beta$-PROB_P-States', fontsize=18)
        ax.tick_params(axis='both', labelsize=14)
        ax.view_init(45, 45)


    def plot_3D_trisurf_for_average_state(self, setting, df):
        df = df[df.Steps == setting.Limited_step]
        ax = plt.axes(projection='3d')
        ax.plot_trisurf(df['beta'], df['PROB_P'], (df['LAYER_A_MEAN'] + df['LAYER_B_MEAN']),
                        cmap='RdBu', edgecolor='none')
        ax.set_xlabel(r'$\beta$', fontsize=18, labelpad=8)
        ax.set_ylabel('PROB_P', fontsize=18, labelpad=8)
        ax.set_zlabel('Average States', fontsize=18, labelpad=8)
        ax.set_title(r'$\beta$-PROB_P-States', fontsize=18)
        ax.tick_params(axis='both', labelsize=14)
        ax.view_init(45, 45)

    def plot_3D_contour_for_average_state(self, setting, df):
        df = df[df.Steps == setting.Limited_step]
        beta_list = RevisedVisualization.making_select_list(df, 'beta')  # list이지만 실제로는 array
        prob_p_list = RevisedVisualization.making_select_list(df, 'PROB_P')
        X, Y = np.meshgrid(beta_list, prob_p_list)
        Z = RevisedVisualization.state_list_function(df, prob_p_list, beta_list)
        ax = plt.axes(projection='3d')
        ax.contour3D(X, Y, Z, 50, cmap='RdBu')
        ax.set_xlabel(r'$\beta$', fontsize=18, labelpad=6)
        ax.set_ylabel('PROB_P', fontsize=18, labelpad=6)
        ax.set_zlabel('Average States', fontsize=18, labelpad=6)
        ax.set_title(r'$\beta$-PROB_P-States', fontsize=18)
        ax.view_init(45, 45)

    def plot_3D_to_2D_contour_for_average_state(self, setting, df):
        df = df[df.Steps == setting.Limited_step]
        beta_list = RevisedVisualization.making_select_list(df, 'beta')  # list이지만 실제로는 array
        prob_p_list = RevisedVisualization.making_select_list(df, 'PROB_P')
        X, Y = np.meshgrid(beta_list, prob_p_list)
        Z = RevisedVisualization.state_list_function(df, prob_p_list, beta_list)
        plt.contourf(X, Y, Z, 50, cmap='RdBu')
        #plt.clabel(contours, inline=True, fontsize=8)

    def flow_prob_beta_chart(self, setting, df, beta_value):
        #beta_value = [min, max], #gamma_value =[min, max]
        df = df[df.Steps <= setting.Limited_step]
        beta_list = RevisedVisualization.making_select_list(df, 'beta')  # 이름은 list이지만 실제로는 array
        beta_min = RevisedVisualization.covert_to_select_list_value(beta_list, beta_value[0])
        beta_max = RevisedVisualization.covert_to_select_list_value(beta_list, beta_value[1])
        df = df[df.beta >= beta_min]
        df = df[df.beta <= beta_max]
        beta_array = pd.DataFrame(df['beta'])
        beta_array = np.array(beta_array.drop_duplicates())
        for i in sorted(beta_array):
            df1 = df[df.beta == i[0]]
            if len(df1) >= setting.Limited_step:
                plt.plot(df1['Steps'], df1['PROB_BETA'], linewidth=0.3)

    def different_state_ratio_chart(self, setting, df, beta_value, select_layer):
        df = df[df.Steps <= setting.Limited_step]
        beta_list = RevisedVisualization.making_select_list(df, 'beta')    # 이름은 list이지만 실제로는 array
        beta_min = RevisedVisualization.covert_to_select_list_value(beta_list, beta_value[0])
        beta_max = RevisedVisualization.covert_to_select_list_value(beta_list, beta_value[1])
        df = df[df.beta >= beta_min]
        df = df[df.beta <= beta_max]
        beta_array = pd.DataFrame(df['beta'])
        beta_array = np.array(beta_array.drop_duplicates())
        for i in sorted(beta_array) :
            df1 = df[df.beta == i[0]]
            if len(df1) >= setting.Limited_step:
                plt.plot(df1['Steps'], df1['%s_DIFFERENT_STATE_RATIO' % select_layer], linewidth=0.7)

    def total_different_state_ratio_chart(self, setting, df, beta_value):
        df = df[df.Steps <= setting.Limited_step]
        beta_list = RevisedVisualization.making_select_list(df, 'beta')    # 이름은 list이지만 실제로는 array
        beta_min = RevisedVisualization.covert_to_select_list_value(beta_list, beta_value[0])
        beta_max = RevisedVisualization.covert_to_select_list_value(beta_list, beta_value[1])
        df = df[df.beta >= beta_min]
        df = df[df.beta <= beta_max]
        beta_array = pd.DataFrame(df['beta'])
        beta_array = np.array(beta_array.drop_duplicates())
        for i in sorted(beta_array):
            df1 = df[df.beta == i[0]]
            if len(df1) >= setting.Limited_step:
                plt.plot(df1['Steps'], abs(df1['A_DIFFERENT_STATE_RATIO'])+abs(df1['B_DIFFERENT_STATE_RATIO']), linewidth=0.7)

    @staticmethod
    def state_list_function(df, A_list, B_list):
        Z = np.zeros([len(A_list), len(B_list)])
        for i, prob_p in enumerate(A_list):
            for j, beta in enumerate(B_list):
                df1 = df[df.PROB_P == prob_p]
                df2 = df1[df1.beta == beta]
                if len(df2) == 0:
                     Z[i][j] = 0
                else:
                    Z[i][j] = df2['LAYER_A_MEAN'].iloc[0] + df2['LAYER_B_MEAN'].iloc[0]
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
    setting.database = 'competition'
    setting.table = 'result_db'
    visualization = RevisedVisualization()
    fig = plt.figure()
    # visualization.plot_2D_gamma_for_average_state(0.5)
    # plt.show()
    # setting.database = 'competition'
    # setting.table ='result3'
    # setting.Limited_step = 30
    # visualization = Visualization(setting)
    visualization.plot_3D_trisurf_for_average_state(setting)
    #visualization.plot_3D_to_2D_contour_for_average_state()
    #visualization.plot_3D_contour_for_average_state('previous_research')
    #visualization.plot_3D_scatter_for_average_state('average_layer_state')    #previous_research
    # fig = visualization.flow_prob_beta_chart([0, 3], [0, 2])
    # fig = visualization.different_state_ratio_chart([0, 3], [0, 2], 'B')
    # visualization.plot_2D_beta_for_average_state(0.2)
    # visualization.plot_2D_beta_for_average_state(0.4)
    plt.show()
    plt.close()
    #visualization.plot_2D_beta_for_average_state('previous_research', 0.4)
    #visualization.plot_2D_beta_for_average_state('previous_research', 0.6)
    print("paint finished")