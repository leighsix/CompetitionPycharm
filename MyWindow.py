import sys
import Changing_Variable
import Visualization
import Interconnected_Layer_Modeling
from Setting_Simulation_Value import *
import Layer_A_Modeling
import Layer_B_Modeling
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import  *
from PyQt5 import uic
import time

MainUI = "mainwindow.ui"

class MyWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None)
        uic.loadUi(MainUI, self)
        #self.timer = QTimer(self)
        #self.timer.start(1000)
        # self.timer.timeout.connect(self.timeout)
        self.condition_settingButton.clicked.connect(self.condition_setting)
        #self.visualization = Visualization.Visualization()
        self.Simulation_Start.clicked.connect(self.simulation_start)
        self.Initial_State_Button.clicked.connect(self.initial_state_graph)


    def condition_setting(self):
        print("1111")
        Setting_Simulation_Value.Structure = str(self.ui.StructuresBox.currentText())
        Setting_Simulation_Value.A_state = eval(self.ui.A_StateBox.currentText())
        Setting_Simulation_Value.A_node = int(self.ui.A_NodeBox.currentText())
        Setting_Simulation_Value.A_edge = int(self.ui.A_InternalEdgeBox.currentText())
        Setting_Simulation_Value.MAX = int(self.ui.A_MAXBox.currentText())
        Setting_Simulation_Value.MIN = int(self.ui.A_MINBox.currentText())
        Setting_Simulation_Value.A_network = int(self.ui.A_StructureBox.currentText())
        Setting_Simulation_Value.B_state = eval(self.ui.B_StateBox.currentText())
        Setting_Simulation_Value.B_node = int(self.ui.B_NodeBox.currentText())
        Setting_Simulation_Value.B_edge = int(self.ui.B_InternalEdgeBox.currentText())
        Setting_Simulation_Value.B_inter_edges = int(self.ui.B_ExternalEdgeBox.currentText())
        Setting_Simulation_Value.A_inter_edges = int(self.ui.A_ExternalEdgeBox.currentText())
        Setting_Simulation_Value.B_network = int(self.ui.B_StructureBox.currentText())
        Setting_Simulation_Value.Limited_step = int(self.ui.StepBox.currentText())
        Setting_Simulation_Value.drawing_graph = bool(self.ui.DrawingBox.currentText())


    def simulation_start(self):
        changing_variable = Changing_Variable.Changing_Variable()
        changing_variable.paralleled_work()

     def initial_state_graph(self):
         layer_A = Layer_A_Modeling.Layer_A_Modeling()
         layer_B = Layer_B_Modeling.Layer_B_Modeling()
         movie = Interconnected_Layer_Modeling.Interconnected_Layer_Modeling()
         movie.draw_interconnected_network(layer_A, layer_B, 'result3')

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
    myindow = MyWindow()
    print(mywindow.ui.StructuresBox.currentText())
    mywindow.show()
    app.exec_()
