# 实验方案

##目的

预测合约（$contract$）的价格变化方向（$dir$），其定义为：
$$
\large
dir = \left \{
\begin{aligned}
close > open & \Leftrightarrow & 上涨 \\
close = open & \Leftrightarrow & 不变 \\
close < open & \Leftrightarrow & 下跌 \\
\end{aligned}
\right.
$$

| direction | value |
| --------- | ----- |
| up        | 0     |
| same      | 1     |
| down      | 2     |



##自变量

###前m日dir

$$
\large
X = (dir_{-1},\ dir_{-2},\ ...,\ dir_{-m})
$$

###前m日return rate (standardization)

$$
\large
X = (\frac{return\ rate_{-1}-\mu_{-1}}{\sigma_{-1}},\ \frac{return\ rate_{-2}-\mu_{-2}}{\sigma_{-2}},\ ...,\ \frac{return\ rate_{-m}-\mu_{-m}}{\sigma_{-m}}) \\
\ \\
\begin{aligned}
where:\ &\mu_i\ represents\ the\ average\ of\ all\ return\ rate_i. \\
&\sigma_i\ represents\ the\ standard\ deviation\ of\ all\ return\ rate_i.
\end{aligned}
$$

### 前m日return rate level

对于过去m日每一日的标准化后的return rate，按照下表划分等级，得到：
$$
\large
X = (return\ rate\ level_{-1},\ return\ rate\ level_{-2},\ ...,\ return\ rate\ level_{-m})
$$

| interval          | value |
| ----------------- | ----- |
| $(-\infty, -1.5)$ | 0     |
| $[-1.5, -1)$      | 1     |
| $[-1, -0.5)$      | 2     |
| $[-0.5, -0.1)$    | 3     |
| $[-0.1, 0.1]$     | 4     |
| $(0.1, 0.5]$      | 5     |
| $(0.5, 1]$        | 6     |
| $(1, 1.5]$        | 7     |
| $(1.5, +\infty)$  | 8     |



## 模型

###Logit回归

####模型定义

$$
\large
\begin{aligned}
P(up|x) & = & \frac{e^{w_1x+b_1}}{1+e^{w_1x+b_1}+e^{w_2x+b_2}} \\
P(down|x) & = & \frac{e^{w_2x+b_2}}{1+e^{w_1x+b_1}+e^{w_2x+b_2}} \\
P(same|x) & = & \frac{1}{1+e^{w_1x+b_1}+e^{w_2x+b_2}} \\
\end{aligned}
\\
\ \\
\begin{aligned}
where: x,\ w_1\ and\ w_2\ are\ m-demensional\ vectors.\ b_1\ and\ b_2\ are\ numbers.
\end{aligned}
$$

####拟合方法

极大似然估计：
$$
\large
(\widehat{w_1},\ \widehat{b_1},\ \widehat{w_2},\ \widehat{b_2}) = \arg\max P(y_1|x_1)*P(y_2|x_2)*...*P(y_n|x_n)
$$
对数形式为：
$$
\large
(\widehat{w_1},\ \widehat{b_1},\ \widehat{w_2},\ \widehat{b_2}) = \arg\max \ln P(y_1|x_1) + \ln P(y_2|x_2) + ... + \ln P(y_n|x_n)
$$


### 朴素贝叶斯方法

####模型定义

根据贝叶斯定理和独立性假设：
$$
\large
\begin{aligned}
P(y|x) & = \frac{P(x|y)*P(y)}{P(x)} \\
& = \frac{P(x^{(1)}|y) * P(x^{(2)}|y) * ... * P(x^{(m)}|y) * P(y)}{P(x)} \\
& = \frac{\displaystyle\prod_{i=1}^{m} P(x^{(i)}|y)*P(y)}{P(x)}
\end{aligned}
$$
因为y有三种取值：up、down、same，故有：
$$
\large
\begin{aligned}
&P(up|x) \\
& = \frac{P(up|x)}{P(up|x) + P(down|x) + P(same|x)} \\
& = \frac{\displaystyle\prod_{i=1}^{m} P(x^{(i)}|up) * P(up)}
{\displaystyle\prod_{i=1}^{m} P(x^{(i)}|up) * P(up) + 
\displaystyle\prod_{i=1}^{m} P(x^{(i)}|down) * P(down) +
\displaystyle\prod_{i=1}^{m} P(x^{(i)}|same) * P(same)}
\end{aligned}
$$
$P(down|x)$和$P(same|x)$的计算方法与$P(up|x)$同理。

#### 拟合方法

先验概率（$prior$）：
$$
\large
\begin{aligned}
P(y=up) & = \frac{\sum_{i=1}^n I(y_i=up) + \lambda}{n + 3\lambda} \\
P(y=down) & = \frac{\sum_{i=1}^n I(y_i=down) + \lambda}{n + 3\lambda} \\
P(y=same) & = \frac{\sum_{i=1}^n I(y_i=same) + \lambda}{n + 3\lambda}
\end{aligned}
$$
似然度（$likelihood$）：
$$
\large
\begin{aligned}
设x的m个维度的可能取值分别为：\\
x^{(1)} & : v_1^{(1)},\ v_2^{(1)},\ ...,\ v_{S_1}^{(1)} \\
x^{(2)} & : v_1^{(2)},\ v_2^{(2)},\ ...,\ v_{S_2}^{(2)} \\
... & :\ ... \\
x^{(m)} & : v_1^{(m)},\ v_2^{(m)},\ ...,\ v_{S_m}^{(m)} \\
\end{aligned}
\\
\large\ \\
\large\ \\
\large
则：P(x^{(i)}=v_j^{(i)}|y=up) = \frac{\displaystyle\sum_{k=1}^{n} I(x_k^{(i)}=v_j^{(i)}\ and\ y_k=up) + \lambda}
{\displaystyle\sum_{k=1}^{n} I(y_k=up) + S_i\lambda} \\
\large
对于y=down和y=same时，同理。
$$


###K近邻

#### 模型定义

输入：一个m维向量x

输出：价格上涨、下跌、不变的概率

算法：

1. 选出所有训练样本中，距离输入向量x距离最近的k个样本
2. 统计被选出样本的标签取各个值的频率，作为概率，输出



####拟合方法

不需要显式的拟合过程，存储训练集即可。



##抽样方法

###抽取被预测合约所有历史数据