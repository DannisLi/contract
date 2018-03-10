#-*- coding:utf8 -*-

from date import shift
from db import DB
import random

class DataSet(object):
    def __init__(self, m, xtype):
        '''
        xtype: ['return_rate', 'std_return_rate', 'return_rate_level', 'direction']
        '''
        self.m = m
        if xtype=='return_rate':
            self.get_x = self.get_return_rates
        elif xtype=='std_return_rate':
            self.get_x = self.get_std_return_rates
        elif xtype=='return_rate_level':
            self.get_x = self.get_return_rate_levels
        elif xtype=='direction':
            self.get_x = self.get_directions
        self.db = DB()
    
    def bootstrap(self, vari, deli, day, n=100):
        days = self.db.execute("select distinct date from contract_daily where vari=%s and deli=%s and date<%s order by date asc",
                               (vari, deli, day))
        assert len(days) > self.m
        days = days[self.m:]
        X = []
        Y = []
        while n>0:
            chosen_day = random.choice(days)
            X.append(self.get_x(vari, deli, chosen_day))
            Y.append(self.get_y(vari, deli, chosen_day))
            n -= 1
        return X,Y
    
    def get_y(self, vari, deli, day):
        '''
        return price change direction of contract vari.deli in day
        up      0
        same    1
        down    2
        '''
        _open,close = self.db.execute("select open,close from contract_daily where vari=%s and deli=%s and date=%s limit 1",
                                      (vari, deli, day))[0]
        if _open is None or _open==close:
            _dir = 1    # same
        elif _open < close:
            _dir = 0    # up
        else:
            _dir = 2    # down
        return _dir
    
    def get_return_rates(self, vari, deli, day):
        pass
    
    def get_std_return_rates(self, vari, deli, day):
        pass
    
    def get_directions(self, vari, deli, day):
        day1 = shift(day, -self.m)
        day2 = shift(day, -1)
        results = self.db.execute("select open,close from contract_daily where vari=%s and deli=%s and \
        date between %s and %s order by date asc", (vari, deli, day1, day2))
        ans = []
        for _open,close in results:
            if _open is None or _open==close:
                _dir = 1    # same
            elif _open < close:
                _dir = 0    # up
            else:
                _dir = 2    # down
            ans.append(_dir)
        return ans
    
    def get_return_rate_levels(self, vari, deli, day):
        pass
    
    
    
if __name__=='__main__':
    import datetime
    data = DataSet(10, 'direction')
    print (data.get_y("cu", "1707", datetime.date(2017,4,14)))
    print (data.get_directions("cu", "1605", datetime.date(2016,3,4)))
    print (data.get_x("cu", "1605", datetime.date(2016,3,4)))
    