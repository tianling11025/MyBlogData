---
title: Pyecharts 可视化初探
copyright: true
permalink: 1
top: 0
date: 2018-04-09 18:54:44
tags:
- Pyecharts
categories: 编程之道
password:
---
<blockquote class="blockquote-center">纸短情长啊，诉不完当时年少，我的故事还是关于你呀</blockquote>

　　最近在开发web应用过程中，需要用到可视化展示功能，因此找了找Python相关的可视化模块。这里简单记录下pyecharts模块的用法。推荐它主要是因为其功能强大，可视化功能选择比较多，且使用比较简单。
<!-- more -->

### pyecharts介绍
　　首先需要了解下pyecharts模块的运行机制，pyecharts是echarts的python-api，而echarts是百度开源的可视化框架。echarts是用来操作js文件的，因此pyecharts的出现其实是为了能够让python语言更好的对接echarts。简单来说，pyecharts会帮我们生成js文件。

### 安装pyecharts
```bash
pip install pyecharts
```
或者Github下载源码安装：https://github.com/pyecharts/pyecharts
```bash
$ git clone https://github.com/pyecharts/pyecharts.git
$ cd pyecharts
$ pip install -r requirements.txt
$ python setup.py install
```

### 简单使用pyecharts
创建一个test.py文件，写入：
```bash
from pyecharts import Bar # 柱状图

attr = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
v1 = [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]
v2 = [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3]
bar = Bar("Bar chart", "precipitation and evaporation one year")
bar.add("precipitation", attr, v1, mark_line=["average"], mark_point=["max", "min"])
bar.add("evaporation", attr, v2, mark_line=["average"], mark_point=["max", "min"])
bar.render() # 生成一个html文件
```
运行test.py，会在当前目录下生成一个render.html文件，即包含柱状图的网页。查看此html文件，会发现其生成了很多js代码。

说明：除了柱状图外，pyecharts还支持其他可视化展示，具体可参考官方文档：http://pyecharts.org/#/zh-cn/charts

### pyecharts+Django
　　前面介绍的是利用pyecharts生成一个存在可视化图表的html页面，那么怎么在Django或者Flask等Web框架中使用呢？即如何在视图层生成图表代码，传递到模版层渲染展示？这里只介绍如何在Django中使用pyecharts，其他web框架同理，可自行研究。

#### view视图层
在Django项目的view.py文件内写入:
```bash
from django.http import HttpResponse
from pyecharts import Pie

REMOTE_HOST = "https://pyecharts.github.io/assets/js"

def Pie_():
    # 生成饼图
    attr = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
    v1 = [11, 12, 13, 10, 10, 10]
    pie = Pie("饼图示例")
    pie.add("", attr, v1, is_label_show=True)
    
    return pie

def index(request):
    # 可视化展示页面
    pie = Pie_()
    myechart=pie.render_embed() # 饼图
    host=REMOTE_HOST # js文件源地址
    script_list=pie.get_js_dependencies() # 获取依赖的js文件名称（只获取当前视图需要的js）

    return render(request,"index.html",{"myechart":myechart,"host":host,"script_list":script_list})

```

说明：REMOTE_HOST可更换成本地地址，即先前往https://github.com/pyecharts/assets clone项目，再将项目中的js目录copy到Django项目的static/js目录下，然后更改代码中的REMOTE_HOST为：
```bash
REMOTE_HOST = "https://pyecharts.github.io/assets/js"
改为：
REMOTE_HOST = "../../static/js/js"
```

#### Django路由
在Django项目的urls.py文件内容写入：
```bash
url(r'^$',views.index, name="index"),
```

#### 模版层
在Django项目的templates目录下创建index.html文件，写入：
```bash
<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <title>Proudly presented by PycCharts</title>
    {% for jsfile_name in script_list %}
        <script src="{{ host }}/{{ jsfile_name }}.js"></script> # 加载js文件
    {% endfor %}
</head>

<body>
  {{ myechart|safe }} # 显示可视化图表，注意要加safe，表示解析视图层传入的html内容
</body>

</html>

```
#### 运行django
```bash
python manage.py runserver
```
打开浏览器：http://127.0.0.1:8000

### 参考资料
官方文档：http://pyecharts.org/#/zh-cn/
Github项目地址：https://github.com/pyecharts/pyecharts
