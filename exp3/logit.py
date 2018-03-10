#-*- coding:utf8 -*-

from sklearn.linear_model import LogisticRegression

class Logit(object):
    def __init__(self, y_classes):
        self.model = LogisticRegression(solver='lbfgs', 
                                        max_iter=200, 
                                        multi_class='multinomial', 
                                        warm_start=False,
                                        fit_intercept=True)
        self.y_classes = y_classes
    
    def fit(self, X, Y):
        self.model.fit(X, Y)
    
    def predict(self, x):
        # 返回一个字典，表示上涨，下跌和不变的概率
        P = self.model.predict_proba([x])[0]
        ans = {}
        for i in range(self.y_classes):
            ans[i] = 0 
        i = 0
        for y in self.model.classes_:
            ans[y] += P[i]
            i += 1
        return ans

if __name__=='__main__':
    from dataSet import DataSet
    import datetime
    data = DataSet(5, 'direction')
    logit = Logit(3)
    X,Y = data.bootstrap('cu', '1707', datetime.date(2017,6,6), n=300)
    logit.fit(X, Y)
    print ('predict:', logit.predict(data.get_x('cu', '1707', datetime.date(2017,5,10))))
    print ('real:', data.get_y('cu', '1707', datetime.date(2017,5,10)))