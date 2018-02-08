#-*- coding:utf8 -*-

import pandas as pd
from sklearn.cluster import AgglomerativeClustering

df = pd.read_csv('data.csv', index_col=False)
clustering = AgglomerativeClustering(n_clusters=1)
clustering.fit(df.iloc[:,2:])
children = clustering.children_
