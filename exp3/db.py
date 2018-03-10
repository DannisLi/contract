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
    
    def execute(self, query, params=()):
        # 执行SQL语句并返回执行结果
        # 若无结果，返回None；若结果只有一列，返回一个列表；过结果为多列，返回一个元组的列表，每个元组代表一行
        self.cursor.execute(query, params)
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
    # test
    db = DB()
    print ("只有一列、不带参数时")
    print (db.execute("show tables"))
    print ()
    print ("不存在时")
    print (db.execute("select * from contract_daily where vari=%s and deli=%s", ('a','2002')))
    print ()
    print ("只有一列、带参数时")
    print (db.execute("select vari from vari2exchange where exchange=%s", ('shfe',)))
    print ()
    print ("有多列、带参数时")
    print (db.execute("select * from contract_daily where vari=%s and deli=%s order by date asc",
                      ('cu', '1712')))
    