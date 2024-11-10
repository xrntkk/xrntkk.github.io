# 特殊的Header头——X-Forwarded-For 与 X-Real-IP

### X-Forwarded-For

记录代理服务器的地址，每经过一个代理，该字段会加上一个记录，由于是记录来源地址，所以该字段不会保存最后一个代理服务器的地址

> - 存储客户端 ip 和反向代理IP 列表，以逗号+空格分隔
> - 记录最后直连实际服务器之前的整个代理过程
> - 可能会被伪造 ip，但是直连实际服务器这段不会被伪造

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0502c9cb16192d595bbe61f8ee5f9fc9.png)

### X-Real-IP

也是用来记录服务器的地址，但是和上面的不同，它不把记录添加到结尾，而是直接替换。

> - 请求实际服务器的 IP
> - 每过一层代理都会被覆盖掉，只需第一层设置代理
> - IP可以被伪造，但如果存在一级以上的代理，它就不会收到影响，因为每经过一次代理，它就会被覆盖

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3bbee021d2f59a0a6d7a41c3bb46a617.png)

总结来自原文[特殊的Header头——X-Forwarded-For 与 X-Real-IP 学习_x-real-ip x-forwarded-for-CSDN博客](https://blog.csdn.net/m0_47404181/article/details/107143156)

### x-client-ip