# Fastjson

### What?

Fastjson 是阿里巴巴的开源 JSON 解析库，它可以解析 JSON 格式的字符串，支持将 Java Bean 序列化为 JSON 字符串，也可以从 JSON 字符串反序列化到 JavaBean，Fastjson不但性能好而且API非常简单易用，所以用户基数巨大，一旦爆出漏洞其影响对于使用了Fastjson的Web应用来说是毁灭性的。

```
        String s = "{\"name\":\"json\",\"age\":12}";
//        String s = "";
        JSONObject jsonObject = JSONObject.parseObject(s);
        System.out.println(jsonObject.toString());
```

###  (fastjson<=1.2.24)

导入fastjson库

在pom.xml中加入

```xml
<dependencies>
    <dependency>
         <groupId>com.alibaba</groupId>
         <artifactId>fastjson</artifactId>
         <version>1.2.24</version>
     </dependency>
</dependencies>
```

### 先看看咋用

Person.java

```java
package org.example;

public class Person {
    private String name;
    private int age;
    public Person() {
        System.out.println("constructor");


    }

    public String getName() {
        System.out.println("getName");
        return name;
    }
    public void setName(String name) {
        System.out.println("setName");
        this.name = name;
    }
    public int getAge() {
        System.out.println("getAge");
        return age;
    }
    public void setAge(int age) {
        System.out.println("setAge");
        this.age = age;
    }
    @Override
    public String toString() {
        return "Person [name=" + name + ", age=" + age + "]";
    }
}

```

以这个Person类为例子

```JAVA
String s = "{\"name\":\"json\",\"age\":12}";
JSONObject jsonObject = JSONObject.parseObject(s);
System.out.println(jsonObject.toString());

'''
  {"name":"json","age":12}
```

这里将一个 JSON 格式的字符串转换为`JSONObject`对象，然后再将这个`JSONObject`对象以字符串形式输出。

```java
String s = "{\"name\":\"json\",\"age\":12}";
Person person  = JSONObject.parseObject(s, Person.class);
System.out.println(person.toString())
  
'''
  constructor
	setName
	setAge
	Person [name=json, age=12]
'''
```

- 当执行`JSONObject.parseObject(s, Person.class)`时，JSON 处理库会尝试将 JSON 字符串`s`中的数据填充到`Person`类的对象中。它会根据 JSON 中的键（如`"name"`和`"age"`）找到`Person`类中对应的成员变量，并设置相应的值。
- 然后，`System.out.println(person.toString())`会调用`Person`类重写的`toString()`方法，输出`Person`对象的信息。如果一切正常，输出结果应该类似于`Person{name='json', age=12}`。

- 同时根据输出的内容，我们可以得知fastjson通过调用setName和setAge来赋予给对象

##### 特性

```java
String s = "{\"@type\":\"org.example.Person\",\"name\":\"json\",\"age\":12}";
JSONObject jsonObject  = JSONObject.parseObject(s);
System.out.println(jsonObject);

'''
  constructor
	setName
	setAge
	getAge
	getName
	{"name":"json","age":12}
'''
```

我们可以通过@type来指定一个类去解析后面的字符串，我们这里指定的是Person类。

根据回显我们可以知道fastjson对Person类进行了解析，实例化，调用等一系列操作

我们可以知道fastjson可以通过输入的字符串执行不同的代码的功能，有点像后门了...



