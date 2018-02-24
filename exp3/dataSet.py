#-*- coding:utf8 -*-

from db import DB

class DataSet(object):
    def __init__(self):
        self.db = DB()
    
    def get_train_set(self):
        pass
    
    def get_x(self, vari, deli, day):
        '''
        '''
        pass
    
    def get_y(self, vari, deli, day):
        '''
        return price change direction of contract vari.deli in day
        '''
        _open,close = self.db.execute_sql("select open,close from contract_daily where vari=%s and deli=%s and date=%s limit 1",
                                          (vari, deli, day))[0]
        if _open is None or _open==close:
            _dir = 1    # same
        elif _open < close:
            _dir = 0    # up
        else:
            _dir = 2    # down
        return _dir
    
if __name__=='__main__':
    import datetime
    data = DataSet()
    print (data.get_y("cu", "1707", datetime.date(2017,4,14)))
    