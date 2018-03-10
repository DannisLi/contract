#方案

$$
X_t = \beta_0 + \beta_1X_{t-1} + \mu
$$

对每个合约建立三个一阶自回归模型（分别使用settle、volume、oi），记录每个模型的$\beta_0$、$\beta_1$和$R^2$到reg.csv。同时，将每个模型的样本绘制成散点图，按照时间顺序将点染色，并把回归曲线绘制到图上，将图片存为路径为 . / settle|volume|oi / vari_deli_beta0_beta1_R2.png 的文件，其中beta0、beta1、R2保留两位小数。



#结果

| 指标   | $R^2\quad(\mu,\ \sigma)$ | $\beta_1\quad(\mu,\ \sigma)$ |
| ------ | ------------------------ | ---------------------------- |
| settle | $(0.961,\ 0.047)$        | $(0.980,\ 0.027)$            |
| volume | $  (0.323,\ 0.352)$      | $(0.419,\ 0.363)$            |
| oi     | $(0.895,\ 0.175)$        | $(0.884,\ 0.251)$            |

![settle_R2](C:\Users\LiZimeng\Desktop\workspace\contract\exp1\settle_R2.png)

![settle_beta1](C:\Users\LiZimeng\Desktop\workspace\contract\exp1\settle_beta1.png)

![volume_R2](C:\Users\LiZimeng\Desktop\workspace\contract\exp1\volume_R2.png)

![volume_beta1](C:\Users\LiZimeng\Desktop\workspace\contract\exp1\volume_beta1.png)

![oi_R2](C:\Users\LiZimeng\Desktop\workspace\contract\exp1\oi_R2.png)

![oi_beta1](C:\Users\LiZimeng\Desktop\workspace\contract\exp1\oi_beta1.png)

