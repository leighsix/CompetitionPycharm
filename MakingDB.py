import sqlalchemy
import pandas as pd

class MakingDB:
    def __init__(self):
        self.SS = Setting_Simulation_Value.Setting_Simulation_Value()


    def average_database_saving(self, panda_db):
        engine = sqlalchemy.create_engine('mysql+pymysql://root:2853@localhost:3306/renew_competition')
        panda_db.to_sql( name = 'average_layer_state', con =engine,index = False, if_exists = 'append')


if __name__ == "__main__":
    cnx = mysql.connector.connect(user='root', password='2853', database='renew_competition')
    cursor = cnx.cursor()
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    print("DATABASE version : %s"%data)
    cursor.close()
    cnx.close()

