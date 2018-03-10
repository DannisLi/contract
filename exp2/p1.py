#-*- coding:utf8 -*-

import pymysql
import tensorflow as tf

conn = pymysql.connect(
    host = '219.224.169.45',
    user = 'lizimeng',
    password = 'codegeass',
    db = 'market',
    charset = 'utf8'
)
cursor = conn.cursor()



cursor.close()
conn.close()