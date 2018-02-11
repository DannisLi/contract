#-*- coding:utf8 -*-

import pymysql
from sklearn.manifold import MDS
import numpy as np
from multiprocessing import Process

def z_score(s, inplace=True):
	# 计算平均值
	avg = 0.
	for x in s:
		avg += x
	avg /= len(s)
	# 计算标准差
	std = 0.
	for x in s:
		var += (x-avg)**2
	std /= len(s) - 1
	std = math.sqrt(std)
	# 计算标准化后的数据值
	if inplace:
		res = s
	else:
		res = [0.] * len(s)
	for i in range(len(s)):
		res[i] = (s[i]-avg) / std
	return res

def dtw(s1, s2):
	n1 = len(s1)
	n2 = len(s2)
	mat = np.mat(np.zeros((n1,n2)))
	mat[0,0] = abs(s1[0]-s2[0])
	for i in range(1,n1):
		mat[i,0] = mat[i-1,0] + abs(s1[i]-s2[0])
	for j in range(1,n2):
		mat[0,j] = mat[0,j-1] + abs(s1[0]-s2[j])
	for i in range(1,n1):
		for j in range(1,n2):
			d = abs(s1[i]-s2[j])
			mat[i,j] = min(mat[i-1,j], mat[i,j-1], mat[i-1,j-1]) + d
	return mat[n1-1,n2-1]
	
def solve(field):
	# 链接数据库
	conn = pymysql.connect(
		'host': '219.224.169.45',
		'user': 'lizimeng',
		'password': 'lizimeng',
		'db': 'market',
		'charset': 'utf8'
	)
	cursor = conn.cursor()
	# 查询研究范围内的合约的品种vari和交割期deli
	cursor.execute("select distinct vari,deli from contract_daily where deli between '1401' and '1712'")
	contracts = cursor.fetchall()
	n = len(contracts)
	# 查询各合约相应字段的数值系列，data中序列顺序与contracts对应
	data = []
	for vari,deli in contracts:
		cursor.execute("select %s from contract_daily where vari=%s and deli=%s order by day asc", (field, vari, deli))
		data.append(z_score([float(row[0]) for row in cursor.fetchall()], inplace=True))
	# 计算时间序列间的距离
	mat = np.mat(np.zeros((n, n)))
	for i in range(n-1):
		for j in range(i+1, n):
			mat[i,j] = dtw(data[i], data[j])
			mat[j,i] = mat[i,j]
	# MDS
	mds = MDS(n_components=2, n_jobs=-1, dissimilarity='precomputed')
	results = mds.fit_transform(mat)
	# 将降维结果写入文件
	with open('{}.csv'.format(field), 'w') as f:
		for row in results:
			f.write('{},{}\n'.format(row[0],row[1]))
	# 关闭数据库链接
	cursor.close()
	conn.close()
	# 宣告结束
	print ('{} finish!'.format(field))
	

if __name__=='__main__':
	Process(target=solve, args=('settle',)).start()
	Process(target=solve, args=('volume',)).start()
	Process(target=solve, args=('oi',)).start()