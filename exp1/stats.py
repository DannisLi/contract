#-*- coding:utf8 -*-

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('reg.csv', header='infer', index_col=0)

for field in ["settle", "volume", "oi"]:
    df2 = df[df.field==field]
    print (field)
    # 输出R2的统计指标
    print ("R2")
    print ("mean", df2.R2.mean())
    print ("std", df2.R2.std())
    fig,ax = plt.subplots(figsize=(18,10))
    plt.title("%s R2" % field, loc="center")
    ax.hist(df2.R2.dropna(), bins=18, rwidth=0.8)
    fig.savefig("%s_R2.png" % field)
    plt.close()
    # 输出beta1的统计指标
    print ("beta1")
    print ("mean", df2.beta1.mean())
    print ("std", df2.beta1.std())
    fig,ax = plt.subplots(figsize=(18,10))
    plt.title("%s beta1" % field, loc="center")
    ax.hist(df2.beta1.dropna(), bins=18, rwidth=0.8)
    fig.savefig("%s_beta1.png" % field)
    plt.close()
    print ()
    