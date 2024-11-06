

# Python_数据容器



## 数据容器：列表（List）、元组（Tuple）、字典（Dictionary）、集合（Set）



![image-20241027235231018](/Users/xrntstudio/Library/Application Support/typora-user-images/image-20241027235231018.png)

### 列表list：有序可变集合

- ##### **tip**：列表可以一次存贮多个数据，且可以为不同的数据类型，支持嵌套

###### 定义列表：

```python
name_list =['itheima','itcast','python']
print(name_list)
print(type(name_list))

‘’‘
itheima
<class 'list'>
’‘’
```

###### 定义空列表：

```python
name_list =[] #定义空列表1
name_list =list() #定义空列表2
```

###### 列表的下标：

![正向索引](/Users/xrntstudio/Library/Application Support/typora-user-images/image-20241027231536748.png)

![反向索引](/Users/xrntstudio/Library/Application Support/typora-user-images/image-20241027231553609.png)

###### 列表常用操作：



![列表常用操作](/Users/xrntstudio/Library/Application Support/typora-user-images/image-20241027231744754.png)

```python
name_list =['itheima','itcast','python']
print(name_list)

name_list.append('abc')
print(name_list)

del name_list[0]
pop=name_list.pop[2]
print(name_list)
print(pop)

index = name_list.index('itcast')
print(index)
print(name_list)
print(name_list[index])
print(f'在第{index}个')
print(len(name_list))
print(count(itcast))

'''
['itheima', 'itcast', 'python']
['itheima', 'itcast', 'python', 'abc']
['itcast', 'python']
abc
0
['itcast', 'python']
itcast
在第0个
2
1
'''

```

###### For\while 循环遍历列表：

```python
name_list = ['itheima','itcast','python']
for element in name_list:
    print(element)
index = 0
while index < len(name_list):
    print(name_list[index])
    index += 1
    
'''
itheima
itcast
python
itheima
itcast
python
'''
```



### 元组tuple:不可以修改的list

###### 元组定义：

```python
my_tuple = ('a','b','c')
```

###### 定义空元组：

```python
my_tuple = ()
my_tuple = tuple
```

###### 元组操作：与列表操作几乎一致，不过操作较少

![image-20241027233835695](/Users/xrntstudio/Library/Application Support/typora-user-images/image-20241027233835695.png)

###### 元组的遍历：同列表

```python
t4 = ("i", "am", "good", "student", "17")
for element in t4:
    print(element)
index = 0
while index < len(t4):
    print(t4[index])
    index += 1
‘’‘
i
am
good
student
17
i
am
good
student
17
’‘’
```



### 字典dict：

- 由两部分组成，一般通过字key 找到信息值value
- 字典的key是不能重复的 如果出现重复的情况的话 后面的会覆盖前面的

![image-20241027234212172](/Users/xrntstudio/Library/Application Support/typora-user-images/image-20241027234212172.png)

###### 字典的定义：

```python
dic_score ={
    'a':{"1":"100","2":'99'},
    'b': {"1": "95","2": '85'},
    'c':{"1":"50","2":"60"}
}
```

![image-20241027234346329](/Users/xrntstudio/Library/Application Support/typora-user-images/image-20241027234346329.png)

###### 字典的使用与循环：

```python
dic_score ={
    'a':{"1":"100",
    "2":'99'},
    'b': {"1": "95",
          "2": '85'},
    'c':{"1":"50",
         "2":"60"}}
print(dic_score)
print(type(dic_score))
print(dic_score['a'])

#方法一：得到所有的key进行遍历
keys = dic_score.keys()
print(keys)
for i in keys:
    print(dic_score[i])

#方法二：直接遍历
for key in stu_score:
    print(key)
    print(stu_score[key])
```

### 集合set：

- 最主要的特点就是不支持元素重复 一般用来去重 但是他的内容和前面的地方不一样的点在于其无序性的特点
- 定义空集合一定是 set（） 因为{} 是空字典

###### 基本语法：

![image-20241027235205691](/Users/xrntstudio/Library/Application Support/typora-user-images/image-20241027235205691.png)

###### 集合操作：

![image-20241027235307275](/Users/xrntstudio/Library/Application Support/typora-user-images/image-20241027235307275.png)

###### 集合运算：高中内容

- 交集（Intersection）：返回两个集合中都包含的元素，即它们的公共元素。格式：set1 & set2 或 set1.intersection(set2)

- 并集（Union）：并集运算会返回两个集合的所有元素，但不会重复，包含两者中的所有唯一元素。格式：set1 | set2 或 set1.union(set2)

- 差集（Difference）：差集运算会返回存在于第一个集合但不存在于第二个集合中的元素。格式：set1 - set2 或 set1.difference(set2)

  

###### 集合的遍历：

```python
#方法一
set1 = {1, 2, 3, 4, 5}
for element in set1:
    print(f"集合的元素有：{element}")
    
```



### Range遍历：

```python
#list
my_list = ['apple', 'banana', 'cherry']
# 使用 range() 和 len() 来按索引访问列表
for i in range(len(my_list)):
    print(f"索引 {i} 对应的元素是 {my_list[i]}")
#tuple
my_tuple = (10, 20, 30)
# 使用 range() 按索引访问元组元素
for i in range(len(my_tuple)):
    print(f"索引 {i} 对应的元素是 {my_tuple[i]}")

```

