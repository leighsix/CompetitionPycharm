import SelectDB
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sympy import *
import numpy as np
from mpl_toolkits import mplot3d


class Visualization:
    def __init__(self):
        self.select_db = SelectDB.SelectDB()

    def plot_3D_for_average_state(self, table, step):
        df = self.select_db.select_data_from_DB(table)
        df2 = df[df.Steps == step]
        sns.set_style("whitegrid")
        ax = plt.axes(projection='3d')
        ax.plot_trisurf(df2['beta'], df2['gamma'], (df2['LAYER_A_MEAN']+df2['LAYER_B_MEAN']),
                        cmap='RdBu', edgecolor='none')
        ax.set_xlabel('beta')
        ax.set_ylabel('gamma')
        ax.set_zlabel('Average States')
        ax.set_title('beta-gamma-States')
        ax.view_init(45, 45)

    def plot_3D_to_2D_contour_for_average_state(self, table, step):
        df = self.select_db.select_data_from_DB(table)
        df2 = df[df.Steps == step]
        sns.set_style("whitegrid")
        result_beta = sorted(np.array(df2['beta']))
        result_gamma = sorted(np.array(df2['gamma']))
        result_state = np.array(df2['LAYER_A_MEAN'] + df2['LAYER_B_MEAN']).reshape(41, 41)

        X, Y = np.meshgrid(result_beta, result_gamma)
        Z = z_function(result, c)
        plt.contourf(X, Y, Z, 50, cmap='RdBu')
        plt.xlabel('beta')
        plt.ylabel('gamma')
        plt.colorbar(label='Average states')

    @staticmethod
    def z_function(result, a):
        final_data = pd.read_pickle(result)
        z = np.array(final_data[str(a)]).reshape(41, 41)
        Z = np.zeros((1681, 1681))
        for i in range(0, 41):
            for j in range(0, 41):
                for k in range(0, 41):
                    for l in range(0, 41):
                        Z[(i * 41) + k][(j * 41) + l] = z[i][j]
        return Z





    def plot_2D_gamma_for_average_state(self, table, beta_min, beta_max):
        df = self.select_db.select_data_from_DB(table)
        df2 = df[df.Steps == 30]
        df3 = df2[df2.beta > beta_min]
        df4 = df3[df3.beta < beta_max]
        sns.set_style("whitegrid")
        plt.plot(df4['gamma'], (df4['LAYER_A_MEAN']+df4['LAYER_B_MEAN']), '-', label='gamma')
        plt.legend(framealpha=1, frameon=True)
        plt.ylim(-1.3, 1.3)
        plt.xlabel('gamma')
        plt.ylabel('Average States')

    def plot_2D_beta_for_average_state(self, table, gamma_min, gamma_max):
        df = self.select_db.select_data_from_DB(table)
        df2 = df[df.Steps == 30]
        df3 = df2[df2.beta > gamma_min]
        df4 = df3[df3.beta < gamma_max]
        sns.set_style("whitegrid")
        plt.plot(df4['beta'], (df4['LAYER_A_MEAN']+df4['LAYER_B_MEAN']), '-', label='beta')
        plt.legend(framealpha=1, frameon=True)
        plt.ylim(-1.3, 1.3)
        plt.xlabel('beta')
        plt.ylabel('Average States')


    def prob_beta_plot_3D(result, number_ganma, t, initial, gap, a, b, c, d, e):
        df = self.select_db.select_data_from_DB(table)
        ganma_data = []
        probbeta = []
        times = np.linspace(0, t - 1, t)
        time = sorted(sorted(times) * number_ganma)
        for i in range(number_ganma):
            ganma_data.append(flow_probbeta_data.iloc[0, initial + (gap * i)])
        ganma_datas = (ganma_data) * t
        for j in range(t):
            for i in range(number_ganma):
                probbeta.append(flow_probbeta_data.iloc[2 + j, initial + (gap * i)])
        sns.set_style("whitegrid")
        ax = plt.axes(projection='3d')
        ax.plot_trisurf(time, ganma_datas, probbeta, cmap='viridis', edgecolor='none')
        ax.set_xlabel(str(a))
        ax.set_ylabel(str(b))
        ax.set_zlabel(str(c))
        ax.view_init(d, e)



# ex__  prob_beta_plot_3D('flow_prob_beta5.0_data.pickle', 51, 20, 10, 101, 'time', 'ganma', 'prob_beta', 45, 45)
def total_flow_prob_beta_chart(filename):
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




