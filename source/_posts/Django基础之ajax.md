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
<form>
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
* $.get 表示ajax使用GET方式发送请求，也可以改成$.ajax，或者$.post表示post请求
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
#### ajax获取返回值后执行js
```bash
<textarea name="content" id="content" class="form-control" rows="20"></textarea>
<script>
    $(document).ready(function(){
      $("#sub_encode").click(function(){
        var content = $("#content").val();
 
        $.get("/add/",{'content':content}, function(ret){
            document.getElementById('content').value = ret
        })
      });
</script>
```
说明：获取返回值后，将返回值填充到textarea文本框内。

#### ajax+post CSRF认证
在ajax代码前，加入以下js。
```bash
<script>
$.ajaxSetup({
    data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
});
</script>
```
#### ajax+按钮加载过渡
有时候网页中的某些功能需要比较长的时间等待，这时候使用ajax是比较好的，因为它不需要整个网页刷新，用户体验比较好。而按钮加载过渡的意思，就是当你点击按钮后，按钮字体内容变为“加载中”，等到ajax返回内容后再恢复，这样会使体验更好。

```bash
<button class="btn btn-primary btn-sm" type="button" id='sub_encode' data-loading-text="Loading加载中..." autocomplete="off" onclick="loag()">运行</button>
<!-- 将按钮过渡的代码整合到ajax中 -->
<script>
    $(document).ready(function(){
      $("#sub_encode").click(function(){
        var content = $("#content").val();
        var btn = $("#sub_encode"); //获取按钮对象
        btn.button('loading');//按钮显示为过渡状态 
 
        $.post("{% url 'run_ajax' %}",{'content':content,"type":"encode"}, function(ret){
            document.getElementById('content').value = ret
            btn.button('reset');//按钮恢复正常
        })
      });
</script>
<!-- 底部加载js -->
<script src="https://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
```

#### ajax+列表字典返回
ajax返回的内容是json格式的列表或者字典时，该如何渲染到页面？如下，若后端返回的数据是json：[{"a":"1","b":"2"},{"c":3,"d":"4"}]
```bash
<script src="https://cdn.bootcss.com/jquery/2.1.1/jquery.min.js"></script>

<input type="text" id="tn" placeholder="请输入搜索关键词">
<button type="button" id="formquery" data-loading-text="努力加载中..." autocomplete="off" onclick="loag()">搜索一下</button>
<!-- 搜索结果列表 -->
<p id="list_result" style="word-wrap:break-word;word-break:break-all;"></p>
       
<!-- ajax请求 -->
<script>
    $(document).ready(function(){
      $('#formquery').click(function(){
          var q = $("#tn").val();
          var btn = $("#formquery"); //获取按钮对象
          btn.button('loading');//按钮显示为过渡状态

          $.getJSON('/search/',{"q":q},function(ret){
            document.getElementById('list_result').innerText = ""; // 重置<p>的内容
            $.each(ret, function(i,item){ // 遍历列表
                $.each(item, function(key,value){ // 遍历字典
                    $('#list_result').append(key+":"+value)
                });
            });
            btn.button('reset');
          })
      })
    });
</script>
<!-- 底部加载js -->
<script src="https://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
```

#### ajax配合页面自动刷新
```bash
<input type="hidden" id="formquery" onclick="loag()"> # 按钮（隐藏）
<div id="task_schedule_result"></div> # 显示内容的地方

# 点击按钮事情时，发送ajax请求js
<script>
    $(document).ready(function(){
      $('#formquery').click(function(){
          $.getJSON("{% url 'task_schedule' %}",function(ret){
            document.getElementById('task_schedule_result').innerHTML = ret;
          })
      })
    });
</script>
# 自动点击按钮js
<script type="text/javascript">
    function myrefresh(){ 
    document.getElementById('formquery').click();
    } 
    setInterval("myrefresh()","10000"); # 每个10秒执行一次点击按钮
</script> 
```
说明：以上html代码是每隔10s利用ajax请求，获取后端数据代码。


### 参考
http://code.ziqiangxuetang.com/django/django-ajax.html
