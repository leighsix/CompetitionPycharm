import mysql.connector
import numpy as np
import Setting_Simulation_Value




class MakingDB:
    def __init__(self):
        self.SS = Setting_Simulation_Value.Setting_Simulation_Value()

    def setting_value_saving(self, layer_A, layer_B, Steps, beta, gamma, prob_beta, time_count):
        cnx = mysql.connector.connect(user='root', password='2853', database='renew_competition')
        cursor = cnx.cursor()

        add_data = ("INSERT INTO layer_state (Structure, A_internal_edges, B_internal_edges, "
                    "A_external_edges, B_external_edges, Steps, beta, gamma, layer_A_mean, "
                    "layer_B_mean, prob_beta, A_different_state_ratio, B_different_state_ratio, Time_count, " 
                    "consensus_index, consensus, Negative_state_number, Positive_state_number, A_node_number, "
                    "B_node_number) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

        data_info = (str(self.SS.Structure), int(self.SS.A_edge), int(self.SS.B_edge), int(self.SS.A_inter_edges),
                     int(self.SS.B_inter_edges),
                     int(Steps), float(beta), float(gamma), int(self.different_state_ratio(layer_A, layer_B)[0]),
                     float(self.different_state_ratio(layer_A, layer_B)[1]),
                     float(prob_beta), float(self.different_state_ratio(layer_A, layer_B)[0]),
                     float(self.different_state_ratio(layer_A, layer_B)[1]),
                     int(time_count), float(self.different_state_ratio(layer_A, layer_B)[2]),
                     bool(self.judging_consensus(layer_A, layer_B)),
                     int(self.counting_negative_node(layer_A, layer_B)),
                     int(self.counting_positive_node(layer_A, layer_B)),
                     int(self.SS.A_node), int(self.SS.B_node))
        cursor.execute(add_data, data_info)
        cnx.commit()
        cursor.close()
        cnx.close()

    def different_state_ratio(self, layer_A, layer_B):
        global A_ratio, B_ratio
        A_plus = sum(layer_A.A > 0)
        A_minus = sum(layer_A.A < 0)
        if A_plus >= A_minus:
            A_ratio = min(A_plus, A_minus) / self.SS.A_node
        elif A_plus < A_minus:
            A_ratio = -(min(A_plus, A_minus)) / self.SS.A_node
        B_plus = sum(layer_B.B > 0)
        B_minus = sum(layer_B.B < 0)
        if B_plus >= B_minus:
            B_ratio = min(B_plus, B_minus) / self.SS.B_node
        elif B_plus < B_minus:
            B_ratio = -(min(B_plus, B_minus)) / self.SS.B_node
        return A_ratio, B_ratio, A_ratio*B_ratio

    def layer_state_mean(self, layer_A, layer_B):
        layer_A_mean = sum(layer_A.A) / self.SS.A_node
        layer_B_mean = sum(layer_B.B) / self.SS.B_node
        return layer_A_mean, layer_B_mean

    @staticmethod
    def judging_consensus(layer_A, layer_B):
        if (((np.all(layer_A.A > 0) == 1) and (np.all(layer_B.B > 0) == 1)) or
                ((np.all(layer_A.A < 0) == 1) and (np.all(layer_B.B < 0) == 1))):
                return True
        else:
            return False

    @staticmethod
    def counting_positive_node(layer_A, layer_B):
        return sum(layer_A.A > 0) + sum(layer_B.B > 0)

    @staticmethod
    def counting_negative_node(layer_A, layer_B):
        return sum(layer_A.A < 0 ) + sum(layer_B.B < 0)

if __name__ == "__main__":
    cnx = mysql.connector.connect(user='root', password='2853', database='renew_competition')
    cursor = cnx.cursor()
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    print("DATABASE version : %s"%data)
    cursor.close()
    cnx.close()

