# sql注入原理

原文：[SQL注入原理、攻击与防御 | 小菜学网络](https://fasionchan.com/network/security/sql-injection/)

**SQL注入**（ *SQL injection* ）是一种将恶意代码插入到程序 *SQL* 语句中，从而误导数据库执行恶意逻辑的攻击技术。通过 *SQL* 注入，攻击者可以达到获取敏感信息，窃取访问权限等目的。





### SQL注入的类型

#### 1.基于错误的信息泄露

攻击者通过触发数据库错误，分析错误消息来推断数据库结构，进而构建更复杂的攻击。

示例：

```
SELECT * FROM users WHERE username = 'admin' AND password = 'wrong_password';
```

如果数据库返回错误消息，攻击者可以从中获取有关数据库结构的信息。

#### 2.联合查询注入

攻击者利用UNION操作符将额外的查询附加到原查询上，以获取额外的信息。

示例：

```
SELECT * FROM users WHERE username = 'admin' UNION SELECT * FROM sensitive_data;
```

#### 4.盲注

当应用程序不会显示任何错误消息时，攻击者通过观察应用程序的行为变化来判断SQL语句的执行结果。这包括基于布尔响应的盲注和基于时间延迟的盲注。

##### (1). 基于布尔响应的盲注

攻击者通过发送不同的查询并观察应用程序的响应来推断数据库内容。

示例：

```
SELECT * FROM users WHERE username = 'admin' AND password = 'password' AND '1'='1';
```


如果查询成功，说明条件成立；否则，条件不成立。

##### (2). 基于时间延迟的盲注

攻击者通过在查询中引入时间延迟来判断数据库的响应时间，从而推断数据库内容。

示例：

```
SELECT * FROM users WHERE username = 'admin' AND password = 'password' AND SLEEP(5);
```

#### 4.基于带外的注入

攻击者利用数据库的功能，如HTTP请求或文件写入，将数据发送到外部服务器，从而泄露信息。

示例：

```
SELECT * FROM users WHERE username = 'admin' AND password = 'password' INTO OUTFILE '/tmp/data.txt';
```




> 原文：[SQL 注入详解：原理、危害与防范措施_sql注入的危害及安全建议-CSDN博客](https://blog.csdn.net/2301_77163982/article/details/143780864)





[SQL注入利用及绕过总结 - Mast1n - 博客园](https://www.cnblogs.com/Mast1n/p/17778123.html)