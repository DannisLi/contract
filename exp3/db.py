#-*- coding:utf8 -*-

import pymysql

class DB(object):
    def __init__(self):
        # 链接数据库
        self.conn = pymysql.connect(
            host = '127.0.0.1',
            user = 'root',
            password = 'codegeass',
            db = 'market',
            charset = 'utf8'
        )
        self.cursor = self.conn.cursor()
    
    def execute_sql(self, sql, params=()):
        self.cursor.execute(sql, params)
        result = self.cursor.fetchall()
        if len(result)==0:
            return None
        else:
            if len(result[0])==1:
                return [row[0] for row in result]
            else:
                return list(result)
    
    def __del__(self):
        self.cursor.close()
        self.conn.close()
        
if __name__=='__main__':
    db = DB()
    print (db.execute_sql("show tables"))
    print ()
    print (db.execute_sql("select * from contract_daily where vari=%s and deli=%s", ('a','1802')))
    print ()
    print (db.execute_sql("select vari from vari2exchange where exchange=%s", ('shfe',)))
    print ()
    print (db.execute_sql("select * from contract_daily where vari=%s and deli=%s order by date asc",
                          ('cu', '1712')))
    