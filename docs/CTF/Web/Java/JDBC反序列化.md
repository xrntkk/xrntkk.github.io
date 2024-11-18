# JDBC反序列化

### 什么是JDBC?

> `JDBC(Java Database Connectivity)`是Java提供对数据库进行连接、操作的标准API。Java自身并不会去实现对数据库的连接、查询、更新等操作而是通过抽象出数据库操作的API接口(`JDBC`)，不同的数据库提供商必须实现JDBC定义的接口从而也就实现了对数据库的一系列操作。

### JDBC Connetion

> Java通过`java.sql.DriverManager`来管理所有数据库的驱动注册，所以如果想要建立数据库连接需要先在`java.sql.DriverManager`中注册对应的驱动类，然后调用`getConnection`方法才能连接上数据库。
>
> JDBC定义了一个叫`java.sql.Driver`的接口类负责实现对数据库的连接，所有的数据库驱动包都必须实现这个接口才能够完成数据库的连接操作。`java.sql.DriverManager.getConnection(xx)`其实就是间接的调用了`java.sql.Driver`类的`connect`方法实现数据库连接的。数据库连接成功后会返回一个叫做`java.sql.Connection`的数据库连接对象，一切对数据库的查询操作都将依赖于这个`Connection`对象。



JDBC Connetion demo

```java
String CLASS_NAME = "com.mysql.jdbc.Driver";
String URL = "jdbc:mysql://localhost:3306/mysql"
String USERNAME = "root";
String PASSWORD = "root";

Class.forName(CLASS_NAME);// 注册JDBC驱动类
Connection connection = DriverManager.getConnection(URL, USERNAME, PASSWORD);
```

我们可以看到通过JDBC来连接数据库要通过两个步骤

1. 注册驱动，`Class.forName("数据库驱动的类名")`。
2. 获取连接，`DriverManager.getConnection(xxx)`。

https://www.javasec.org/javase/JDBC/Connection.html#jdbc-connection

### JDBC反序列化

pom.xml依赖

```xml
    <dependencies>
        <dependency>
         <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <version>8.0.19</version>
        </dependency>

        <dependency>
            <groupId>commons-collections</groupId>
            <artifactId>commons-collections</artifactId>
            <version>3.2.1</version>
        </dependency>
    </dependencies>
```





