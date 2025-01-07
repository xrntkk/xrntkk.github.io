# php原生类利用

原文：https://blog.csdn.net/qq_44640313/article/details/134310900

### 通过脚本获取调用了常见魔术方法的原生类（有需要可以加）

```php
<?php
$classes = get_declared_classes();
foreach ($classes as $class) {
    $methods = get_class_methods($class);
    foreach ($methods as $method) {
        if (in_array($method, array(
            '__destruct',
            '__toString',
            '__wakeup',
            '__call',
            '__callStatic',
            '__get',
            '__set',
            '__isset',
            '__unset',
            '__invoke',
            '__set_state'    // 如果题目中有其他的魔术方法，可自行添加进来, 来遍历存在指定方法的原生类
        ))) {
            print $class . '::' . $method . "\n";
        }
    }
} 
```

其输出结果如下

```
Exception::__wakeup
Exception::__toString
ErrorException::__wakeup
ErrorException::__toString
Error::__wakeup
Error::__toString
ParseError::__wakeup
ParseError::__toString
TypeError::__wakeup
TypeError::__toString
ArgumentCountError::__wakeup
ArgumentCountError::__toString
ArithmeticError::__wakeup
ArithmeticError::__toString
DivisionByZeroError::__wakeup
DivisionByZeroError::__toString
Generator::__wakeup
ClosedGeneratorException::__wakeup
ClosedGeneratorException::__toString
...
```

常用的有以下几个

```
Error
Exception
SoapClient
DirectoryIterator
SimpleXMLElement
SplFileObject
```


