#-*- coding:utf8 -*-

import pymysql, math, datetime, random, numpy as np

db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'codegeass',
    'db': 'commodity'
}


class Model(object):
    pass


class NaiveBayes(object):
    def __init__(self, laplace):
        self.laplace = laplace
    
    def fit(self, X, Y):
        '''
        parameter:
        X    (samples, features)
        Y    (samples,)
        '''
        
        pass
    
    def predict(self, X):
        '''
        parameter:
        X    (samples, features)
        
        return:
        Y    (samples,)
        '''
        pass


class Knn(object):
    def __init__(self):
        pass
    
    def fit(self):
        pass
    
    def predict(self):
        pass


class Logit(object):
    def __init__(self):
        pass
    
    def fit(self):
        pass
    
    def predict(self):
        pass


class DataSet(object):
    def get_train_set(self):
        pass
    
    def get_x(self):
        pass
    
    def get_y(self):
        pass


conn = pymysql.connect(**db_config)
cursor = conn.cursor()
cursor.execute("select distinct date from contract_daily where date between %s and %s order by date asc",
               (datetime.date(2014,1,1), datetime.date(2017,10,31)))
tday = [row[0] for row in cursor.fetchall()]
cursor.close()
conn.close()

def z_score(L):
    n = len(L)
    avg = 0
    std = 0
    for x in L:
        avg += x
    avg /= float(n)
    for x in L:
        std += (x-avg)**2
    std = math.sqrt(std/float(n-1))
    if std==0:
        return [0.] * n
    else:
        res = []
        for x in L:
            res.append((x-avg)/std)
        return res

def shift(day, n):
    '''
    require: day is a trading day
    function: calculate the date which is the n-th day after day
    modify: null
    '''
    i = tday.index(day)
    assert 0 <= i+n < len(tday)
    return tday[i+n]

def between(a, interval):
    '''
    require: len(interval)==2 and type(a)==type(interval[0])==type(interval[1]) and a can be compared with interval[0] and interval[1]
    function: determinate if a is between interval[0] and interval[1]
    modify: null
    '''
    return interval[0] <= a <= interval[1]

class Model(object):
    RANGE_OF_M = [1,30]
    def __init__(self, m):
        '''
        require: m is int and m > 0
        function: bind the parameter m to self and connect to database
        modify: self
        '''
        # test the range of m
        if not between(m, Model.RANGE_OF_M):
            raise Exception("m must between {} and {}.".format(*Model.RANGE_OF_M))
        # bind
        self.m = m
        # connect
        self.conn = pymysql.connect(**db_config)
        self.cursor = self.conn.cursor()
        # flag=False means the model hasn't been fit
        self.flag = False
    
    def is_traded(self, vari, deli, day):
        '''
        require: null
        function: If the contract vari.deli is traded in day, return True. On the contrary, return False.
        modify: null
        '''
        if self.cursor.execute("select * from contract_daily where vari=%s and deli=%s and date=%s", (vari,deli,day))==1:
            return True
        else:
            return False
    
    def get_x(self, vari, deli, day):
        '''
        require: is_traded(vari, deli, day)==True
        function: get the input which is used to predict the direction of price change in day
        modify: null
        '''
        try:
            day1 = shift(day, -self.m)
            day2 = shift(day, -1)
        except:
            raise Exception("Data is not enough.")
        sql = "select return_rate from contract_daily where vari=%s and deli=%s and date between %s and %s and return_rate is not null"
        if self.cursor.execute(sql, (vari, deli, day1, day2))!=self.m:
            raise Exception("Data is not enough.")
        return_rate = [row[0] for row in self.cursor.fetchall()]
        # z score
        z_return_rate = z_score(return_rate)
        # convert z return rate to return rate level
        rrl = []
        for x in z_return_rate:
            if x < -1.5:
                tmp = 0
            elif -1.5 <= x < -1:
                tmp = 1
            elif -1 <= x < -0.5:
                tmp = 2
            elif -0.5 <= x < -0.1:
                tmp = 3
            elif -0.1 <= x <= 0.1:
                tmp = 4
            elif 0.1 < x <= 0.5:
                tmp = 5
            elif 0.5 < x <= 1:
                tmp = 6
            elif 1 < x <= 1.5:
                tmp = 7
            else:
                tmp = 8
            rrl.append(tmp)
        return rrl
    
    def get_y(self, vari, deli, day):
        '''
        require: is_traded(vari, deli, day)==True
        function: Get the direction of vari.deli price change in day. If vari.deli is not traded in day, 
                  raise an exception.
        modify: null
        '''
        self.cursor.execute("select dir from contract_daily where vari=%s and deli=%s and date=%s limit 1", 
                            (vari, deli, day))
        direction = self.cursor.fetchone()[0]
        return direction
    
    def fit(self, vari, deli, day):
        '''
        require: null
        function: train the model. if is_traded(vari, deli, day)==False, raise exception
        modify: self
        '''
        if not self.is_traded(vari, deli, day):
            raise Exception("({}, {}, {}) can't be predicted.".format(vari, deli, day))
        n = 600
        self.prior = np.zeros(3)
        self.likelihood = np.zeros((3, self.m, 9))
        for i in range(n):
            stop = False
            while not stop:
                try:
                    t = -random.randint(1, 80)
                    d = shift(day, t)
                    self.cursor.execute("select deli from contract_daily where vari=%s and date=%s order by rand() limit 1",
                                        (vari, d))
                    de = self.cursor.fetchone()[0]
                    _dir = self.get_y(vari, de, d)
                    rrl = self.get_x(vari, de, d)
                except:
                    continue
                self.prior[_dir] += 1
                for j in range(self.m):
                    self.likelihood[_dir][j][rrl[j]] += 1
                stop = True
        for i in range(3):
            self.prior[i] = 1. * self.prior[i] / n
        for i in range(3):
            for j in range(self.m):
                for k in range(9):
                    self.likelihood[i][j][k] = 1. * self.likelihood[i][j][k] / n
        self.flag = True
    
    def predict(self, vari, deli, day):
        '''
        require: null
        function: predict the direction of vari.deli price change in day.
                  0 means up. 1 means down. 2 means equal.
        modify: null
        '''
        if not self.flag:
            raise Exception("The model hasn't been fit.")
        if not self.is_traded(vari, deli, day):
            raise Exception("The contract vari.deli isn't traded in this day.")
        prob = np.ones(3)
        rrl = self.get_x(vari, deli, day)
        for i in range(3):
            for p in [self.prior[i]*self.likelihood[i][j][rrl[j]] for j in range(self.m)]:
                prob[i] *= p
        s = sum(prob)
        return [p/s for p in prob]
    
    def evaluate(self):
        '''
        '''
        pass
    
    def __del__(self):
        self.cursor.close()
        self.conn.close()
    
    

if __name__=='__main__':
    vari = 'cu'
    deli = '1607'
    model = Model(5)
    day = datetime.date(2016,6,1)
    while day < datetime.date(2016,7,1):
        try:
            model.fit(vari, deli, day)
            print ('日期：', day.isoformat())
            print ('先验概率：', model.prior)
            print ('预测概率:', model.predict(vari, deli, day))
            print ('实际结果：', model.get_y(vari, deli, day))
            print ()
        except:
            pass
        day += datetime.timedelta(1)
