---
title: Django基础之模版
copyright: true
permalink: 2
top: 0
date: 2017-09-15 16:33:11
tags:
- django
categories: 编程之道
password:
---
<blockquote class="blockquote-center">Life is not all roses
人生并不是康庄大道</blockquote>
　　Django中的模版即前端展示，或者说HTML页面，涉及到html、js、css的部分我不做太多了介绍，因为主要是前端的一些东西。本篇主要介绍一下模版与视图的相互传值，以及模版的继承等内容。
<!--more-->
### 创建模版
默认情况下，我们在视图函数中使用render渲染index.html页面。
```bash
def home(request):
    return render(request, 'index.html')
```
之后在应用目录下新建一个templates文件，里面新建index.html文件即可。

### 模版给视图传参
　　这一部分比较简单，比如使用form表单，向具体某个url传递一些参数，当然这里需要设置urls.py路由，不然模版的请求无法准确传达到视图的具体处理函数上。
模版：
```bash
<form action="/add/" method="get">
<input type="text" name="content">
<input type="submit">
</form>
```
视图：
```bash
def add(request):
    content=request.GET.get("content")

    return HttpResponse(content)
```
urls.py:
```bash
from django.conf.urls import url
from webapp import views #导入app的views文件

urlpatterns = [
    url(r'^add/', views.add),
```

模版给视图传默认值的参数:
```bash
<form action="/update/" method="GET">
    <input type="hidden" name="nid" value="{{ i.nid }}">
    <input type="submit" value="获取详情" />
</form>
```
说明：模版传给视图的update方法，参数为nid，值为i.nid。

### 视图给模版传参
将上面的视图代码改成：
```bash
def add(request):
    content="123"
    return render(request,"index.html",{"content":content})
```
模版代码：
```bash
<p>content is {{content}}</p>
```
说明：除了字符串，还可以传递字典、列表等数据结构。

#### 列表
python中字典的取值是list[0]，在模版中使用
```bash
{{ list.0 }}
```
#### 字典
python中字典的取值是dict["key"]，在模版中使用
```bash
{{ dict.key }}
```
#### FOR循环
遍历列表：
```bash
{% for i in content %}
{{ i }}
{% endfor %}
```
遍历列表且输出的值后面添加，：
```bash
{% for i in content %}
{{ i }},
{% endfor %}
```
遍历字典：
```bash
{% for key, value in info_dict.items %}
    {{ key }}: {{ value }}
{% endfor %}
```
多层循环
```bash
{% for i in content %}
{% for j in i.pan %}
{{ j }}
{% endfor %}
{% endfor %}
```
循环的参数：
```bash
forloop.counter 索引从 1 开始算
forloop.counter0    索引从 0 开始算
forloop.revcounter  索引从最大长度到 1
forloop.revcounter0 索引从最大长度到 0
forloop.first   当遍历的元素为第一项时为真
forloop.last    当遍历的元素为最后一项时为真
forloop.parentloop  用在嵌套的 for 循环中，获取上一层 for 循环的 forloop
```
判断列表是否为空：
```bash
{% for i in list %}
    <li>{{ i.name }}</li>
{% empty %}
    <li>抱歉，列表为空</li>
{% endfor %}
```
#### 逻辑判断
##### == != >= <= < >
```bash
{% if var >= 90 %}
case 1
{% elif var >= 80 %}
case 2
{% elif var >= 70 %}
case 3
{% elif var >= 60 %}
case 4
{% else %}
case 5
{% endif %}
```
##### and not or in not in
```bash
{% if num <= 100 and num >= 0 %}
case 1
{% else %}
case 2
{% endif %}
```
判断元素是否在列表中：
```bash
{% if 'nmask' in List %}
case 1
{% endif %}
```
##### 内置变量
```bash
{{ request.user }} 当前用户
{{ request.path }} 当前网址
{{ request.GET.urlencode }} 当前get参数
```

### 模版继承
　　一般开发网页都需要写一些模版页面，比如导航栏、底部版权、侧边导航等，或者是某些功能代码。以前可能会使用iframe框架，但现在已经被淘汰了。为了避免重复写代码，也为了后期修改方便，可以使用模版继承的方式。所谓模版继承，就是先写好一个通用的模版，然后标记一些变量，其他页面继承后对标记的地方可以自行修改，若不修改模版使用模版页的内容。
base.html
```bash
<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="style.css" />
    <title>{% block title %}My amazing site{% endblock %}</title>
</head>

<body>
    <div id="sidebar">
        {% block sidebar %}
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/blog/">Blog</a></li>
        </ul>
        {% endblock %}
    </div>

    <div id="content">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```
说明：可以尽可能多的定义block块，这样可以自定义的地方就会比较多，可以更灵活使用。

index.html
```bash
{% extends "base.html" %}

{% block title %}My amazing blog{% endblock %}
{% block content %}
{% for entry in blog_entries %}
    <h2>{{ entry.title }}</h2>
    <p>{{ entry.body }}</p>
{% endfor %}
{% endblock %}
```
#### 多模版继承
环境：先有一个根模版，然后创建一个子模版，用来继承根模版，然后其他页面继承子模版。
base.html（父模版页面）
```bash
<!DOCTYPE html>
<html>
<head>
    {% block head %}{% endblock %}
    <title>{% block title %}{% endblock %}</title>
</head> 
<body>
{% block body %}{% endblock %}
</body>
</html>
```
base_ch.html（子模版页面）
```bash
{% extends "base.html" %}
{% block body %}

{% block js %}
<script type="text/javascript">
    var a = 1;
</script>
{% endblock %}

{% block label %}
<label>This is a base_ch module test!</label>
{% endblock %}

{% endblock %}
```
index.html(普通继承页面)
```bash
{% extends "base_ch.html" %}
{% block js %}{% endblock %}

{% block label %}
<label>This is a index page test!</label>
{% endblock %}
```
### 参考文章
http://code.ziqiangxuetang.com/django/django-template2.html
