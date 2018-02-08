#-*- coding:utf8 -*-

import pymysql
import pandas as pd
from statsmodels.regression.linear_model import OLS
from sklearn.preprocessing import MinMaxScaler

# 连接数据库
conn = pymysql.connect(host="219.224.169.45", user="lizimeng",
	password="codegeass", db="market", charset="utf8")
cursor = conn.cursor()

# 初始化数据集
data = []

# 查询所有合约
cursor.execute("select distinct vari,deli from contract_daily where deli between '1401' and '1712'")
for vari,deli in cursor.fetchall():
	# 查询合约结算价
	cursor.execute("select settle from contract_daily where vari=%s and deli=%s order by day asc", (vari,deli))
	# 标准化
	scaler = MinMaxScaler()
	settle = scaler.fit_transform(cursor.fetchall())
	settle = [row[0] for row in settle]
	# 估计一阶差分方程的系数
	ols = OLS(settle[1:], [[1.,x] for x in settle[:-1]])
	result = ols.fit()
	data.append([vari, deli, result.params[0], result.params[1], result.rsquared])

# 生成DataFrame对象
df = pd.DataFrame(data, columns=['vari','deli','beta0','beta1','R2'])

# 对beta0, beta1, R2做Z标准化

# 存入文件
df.to_csv('ols.csv', index=False)

# 关闭数据库
cursor.close()
conn.close()


