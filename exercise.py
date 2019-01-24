import numpy as np
import math
import sys
import Setting_Simulation_Value
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import  *
from PyQt5 import uic
import time

MainUI = "mainwindow.ui"


class Ex_Setting_Simulation_Value(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None)
        uic.loadUi(MainUI, self)
        #self.timer = QTimer(self)
        #self.timer.start(1000)
        # self.timer.timeout.connect(self.timeout)
        self.condition_settingButton.clicked.connect(self.condition_setting)
        self.Structure = self.comboBox_16.currentText()
        self.A_state = self.comboBox_5.currentText()
        self.A_node = self.comboBox.currentText()
        self.A_edge = self.comboBox_2.currentText()
        self.MAX = self.comboBox_6.currentText()
        self.MIN = self.comboBox_15.currentText()
        self.A_network = self.comboBox_4.currentText()
        self.B_state = self.comboBox_10.currentText()
        self.B_node = self.comboBox_11.currentText()
        self.B_edge = self.comboBox_9.currentText()
        self.B_inter_edges = self.comboBox_7.currentText()
        self.A_inter_edges = self.comboBox_3.currentText()
        self.B_network = self.comboBox_8.currentText()  # network : 1 = random regular graph   2 = barabasi-albert graph
        self.gap = 30
        self.Repeating_number = 100
        self.Limited_step = self.comboBox_12.currentText()
        self.R = self.simulation_condition(self.gap)[0]
        self.D = self.simulation_condition(self.gap)[1]
        self.variable_list = self.gamma_and_beta_list(self.R, self.D)
        self.NodeColorDict = {1: 'hotpink', 2: 'red', -1: 'skyblue', -2: 'blue'}
        self.EdgeColorDict = {1: 'yellow', 2: 'hotpink', 4: 'red', -1: 'skyblue', -2: 'blue', -4: 'darkblue'}
        self.database = 'renew_competition'  # 'competition  renew_competition'
        self.drawing_graph = self.comboBox_13.currentText()
        self.workers = 4

    def simulation_condition(self, gap):
        self.R = np.linspace(1, 2, gap)
        self.D = np.linspace(self.making_beta_scale(gap)[0], self.making_beta_scale(gap)[1], gap)
        return self.R, self.D

    def gamma_and_beta_list(self, gamma_list, beta_list):
        variable_list = []
        for gamma in gamma_list:
            for beta in beta_list:
                variable_list.append((gamma, beta))
        return variable_list

    def making_beta_scale(self, a):
        scale = math.log((1 / (self.B_edge + 1)) ** 3) \
                / math.log(self.B_inter_edges / (self.B_edge + self.B_inter_edges))
        return 0, scale, a

    def condition_setting(self):
        Setting_Simulation_Value.Setting_Simulation_Value.Structure = self.comboBox_16.currentText()
        Setting_Simulation_Value.Setting_Simulation_Value.A_state = eval(self.comboBox_5.currentText())
        Setting_Simulation_Value.Setting_Simulation_Value.A_node = int(self.comboBox.currentText())
        Setting_Simulation_Value.Setting_Simulation_Value.A_edge = int(self.comboBox_2.currentText())
        Setting_Simulation_Value.Setting_Simulation_Value.MAX = int(self.comboBox_6.currentText())
        Setting_Simulation_Value.Setting_Simulation_Value.MIN = int(self.comboBox_15.currentText())
        Setting_Simulation_Value.Setting_Simulation_Value.A_network = int(self.comboBox_4.currentText())
        Setting_Simulation_Value.Setting_Simulation_Value.B_state = eval(self.comboBox_10.currentText())
        Setting_Simulation_Value.Setting_Simulation_Value.B_node = int(self.comboBox_11.currentText())
        Setting_Simulation_Value.Setting_Simulation_Value.B_edge = int(self.comboBox_9.currentText())
        Setting_Simulation_Value.Setting_Simulation_Value.B_inter_edges = int(self.comboBox_7.currentText())
        Setting_Simulation_Value.Setting_Simulation_Value.A_inter_edges = int(self.comboBox_3.currentText())
        Setting_Simulation_Value.Setting_Simulation_Value.B_network = int(self.comboBox_8.currentText())
        Setting_Simulation_Value.Setting_Simulation_Value.Limited_step = int(self.comboBox_12.currentText())
        Setting_Simulation_Value.Setting_Simulation_Value.drawing_graph = bool(self.comboBox_13.currentText())
        print(Setting_Simulation_Value.Setting_Simulation_Value.A_node)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = Ex_Setting_Simulation_Value()
    myWindow.show()
    app.exec_()

