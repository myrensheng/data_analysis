### GroupBy()：

官网地址：https://pandas.pydata.org/docs/reference/groupby.html

pandas中对数据进行分组操作的方法，官方有很详细的教程。下面的案例是真实遇到的问题，看一看用pandas是如何解决的。

### 构造数据：

```python
import pandas as pd
import numpy as np
```


```python
df = pd.DataFrame(data={
    "boss":["A"]*3+["B"]*3+["C"]*4,
    "owner":["A1","A1","A2","B1","B2","B2","C1","C1","C2","C2"],
    "month":[1,2,1,1,1,2,1,2,1,2],
    "fk_money":[10,20,30,40,50,60,70,80,90,100],
})
```

### 数据展示：

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>boss</th>
      <th>owner</th>
      <th>month</th>
      <th>fk_money</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>A</td>
      <td>A1</td>
      <td>1</td>
      <td>10</td>
    </tr>
    <tr>
      <th>1</th>
      <td>A</td>
      <td>A1</td>
      <td>2</td>
      <td>20</td>
    </tr>
    <tr>
      <th>2</th>
      <td>A</td>
      <td>A2</td>
      <td>1</td>
      <td>30</td>
    </tr>
    <tr>
      <th>3</th>
      <td>B</td>
      <td>B1</td>
      <td>1</td>
      <td>40</td>
    </tr>
    <tr>
      <th>4</th>
      <td>B</td>
      <td>B2</td>
      <td>1</td>
      <td>50</td>
    </tr>
    <tr>
      <th>5</th>
      <td>B</td>
      <td>B2</td>
      <td>2</td>
      <td>60</td>
    </tr>
    <tr>
      <th>6</th>
      <td>C</td>
      <td>C1</td>
      <td>1</td>
      <td>70</td>
    </tr>
    <tr>
      <th>7</th>
      <td>C</td>
      <td>C1</td>
      <td>2</td>
      <td>80</td>
    </tr>
    <tr>
      <th>8</th>
      <td>C</td>
      <td>C2</td>
      <td>1</td>
      <td>90</td>
    </tr>
    <tr>
      <th>9</th>
      <td>C</td>
      <td>C2</td>
      <td>2</td>
      <td>100</td>
    </tr>
  </tbody>
</table>
### 数据解释：
比如第一条数据，老板A手下的业务员A1，在第1个月的放款金额为10万。

### 问题一：老板手下的业务员在那个月的放款金额最多？
解决方法：
- 按照owner分组，对fk_money降序排列，取第一个数据

```python
result1_df = df.sort_values(by="fk_money",ascending=False).groupby(by="owner").head(1)
```


```python
result1_df
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>boss</th>
      <th>owner</th>
      <th>month</th>
      <th>fk_money</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>9</th>
      <td>C</td>
      <td>C2</td>
      <td>2</td>
      <td>100</td>
    </tr>
    <tr>
      <th>7</th>
      <td>C</td>
      <td>C1</td>
      <td>2</td>
      <td>80</td>
    </tr>
    <tr>
      <th>5</th>
      <td>B</td>
      <td>B2</td>
      <td>2</td>
      <td>60</td>
    </tr>
    <tr>
      <th>3</th>
      <td>B</td>
      <td>B1</td>
      <td>1</td>
      <td>40</td>
    </tr>
    <tr>
      <th>2</th>
      <td>A</td>
      <td>A2</td>
      <td>1</td>
      <td>30</td>
    </tr>
    <tr>
      <th>1</th>
      <td>A</td>
      <td>A1</td>
      <td>2</td>
      <td>20</td>
    </tr>
  </tbody>
</table>
解释：老板C手下的业务员C2在第2个月的放款金额最大为100万。



#### 拓展：如何取第二大的数据？

- GroupBy.nth()，取每一组第n行的数据，n从0开始，0代表第一行。
- 没有第n行的时候，不取。


```python
result1_df = df.sort_values(by="fk_money",ascending=False).groupby(by="owner",as_index=False).nth(1)
```


```python
result1_df
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>owner</th>
      <th>boss</th>
      <th>month</th>
      <th>fk_money</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>A1</th>
      <td>A</td>
      <td>1</td>
      <td>10</td>
    </tr>
    <tr>
      <th>B2</th>
      <td>B</td>
      <td>1</td>
      <td>50</td>
    </tr>
    <tr>
      <th>C1</th>
      <td>C</td>
      <td>1</td>
      <td>70</td>
    </tr>
    <tr>
      <th>C2</th>
      <td>C</td>
      <td>1</td>
      <td>90</td>
    </tr>
  </tbody>
</table>

解释：老板A手下的A1，所有放款金额中，放款金额第二多的月份是在第一个月。



### 问题二：业务员每个月的放款金额占比情况？
解决方案：
1. 计算出每个业务员总的放款金额owner_total_fk_money
2. 将df与计算好的owner_total_fk_money合并
3. fk_money除以owner_total_fk_money得到需要的数据


```python
### 代码实现：
owner_total_fk_money = df.groupby(by="owner",as_index=False).agg({"fk_money":"sum"})
```


```python
result1_df = pd.merge(df,owner_total_fk_money,on="owner",how="left",suffixes=("","_total"))
```


```python
result1_df["rate"] = (result1_df["fk_money"]/result1_df["fk_money_total"]).map(lambda x:"{:.2%}".format(x))
```


```python
result1_df
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>boss</th>
      <th>owner</th>
      <th>month</th>
      <th>fk_money</th>
      <th>fk_money_total</th>
      <th>rate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>A</td>
      <td>A1</td>
      <td>1</td>
      <td>10</td>
      <td>30</td>
      <td>33.33%</td>
    </tr>
    <tr>
      <th>1</th>
      <td>A</td>
      <td>A1</td>
      <td>2</td>
      <td>20</td>
      <td>30</td>
      <td>66.67%</td>
    </tr>
    <tr>
      <th>2</th>
      <td>A</td>
      <td>A2</td>
      <td>1</td>
      <td>30</td>
      <td>30</td>
      <td>100.00%</td>
    </tr>
    <tr>
      <th>3</th>
      <td>B</td>
      <td>B1</td>
      <td>1</td>
      <td>40</td>
      <td>40</td>
      <td>100.00%</td>
    </tr>
    <tr>
      <th>4</th>
      <td>B</td>
      <td>B2</td>
      <td>1</td>
      <td>50</td>
      <td>110</td>
      <td>45.45%</td>
    </tr>
    <tr>
      <th>5</th>
      <td>B</td>
      <td>B2</td>
      <td>2</td>
      <td>60</td>
      <td>110</td>
      <td>54.55%</td>
    </tr>
    <tr>
      <th>6</th>
      <td>C</td>
      <td>C1</td>
      <td>1</td>
      <td>70</td>
      <td>150</td>
      <td>46.67%</td>
    </tr>
    <tr>
      <th>7</th>
      <td>C</td>
      <td>C1</td>
      <td>2</td>
      <td>80</td>
      <td>150</td>
      <td>53.33%</td>
    </tr>
    <tr>
      <th>8</th>
      <td>C</td>
      <td>C2</td>
      <td>1</td>
      <td>90</td>
      <td>190</td>
      <td>47.37%</td>
    </tr>
    <tr>
      <th>9</th>
      <td>C</td>
      <td>C2</td>
      <td>2</td>
      <td>100</td>
      <td>190</td>
      <td>52.63%</td>
    </tr>
  </tbody>
</table>
解释：A1业务员在第一个月放款10万，占其总放款（30万）比例为33.33%，第二个月放款20万，占比为66.67%



### 问题三：每个老板手下业务员放款占比？
解决思路：
1. 需要知道每个老板总的放款金额，boss_df
2. 需要知道每个业务员的放款金额，owner_df
3. 按照boss字段合并boss_df和owner_df
4. 业务员的放款金额除以每个老板总的放款金额


```python
# 计算每一个boss的总fk_money
boss_df = df.groupby(by="boss",as_index=False).agg({"fk_money":"sum"})
```


```python
# 计算每一个owner的总fk_money
owner_df = df.groupby(by=["boss","owner"],as_index=False).agg({"fk_money":"sum"})
```


```python
# 合并owner_df和boss_df
result2_df = pd.merge(owner_df,boss_df,on="boss",how="left",suffixes=("_owner","_boss"))
```


```python
result2_df["占比"] = (result_df["fk_money_owner"]/result_df["fk_money_boss"]).map(lambda x:"{:.2%}".format(x))
```


```python
result2_df
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>boss</th>
      <th>owner</th>
      <th>fk_money_owner</th>
      <th>fk_money_boss</th>
      <th>占比</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>A</td>
      <td>A1</td>
      <td>30</td>
      <td>60</td>
      <td>50.00%</td>
    </tr>
    <tr>
      <th>1</th>
      <td>A</td>
      <td>A2</td>
      <td>30</td>
      <td>60</td>
      <td>50.00%</td>
    </tr>
    <tr>
      <th>2</th>
      <td>B</td>
      <td>B1</td>
      <td>40</td>
      <td>150</td>
      <td>26.67%</td>
    </tr>
    <tr>
      <th>3</th>
      <td>B</td>
      <td>B2</td>
      <td>110</td>
      <td>150</td>
      <td>73.33%</td>
    </tr>
    <tr>
      <th>4</th>
      <td>C</td>
      <td>C1</td>
      <td>150</td>
      <td>340</td>
      <td>44.12%</td>
    </tr>
    <tr>
      <th>5</th>
      <td>C</td>
      <td>C2</td>
      <td>190</td>
      <td>340</td>
      <td>55.88%</td>
    </tr>
  </tbody>
</table>
解释：老板A手下的A1占总放款金额（60万）比例为50%。
