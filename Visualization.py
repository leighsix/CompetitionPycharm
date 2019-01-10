import SelectDB
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sympy import *
import numpy as np
from mplimport mplot3d


class Visualization:
    def __init__(self):
        self.select_db = SelectDB.SelectDB()

    def making_select_list(self, table, step, list_name):
        df = self.select_db.select_data_from_DB(table)
        df = df[df.Steps == step]
        df = pd.DataFrame(df[list_name])
        select_list = np.array(df.drop_duplicates())
        np.sort(select_list)
        return select_list

    def plot_2D_gamma_for_average_state(self, table, step, beta_value):
        df = self.select_db.select_data_from_DB(table)
        beta_list = self.making_select_list(table, step, 'beta')
        loc = sum(beta_list <= beta_value)[0]
        temp_value = beta_list[loc][0]
        df = df[df.Steps == step]
        df = df[df.beta == temp_value]
        plt.figure()
        sns.set_style("whitegrid")
        plt.plot(df['gamma'], (df['LAYER_A_MEAN'] + df['LAYER_B_MEAN']), '-', label='beta=%s' % temp_value)
        plt.legend(framealpha=1, frameon=True)
        plt.ylim(-3.3, 3.3)
        plt.xlabel('gamma')
        plt.ylabel('Average States')

    def plot_2D_beta_for_average_state(self, table, step, gamma_value):
        df = self.select_db.select_data_from_DB(table)
        gamma_list = self.making_select_list(table, step, 'gamma')
        loc = sum(gamma_list <= gamma_value)[0]
        temp_value = gamma_list[loc][0]
        df = df[df.Steps == step]
        df = df[df.gamma == temp_value]
        plt.figure()
        sns.set_style("whitegrid")
        plt.plot(df['beta'], (df['LAYER_A_MEAN'] + df['LAYER_B_MEAN']), '-', label='gamma=%s' % temp_value)
        plt.legend(framealpha=1, frameon=True)
        plt.ylim(-3.3, 3.3)
        plt.xlabel('beta')
        plt.ylabel('Average States')

    def plot_3D_trisurf_for_average_state(self, table, step):
        df = self.select_db.select_data_from_DB(table)
        df2 = df[df.Steps == step]
        sns.set_style("whitegrid")
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        ax.plot_trisurf(df2['beta'], df2['gamma'], (df2['LAYER_A_MEAN'] + df2['LAYER_B_MEAN']),
                        cmap='RdBu', edgecolor='none')
        ax.set_xlabel('beta')
        ax.set_ylabel('gamma')
        ax.set_zlabel('Average States')
        ax.set_title('beta-gamma-States')
        ax.view_init(45, 45)

    def plot_3D_contour_for_average_state(self, table, step):
        df = self.select_db.select_data_from_DB(table)
        df = df[df.Steps == step]
        sns.set_style("whitegrid")
        beta_list = list(self.making_select_list(table, step, 'beta'))  # list이지만 실제로는 array
        gamma_list = list(self.making_select_list(table, step, 'gamma'))
        state_list = np.array(df['LAYER_A_MEAN'] + df['LAYER_B_MEAN'])
        result_beta = sorted(beta_list * len(gamma_list))
        result_gamma = sorted(gamma_list * len(beta_list))
        X, Y = np.meshgrid(result_beta, result_gamma)
        Z = Visualization.contour_Z_function(beta_list, gamma_list, state_list)
        ax = plt.axes(projection='3d')
        ax.contour3D(X, Y, Z, 50, cmap='RdBu')
        ax.set_xlabel('beta')
        ax.set_ylabel('gamma')
        ax.set_zlabel('Average States')
        ax.set_title('beta-gamma-States')
        ax.view_init(45, 45)

    def plot_3D_to_2D_contour_for_average_state(self, table, step):
        df = self.select_db.select_data_from_DB(table)
        df = df[df.Steps == step]
        sns.set_style("whitegrid")
        beta_list = list(self.making_select_list(table, step, 'beta'))  # list이지만 실제로는 array
        gamma_list = list(self.making_select_list(table, step, 'gamma'))
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



    def flow_prob_beta_chart(self, table, step):
        plt.figure()
        sns.set()
        da = pd.read_pickle(filename)
        plt.plot(da, linewidth=0.2)
        plt.ylabel('probability for layer B')
        plt.xlabel('time(step)')


    def total_different_state_ratio_chart(filename, ylabel):
        plt.figure()
        sns.set()
        da = pd.read_pickle(filename)
        plt.plot(da, linewidth=0.2)
        plt.ylabel(ylabel)
        plt.xlabel('time(step)')


    def beta_scale_for_chart(filename, y_axis, a, b):  # 0 < a, b < 3
        plt.figure()
        sns.set()
        da = pd.read_pickle(filename)
        plt.ylim(-0.5, 0.5)
        plt.ylabel(y_axis)
        plt.xlabel('time(step)')
        beta_scale = da.columns.levels[0]
        min_beta = sum(beta_scale < a)
        max_beta = sum(beta_scale < b)
        for i in range(min_beta, max_beta):
            pic = da[beta_scale[i]]
            plt.plot(pic, linewidth=0.3)




    def ganma_scale_for_chart(filename, y_axis, a, b):  # 0 < a, b < 3
        plt.figure()
        sns.set()
        da = pd.read_pickle(filename)
        unstack = da.unstack()
        reset = unstack.reset_index(name='different_state')
        Reset = pd.DataFrame(reset)
        final_table = Reset.pivot_table('different_state', 'time', ['ganma', 'beta'])
        plt.ylim(-0.5, 0.5)
        plt.ylabel(y_axis)
        plt.xlabel('time(step)')
        ganma_scale = final_table.columns.levels[0]
        min_beta = sum(ganma_scale < a)
        max_beta = sum(ganma_scale < b)
        for i in range(min_beta, max_beta):
            pic = final_table[ganma_scale[i]]
            plt.plot(pic, linewidth=0.3)


if __name__ == "__main__":
    print("Visualization")

