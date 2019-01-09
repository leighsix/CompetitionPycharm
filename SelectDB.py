import pandas as pd
import Setting_Simulation_Value
import sqlalchemy


class SelectDB:
    def __init__(self):
        self.SS = Setting_Simulation_Value.Setting_Simulation_Value()

    def select_data_from_DB(self, table):
        engine = sqlalchemy.create_engine('mysql+pymysql://root:2853@localhost:3306/renew_competition')
        query = "SELECT * FROM %s" % table \
                + " WHERE Structure = '%s'" % str(self.SS.Structure) \
                + " AND A_internal_edges = %s" % int(self.SS.A_edge) \
                + " AND B_internal_edges = %s" % int(self.SS.B_edge) \
                + " AND A_external_edges = %s" % int(self.SS.A_inter_edges) \
                + " AND B_external_edges = %s" % int(self.SS.B_inter_edges) \
                + " AND A_node_number = %s" % int(self.SS.A_node) \
                + " AND B_node_number = %s;" % int(self.SS.B_node)
        df = pd.read_sql_query(query, engine)
        return df
