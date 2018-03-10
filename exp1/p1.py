#-*- coding:utf8 -*-

from db import get_connection
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm

conn = get_connection("market")
cursor = conn.cursor()
reg = []

def solve(vari, deli):
    global cursor
    cursor.execute("select settle,volume,oi from contract_daily where vari=%s and deli=%s order by date asc", (vari, deli))
    df = pd.DataFrame(list(cursor.fetchall()), columns=['settle', 'volume', 'oi'])
    rows = len(df)
    for field,series in df.items():
        X = series[:-1].values
        Y = series[1:].values
        # 绘制该合约该字段的散点图
        fig,ax = plt.subplots(figsize=(12,10))
        ax.scatter(X, Y, c=[(1,i/rows,0) for i in range(rows,0,-1)], alpha=1)
        # 建立回归模型
        ols = sm.OLS(Y, sm.add_constant(X))
        result = ols.fit()
        beta0,beta1 = result.params
        R2 = result.rsquared
        # 保存模型参数
        reg.append([vari, deli, field, beta0, beta1, R2])
        # 在图中绘制回归曲线
        x_l = min(X) - (max(X) - min(X)) * 0.05
        x_r = max(X) + (max(X) - min(X)) * 0.05
        y_l = x_l * beta1 + beta0
        y_r = x_r * beta1 + beta0
        ax.plot([x_l, x_r], [y_l, y_r], color='blue')
        # 保存图片
        fig.savefig('./%s/%s_%s_%.2f_%.2f_%.2f.png' % (field, vari, deli, beta0, beta1, R2))
        # 关闭图片
        plt.close(fig)

cursor.execute("select distinct vari,deli from contract_daily where deli between '1401' and '1712'")

for vari,deli in cursor.fetchall():
    solve(vari, deli)

# 保存回归结果
df = pd.DataFrame(reg, columns=['vari', 'deli', 'field', 'beta0', 'beta1', 'R2'])
df.to_csv('reg.csv')

cursor.close()
conn.close()