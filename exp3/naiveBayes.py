#-*- coding:utf8 -*-


class NaiveBayes(object):
    def __init__(self, xtype, laplace=0.):
        '''
        xtype      int      输入向量的类型，有效的取值为0，1，2
        laplace    float    平滑系数
        '''
        self.laplace = laplace
        if xtype in [0,2]:
            # 特征为离散型
            pass
        elif xtype==1:
            # 特征为连续型
            pass
        else:
            assert False
    
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