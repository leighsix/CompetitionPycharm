import Setting_Simulation_Value
import SelectDB
import mysql.connector


class DB_Management:
    def __init__(self):
        self.SS = Setting_Simulation_Value.Setting_Simulation_Value()
        self.select_db = SelectDB.SelectDB()

    def db_update_query(self, table):
        cnx = mysql.connector.connect(user='root', password='2853',
                                      host='127.0.0.1', database='renew_competition')
        curA = cnx.cursor(buffered=True)
        curB = cnx.cursor(buffered=True)
        gamma_list = (self.select_db.making_select_list(table, 'gamma')).tolist()
        beta_list = (self.select_db.making_select_list(table, 'beta')).tolist()
        for gamma in gamma_list:
            for beta in beta_list:
                for i in range(1, self.SS.Limited_step+1):
                    average_query = (
                        "SELECT AVG(LAYER_A_MEAN), AVG(LAYER_B_MEAN), AVG(PROB_P), AVG(PROB_BETA), "
                        "AVG(A_DIFFERENT_STATE_RATIO), "
                        "AVG(B_DIFFERENT_STATE_RATIO), AVG(CONSENSUS_INDEX), AVG(CONSENSUS), "
                        "AVG(NEGATIVE_STATE_NUMBER), "
                        "AVG(POSITIVE_STATE_NUMBER), AVG(TIME_COUNT) "
                        "FROM %s" % table + " WHERE Structure = '%s'" % str(self.SS.Structure)
                        + " AND A_internal_edges = %s" % int(self.SS.A_edge)
                        + " AND B_internal_edges = %s" % int(self.SS.B_edge)
                        + " AND A_external_edges = %s" % int(self.SS.A_inter_edges)
                        + " AND B_external_edges = %s" % int(self.SS.B_inter_edges)
                        + " AND A_node_number = %s" % int(self.SS.A_node)
                        + " AND B_node_number = %s" % int(self.SS.B_node)
                        + " AND gamma = %s" % gamma + " AND beta = %s" % beta
                        + " AND Steps = %s;" % i)

                    update_query = (
                        "UPDATE %s" % table + " SET LAYER_A_MEAN = %s,"
                        " LAYER_B_MEAN = %s, PROB_P = %s, PROB_BETA = %s," 
                        " A_DIFFERENT_STATE_RATIO = %s, B_DIFFERENT_STATE_RATIO = %s," 
                        " CONSENSUS_INDEX = %s, CONSENSUS = %s,"
                        " NEGATIVE_STATE_NUMBER = %s, POSITIVE_STATE_NUMBER = %s, TIME_COUNT = %s" +
                        " WHERE Structure = '%s'" % str(self.SS.Structure)
                        + " AND A_internal_edges = %s" % int(self.SS.A_edge)
                        + " AND B_internal_edges = %s" % int(self.SS.B_edge)
                        + " AND A_external_edges = %s" % int(self.SS.A_inter_edges)
                        + " AND B_external_edges = %s" % int(self.SS.B_inter_edges)
                        + " AND A_node_number = %s" % int(self.SS.A_node)
                        + " AND B_node_number = %s" % int(self.SS.B_node)
                        + " AND gamma = %s" % gamma + " AND beta = %s" % beta
                        + " AND Steps = %s;" % i)

                    curA.execute(average_query)
                    for (LAYER_A_MEAN, LAYER_B_MEAN, PROB_P, PROB_BETA,
                         A_DIFFERENT_STATE_RATIO, B_DIFFERENT_STATE_RATIO, CONSENSUS_INDEX,
                         CONSENSUS, NEGATIVE_STATE_NUMBER, POSITIVE_STATE_NUMBER, TIME_COUNT) in curA:

                        curB.execute(update_query, (LAYER_A_MEAN, LAYER_B_MEAN, PROB_P, PROB_BETA,
                                                    A_DIFFERENT_STATE_RATIO, B_DIFFERENT_STATE_RATIO, CONSENSUS_INDEX,
                                                    CONSENSUS, NEGATIVE_STATE_NUMBER, POSITIVE_STATE_NUMBER,
                                                    TIME_COUNT))

                        cnx.commit()
                        print("{}, {}".format(PROB_P, PROB_BETA))
        cnx.close()


if __name__ == "__main__":
    print("DB_Management")
    db_management = DB_Management()
    db_management.db_update_query('average_layer_state')
    print("DB_Management_finished")

