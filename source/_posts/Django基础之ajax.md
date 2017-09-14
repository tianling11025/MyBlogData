---
title: Django基础之ajax
copyright: true
permalink: 3
top: 0
date: 2017-09-14 19:15:58
tags:
- django
categories: 编程之道
password:
---
<blockquote class="blockquote-center">Take control of your own desting
命运掌握在自己手上</blockquote>
　　本篇主要用来记录django+ajax的一些用法以及注意点，Django使用ajax最大的一个用处，就是不用刷新整个页面的前提下，请求服务端内容来更改页面中某些元素的值。如果使用http请求，就必须重新加载一遍页面，而ajax可以只更改一部分内容。
<!-- more-->
### django+ajax基础使用
#### 模版页面
index.html
```bash
<form action="/query/" method="get">
<input type="text" id="tn">
<button type="button" id="formquery">提交</button>
</form>

<span id='result'></span>

<script>
    $(document).ready(function(){
      $("#formquery").click(function(){
        var toolsname = $("#tn").val();

        $.get("/query/",{'toolsname':toolsname}, function(ret){
            $('#result').html(ret) #在页面中显示。可以用用$.ajax方法代替$.get
        })
      });
    });
</script>
```
以上代码的参数说明：
* method="get" 表示ajax使用GET方式发送请求
* id="tn" 对应着js中获取的参数名称$("#tn")
* id="formquery" 对应着按钮事件所对应的js的函数名称
* id='result' 对应着结果返回到哪个位置$('#result')

注意：这里需要注意的是button的type不能写submit，因为写了submit就直接使用get请求/query/了，而没有执行ajax请求。

#### view.py
```bash
from django.http import HttpResponse

def query(request):
    r=request.GET.get("toolsname")
    name_dict="123"
    return HttpResponse(json.dumps(name_dict), content_type='application/json')

或者可以使用JsonResponse：

from django.http import JsonResponse
def query(request):
    r=request.GET.get("toolsname")
    name_dict="123"
    return JsonResponse(name_dict)
```
说明：在视图层，即view.py中，跟正常的接受http请求的方式一样。views.py 中可以用  request.is_ajax() 方法判断是否是 ajax 请求。

### 关于ajax的一些高级用法
等我实验完再记录.......


### 参考
http://code.ziqiangxuetang.com/django/django-ajax.html
