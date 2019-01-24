import sys
import Setting_Simulation_Value
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import  *
from PyQt5 import uic
import time

MainUI = "mainwindow.ui"


class Making_GUI(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None)
        uic.loadUi(MainUI, self)
        #self.timer = QTimer(self)
        #self.timer.start(1000)
        # self.timer.timeout.connect(self.timeout)
        self.condition_settingButton.clicked.connect(self.condition_setting)

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







    def timeout(self):
        current_time = QTime.currentTime()
        text_time = current_time.toString("hh:mm:ss")
        time_msg = "현재시간: " + text_time
        state = self.kiwoom.get_connect_state()
        if state == 1:
            state_msg = "서버 연결 중"
        else:
            state_msg = "서버 미 연결 중"
        self.statusbar.showMessage(state_msg + " | " + time_msg)

    def insert_initial_condition(self):
        code = self.comboBox.currentText()
        return code


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = Making_GUI()
    myWindow.show()
    app.exec_()
