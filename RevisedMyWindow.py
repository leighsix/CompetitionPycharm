import sys
from pymnet import *
import Layer_A_Modeling
import Layer_B_Modeling
from Setting_Revised_Value import *
import Layer_A_Modeling
import Layer_B_Modeling
import Revised_Changing_Variable
import RevisedVisualization
import Revised_Interconnected_Layer_Modeling
import DB_Management
import RevisedSelectDB
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
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon
import sys


from mpl_toolkits.mplot3d.axes3d import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib
matplotlib.use("TkAgg")
WindowModel = uic.loadUiType("revisedmainwindow.ui")[0]


class RevisedMyWindow(QMainWindow, WindowModel):
    def __init__(self, setting):
        QMainWindow.__init__(self, None)
        self.setupUi(self)
        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget = QVideoWidget()
        self.changing_variable = Revised_Changing_Variable.Revised_Changing_Variable(setting)
        self.visualization = RevisedVisualization.RevisedVisualization()
        self.network = Revised_Interconnected_Layer_Modeling.Revised_Interconnected_Layer_Modeling()
        self.db_manager = DB_Management.DB_Management()
        self.select_db = RevisedSelectDB.RevisedSelectDB()
        self.select_sql = RevisedSelectDB.SelectSQlite()

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
            df = self.select_db.select_data_from_DB(setting)
        elif setting.DB == 'SQLITE':
            df = self.select_sql.select_data_from_sqlite(setting)
        return df

    def making_duplicate_df(self, setting):
        df = pd.DataFrame()
        if setting.DB == 'MySQL':
            df = self.select_db.select_duplicates_from_DB(setting)
        return df

    def initial_state_graph(self, state, setting):
        print('drawing initial state...')
        self.Initial_State_layout.takeAt(0)
        layer_A = Layer_A_Modeling.Layer_A_Modeling(setting)
        layer_B = Layer_B_Modeling.Layer_B_Modeling(setting)
        fig = self.network.draw_interconnected_network(setting, layer_A, layer_B, 'result.png')[1]
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
        A_initial_value = eval(self.A_InitialStateBox_3.currentText())
        B_initial_value = eval(self.B_InitialStateBox_3.currentText())
        if self.display_typeBox.currentText() == 'scatter':
            print('scatter type...')
            if self.display_locBox.currentText() == 'outer graph':
                plt.figure()
                plt.style.use('seaborn-whitegrid')
                df = self.making_df(setting)
                if A_initial_value is not None:
                    df = df[df.A_Initial_State == A_initial_value]
                if B_initial_value is not None:
                    df = df[df.B_Initial_State == B_initial_value]
                self.visualization.plot_3D_scatter_for_average_state(setting, df)
                plt.show()
                plt.close()
            elif self.display_locBox.currentText() == 'inner graph':
                self.Total_Result_layout.takeAt(0)
                fig = plt.figure()
                plt.style.use('seaborn-whitegrid')
                df = self.making_df(setting)
                if A_initial_value is not None:
                    df = df[df.A_Initial_State == A_initial_value]
                if B_initial_value is not None:
                    df = df[df.B_Initial_State == B_initial_value]
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
                if A_initial_value is not None:
                    df = df[df.A_Initial_State == A_initial_value]
                if B_initial_value is not None:
                    df = df[df.B_Initial_State == B_initial_value]
                self.visualization.plot_3D_trisurf_for_average_state(setting, df)
                plt.show()
                plt.close()
            elif self.display_locBox.currentText() == 'inner graph':
                self.Total_Result_layout.takeAt(0)
                fig = plt.figure()
                plt.style.use('seaborn-whitegrid')
                df = self.making_df(setting)
                if A_initial_value is not None:
                    df = df[df.A_Initial_State == A_initial_value]
                if B_initial_value is not None:
                    df = df[df.B_Initial_State == B_initial_value]
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
                if A_initial_value is not None:
                    df = df[df.A_Initial_State == A_initial_value]
                if B_initial_value is not None:
                    df = df[df.B_Initial_State == B_initial_value]
                self.visualization.plot_3D_to_2D_contour_for_average_state(setting, df)
                cb = plt.colorbar()
                cb.set_label(label='Average states', size=15, labelpad=10)
                cb.ax.tick_params(labelsize=12)
                plt.clim(-3, 3)
                plt.xlabel(r'$\beta$', fontsize=18, labelpad=6)
                plt.ylabel('PROB_P', fontsize=18, labelpad=6)
                plt.show()
                plt.close()

            elif self.display_locBox.currentText() == 'inner graph':
                self.Total_Result_layout.takeAt(0)
                fig = plt.figure()
                plt.style.use('seaborn-whitegrid')
                ax = fig.add_subplot(111)
                ax.tick_params(axis='both', labelsize=14)
                df = self.making_df(setting)
                if A_initial_value is not None:
                    df = df[df.A_Initial_State == A_initial_value]
                if B_initial_value is not None:
                    df = df[df.B_Initial_State == B_initial_value]
                self.visualization.plot_3D_to_2D_contour_for_average_state(setting, df)
                cb = plt.colorbar()
                cb.set_label(label='Average states', size=15, labelpad=10)
                cb.ax.tick_params(labelsize=12)
                plt.clim(-3, 3)
                plt.xlabel(r'$\beta$', fontsize=18, labelpad=6)
                plt.ylabel('PROB_P', fontsize=18, labelpad=6)
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
                if A_initial_value is not None:
                    df = df[df.A_Initial_State == A_initial_value]
                if B_initial_value is not None:
                    df = df[df.B_Initial_State == B_initial_value]
                self.visualization.plot_3D_contour_for_average_state(setting, df)
                plt.show()
                plt.close()

            elif self.display_locBox.currentText() == 'inner graph':
                self.Total_Result_layout.takeAt(0)
                fig = plt.figure()
                plt.style.use('seaborn-whitegrid')
                df = self.making_df(setting)
                if A_initial_value is not None:
                    df = df[df.A_Initial_State == A_initial_value]
                if B_initial_value is not None:
                    df = df[df.B_Initial_State == B_initial_value]
                self.visualization.plot_3D_contour_for_average_state(setting, df)
                canvas = FigureCanvas(fig)
                layout = self.Total_Result_layout
                layout.addWidget(canvas)
                canvas.draw()
                canvas.show()
                plt.close()

    def result_beta_graph(self, state, setting):
        print('drawing beta graph...')
        A_initial_value = eval(self.A_InitialStateBox_2.currentText())
        B_initial_value = eval(self.B_InitialStateBox_2.currentText())
        if self.result_beta_locBox.currentText() == 'outer graph':
            fig = plt.figure()
            plt.style.use('seaborn-whitegrid')
            ax = fig.add_subplot(111)
            ax.tick_params(axis='both', labelsize=14)
            df = self.making_df(setting)
            if A_initial_value is not None:
                df = df[df.A_Initial_State == A_initial_value]
            if B_initial_value is not None:
                df = df[df.B_Initial_State == B_initial_value]
            self.visualization.plot_2D_beta_for_average_state(setting, df)
            plt.ylim(-4, 4)
            plt.xlabel(r'$\beta$', fontsize=18, labelpad=4)
            plt.ylabel('Average States', fontsize=18, labelpad=4)
            plt.show()
            plt.close()
        elif self.result_beta_locBox.currentText() == 'inner graph':
            self.Result_beta_layout.takeAt(0)
            fig = plt.figure()
            plt.style.use('seaborn-whitegrid')
            ax = fig.add_subplot(111)
            ax.tick_params(axis='both', labelsize=14)
            df = self.making_df(setting)
            if A_initial_value is not None:
                df = df[df.A_Initial_State == A_initial_value]
            if B_initial_value is not None:
                df = df[df.B_Initial_State == B_initial_value]
            self.visualization.plot_2D_beta_for_average_state(setting, df)
            plt.legend(framealpha=1, frameon=True,  prop={'size': 14})
            plt.ylim(-4, 4)
            plt.xlabel(r'$\beta$', fontsize=18, labelpad=4)
            plt.ylabel('Average States', fontsize=18, labelpad=4)
            canvas = FigureCanvas(fig)
            layout = self.Result_beta_layout
            layout.addWidget(canvas)
            canvas.draw()
            canvas.show()
            plt.close()

    def prob_beta_graph(self, state, setting):
        print('drawing prob beta graph...')
        beta_value = [eval(self.beta_minBox.text()), eval(self.beta_maxBox.text())]
        A_initial_value = eval(self.A_InitialStateBox.currentText())
        B_initial_value = eval(self.B_InitialStateBox.currentText())
        if self.prob_beta_locBox.currentText() == 'outer graph':
            fig = plt.figure()
            sns.set()
            ax = fig.add_subplot(111)
            ax.tick_params(axis='both', labelsize=14)
            df = self.making_df(setting)
            if A_initial_value is not None:
                df = df[df.A_Initial_State == A_initial_value]
            if B_initial_value is not None:
                df = df[df.B_Initial_State == B_initial_value]
            self.visualization.flow_prob_beta_chart(setting, df, beta_value)
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
            if A_initial_value is not None:
                df = df[df.A_Initial_State == A_initial_value]
            if B_initial_value is not None:
                df = df[df.B_Initial_State == B_initial_value]
            self.visualization.flow_prob_beta_chart(setting, df, beta_value)
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
        select_layer = str(self.select_layerBox.currentText())
        A_initial_value = eval(self.A_InitialStateBox_4.currentText())
        B_initial_value = eval(self.B_InitialStateBox_4.currentText())
        if select_layer != 'Total':
            if self.prob_beta_locBox.currentText() == 'outer graph':
                fig = plt.figure()
                sns.set()
                ax = fig.add_subplot(111)
                ax.tick_params(axis='both', labelsize=14)
                df = self.making_df(setting)
                if A_initial_value is not None:
                    df = df[df.A_Initial_State == A_initial_value]
                if B_initial_value is not None:
                    df = df[df.B_Initial_State == B_initial_value]
                self.visualization.different_state_ratio_chart(setting, df, beta_value, select_layer)
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
                if A_initial_value is not None:
                    df = df[df.A_Initial_State == A_initial_value]
                if B_initial_value is not None:
                    df = df[df.B_Initial_State == B_initial_value]
                self.visualization.different_state_ratio_chart(setting, df, beta_value, select_layer)
                plt.ylabel('different state ratio for layer %s' % select_layer, fontsize=18, labelpad=6)
                plt.xlabel('time(step)', fontsize=18, labelpad=6)
                canvas = FigureCanvas(fig)
                layout = self.different_state_layout
                layout.addWidget(canvas)
                canvas.draw()
                canvas.show()
                plt.close()
        elif select_layer == 'Total':
            if self.prob_beta_locBox.currentText() == 'outer graph':
                fig = plt.figure()
                sns.set()
                ax = fig.add_subplot(111)
                ax.tick_params(axis='both', labelsize=14)
                df = self.making_df(setting)
                self.visualization.total_different_state_ratio_chart(setting, df, beta_value)
                plt.ylabel('different state ratio', fontsize=18, labelpad=6)
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
                self.visualization.total_different_state_ratio_chart(setting, df, beta_value)
                plt.ylabel('different state ratio', fontsize=18, labelpad=6)
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
        df = df.loc[0:99, :]
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
        df = self.making_duplicate_df(setting)
        print(len(df))
        if len(df) == 0:
            print('no duplicates')
            pass
        if len(df) > 0 :
            table.setColumnCount(len(df.columns))
            table.setRowCount(len(df.index))
            table.setHorizontalHeaderLabels(df.columns)
            for i in range(len(df.index)):
                for j in range(len(df.columns)):
                    table.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))
            self.table_widget.show()

    def making_movie_function(self):
        print('making movie...')
        self.movieLayout.takeAt(0)
        self.movieLayout.addWidget(self.videoWidget)
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie", QDir.homePath())
        if fileName != '':
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
        self.player.setVideoOutput(self.videoWidget)
        self.player.play()

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
    SS = Setting_Revised_Value()
    app = QApplication(sys.argv)
    my_window = RevisedMyWindow(SS)
    my_window.show()
    app.exec_()

