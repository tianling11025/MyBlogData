---
title: Django基础之URL路由
copyright: true
permalink: 1
top: 0
date: 2017-09-15 15:59:48
tags:
- django
categories: 编程之道
password:
---
<blockquote class="blockquote-center">Read, study and learn about everything imporant in your life
点点滴滴皆重要，处处学习是诀窍</blockquote>
　　Django中有个urls.py文件，专门用于管理django的url即路由，我们可以在urls.py文件中创建或者修改路由，以达到访问不同url执行不同view函数的作用。
<!--more-->
### urls.py
先看下urls.py长啥样？
```bash
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
```
　　默认情况下，django只有一条路由，即admin，当我们开启manage.py，我们只能访问到127.0.0.1:8000/admin/目录，其余的都无法访问。

#### 创建路由
　　可以看到，路由的创建符合正则表达式的规则，^表示开始，$表示结尾；
　　另外路由的匹配是从上到下的，也就是说从第一条路由开启匹配，如果满足则不往下匹配，如果不匹配则继续往下。因此为了避免访问到不存在的url，而导致报错，可以再最后添加一条匹配任何url的路由，可以跳转到404页面（自己定义），也可以跳转到主页。
```bash
from django.conf.urls import url
from django.contrib import admin
from webapp import views #导入app的views文件

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^.*$',views.index,name="index"), #定义万能路由，注意这条路由一定要放在最后。
```

#### URL伪静态改造
一般当我们要传参时，url类似：127.0.0.1/app/?a=1&b=2
此时urls.py的配置是这样的：
```bash
from django.conf.urls import url
from webapp import views #导入app的views文件

urlpatterns = [
    url(r'^app/$', views.app , name="app"),
```
此时view.py的代码是这样的：
```bash

def app(request):
    a=request.GET.get("a")
    b=request.GET.get("b")

    return HttpResponse(a+b)
```

然而如果我们想要将URL变成：127.0.0.1/app/1/2/呢？

修改urls.py：
```bash
from django.conf.urls import url
from webapp import views #导入app的views文件

urlpatterns = [
    url(r'^app/(\d+)/(\d+)/$', views.app , name="app"),
```
修改view.py：
```bash

def app(request,a,b):

    return HttpResponse(str(int(a)+int(b)))
```

#### Url name
我们看到urls.py中的路由配置中，有name字段，可有可无，但建议写上。
```bash
urlpatterns = [
    url(r'^app/$', views.app , name="app"),
```
说明：name相当于给这条路由起一个名称，好处在于路由的正则可能会经常变，随之而来的时html里面的url也需要变，因为需要与urls里的路由对应起来。但如果给路由起了名字，则可以在html中使用路由的名字，这样当路由的正则发生改变，但只要名字不变，html中就不需要改。

HTML页面中可以这样用：
```bash
{% url 'name' %} 不带参数
{% url 'name' 参数 %}  带参数的：参数可以是变量名
 
<a href="{% url 'app' 4 5 %}">link</a>
<a href="{% url 'app' %}">link</a>
<a href="{% url 'app' %}?a=1&b=2">link</a>
```

