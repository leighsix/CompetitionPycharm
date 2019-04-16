import sys
from pymnet import *
import InterconnectedLayerModeling
from Setting_Simulation_Value import *
import Layer_A_Modeling
import Layer_B_Modeling
import Changing_Variable
import Visualization
import Interconnected_Network_Visualization
import DB_Management
import SelectDB
import seaborn as sns
import pandas as pd
import PyQt5
from PyQt5.QtWidgets import *
from matplotlib.image import imread
import matplotlib.pyplot as plt
import time
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import  *
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QWidget, QLabel, QScrollArea, QTableWidget
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon
from mpl_toolkits.mplot3d.axes3d import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib
matplotlib.use("TkAgg")
WindowModel = uic.loadUiType("mainwindow.ui")[0]


class MyWindow(QMainWindow, WindowModel):
    def __init__(self, setting):
        QMainWindow.__init__(self, None)
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.setupUi(self)
        self.changing_variable = Changing_Variable.Changing_Variable()
        self.visualization = Visualization.Visualization()
        self.network = Interconnected_Network_Visualization.Interconnected_Network_Visualization()
        self.db_manager = DB_Management.DB_Management()
        self.select_db = SelectDB.SelectDB()
        self.select_sql = SelectDB.SelectSQlite()

        self.condition_settingButton.clicked.connect(lambda state, sets=setting: self.condition_setting(state, sets))
        self.Simulation_Start.clicked.connect(lambda state, sets=setting: self.doing_simulation(state, sets))
        self.Initial_State_Button.clicked.connect(lambda state, sets=setting: self.initial_state_graph(state, sets))
        self.Total_Result_Button.clicked.connect(lambda state, sets=setting: self.total_result_graph(state, sets))
        self.result_gamma_Button.clicked.connect(lambda state, sets=setting: self.result_gamma_graph(state, sets))
        self.result_beta_Button.clicked.connect(lambda state, sets=setting: self.result_beta_graph(state, sets))
        self.prob_beta_Button.clicked.connect(lambda state, sets=setting: self.prob_beta_graph(state, sets))
        self.different_ratio_Button.clicked.connect(lambda state, sets=setting: self.different_state_ratio_graph(state, sets))
        self.play_movie_Button.clicked.connect(self.making_movie_function)
        self.drop_duplicate_Button.clicked.connect(lambda state, sets=setting: self.db_drop_duplicate_row(state, sets))
        self.duplicate_Button.clicked.connect(lambda state, sets=setting: self.duplicate_db_func(state, sets))
        self.select_db_Button.clicked.connect(lambda state, sets=setting: self.select_db_func(state, sets))


    def making_df(self, setting):
        df = pd.DataFrame()
        if setting.DB == 'MySQL':
            df = self.select_db.select_data_from_setting(setting)
        elif setting.DB == 'SQLITE':
            df = self.select_sql.select_data_from_sqlite(setting)
        return df

    def initial_state_graph(self, state, setting):
        print('drawing initial state...')
        self.Initial_State_layout.takeAt(0)
        inter_layer = InterconnectedLayerModeling.InterconnectedLayerModeling(setting)
        fig = self.network.draw_interconnected_network(setting, inter_layer, 'result.png')[1]
        if self.display_locBox_2.currentText() == 'outer graph':
            plt.show()
        elif self.display_locBox_2.currentText() == 'inner graph':
            canvas = FigureCanvas(fig)
            layout = self.Initial_State_layout
            layout.addWidget(canvas)
            canvas.draw()
            canvas.show()

    def total_result_graph(self, state, setting):
        print('drawing total result...')
        if self.display_typeBox.currentText() == 'scatter':
            print('scatter type...')
            if self.display_locBox.currentText() == 'outer graph':
                plt.figure()
                plt.style.use('seaborn-whitegrid')
                df = self.making_df(setting)
                self.visualization.plot_3D_scatter_for_average_state(setting, df)
                plt.show()
                plt.close()
            elif self.display_locBox.currentText() == 'inner graph':
                self.Total_Result_layout.takeAt(0)
                fig = plt.figure()
                plt.style.use('seaborn-whitegrid')
                df = self.making_df(setting)
                self.visualization.plot_3D_scatter_for_average_state(setting, df)
                canvas = FigureCanvas(fig)
                layout = self.Total_Result_layout
                layout.addWidget(canvas)
                canvas.draw()
                canvas.show()
                plt.close()

        elif self.display_typeBox.currentText() == 'trisurf':
            print('trisurf type...')
            if self.display_locBox.currentText() == 'outer graph':
                plt.figure()
                plt.style.use('seaborn-whitegrid')
                df = self.making_df(setting)
                self.visualization.plot_3D_trisurf_for_average_state(setting, df)
                plt.show()
                plt.close()
            elif self.display_locBox.currentText() == 'inner graph':
                self.Total_Result_layout.takeAt(0)
                fig = plt.figure()
                plt.style.use('seaborn-whitegrid')
                df = self.making_df(setting)
                self.visualization.plot_3D_trisurf_for_average_state(setting, df)
                canvas = FigureCanvas(fig)
                layout = self.Total_Result_layout
                layout.addWidget(canvas)
                canvas.draw()
                canvas.show()
                plt.close()

        elif self.display_typeBox.currentText() == 'contour2D':
            print('contour2D type...')
            if self.display_locBox.currentText() == 'outer graph':
                fig = plt.figure()
                plt.style.use('seaborn-whitegrid')
                ax = fig.add_subplot(111)
                ax.tick_params(axis='both', labelsize=14)
                df = self.making_df(setting)
                self.visualization.plot_3D_to_2D_contour_for_average_state(setting, df)
                cb = plt.colorbar()
                cb.set_label(label='AS', size=15, labelpad=10)
                cb.ax.tick_params(labelsize=12)
                plt.clim(-1, 1)
                plt.xlabel(r'$\beta$', fontsize=18, labelpad=6)
                plt.ylabel(r'$\gamma$', fontsize=18, labelpad=6)
                plt.show()
                plt.close()

            elif self.display_locBox.currentText() == 'inner graph':
                self.Total_Result_layout.takeAt(0)
                fig = plt.figure()
                plt.style.use('seaborn-whitegrid')
                ax = fig.add_subplot(111)
                ax.tick_params(axis='both', labelsize=14)
                df = self.making_df(setting)
                self.visualization.plot_3D_to_2D_contour_for_average_state(setting, df)
                cb = plt.colorbar()
                cb.set_label(label='AS', size=15, labelpad=10)
                cb.ax.tick_params(labelsize=12)
                plt.clim(-1, 1)
                plt.xlabel(r'$\beta$', fontsize=18, labelpad=6)
                plt.ylabel(r'$\gamma$', fontsize=18, labelpad=6)
                canvas = FigureCanvas(fig)
                layout = self.Total_Result_layout
                layout.addWidget(canvas)
                canvas.draw()
                canvas.show()
                plt.close()

        elif self.display_typeBox.currentText() == 'contour3D':
            print('contour3D type...')
            if self.display_locBox.currentText() == 'outer graph':
                plt.figure()
                plt.style.use('seaborn-whitegrid')
                df = self.making_df(setting)
                self.visualization.plot_3D_contour_for_average_state(setting, df)
                plt.show()
                plt.close()

            elif self.display_locBox.currentText() == 'inner graph':
                self.Total_Result_layout.takeAt(0)
                fig = plt.figure()
                plt.style.use('seaborn-whitegrid')
                df = self.making_df(setting)
                self.visualization.plot_3D_contour_for_average_state(setting, df)
                canvas = FigureCanvas(fig)
                layout = self.Total_Result_layout
                layout.addWidget(canvas)
                canvas.draw()
                canvas.show()
                plt.close()

    def result_gamma_graph(self, state, setting):
        print('drawing gamma graph...')
        box = [eval(self.beta_spinBox1.text()), eval(self.beta_spinBox2.text()),
               eval(self.beta_spinBox3.text()), eval(self.beta_spinBox4.text()),
               eval(self.beta_spinBox5.text()), eval(self.beta_spinBox6.text())]
        marker = ['-o', '-x', '-v', '-^', '-s', '-d']
        if self.result_gamma_locBox.currentText() == 'outer graph':
            fig = plt.figure()
            plt.style.use('seaborn-whitegrid')
            ax = fig.add_subplot(111)
            ax.tick_params(axis='both', labelsize=14)
            df = self.making_df(setting)
            for i, j in enumerate(box):
                if j > 0:
                    self.visualization.plot_2D_gamma_for_average_state(setting, df, j, marker[i])
            plt.legend(framealpha=1, frameon=True,  prop={'size': 12})
            plt.ylim(-1.7, 1.7)
            plt.xlabel(r'$\gamma$', fontsize=18, labelpad=4)
            plt.ylabel('AS', fontsize=18, labelpad=4)
            plt.show()
            plt.close()
        elif self.result_gamma_locBox.currentText() == 'inner graph':
            self.Result_gamma_layout.takeAt(0)
            fig = plt.figure()
            plt.style.use('seaborn-whitegrid')
            ax = fig.add_subplot(111)
            ax.tick_params(axis='both', labelsize=14)
            df = self.making_df(setting)
            for i, j in enumerate(box):
                if j > 0:
                    self.visualization.plot_2D_gamma_for_average_state(setting, df, j, marker[i])
            plt.legend(framealpha=1, frameon=True,  prop={'size': 12})
            plt.ylim(-1.7, 1.7)
            plt.xlabel(r'$\gamma$', fontsize=18, labelpad=4)
            plt.ylabel('AS', fontsize=18, labelpad=4)
            canvas = FigureCanvas(fig)
            layout = self.Result_gamma_layout
            layout.addWidget(canvas)
            canvas.draw()
            canvas.show()
            plt.close()

    def result_beta_graph(self, state, setting):
        print('drawing beta graph...')
        box = [eval(self.gamma_spinBox1.text()), eval(self.gamma_spinBox2.text()),
               eval(self.gamma_spinBox3.text()), eval(self.gamma_spinBox4.text()),
               eval(self.gamma_spinBox5.text()), eval(self.gamma_spinBox6.text())]
        marker = ['-o', '-x', '-v', '-^', '-s', '-d']
        if self.result_beta_locBox.currentText() == 'outer graph':
            fig = plt.figure()
            plt.style.use('seaborn-whitegrid')
            ax = fig.add_subplot(111)
            ax.tick_params(axis='both', labelsize=14)
            df = self.making_df(setting)
            for i, j in enumerate(box):
                if j > 0:
                    self.visualization.plot_2D_beta_for_average_state(setting, df, j, marker[i])
            plt.legend(framealpha=1, frameon=True,  prop={'size': 12})
            plt.ylim(-1.7, 1.7)
            plt.xlabel(r'$\beta$', fontsize=18, labelpad=4)
            plt.ylabel('AS', fontsize=18, labelpad=4)
            plt.show()
            plt.close()
        elif self.result_beta_locBox.currentText() == 'inner graph':
            self.Result_beta_layout.takeAt(0)
            fig = plt.figure()
            plt.style.use('seaborn-whitegrid')
            ax = fig.add_subplot(111)
            ax.tick_params(axis='both', labelsize=14)
            df = self.making_df(setting)
            for i, j in enumerate(box):
                if j > 0:
                    self.visualization.plot_2D_beta_for_average_state(setting, df, j, marker[i])
            plt.legend(framealpha=1, frameon=True,  prop={'size': 12})
            plt.ylim(-1.7, 1.7)
            plt.xlabel(r'$\beta$', fontsize=18, labelpad=4)
            plt.ylabel('AS', fontsize=18, labelpad=4)
            canvas = FigureCanvas(fig)
            layout = self.Result_beta_layout
            layout.addWidget(canvas)
            canvas.draw()
            canvas.show()
            plt.close()

    def prob_beta_graph(self, state, setting):
        print('drawing prob beta graph...')
        beta_value = [eval(self.beta_minBox.text()), eval(self.beta_maxBox.text())]
        gamma_value = [eval(self.gamma_minBox.text()), eval(self.gamma_maxBox.text())]
        if self.prob_beta_locBox.currentText() == 'outer graph':
            fig = plt.figure()
            sns.set()
            ax = fig.add_subplot(111)
            ax.tick_params(axis='both', labelsize=14)
            df = self.making_df(setting)
            self.visualization.flow_prob_beta_chart(setting, df, beta_value, gamma_value)
            plt.ylabel('probability for layer B', fontsize=18, labelpad=4)
            plt.xlabel('time(step)', fontsize=18, labelpad=4)
            plt.show()
            plt.close()
        elif self.prob_beta_locBox.currentText() == 'inner graph':
            self.prob_beta_layout.takeAt(0)
            fig = plt.figure()
            sns.set()
            ax = fig.add_subplot(111)
            ax.tick_params(axis='both', labelsize=14)
            df = self.making_df(setting)
            self.visualization.flow_prob_beta_chart(setting, df, beta_value, gamma_value)
            plt.ylabel('probability for layer B', fontsize=18, labelpad=4)
            plt.xlabel('time(step)', fontsize=18, labelpad=4)
            canvas = FigureCanvas(fig)
            layout = self.prob_beta_layout
            layout.addWidget(canvas)
            canvas.draw()
            canvas.show()
            plt.close()

    def different_state_ratio_graph(self, state, setting):
        print('drawing different state ratio graph...')
        beta_value = [eval(self.beta_minBox_4.text()), eval(self.beta_maxBox_4.text())]
        gamma_value = [eval(self.gamma_minBox_4.text()), eval(self.gamma_maxBox_4.text())]
        select_layer = str(self.select_layerBox.currentText())
        if self.prob_beta_locBox.currentText() == 'outer graph':
            fig = plt.figure()
            sns.set()
            ax = fig.add_subplot(111)
            ax.tick_params(axis='both', labelsize=14)
            df = self.making_df(setting)
            self.visualization.different_state_ratio_chart(setting, df, beta_value, gamma_value, select_layer)
            plt.ylabel('different state ratio for layer %s' % select_layer, fontsize=18, labelpad=6)
            plt.xlabel('time(step)', fontsize=18, labelpad=6)
            plt.show()
            plt.close()
        elif self.state_ratio_locBox.currentText() == 'inner graph':
            self.different_state_layout.takeAt(0)
            fig = plt.figure()
            sns.set()
            ax = fig.add_subplot(111)
            ax.tick_params(axis='both', labelsize=14)
            df = self.making_df(setting)
            self.visualization.different_state_ratio_chart(setting, df, beta_value, gamma_value, select_layer)
            plt.ylabel('different state ratio for layer %s' % select_layer, fontsize=18, labelpad=6)
            plt.xlabel('time(step)', fontsize=18, labelpad=6)
            canvas = FigureCanvas(fig)
            layout = self.different_state_layout
            layout.addWidget(canvas)
            canvas.draw()
            canvas.show()
            plt.close()

    def db_drop_duplicate_row(self, state, setting):
        print('duplicate DB dropped...')
        self.db_manager.drop_duplicate_row(setting)

    def select_db_func(self, state, setting):
        print('select DB...')
        table = self.DB_table
        df = self.making_df(setting)
        df.head(100)
        table.setColumnCount(len(df.columns))
        table.setRowCount(len(df.index))
        table.setHorizontalHeaderLabels(df.columns)
        for i in range(len(df.index)):
            for j in range(len(df.columns)):
                table.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))
        self.table_widget.show()

    def duplicate_db_func(self, state, setting):
        print('duplicate DB...')
        table = self.DB_table
        df = self.making_df(setting)
        df.head(100)
        table.setColumnCount(len(df.columns))
        table.setRowCount(len(df.index))
        table.setHorizontalHeaderLabels(df.columns)
        for i in range(len(df.index)):
            for j in range(len(df.columns)):
                table.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))
        self.table_widget.show()

    def making_movie_function(self):
        print('making movie...')
        self.movie_layout.takeAt(0)
        layout = self.movie_layout
        videoWidget = QVideoWidget()
        layout.addWidget(videoWidget)
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile('C:/Users/Purple/CompetingLayer/dynamics.mp4')))
        self.mediaPlayer.play()

    def doing_simulation(self, state, setting):
        print('doing simulation...')
        self.changing_variable.paralleled_work(setting)

    def condition_setting(self, state, setting):
        setting.Structure = str(self.StructuresBox.currentText())
        setting.A_state = eval(self.A_StateBox.currentText())
        setting.A_node = int(self.A_NodeBox.currentText())
        setting.A_edge = int(self.A_InternalEdgeBox.currentText())
        setting.MAX = int(self.A_MAXBox.currentText())
        setting.MIN = int(self.A_MINBox.currentText())
        setting.B_state = eval(self.B_StateBox.currentText())
        setting.B_node = int(self.B_NodeBox.currentText())
        setting.B_edge = int(self.B_InternalEdgeBox.currentText())
        setting.B_inter_edges = int(self.B_ExternalEdgeBox.currentText())
        setting.A_inter_edges = int(self.A_ExternalEdgeBox.currentText())
        setting.Limited_step = int(self.StepBox.currentText())
        setting.drawing_graph = bool(self.DrawingBox.currentText() == 'True')
        setting.database = str(self.DatabaseBox.currentText())
        setting.table = str(self.TableBox.currentText())
        setting.DB = str(self.DBBox.currentText())
        print('setting is completed')


if __name__ == "__main__":
    SS = Setting_Simulation_Value()
    app = QApplication(sys.argv)
    my_window = MyWindow(SS)
    my_window.show()
    app.exec_()


