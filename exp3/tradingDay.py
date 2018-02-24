#-*- coding:utf8 -*-

from db import DB
import datetime

db = DB()
tdays = db.execute_sql("select distinct date from contract_daily where date between %s and %s \
order by date asc", (datetime.date(2013,1,1), datetime.date(2017,12,31)))
tdays_num = len(tdays)

def is_trading(vari, deli, day):
    res = db.execute_sql("select * from contract_daily where vari=%s and deli=%s and date=%s",
                         (vari,deli,day))
    return res is not None

def shift(day, n):
    i = tdays.index(day) + n
    assert 0 <= i < tdays_num
    return tdays[i]
