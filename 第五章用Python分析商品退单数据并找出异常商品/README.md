## 第五章：用Python分析商品退单数据并找出异常商品

本文可以学习到以下内容：

>1. 使用 pandas 中的 read_sql 读取 sqlite 中的数据
>2. 使用飞浆模型 senta_bilstm 对评论数据进行情感分析
>3. 使用飞浆模型 lac 对评论数据进行分词
>4. 使用 groupby+agg 方法统计评论主题中消极和积极用户分布
>5. 使用 value_counts 方法统计整体评论分布情况
>6. 使用 pyecharts 绘制柱状图、词云图

**关注微信公众号《帅帅的Python》，后台回复《数据分析》获取数据及源码**

![帅帅的Python](C:/Users/admin/data_analysis/images/sspython.png)

## 项目背景

早上刚到公司，小凡就被叫去开晨会。

这么早，肯定有大事要发生。偌大的会议室，挤满了各个部门的人......

""



新的一天，从敲代码开始！

### 获取数据

```python
import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from datetime import datetime,timedelta

# 数据库地址：数据库放在上一级目录下
db_path = os.path.join(os.path.dirname(os.getcwd()), "data.db")
engine_path = "sqlite:///" + db_path
# 创建数据库引擎
engine = create_engine(engine_path)

sql = """
select 
*
from
shopRefuse
"""

df = pd.read_sql(sql, engine)

df2.sample(5)
```

![](./图片/1.png)

> shopid：商品id
>
> create_time：商品订单创建时间
>
> total_num：当天总销售商品数
>
> td_num：当天销售商品退单数

### 数据计算

根据商品的创建时间获取当天对应的周一和周日，函数如下：


```python
def get_monday_to_sunday(today, weekly=0):
    """
    :function: 获取指定日期的周一和周日的日期
    :param today: '2021-11-16'; 当前日期：today = datetime.now().strftime('%Y-%m-%d')
    :param weekly: 获取指定日期的上几周或者下几周，weekly=0当前周，weekly=-1上一周，weekly=1下一周
    :return: 返回指定日期的周一和周日日期
    :return_type: tuple
    """
    last = weekly * 7
    today = datetime.strptime(str(today), "%Y-%m-%d")
    monday = datetime.strftime(today - timedelta(today.weekday() - last), "%Y-%m-%d")
    monday_ = datetime.strptime(monday, "%Y-%m-%d")
    sunday = datetime.strftime(monday_ + timedelta(monday_.weekday() + 6), "%Y-%m-%d")
    return "{0}|{1}".format(monday, sunday)
```

将数据重新拷贝一份，避免操作失误导致数据重跑。

为新数据添加周维度数据


```python
df2 = df.copy()
df2["week_range"] = df2["create_time"].map(lambda x:get_monday_to_sunday(str(x)[:10]))
df2.sample(5)
```

![](./图片/2.png)

根据新增的周维度数据，统计每周商品的退单率


```python
td_rate_df = df2.groupby(by=["shopid","week_range"],as_index=False).agg({"total_num":"sum","td_num":"sum"})
td_rate_df["td_rate"] = td_rate_df["td_num"]/td_rate_df["total_num"]
td_rate_df.sample(1)
```

![](./图片/3.png)

统计每周总体的退单率


```python
week_td_rate_df = df2.groupby(by="week_range",as_index=False).agg({"total_num":"sum","td_num":"sum"})

week_td_rate_df["week_td_rate"] = week_td_rate_df["td_num"]/week_td_rate_df["total_num"]

week_td_rate_df
```

![](./图片/4.png)

### 统计次数

统计每周高于均值的商品的次数


```python
merge_df = pd.merge(
    td_rate_df,week_td_rate_df[["week_range","week_td_rate"]],
    on="week_range",
    how="left"
)

merge_df["td_count"] = merge_df[["td_rate","week_td_rate"]].apply(lambda x:0 if x[0]<=x[1] else 1,axis=1)

result_df = merge_df.pivot_table(index="shopid",columns="week_range",values="td_count",margins=True,aggfunc=lambda x:x.sum())

result_df
```

![](./图片/5.png)

### 异常商品

将超过5次退单率的商品定义为异常商品


```python
unnormal_shop_df = result_df[result_df["All"]>5]
unnormal_shop_df
```

![](./图片/6.png)





