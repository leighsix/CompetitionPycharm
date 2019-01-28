import mysql.connector


class DB_Management:
    def drop_duplicate_row(self, setting):
        creating_intermediate_table = ('''
                    CREATE TABLE %s_copy LIKE %s;''' % (setting.table, setting.table))
        insert_to_intermediate_table = ('''
                    INSERT INTO %s_copy
                    SELECT * FROM %s
                    GROUP BY 
                        Structure, A_node_number, B_node_number, A_internal_edges, B_internal_edges,
                        A_external_edges, B_external_edges, beta, gamma, Steps;''' % (setting.table, setting.table))
        drop_and_rename_table = ('''
                    DROP TABLE %s;
                    ALTER TABLE %s_copy RENAME TO %s;''' % (setting.table, setting.table, setting.table))
        cnx = mysql.connector.connect(user='root', password='2853',
                                      host='127.0.0.1', database=setting.database)
        cur = cnx.cursor(buffered=True)
        cur.execute(creating_intermediate_table)
        cur.execute(insert_to_intermediate_table)
        cur.execute(drop_and_rename_table)
        cnx.commit()
        cnx.close()

if __name__ == "__main__":
    print("DB_Management")
    #setting = Setting_Simulation_Value.Setting_Simulation_Value()
    #db_management = DB_Management(setting)
    #db_management.drop_duplicate_row()
    print("DB_Management_finished")

