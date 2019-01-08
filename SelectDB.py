import MySQLdb
import pandas as pd

mysql_cn = MySQLdb.connect('localhost', user='root', passwd='2853', db='renew_competition')
my_cursor = mysql_cn.cursor()
class SelectDB:
    def __init__(self):
        s






def getDF_from_DB(db, table, structure, steps, A_in, B_in, A_ex, B_ex, layer,
                  beta_min, beta_max, ganma_min, ganma_max):
    mysql_cn = MySQLdb.connect('localhost', user='root', passwd='2853', db='%s'%db)
    my_cursor = mysql_cn.cursor()
    df = pd.read_sql_query("SELECT * FROM %s"%table+" WHERE Structure ='%s'"%structure
                           +" AND steps = %d"%steps+" AND A_internal_edges = %d"%A_in
                           +" AND B_internal_edges = %d"%B_in +" AND A_external_edges = %d"%A_ex
                           +" AND B_external_edges = %d"%B_ex +" AND Layer = '%s'"%layer
                           +" AND beta > %f"%beta_min +" AND beta <%f"&beta_max
                           +" And ganma > %f"%ganma_min+" AND ganma <%f;"&ganma_max
                           , my_cursor, index_col='index')
    return df