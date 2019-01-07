import numpy as np
import Layer_A_Modeling
import Layer_B_Modeling
import math


class Modeling(Layer_A_Modeling, Layer_B_Modeling) :

    def making_interconnected_edges(self):
        for i in range(int(Layer_A_Modeling.A_node / self.inter_edges)):
            for j in range(self.inter_edges):
                connected_A_node = np.array(Layer_A_Modeling.A_edges.nodes).reshape(-1, inter_edges)[i][j]
                AB_neighbor.append(connected_A_node)
                AB_edges.append((i, connected_A_node))
        AB_neighbor = np.array(AB_neighbor).reshape(-1, inter_edges)
        return AB_edges, AB_neighbor

    def simulation_condition(self, gamma_scale, beta_scale, Repeating_number, Limited_time):
        global r, D, repeating_number, limited_time
        r = np.linspace(gamma_scale[0], gamma_scale[1], gamma_scale[2])
        D = np.linspace(beta_scale[0], beta_scale[1], beta_scale[2])
        repeating_number = Repeating_number  # 평균을 내기위한 반복 횟수
        limited_time = Limited_time  # layer 변화를 위한 반복 횟수
        return r, D, repeating_number, limited_time

    def making_beta_scale(self, a):
        scale = math.log((1 / (self.B_edge + 1)) ** 3) / math.log(self.inter_edges / (self.B_edge + self.inter_edges))
        return (0, scale, a)


if __name__ == "__main__" :
    modeling = Modeling()






