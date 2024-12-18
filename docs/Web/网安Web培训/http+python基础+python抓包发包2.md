http+python基础+python发包抓包

# HTTP

## IP地址

- 连入互联网的计算机，每台计算机或者路由器都有一个***\*由授权机构分配的号码\****，IP地址代表这一台***\*计算机在网络中的地址\****
- **ipv4用来表示地址(127.0.0.1)，127.0.0.1是互联网上的环回地址，用于主机自我通信，也就是本机地址**
- **ipv6（十六进制），目前全球接入太多互联网设备了，ipv4不够用了，ipv6是未来的方向**

## DNS（Domain name system域名系统）

**用来将域名解析为ip地址**

## URL

**URL 是统一资源定位符，它代表了 Web 资源的唯一标识**，如同电脑上的盘符路径。最常见的 URL 格式如下所示：

```
protocol://[user[:password]@]hostname[:post]/[path]/file[?param=value]
协议   分隔符   用户信息        域名      端口   路径   资源文件   参数键   参数值
```

协议：通常来说是**http或者https，还有ftp**（File Transfer Protocol，文本传输协议）

域名：**由于IP地址具有不方便记忆并且不能显示地址组织的名称和性质等缺点，人们设计出了域名**，并通过网域名称系统（DNS，Domain Name System）来将域名和IP地址相互映射，使人更方便地访问互联网，而不用去记住能够被机器直接读取的IP地址数串。例子：（www.baidu.com）。

顶级域名是域名系统中最高级别的域名，位于域名的最右边。它通常由几个字母组成，代表[不同的](https://so.csdn.net/so/search?q=不同的&spm=1001.2101.3001.7020)含义和分类。顶级域名分为两种类型：通用顶级域名和国家顶级域名。（通用顶级域名：.com：代表商业，是最常见和最受欢迎的顶级域名之一 .net：代表网络，通常被网络服务提供商或技术相关机构使用。.org：代表组织，通常被非盈利组织或公益机构使用。）

国家顶级域名代表特定的国家或地区。每个国家或地区都有自己的国家顶级域名，例如：.cn：代表中国 .uk：代表英国 .jp：代表日本

一级域名baidu.com

二级级域名www.baidu.com，万维网，万维网利用网页之间的链接将不同网站的网页链接成一张逻辑上的信息网，从而用户可以方便的从internet上的一个站点去访问另一个站点 。

域名等级由点号个数区分

端口：ip比作宿舍，端口就像宿舍门牌号（80，443）

## 什么是 HTTP

HTTP 是 Web 领域的核心通信协议。最初的 HTTP 支持基于文本的静态资源获取，随着协议版本的不断迭代，它已经支持如今常见的复杂分布式应用程序。

HTTP 使用一种基于消息的模型，建立于 TCP 层之上。由客户端发送一条请求消息，而后由服务器返回一条响应消息。

（**hypertext transfer protocol超文本传输协议，hypertext是一种文本类型，它允许通过链接（通常称为超链接）从一个文档跳转到另一个文档或文档中的特定部分**。）

## HTTP 协议的工作过程

当我们在浏览器输入一个网址，此时浏览器就会给对应的服务器发送一个 HTTP 请求，对应的服务器收到这个请求之后，经过计算处理，就会返回一个 HTTP 响应。并且当我们访问一个网站时，可能涉及不止一次的 HTTP 请求和响应的交互过程。

**基础术语：**

- **客户端：** 主动发起网络请求的一端
- **服务器：** 被动接收网络请求的一端
- **请求：** 客户端给服务器发送的数据
- **响应：** 服务器给客户端返回的数据
- **HTTP 协议的重要特点：** 一发一收，一问一答

## 代理抓包

burpsuite

原理：我们在客户端和服务器中间加了一个代理。**代理，也可以理解为中介或代购，就比如你想通过中介去租房或者买房，你会将你的需求告诉给中介，中介就会去寻找房源并将找到的结果的详细情况反应给你**。代理将服务器的响应内容抓了下来。对于客户端来说，代理就相当于服务器，对于服务器来说代理就相当于客户端。

## HTTP属性

常见状态码

```
100 //请求者应当继续提出请求。 请求的初始部分已经被服务器收到，并且没有被服务器拒绝。客户端应该继续发送剩余的请求，如果请求已经完成，就忽略这个响应。服务器必须在请求完成后发送一个最终的响应。
200 OK //客户端请求成功
4xx：客户端错误 5xx：服务端错误
400 Bad Request //客户端请求有语法错误，不能被服务器所理解
401 Unauthorized //请求未经授权，这个状态代码必须和WWW-Authenticate报头域一起使用
403 Forbidden //服务器收到请求，但是拒绝提供服务（权限限制，ip限制）
404 Not Found //请求资源不存在，eg：输入了错误的URL
500 Internal Server Error //服务器发生不可预期的错误
503 Server Unavailable //服务器当前不能处理客户端的请求，一段时间后可能恢复正常
```



## HTTP请求数据格式 

HTTP请求格式是由三部分组成：

请求行（Request line）：包括请求方法、URL和协议版本。请求方法（Request method）：表示要执行的操作，常见的方法有GET、POST、PUT、DELETE等。
URL（Uniform Resource Locator）：表示要访问的资源路径。
协议版本（Protocol version）：表示使用的HTTP协议版本，如HTTP/1.1。

请求头部（Request headers）：包括一些关于请求的额外信息，如User-Agent、Content-Type、Authorization等。

请求体（Request body）：用于传输请求的数据，对于GET请求来说，请求体通常为空。

```
GET /index.html HTTP/1.1
Host: www.example.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9
 
```

上图是一个示例http请求的格式

在这个示例中：

请求行包括***\*GET方法\****、***\*URL为/index.html\****（这个不是完整的url，仅包含请求资源的路径）和***\*协议版本为HTTP/1.1\****。

请求头部包括**Host**、**User-Agent**、**Accept**、**Accept-Encoding**和**Accept-Language**等字段。

请求体为空，因为这是一个GET请求。

## HTTP请求方法

| 请求方法 | 描述                                  |
| -------- | ------------------------------------- |
| GET      | 请求获取 URL 资源                     |
| POST     | 执行操作，请求 URL 资源后附加新的数据 |
| HEAD     | 只获取资源响应消息报头                |
| PUT      | 请求服务器存储一个资源                |
| DELETE   | 请求服务器删除资源                    |
| TRACE    | 请求服务器回送收到的信息              |
| OPTIONS  | 查询服务器的支持选项                  |

1. GET：用于从服务器获取资源，也是最常见的请求方式。GET请求将请求的参数附加在URL的末尾，发送给服务器。（安全性低于post）
2. POST：用于向服务器提交数据，一般用于发送表单数据。POST请求将请求的参数放在请求体中，而不是URL中。
3. 此外，对于其他一些不太常见的请求方式，比如PATCH、TRACE等，用途较少。

## HTTP版本

| 版本     | 简述                                                         |
| -------- | ------------------------------------------------------------ |
| HTTP 0.9 | 该版本只允许 GET 方法，具有典型的无状态性，无协议头和状态码，支持纯文本 |
| HTTP 1.0 | 增加了 HEAD 和 POST 方法，支持长连接、缓存和身份认证         |
| HTTP 1.1 | 增加了 Keep-alive 机制和 PipeLining 流水线，新增了 OPTIONS、PUT、DELETE、TRACE、CONNECT 方法 |
| HTTP 2.0 | 增加了多路复用、头部压缩、随时复位等功能                     |

一般来说1.1用的最多

## HTTP请求头

```
Host: www.example.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9
```

常用的请求头参数

Accept-Language：接受的语言类型

Accept：接受的内容类型

Host：从HTTP / 1.1开始，HTTP Host标头是必需的请求标头。 它指定客户端要访问的域名。

Cookie：cookie的中文翻译是曲奇，小甜饼的意思。cookie其实就是一些数据信息，类型为“小型文本文件”，存储于电脑上的文本文件中。我们想象一个场景，当我们打开一个网站时，如果这个网站我们曾经登录过，那么当我们再次打开网站时，发现就不需要再次登录了，而是直接进入了首页。例如bilibili，csdn等网站。这是怎么做到的呢？用户第一次访问网站时，服务器对用户没有任何了解，于是通过http响应给用户发送一个cookie，让浏览器存下来，浏览器记住这个cookie之后，用户再向这个网站发送http请求的时候就带上这个cookie，服务器收到这个cookie后就能识别出这个特定的用户。一般情况下，cookie是以键值对进行表示的(key-value)，例如name=jack，这个就表示cookie的名字是name，cookie携带的值是jack。总的来说，Cookie 是服务器让浏览器帮忙携带信息的手段，就像饼干里的纸条，**浏览器会储存它，并且在后续的 HTTP 请求中再次发送给服务器**。

Referer：指定提出当前请求的原始 URL

User-Agent：提供浏览器或者客户端软件的有关信息

X-Forwarded-For：xff是告诉服务器当前请求者的最终ip的http请求头字段

## HTTP请求体

post传参，是键值对

## 实践

buuctf 极客大挑战2019 http

​			 newstarctf 公开赛道http Content-Type: application/x-www-form-urlencoded

​			 bugku[MoeCTF 2021]Do you know HTTP

​			 newstarctf 2023公开赛道 begin of http

`Content-Type`头部用于指明发送到服务器的数据类型，以便服务器正确解析请求体中的数据。

禁用xff怎么办

```
***Client-IP:127.0.0.1
***X-Real-IP:127.0.0.1 
X-Forwarded-For:127.0.0.1
X-Forwarded:127.0.0.1
Forwarded-For:127.0.0.1
Forwarded:127.0.0.1
X-Forwarded-Host:127.0.0.1 
X-remote-IP:127.0.0.1 
X-remote-addr:127.0.0.1 
True-Client-IP:127.0.0.1 
X-Client-IP:127.0.0.1 
Ali-CDN-Real-IP:127.0.0.1 
Cdn-Src-Ip:127.0.0.1 
Cdn-Real-Ip:127.0.0.1 
CF-Connecting-IP:127.0.0.1 
X-Cluster-Client-IP:127.0.0.1 
WL-Proxy-Client-IP:127.0.0.1 
Proxy-Client-IP:127.0.0.1 
Fastly-Client-Ip:127.0.0.1
True-Client-Ip:127.0.0.1
Host: 127.0.0.1
```



# Python基础

## Python环境配置

https://www.python.org/

https://www.jetbrains.com/pycharm/download/?section=windows

python下载勾选

pycharm解释器（python下载路径）

## Python中文编码

utf-8可以用来中文编码

python3默认使用utf-8编码，无需指定

## Python基础语法

不向下兼容：python3是不兼容python2的

交互式编程（cmd）：交互式编程不需要创建脚本文件，是通过 Python 解释器的交互模式进来编写代码。可以即时反馈，立刻看到代码的效果，但是不可重用，每次退出之后之前的代码不会保存

脚本式编程（pycharm）：代码通常保存在一个或多个.py文件中。通过Python解释器执行这些文件。适用于编写复杂程序、算法或长时间运行的任务。脚本可以多次运行，无需每次重新输入代码。



python标识符：标识符就是我们编程的时候使用的“名字“ , 给类、接口、方法、变量、常量名，包名等起名字的字符序列。在 Python 里，标识符由字母、数字、下划线组成，但是不能以数字开头。



python保留字符：

| and      | exec    | not    |
| -------- | ------- | ------ |
| assert   | finally | or     |
| break    | for     | pass   |
| class    | from    | print  |
| continue | global  | raise  |
| def      | if      | return |
| del      | import  | try    |
| elif     | in      | while  |
| else     | is      | with   |
| except   | lambda  | yield  |

列表显示了在Python中的保留字。这些保留字不能用作常数或变数，或任何其他标识符名称。



行和缩进：学习 Python 与其他语言最大的区别就是，Python 的代码块不使用大括号 **{}** 来控制类，函数以及其他逻辑判断。python 最具特色的就是用缩进来写模块。缩进的空白数量是可变的，但是所有代码块语句必须包含相同的缩进空白数量，这个必须严格执行。



结束符：Python语句中一般以新行作为语句的结束符。如果要在一行内写多条语句，就要用‘；’。



python引号：Python 可以使用引号( **'** )、双引号( **"** )、三引号( **'''** 或 **"""** ) 来表示字符串，引号的开始与结束必须是相同类型的



python注释：python中单行注释采用 **#** 开头。



print：python3中的print是个函数，因此必须要加（），python2不用。



## Python变量类型

赋值：“=”

多变量赋值：a=b=c=1、a,b,c=1,2,3

标准数据类型：数字，字符串，列表，元组，字典



数字：int，long，float，complex



字符串：str="very good"

- 从左到右索引默认0开始的，最大范围是字符串长度少1
- 从右到左索引默认-1开始的，最大范围是字符串开头

如果你要实现从字符串中获取一段子字符串的话，可以使用 **[头下标:尾下标]** 来截取相应的字符串，其中下标是从 0 开始算起，可以是正数或负数，下标可以为空表示取到头或尾。(左闭右开)



列表：a=[1,2,3,"haha"]

List（列表） 是 Python 中使用最频繁的数据类型。

列表用 **[ ]** 标识，是 python 最通用的复合数据类型。

列表可以完成大多数集合类的数据结构实现。它支持字符，数字，字符串甚至可以包含列表（即嵌套）。

列表中值的切割也可以用到变量 **[头下标:尾下标]** ，就可以截取相应的列表，从左到右索引默认 0 开始，从右到左索引默认 -1 开始，下标可以为空表示取到头或尾。



元组：a=(1,2,3,"haha")

元组是另一个数据类型，类似于 List（列表）。

元组用 **()** 标识。内部元素用逗号隔开。但是元组不能**二次赋值**，相当于只读列表。



字典：a={"1"=1,"2"="haha"}

字典(dictionary)是除列表以外python之中最灵活的内置数据结构类型。列表是有序的对象集合，字典是无序的对象集合。

两者之间的区别在于：字典当中的元素是通过**键**来存取的，而不是通过偏移存取。

字典用"{ }"标识。字典由索引(key)和它对应的值value组成。



## Python运算符

算数运算符：

以下假设变量： **a=10，b=20**：

| 运算符 | 描述                                            | 实例                                               |
| :----- | :---------------------------------------------- | :------------------------------------------------- |
| +      | 加 - 两个对象相加                               | a + b 输出结果 30                                  |
| -      | 减 - 得到负数或是一个数减去另一个数             | a - b 输出结果 -10                                 |
| *      | 乘 - 两个数相乘或是返回一个被重复若干次的字符串 | a * b 输出结果 200                                 |
| /      | 除 - x除以y                                     | b / a 输出结果 2                                   |
| %      | 取模 - 返回除法的余数                           | b % a 输出结果 0                                   |
| **     | 幂 - 返回x的y次幂                               | a**b 为10的20次方， 输出结果 100000000000000000000 |
| //     | 取整除 - 返回商的整数部分（**向下取整**）       | `>>> 9//2 4 >>> -9//2 -5`                          |



比较运算符：

以下假设变量a为10，变量b为20：

| 运算符 | 描述                                                         | 实例                                     |
| :----- | :----------------------------------------------------------- | :--------------------------------------- |
| ==     | 等于 - 比较对象是否相等                                      | (a == b) 返回 False。                    |
| !=     | 不等于 - 比较两个对象是否不相等                              | (a != b) 返回 True。                     |
| <>     | 不等于 - 比较两个对象是否不相等。**python3 已废弃。**        | (a <> b) 返回 True。这个运算符类似 != 。 |
| >      | 大于 - 返回x是否大于y                                        | (a > b) 返回 False。                     |
| <      | 小于 - 返回x是否小于y。所有比较运算符返回1表示真，返回0表示假。这分别与特殊的变量 True 和 False 等价。 | (a < b) 返回 True。                      |
| >=     | 大于等于 - 返回x是否大于等于y。                              | (a >= b) 返回 False。                    |
| <=     | 小于等于 - 返回x是否小于等于y。                              | (a <= b) 返回 True。                     |



赋值运算符：

以下假设变量a为10，变量b为20：

| 运算符 | 描述             | 实例                                  |
| :----- | :--------------- | :------------------------------------ |
| =      | 简单的赋值运算符 | c = a + b 将 a + b 的运算结果赋值为 c |
| +=     | 加法赋值运算符   | c += a 等效于 c = c + a               |
| -=     | 减法赋值运算符   | c -= a 等效于 c = c - a               |
| *=     | 乘法赋值运算符   | c *= a 等效于 c = c * a               |
| /=     | 除法赋值运算符   | c /= a 等效于 c = c / a               |
| %=     | 取模赋值运算符   | c %= a 等效于 c = c % a               |
| **=    | 幂赋值运算符     | c **= a 等效于 c = c ** a             |
| //=    | 取整除赋值运算符 | c //= a 等效于 c = c // a             |

在python中没有++自增



逻辑运算符：

and（&&），or（||)，not（!）



成员运算符：

除了以上的一些运算符之外，Python还支持成员运算符，测试实例中包含了一系列的成员，包括字符串，列表或元组。

| 运算符 | 描述                                                    | 实例                                              |
| :----- | :------------------------------------------------------ | :------------------------------------------------ |
| in     | 如果在指定的序列中找到值返回 True，否则返回 False。     | x 在 y 序列中 , 如果 x 在 y 序列中返回 True。     |
| not in | 如果在指定的序列中没有找到值返回 True，否则返回 False。 | x 不在 y 序列中 , 如果 x 不在 y 序列中返回 True。 |



## Python条件语句

```python
if 判断条件：
    执行语句……
else：
    执行语句……
```



## Python循环语句

while循环语句

```python
while 判断条件(condition)：
    执行语句(statements)……
```

for循环语句

```
for iterating_var in sequence:
   statements(s)
```



## break，continue

break跳出循环，continue进行下一次循环



# Python抓包发包

## Python库，包，模块

库>包>模块>类>函数>变量

类中包含了一些方法（函数）和变量，模块是一个.py文件，一个包是几个模块的集合，一个库是几个包的集合

## Python request库

用来get和post

requests.get(url).(text（源代码）,headers（请求头信息）, params=? )，如果get后没东西，会输出状态码

requests.post(url,data=data)，和get差不多，但多了一个要传入的post参数，记住是键值对，在python中就是字典

request.Session()

## Session

中文直译就是会话

http协议是**无状态性的**。每条http请求/响应是互相独立的，服务器并不知道两条http请求是同一用户发送的还是不同的用户发送的，就好比生活中常见的饮料自动贩售机，投入硬币，选择饮料，然后饮料出来，买饮料的人拿到饮料，整个过程中贩售机只负责识别要买的是哪种饮料并且给出饮料，并没有记录是哪个人买的，以及某个人买了哪几种，每种买了几瓶。如果考虑现在的购物网站的购物车功能，记录用户状态就很有必要了，这就需要用到会话，而http协议由于本身的无状态性就需要cookie来实现会话。Session可以让cookie保持在后续的一串请求中

```python
import requests

s = requests.Session()
# 第一步：发送一个请求，用于设置请求中的cookies
# tips: http://httpbin.org能够用于测试http请求和响应
s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
# 第二步：再发送一个请求，用于查看当前请求中的cookies
r = s.get("http://httpbin.org/cookies")
print(r.text)
```

## Python re库

正则表达式

## 正则表达式基础

python re库

在Python中需要通过正则表达式对字符串进行匹配的时候，可以使⽤⼀个python自带的模块，名字为re。

正则表达式的大致匹配过程是：
1.依次拿出表达式和文本中的字符比较，
2.如果每一个字符都能匹配，则匹配成功；一旦有匹配不成功的字符则匹配失败。
3.如果表达式中有量词或边界，这个过程会稍微有一些不同。

r：Python 中字符串的前导 r 代表原始字符串标识符，该字符串中的特殊符号不会被转义，适用于正则表达式中繁杂的特殊符号表示。 因此 r"\n" 表示包含 '\' 和 'n' 两个字符的字符串，而 "\n" 则表示只包含一个换行符的字符串。

```python
print("\\n") # 输出 \n
print(r"\n") #输出 \n
```



re.match()

语法：re.match(pattern, string, flags=0)

尝试从字符串的起始位置匹配一个模式，如果不是起始位置匹配成功的话，match()就返回none。匹配成功re.match方法返回一个匹配的对象。

如果上⼀步匹配到数据的话，可以使⽤group⽅法来提取数据。以使用group(num) 或 groups() 匹配对象函数来获取匹配表达式。

group()用来提出分组截获的字符串，（）用来分组，group() 同group（0）就是匹配正则表达式整体结果，group(1) 列出第一个括号匹配部分，group(2) 列出第二个括号匹配部分，group(3) 列出第三个括号匹配部分。没有匹配成功的，re.search()返回None。

```python
>>> import re
>>> result = re.match("itcast","itcast.cn")
>>> result.group()
'itcast'
```



字符	功能	位置
.	匹配任意1个字符（除了\n）	
[ ]	匹配[ ]中列举的字符	
\d	匹配数字，即0-9	可以写在字符集[...]中
\D	匹配⾮数字，即不是数字	可以写在字符集[...]中
\s	匹配空⽩，即空格，tab键	可以写在字符集[...]中
\S	匹配⾮空⽩字符	可以写在字符集[...]中
\w	匹配单词字符，即a-z、A-Z、0-9、_	可以写在字符集[...]中
\W	匹配⾮单词字符	可以写在字符集[...]中

```python
import re
ret = re.match(".","M")
print(ret.group())
ret = re.match("t.o","too")
print(ret.group())
ret = re.match("t.o","two")
print(ret.group())
# 如果hello的⾸字符⼩写，那么正则表达式需要⼩写的h
ret = re.match("h","hello Python")
print(ret.group())
# 如果hello的⾸字符⼤写，那么正则表达式需要⼤写的H
ret = re.match("H","Hello Python")
print(ret.group())
# ⼤⼩写h都可以的情况
ret = re.match("[hH]","hello Python")
print(ret.group())
ret = re.match("[hH]","Hello Python")
print(ret.group())
ret = re.match("[hH]ello Python","Hello Python")
print(ret.group())
# 匹配0到9的多种写法
ret = re.match("[0123456789]Hello Python","7Hello Python")
print(ret.group())
ret = re.match("[0-9]Hello Python","7Hello Python")
print(ret.group())
# 匹配0到3和5-9
ret = re.match("[0-35-9]Hello Python","7Hello Python")
print(ret.group())
ret = re.match("[0-35-9]Hello Python","4Hello Python")
#print(ret.group())
ret = re.match("嫦娥\d号","嫦娥1号发射成功")
print(ret.group())
ret = re.match("嫦娥\d号","嫦娥2号发射成功")
print(ret.group())
```

结果：

M
too
two
h
H
h
H
Hello Python
7Hello Python
7Hello Python
7Hello Python

报错

嫦娥1号
嫦娥2号



| 字符 | 功能           |
| ---- | -------------- |
| ^    | 匹配字符串开头 |
| $    | 匹配字符串结尾 |



字符	功能	位置	表达式实例	完整匹配的字符串

*	匹配前⼀个字符出现0次或者⽆限次，即可有可⽆	用在字符或(...)之后	abc*	abccc

+	匹配前⼀个字符出现1次或者⽆限次，即⾄少有1次	用在字符或(...)之后	abc+	abccc
  ?	匹配前⼀个字符出现1次或者0次，即要么有1次，要么没有	用在字符或(...)之后	abc?	ab,abc
  {m}	匹配前⼀个字符出现m次	用在字符或(...)之后	ab{2}c	abbc
  {m,n}	匹配前⼀个字符出现从m到n次，若省略m，则匹配0到n次，若省略n，则匹配m到无限次	用在字符或(...)之后	ab{1,2}c 对应的是abc,abbc



| 字符       | 功能                                                         |
| ---------- | ------------------------------------------------------------ |
| \|         | 匹配左右任意⼀个表达式                                       |
| (ab)       | 将括号中字符作为⼀个分组                                     |
| \num       | 引⽤分组num匹配到的字符串                                    |
| (?P<name>) | 分组起别名，匹配到的子串组在外部是通过定义的 *name* 来获取的 |
| (?P=name)  | 引⽤别名为name分组匹配到的字符串                             |

举例：|

```python
#匹配出0-100之间的数字
import re
ret = re.match("[1-9]?\d$|100","8")
print(ret.group()) # 8
ret = re.match("[1-9]?\d$|100","78")
print(ret.group()) # 78
ret = re.match("[1-9]?\d$|100","08")
# print(ret.group()) # 不是0-100之间
ret = re.match("[1-9]?\d$|100","100")
print(ret.group()) # 100
```

举例：()

```python
#需求：匹配出163、126、qq邮箱
ret = re.match("\w{4,20}@163\.com", "test@163.com")
print(ret.group()) # test@163.com
ret = re.match("\w{4,20}@(163|126|qq)\.com", "test@126.com")
print(ret.group()) # test@126.com
ret = re.match("\w{4,20}@(163|126|qq)\.com", "test@qq.com")
print(ret.group()) # test@qq.com
ret = re.match("\w{4,20}@(163|126|qq)\.com", "test@gmail.com")
if ret:
    print(ret.group())
else:
    print("不是163、126、qq邮箱") # 不是163、126、qq邮箱
#不是以4、7结尾的⼿机号码(11位)
tels = ["13100001234", "18912344321", "10086", "18800007777"]
for tel in tels:
    ret = re.match("1\d{9}[0-35-68-9]", tel)
    if ret:
        print(ret.group())
    else:
        print("%s 不是想要的⼿机号" % tel)
#提取区号和电话号码
ret = re.match("([^-]*)-(\d+)","010-12345678")
print(ret.group())
print(ret.group(1))
print(ret.group(2))
```

举例：\number

匹配数字代表的组合。每个括号是一个组合，组合从1开始编号。比如 (.+) \1 匹配 'the the' 或者 '55 55', 但不会匹配 'thethe' (注意组合后面的空格)。这个特殊序列只能用于匹配前面99个组合。如果 number 的第一个数位是0， 或者 number 是三个八进制数，它将不会被看作是一个组合，而是八进制的数字值。在 '[' 和 ']' 字符集合内，任何数字转义都被看作是字符。

```python
import re
# 正确的理解思路：如果在第⼀对<>中是什么，按理说在后⾯的那对<>中就应该是什么。通过引⽤分组中匹配到的数据即可，但是要注意是元字符串，即类似 r""这种格式。
ret = re.match(r"<([a-zA-Z]*)>\w*</\1>", "<html>hh</html>")
# 因为2对<>中的数据不⼀致，所以没有匹配出来
test_label = ["<html>hh</html>","<html>hh</htmlbalabala>"]
for label in test_label:
    ret = re.match(r"<([a-zA-Z]*)>\w*</\1>", label)
    if ret:
        print("%s 这是一对正确的标签" % ret.group())
    else:
        print("%s 这是⼀对不正确的标签" % label)
```

结果：

<html>hh</html> 这是一对正确的标签
<html>hh</htmlbalabala> 这是⼀对不正确的标签

  例子2：匹配出 <html><h1>www.itcast.cn</h1></html>

## Python base64库

可以用来base64解码

base64.b64decode

## bugku 秋名山车神

```python
import re
import requests

s=requests.Session()
url="http://114.67.175.224:19399/"
n=s.get(url)
res=re.search("<div>(.*)=",n.text)
p=res.group(1)
num=eval(p)
data={"value":num}
re1=s.post(url,data=data)
re1.encoding='utf-8'
print(re1.text)
```



## bugku 速度要快

```python
import requests
import re
import base64

s=requests.Session()
url="http://114.67.175.224:16814/"
get=s.get(url)
get.encoding="utf-8"
head=get.headers
flag=head["Flag"]
ba1=base64.b64decode(flag).decode("utf-8")
re1=re.search(":(.*)",ba1)
ba2=base64.b64decode(re1.group(1)).decode("utf-8")
payload={"margin":ba2}
post=s.post(url,payload)
post.encoding="utf-8"
print(post.text)
```









