#-*- coding:utf8 -*-

from db import DB
import datetime

db = DB()
tdays = db.execute("select distinct date from contract_daily where date between %s and %s \
order by date asc", (datetime.date(2013,1,1), datetime.date(2017,12,31)))
tdays_num = len(tdays)

def is_trading(vari, deli, day):
    # 判断该日该合约是否交易
    res = db.execute("select * from contract_daily where vari=%s and deli=%s and date=%s limit 1",
                     (vari,deli,day))
    return res is not None

def shift(day, n):
    i = tdays.index(day) + n
    assert 0 <= i < tdays_num
    return tdays[i]

if __name__=='__main__':
    d = datetime.date(2016,6,23)
    print (shift(d, 3))    # 28
    print (shift(d, -3))   # 20
    print (is_trading('cu', '1607', d))   # True
    print (is_trading('cu', '1508', d))   # False
