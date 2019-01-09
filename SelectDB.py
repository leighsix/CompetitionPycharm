import mysql.connector
import pandas as pd
import Setting_Simulation_Value
import sqlalchemy

engine1 = sqlalchemy.create_engine('mysql://root:2853@localhost:3306/layer_state')
engine2 = sqlalchemy.create_engine('mysql://root:2853@localhost:3306/average_layer_state')
cnx1 = mysql.connector.connect(user='root', password='2853', database='renew_competition')
cursor1 = cnx1.cursor()

class SelectDB:
    def __init__(self):
        self.SS = Setting_Simulation_Value.Setting_Simulation_Value()

    def select_data_for_avg_from_DB(self, beta, gamma, value):
        query = "SELECT AVG(%s)" % value + "FROM layer_state WHERE Structure = %s" % str(self.SS.Structure) \
                + "AND A_internal_edges = %s" % int(self.SS.A_edge) \
                + "AND B_internal_edges = %s" % int(self.SS.B_edge) \
                + "AND A_external_edges = %s" % int(self.SS.A_inter_edges) \
                + "AND B_external_edges = %s" % int(self.SS.B_inter_edges) \
                + "AND Steps = %s" % int(self.SS.Limited_step) + "AND beta = %s" % beta \
                + "AND gamma = %s" % gamma + "AND A_node_number = %s"% int(self.SS.A_node) \
                + "AND B_node_number = %s;" % int(self.SS.B_node)
        df = pd.read_sql_query(query, engine1)
        return df

        # 선택 사항
        # layer_A_mean, layer_B_mean, prob_beta, A_different_state_ratio, B_different_state_ratio, Time_count,
        # consensus_index, consensus, negative_state_number, positive_state_number



    def getDataFrame_from_DB(self, table, structure, steps, A_in, B_in, A_ex, B_ex,
                             layer, beta_min, beta_max, gamma_min, gamma_max):
        df = pd.read_sql_query("SELECT * FROM %s" % table + " WHERE Structure ='%s'" % structure
                               + " AND steps = %d" % steps + " AND A_internal_edges = %d" % A_in
                               + " AND B_internal_edges = %d" % B_in + " AND A_external_edges = %d" % A_ex
                               + " AND B_external_edges = %d" % B_ex + " AND Layer = '%s'" % layer
                               + " AND beta > %f" % beta_min + " AND beta <%f" % beta_max
                               + " And gamma > %f" % gamma_min + " AND gamma <%f;" % gamma_max
                               , engine1, index_col='index')
        return df







