# 用pandas将数据划分区间
在数据分析的过程中，经常会遇到：年龄，收入，价格以及类似的数据，在数据分析前，需要将这些数据划分到一系列区间中，再将区间进行不同的编码，对编码后的数据进行分析。

在pandas中可以使用pandas.cut()方法实现对数据的区间划分，以及对区间进行标记。

# 案例数据
- 以name,age,score为例，使用pandas.cut()方法对age、score进行区间划分。


```python
import pandas as pd
import numpy as np

df = pd.DataFrame(data={
    "name":["A","B","C","D","E","F","G","H","I","J"],
    "age":[23,26,37,46,85,12,53,80,66,32],
    "score":[13,23,22,76,56,89,99,100,10,54],
})
```

数据形式展示：

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: left;">
      <th></th>
      <th>name</th>
      <th>age</th>
      <th>score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>A</td>
      <td>23</td>
      <td>13</td>
    </tr>
    <tr>
      <th>1</th>
      <td>B</td>
      <td>26</td>
      <td>23</td>
    </tr>
    <tr>
      <th>2</th>
      <td>C</td>
      <td>37</td>
      <td>22</td>
    </tr>
    <tr>
      <th>3</th>
      <td>D</td>
      <td>46</td>
      <td>76</td>
    </tr>
    <tr>
      <th>4</th>
      <td>E</td>
      <td>85</td>
      <td>56</td>
    </tr>
    <tr>
      <th>5</th>
      <td>F</td>
      <td>12</td>
      <td>89</td>
    </tr>
    <tr>
      <th>6</th>
      <td>G</td>
      <td>53</td>
      <td>99</td>
    </tr>
    <tr>
      <th>7</th>
      <td>H</td>
      <td>80</td>
      <td>100</td>
    </tr>
    <tr>
      <th>8</th>
      <td>I</td>
      <td>66</td>
      <td>10</td>
    </tr>
    <tr>
      <th>9</th>
      <td>J</td>
      <td>32</td>
      <td>54</td>
    </tr>
  </tbody>
</table>


#  pandas.cut()介绍
用来将数据划分为不同的区间  

- x：array型数据（DataFrame的每一列数据都是array型数据）
- bins：传入int型数据，表示划分的区间个数，传入list型数据，表示自定义的区间
- labels：与bins对应区间的标签（默认为None）
- retbins：True表示返回划分的区间，False表示不返回划分的区间（默认为False）
- right：True表示左开右闭，False表示左闭右开（默认为True）

返回数据：
- x对应所在的区间，array类型
- retbins为True时，还会返回划分区间

## 一、自动划分区间
例如：bins=3,right=True,pandas会将数据划分为3个区间,划分方法,  
(max-(max-min)/bins,max]==>(60.667,85]  
(max-(max-min)/bins\*2,max-(max-min)/bins]==>(36.333.60.667]  
(max-(max-min)/bins\*3,max-(max-min)/bins\*2]==>(11.927, 36.333] 


```python
a,b = pd.cut(x=df["age"],bins=3,right=True,retbins=True)
```


```python
# a,bins传入的是int类型，自动生成的区间
0    (11.927, 36.333]
1    (11.927, 36.333]
2    (36.333, 60.667]
3    (36.333, 60.667]
4      (60.667, 85.0]
5    (11.927, 36.333]
6    (36.333, 60.667]
7      (60.667, 85.0]
8      (60.667, 85.0]
9    (11.927, 36.333]
Name: age, dtype: category
Categories (3, interval[float64]): [(11.927, 36.333] < (36.333, 60.667] < (60.667, 85.0]]
                                                                           
# b,自动划分的区间
array([11.927, 36.333, 60.667, 85.0])
```

## 二、自定义划分区间

eg：自定义一个年龄分段列表，age_bins = \[10,20,30,50,70,80,90\]  

对应的区间为：\[(10, 20\] < (20, 30] < (30, 50] < (50, 70] < (70, 80] < (80, 90]] 

这样pandas会按照age_bins指定的区间进行划分


```python
age_bins = [10,20,30,50,70,80,90]
a,b = pd.cut(x=df["age"],bins=age_bins,right=True,retbins=True)
```

a和b的值：


```python
# a返回的数据区间array对象
0    (20, 30]
1    (20, 30]
2    (30, 50]
3    (30, 50]
4    (80, 90]
5    (10, 20]
6    (50, 70]
7    (70, 80]
8    (50, 70]
9    (30, 50]
Name: age, dtype: category
Categories (6, interval[int64]): [(10, 20] < (20, 30] < (30, 50] < (50, 70] < (70, 80] < (80, 90]]

# b数据区间retbins=True
array([10, 20, 30, 50, 70, 80, 90])
```

## 三、区间左边是否包含
使用场景：当age为80的时候，应该归为(70,80]还是\[80,90)，这是个问题  

eg：bins = \[10,20,30,50,70,80,90\]，right=True

对应的区间为：\[(10, 20\] < (20, 30] < (30, 50] < (50, 70] < (70, 80] < (80, 90]]  

```python
pd.cut(x=df.age,bins=age_bins,retbins=True,right=True)

(0    (20, 30]
 1    (20, 30]
 2    (30, 50]
 3    (30, 50]
 4    (80, 90]
 5    (10, 20]
 6    (50, 70]
 7    (70, 80]
 8    (50, 70]
 9    (30, 50]
 Name: age, dtype: category
 Categories (6, interval[int64]): [(10, 20] < (20, 30] < (30, 50] < (50, 70] < (70, 80] < (80, 90]],
 array([10, 20, 30, 50, 70, 80, 90]))      
```

bins = \[10,20,30,50,70,80,90\]，right=False

对应的区间为：\[[10, 20) < [20, 30) < [30, 50) < [50, 70) < [70, 80) < [80, 90)]  


```python
pd.cut(x=df.age,bins=age_bins,retbins=True,right=False)

(0    [20, 30)
 1    [20, 30)
 2    [30, 50)
 3    [30, 50)
 4    [80, 90)
 5    [10, 20)
 6    [50, 70)
 7    [80, 90)
 8    [50, 70)
 9    [30, 50)
 Name: age, dtype: category
 Categories (6, interval[int64]): [[10, 20) < [20, 30) < [30, 50) < [50, 70) < [70, 80) < [80, 90)],
 array([10, 20, 30, 50, 70, 80, 90]))
```

## 四、区间加上标签
使用labels参数可以对区间加上标签，例如score列，小于60为不及格，60-80良好，80以上优秀  

eg:bins:\[0,60,80,100\],labels：\["不及格","良好","优秀"\]  

返回的是对应的标签，而不是对应的区间


```python
pd.cut(x=df.score,bins=[0,60,80,100],labels=["不及格","良好","优秀"])
```

代码运行结果：


```python
0    不及格
1    不及格
2    不及格
3     良好
4    不及格
5     优秀
6     优秀
7     优秀
8    不及格
9    不及格
Name: score, dtype: category
Categories (3, object): ['不及格' < '良好' < '优秀']
```



# 给数据加上区间和标签

回到最开始，给df数据加上age_range和score_label列。


```python
df["age_range"] = pd.cut(x=df["age"],bins=[10, 20, 30, 50, 70, 80, 90])
df["score_label"] = pd.cut(x=df["score"],bins=[0,60,80,100],labels=["不及格","良好","优秀"])
```

代码运行结果：

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: left;">
      <th></th>
      <th>name</th>
      <th>age</th>
      <th>score</th>
      <th>age_range</th>
      <th>score_label</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>A</td>
      <td>23</td>
      <td>13</td>
      <td>(20, 30]</td>
      <td>不及格</td>
    </tr>
    <tr>
      <th>1</th>
      <td>B</td>
      <td>26</td>
      <td>23</td>
      <td>(20, 30]</td>
      <td>不及格</td>
    </tr>
    <tr>
      <th>2</th>
      <td>C</td>
      <td>37</td>
      <td>22</td>
      <td>(30, 50]</td>
      <td>不及格</td>
    </tr>
    <tr>
      <th>3</th>
      <td>D</td>
      <td>46</td>
      <td>76</td>
      <td>(30, 50]</td>
      <td>良好</td>
    </tr>
    <tr>
      <th>4</th>
      <td>E</td>
      <td>85</td>
      <td>56</td>
      <td>(80, 90]</td>
      <td>不及格</td>
    </tr>
    <tr>
      <th>5</th>
      <td>F</td>
      <td>12</td>
      <td>89</td>
      <td>(10, 20]</td>
      <td>优秀</td>
    </tr>
    <tr>
      <th>6</th>
      <td>G</td>
      <td>53</td>
      <td>99</td>
      <td>(50, 70]</td>
      <td>优秀</td>
    </tr>
    <tr>
      <th>7</th>
      <td>H</td>
      <td>80</td>
      <td>100</td>
      <td>(70, 80]</td>
      <td>优秀</td>
    </tr>
    <tr>
      <th>8</th>
      <td>I</td>
      <td>66</td>
      <td>10</td>
      <td>(50, 70]</td>
      <td>不及格</td>
    </tr>
    <tr>
      <th>9</th>
      <td>J</td>
      <td>32</td>
      <td>54</td>
      <td>(30, 50]</td>
      <td>不及格</td>
    </tr>
  </tbody>
</table>
## 简单的分析一下

## 一、统计一下各年龄段的数量

```python
df["age_range"].value_counts()

# 分析结果
(30, 50]    3
(50, 70]    2
(20, 30]    2
(80, 90]    1
(70, 80]    1
(10, 20]    1
Name: age_range, dtype: int64
```

## 二、查看各年龄段分数分布情况

```python
pd.pivot_table(data=df,index="age_range",columns="score_label",values="name",aggfunc=lambda x:len(x),fill_value=0)

# 分析结果
score_label	不及格	良好	优秀
age_range			
(10, 20]	0	0	1
(20, 30]	2	0	0
(30, 50]	2	1	0
(50, 70]	1	0	1
(70, 80]	0	0	1
(80, 90]	1	0	0
```

