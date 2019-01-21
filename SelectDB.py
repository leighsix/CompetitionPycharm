import pandas as pd
import numpy as np
import Setting_Simulation_Value
import sqlalchemy


class SelectDB:
    def __init__(self):
        self.SS = Setting_Simulation_Value.Setting_Simulation_Value()

    def select_data_from_DB(self, table):
        engine = sqlalchemy.create_engine('mysql+pymysql://root:2853@localhost:3306/%s' % self.SS.database)
        query = "SELECT * FROM %s" % table \
                + " WHERE Structure = '%s'" % str(self.SS.Structure) \
                + " AND A_internal_edges = %s" % int(self.SS.A_edge) \
                + " AND B_internal_edges = %s" % int(self.SS.B_edge) \
                + " AND A_external_edges = %s" % int(self.SS.A_inter_edges) \
                + " AND B_external_edges = %s" % int(self.SS.B_inter_edges) \
                + " AND A_node_number = %s" % int(self.SS.A_node) \
                + " AND B_node_number = %s;" % int(self.SS.B_node)
        df = pd.read_sql_query(query, engine)
        df.drop_duplicates(inplace=True)
        return df

    def making_select_list(self, table, list_name):
        df = self.select_data_from_DB(table)
        df = pd.DataFrame(df[list_name])
        select_list = np.array(df.drop_duplicates())
        np.sort(select_list)
        return select_list


if __name__ == "__main__":
    print("Select DB")