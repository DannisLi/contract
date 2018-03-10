#-*- coding：utf8 -*-

import datetime
from db import DB
from logit import Logit
from naiveBayes import NaiveBayes
from knn import Knn
from dataSet import DataSet
from sklearn.metrics import accuracy_score

def predict(model, dataset, vari, deli, day):
    X,Y = dataset.bootstrap(vari, deli, day, n=10**4)
    model.fit(X, Y)
    x = dataset.get_x(vari, deli, day)
    return model.predict(x)

if __name__=='__main__':
    vari,deli,m = 'cu','1712',7
    
    db = DB()
    days = db.execute("select date from contract_daily where vari=%s and deli=%s order by date asc",
                      (vari, deli))[30:]
    
    data = DataSet(m, 'direction')
    
    model = NaiveBayes(m)
    
    y_real = []
    y_pred = []
    for day in days:
        model.fit(*data.bootstrap(vari, deli, day, 300))
        r = model.predict(data.get_x(vari, deli, day))
        if r[0]>=r[1] and r[0]>=r[2]:
            r = 0
        elif r[1]>=r[0] and r[1]>=r[2]:
            r = 1
        else:
            r = 2
        y_pred.append(r)
        y_real.append(data.get_y(vari, deli, day))
    
    print (accuracy_score(y_real, y_pred))
    print (y_real)
    print (y_pred)
