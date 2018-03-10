#-*- coding:utf8 -*-

import numpy as np

class NaiveBayes(object):
    def __init__(self, m, x_classes=3, y_classes=3, laplace=1.):
        '''
        m            int      输入向量的长度
        x_classes    int      if x==0 x各维度均为连续性  else x各维度的分类数
        y_classes    int      y是分类数
        laplace      float    平滑系数
        '''
        assert laplace>=0 and x_classes>=0 and y_classes>=2 and m>0
        self.m = m
        self.x_classes = x_classes
        self.y_classes = y_classes
        self.laplace = laplace
        if self.x_classes>0:
            self.likelihood = self.discrete_likelihood
    
    def discrete_likelihood(self, y_value, x_dim, x_value):
        '''
        return P(x_{x_dim}|y)
        '''
        return self.likelihood_tensor[y_value, x_dim, x_value]
    
    def continual_likelihood(self,y, x_dim):
        pass
    
    def fit(self, X, Y):
        n = len(Y)
        # 计算先验概率和似然度
        self.prior = np.zeros(self.y_classes)
        self.likelihood_tensor = np.zeros((self.y_classes, self.m, self.x_classes))
        for i in range(n):
            x = X[i]
            y = Y[i]
            self.prior[y] += 1
            for j in range(self.m):
                self.likelihood_tensor[y, j, x[j]] += 1
        for y in range(self.y_classes):
            for x_dim in range(self.m):
                self.likelihood_tensor[y, x_dim] = [(self.likelihood_tensor[y,x_dim,x]+self.laplace)/(self.prior[y]+self.x_classes*self.laplace) for x in range(self.x_classes)]
        self.prior = np.array([(x+self.laplace)/(n+self.y_classes*self.laplace) for x in self.prior])
        
    
    def predict(self, x):
        P = [1.] * self.y_classes
        for i in range(self.y_classes):
            P[i] = self.prior[i]
            for j in range(self.m):
                P[i] *= self.likelihood(i, j, x[j])
        s = sum(P)
        P = [1.*x/s for x in P]
        res = {}
        for i in range(self.y_classes):
            res[i] = P[i]
        return res
    
if __name__=='__main__':
    from dataSet import DataSet
    import datetime
    data = DataSet(5, 'direction')
    model = NaiveBayes(5)
    X,Y = data.bootstrap('cu', '1707', datetime.date(2017,6,6), n=300)
    model.fit(X, Y)
    print ('predict:', model.predict(data.get_x('cu', '1707', datetime.date(2017,6,6))))
    print ('real:', data.get_y('cu', '1707', datetime.date(2017,6,6)))
    