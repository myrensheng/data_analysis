```python
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import os
```

### 获取数据


```python
# 数据库地址：数据库放在上一级目录下
db_path = os.path.join(os.path.dirname(os.getcwd()),"data.db")
engine_path = "sqlite:///"+db_path
```


```python
# 获取数据函数，根据输入的SQL语句返回 DataFrame 类型数据
def link_sqlite(sql):
    engine = create_engine(engine_path)
    df = pd.read_sql(sql,con=engine)
    return df
```

### 线性数据


```python
sql = "select * from predictSalesSummary where shopid=1"
df = link_sqlite(sql)
```


```python
df.tail()
```


```python
from pyecharts import options as opts
from pyecharts.charts import Bar

x_names = df["month"].tolist()
tao_bao = df["amount"].tolist()

c = (
    Bar()
    .add_xaxis(x_names)
    .add_yaxis("销售额", tao_bao)
    .set_global_opts(
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=20)),
        title_opts=opts.TitleOpts(title="商品每个月销售额"),
    )
)
c.render_notebook()
```


```python
# 从2021年2月份开始，数据呈现上升的线性趋势
df2 = df.iloc[3:,:]
```


```python
# 数据复制一份，避免操作失误导致数据受损
df3 = df2.copy()
```


```python
df3["x"] = list(range(2,11))
```


```python
df3
```


```python
from sklearn import linear_model
from sklearn.metrics import mean_squared_error,r2_score
```


```python
x = df3["x"].values.tolist()
y = df3["amount"].values.tolist()

x_reshape = np.array(x).reshape(-1,1)

# x_reshape

lr = linear_model.LinearRegression()

lr.fit(x_reshape,y)

x_predict = np.array([11]).reshape(-1,1)

lr.predict(x_predict)
```

### 非线性数据


```python
shop_2_sql = "select * from predictSalesSummary where shopid=2"
shop_2_df = link_sqlite(shop_2_sql)
```


```python
shop_2_df
```


```python
from pyecharts import options as opts
from pyecharts.charts import Bar

x_names = shop_2_df["month"].tolist()
tao_bao = shop_2_df["amount"].tolist()

c = (
    Bar()
    .add_xaxis(x_names)
    .add_yaxis("销售额", tao_bao)
    .set_global_opts(
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=20)),
        title_opts=opts.TitleOpts(title="商品每个月销售额"),
    )
)
c.render_notebook()
```

商品2的销售额，在最近5个月内变化幅度不大，可以用加权平均值的方法预测下个月销售额


```python
np.sum(shop_2_df.iloc[4:,1]*np.array([0.2,0.2,0.6]))
```


```python
shop_2_df.iloc[4:,1].mean()
```


```python

```
