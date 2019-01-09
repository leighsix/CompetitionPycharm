import mysql.connector
import numpy as np
import Setting_Simulation_Value
import SelectDB


class MakingDB:
    def __init__(self):
        self.SS = Setting_Simulation_Value.Setting_Simulation_Value()
        self.selectdb = SelectDB.SelectDB()

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




    def average_value_saving(self, gamma, beta):
        cnx = mysql.connector.connect(user='root', password='2853', database='renew_competition')
        cursor = cnx.cursor()
        add_avg_data = ("INSERT INTO layer_state (Structure, A_internal_edges, B_internal_edges, "
                        "A_external_edges, B_external_edges, Steps, beta, gamma, LAYER_A_MEAN, "
                        "LAYER_B_MEAN, PROB_BETA, A_DIFFERENT_STATE_RATIO, B_DIFFERENT_STATE_RATIO, TIME_COUNT, " 
                        "CONSENSUS_INDEX, CONSENSUS, NEGATIVE_STATE_NUMBER, POSITIVE_STATE_NUMBER, A_node_number, "
                        "B_node_number) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

        data_avg_info = (str(self.SS.Structure), int(self.SS.A_edge), int(self.SS.B_edge), int(self.SS.A_inter_edges),
                         int(self.SS.B_inter_edges),
                         int(self.SS.Limited_step), float(beta), float(gamma),
                         int(self.different_state_ratio(layer_A, layer_B)[0]),
                         float(self.different_state_ratio(layer_A, layer_B)[1]),
                         float(prob_beta), float(self.different_state_ratio(layer_A, layer_B)[0]),
                         float(self.different_state_ratio(layer_A, layer_B)[1]),
                         int(time_count), float(self.different_state_ratio(layer_A, layer_B)[2]),
                         bool(self.judging_consensus(layer_A, layer_B)),
                         int(self.counting_negative_node(layer_A, layer_B)),
                         int(self.counting_positive_node(layer_A, layer_B)),
                         int(self.SS.A_node), int(self.SS.B_node))
        cursor.execute(add_avg_data, data_avg_info)
        cnx.commit()
        cursor.close()
        cnx.close()

    def avg_layer_A_mean(self, gamma, beta):
        self.selectdb.select_data_for_avg_from_DB(beta, gamma, "layer_A_mean")




    def avg_layer_B_mean(self, gamma, beta):


if __name__ == "__main__":
    cnx = mysql.connector.connect(user='root', password='2853', database='renew_competition')
    cursor = cnx.cursor()
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    print("DATABASE version : %s"%data)
    cursor.close()
    cnx.close()

