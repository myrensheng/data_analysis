## 将json数据转为DataFrame数据

```python
pd.DataFrame(index=c["billno"].tolist(),data=c["json_data"].map(lambda x:json.loads(x)).tolist())
```

## 统计高于某个series的个数

```python
s.where(s>s1).count()
```

## 查看历史有M3的客户

```python
dff = pd.DataFrame(df.groupby(by="FBillNo").OverdueStatus.unique()).reset_index()
dff["M3"] = dff["OverdueStatus"].map(lambda x:1 if "M3" in x else 0)
```

## 查看重复值

```python
df.iloc[df.drop_duplicates(subset="boss").index,:]
```

