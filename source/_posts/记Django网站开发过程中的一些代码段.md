---
title: 记Django开发中的一些常用代码段
copyright: true
permalink: 1
top: 0
date: 2018-01-26 18:01:13
tags:
- django
categories: 编程之道
password:
---
<blockquote class="blockquote-center">2018年的第一场雪，比2002年来得更晚一些</blockquote>
　　记得之前有分享过Django开发相关的系列文章（可在博客右上方自行搜索），内容包括模版、视图、路由等。那么本篇再补充一些Django开发过程中常用到的一些功能代码块，内容涉及前端、后端相关功能代码。这些代码块都是平常开发中常用的，因此在此做个备份，方便查询。
<!-- more -->

### 前端功能
搞安全的还需要会前端？当然啊，搞安全的也需要出产品，出产品了没前端不就显得很low吗？不过自己写前端太累了，因此还得用框架，这里推荐[Bootstrap](http://v3.bootcss.com/)。在尝试使用文章下方介绍的前端代码前，先在代码中添加上Bootstrap框架提供给的css、js连接。

#### 面板折叠
![](/upload_image/20180126/6.png)
![](/upload_image/20180126/1.png)
这个功能经常在侧边菜单栏中用到，面板折叠可有效的保持界面整洁。
```bash
<div class="panel panel-success">
<div class="panel-heading" data-toggle="collapse" data-parent="#accordion" href="#collapse">
  <h1 class="panel-title"><span class="glyphicon glyphicon-tag" aria-hidden="true"></span>Index</h1>
</div>
<div id="collapse" class="panel-collapse collapse out"> # out or in 控制折叠状态
  <div class="panel-body">
    <a href="">index1</a><br><br>
    <a href="">index2</a><br><br>
  </div>
</div>
</div>
```

#### 表格分页
![](/upload_image/20180126/7.png)
表格分页前端比较简单，想要实现真正的分页显示数据，需要结合后端代码，文章后面会介绍。
```bash
<!-- 分页 -->
<form action="{% url 'asset_list' %}" method="POST">
{% csrf_token %}
<ul class="pagination pagination">
    <li><a href="{% url 'asset_list' %}?page=0&search_key={{search_key}}">首页</a></li>
    <li><a href="{% url 'asset_list' %}?page={{pre_page}}&search_key={{search_key}}">上一页</a></li>
    {% for i in page_list %}
        <li><a href="{% url 'asset_list' %}?page={{ i }}&search_key={{search_key}}" class="active">{{ i }}</a></li>
    {% endfor %}
    <li><a href="{% url 'asset_list' %}?page={{ next_page }}&search_key={{search_key}}">下一页</a></li>
    <li><a href="{% url 'asset_list' %}?page={{ last_page }}&search_key={{search_key}}">尾页</a></li>
    &nbsp;
     <li>
        <input type="text" placeholder="输入页码" ng-model="gotoPage" class="" style="width: 80px" name="page">
        &nbsp;
        <input type="submit" class="btn btn-default" name="" value="跳转到" style="width:70px;height: 34px">
    </li>
 </ul>
</form>
```

#### 控制表格单元格内容自动换行
有些时候表格中单元格内容太长，会导致表格整体很不好看，因此对于内容会很长的表格列需要添加如下style
```bash
<td style="word-wrap:break-word;word-break:break-all;">test</td>
```

#### 弹出框（可编辑）
![](/upload_image/20180126/2.png)
有些时候需要修改一些表格数据，之前的做法是点击一个按钮，跳转到一个修改的页面，但这种做法不够优雅，因此可以选择点击按钮弹出一个可编辑的对话框。
```bash
<form action="/index/" method="POST">
<div class="modal fade" id="update" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
          &times;
        </button>
        <h4 class="modal-title" id="myModalLabel">
          提醒框
        </h4>
      </div>
      <div class="modal-body">
        <label>KEY</label>
        <input type="text" class="form-control" name="new_key" value="{{i.key_}}">
        <label>VALUES</label>
        <input type="text" class="form-control" name="new_value" value="{{i.value_}}">

      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">关闭
        </button>
        <button type="submit" name="update_id" value="{{i.id}}" class="btn btn-primary">
          确定修改
        </button>
      </div>
    </div>
  </div>
</div>
<input type="button" data-toggle="modal" data-target="#update" class="btn btn-info" value="修改">
</form>
```

#### 弹出提醒框（不可编辑）
![](/upload_image/20180126/3.png)
这个功能主要作用删除数据、修改数据时的提醒。
```bash
<form action="/index/" method="POST">
<div class="modal fade" id="del" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
<div class="modal-dialog">
<div class="modal-content">
  <div class="modal-header">
    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
      &times;
    </button>
    <h4 class="modal-title" id="myModalLabel">
      提醒框
    </h4>
  </div>
  <div class="modal-body">
    您确定要删除记录吗？
  </div>
  <div class="modal-footer">
    <button type="button" class="btn btn-default" data-dismiss="modal">关闭
    </button>
    <button type="submit" name="del_id" value="{{i.id}}" class="btn btn-primary">
      确定删除
    </button>
  </div>
</div>
</div>
</div>
<input type="button" data-toggle="modal" data-target="#del" class="btn btn-danger" value="删除">
</form>
```

#### 搜索框自动补全
![](/upload_image/20180126/4.png)
这个就厉害啦，当搜索一些资源的时候，如果能自动补全是不是会方便很多呢？
```bash
<label for="autocomplete">选择扫描插件（必选）</label><br>
<input  class="form-control" id="autocomplete" name="vul_name" placeholder="输入漏洞名称"><br><br>


<script type="text/javascript">
var tags = {{ plugin_list|safe }}; # 注plugin_list
$( "#autocomplete" ).autocomplete({
  source: tags
});
</script>
```

#### ajax请求
用ajax发送请求有好有坏，具体用法可参考：https://thief.one/2017/09/14/3/

#### 界面面板布局
![](/upload_image/20180126/5.png)
这个纯粹为了装逼。
```bash
<div class="container">
  <div class="row">
        ####### 面板 ##########
        <div class="col-md-3">
            <div class="list-group">
                <form class="list-group-item"> 
                    <a href="">test</a>
                </form>
            </div>
        </div>

       ####### 面板 ##########
        <div class="col-md-3">
            <div class="list-group">
                <form class="list-group-item"> 
                    <a href="">test2</a>
                </form>
            </div>
        </div>
  
  </div>
</div>

```

#### 表格单选框
表格显示数据是常见的功能，一般情况下需要多表格数据进行删改，因此批量选中就很重要。一般表格中的批量选择，可以使用单选框实现。
```bash
    <!-- 导入js -->
    <script src="https://cdn.bootcss.com/jquery/2.1.1/jquery.min.js"></script>
    <!-- 表格数据 -->
    <div id="list">
        <table class="table table-hover table-bordered table-striped">
            <thead>
                <tr>
                    <th><input type="checkbox" id="all" name="task_check_" value=""></th>
                    <th>ID</th>
                    <th>User</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <th><input type="checkbox" id="" name="task_check" value=""></th>
                    <td>01</td>
                    <td>nmask</td>
                    <td>
                        <a href="" class="link">修改</a>&nbsp;&nbsp;
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
    <!-- js -->
    <script>
    $(document).ready(function () {
        //全选或全不选
        $("#all").click(function () {
            if (this.checked) {
                $("#list :checkbox").prop("checked", true);
            } else {
                $("#list :checkbox").attr("checked", false);
            }
        });
        //设置全选复选框
        $("#list :checkbox").click(function () {
            allchk();
        });
        function selectAll(check){
            $(check).click(function(){
                if ($(check).is(':checked')) {
                    $(".list input").prop("checked",true);
                }else{
                    $(".list input").prop("checked",false);
                };
            });
            
        }
        //显示时执行一次
        selectAll();
    });
    </script>
```





### 后端功能
#### 表格分页
前面介绍了前端的分页，那么后端怎么写分页的功能呢？django框架有内置的分页模块Paginator，其他框架也有，比如flask等。
```bash
from django.core.paginator import Paginator

def page_fenye(objects,page,num=10):
    '''分页函数
    @num:每页显示多少条数据
    @page:当前页码
    @fenye_num:分页栏显示的数字数量

    return：
    @object_list:该页显示的数据对象
    @page_range:分页栏显示的数字范围
    @last_page:最后一页的数字
    '''
    fenye_num=6
    fenye_num_av=fenye_num/2

    try:
        page=int(page)
    except:
        page=1

    if page<1:
        page=1

    range_first_page=page-fenye_num_av
    range_last_page=page+fenye_num_av

    if range_first_page<0:
        range_first_page=0
        range_last_page=fenye_num

    p = Paginator(objects, num)

    page_range=list(p.page_range)[range_first_page:range_last_page]

    last_page=len(p.page_range)

    if page>last_page:
        page=1

    page1 = p.page(page)

    object_list=page1.object_list

    return object_list,page_range,last_page
```
但个人使用以后发现性能不好，因为每次请求页面需要先获取所有的数据，再通过此模块计算出此页面需要展示的数据，当所有的数据量比较大时，返回就比较慢了(也可能是我没用对这个模块)。因此，我自己写了一个分页的模块。
```bash
def fenye(all_num,page,num,page_list_num):
    '''分页计算
    @all_num:数据库记录总量
    @page:当前页码
    @num:每一页显示的记录条数
    @page_list_num:分页导航显示多少个数字，要为偶数
    @page_list_aver:page_list_num除以2

    return：
    @page:显示第几页
    @last_page:最后一页的数字
    @page_list:分页栏显示的数字范围
    '''

    page=int(page)
    
    if all_num!=0:
        last_page = all_num/num-1 if all_num%num == 0 else all_num/num #计算最后一页数字
    else:
        last_page=0

    page_list_aver=page_list_num/2
 
    page=last_page if page > last_page else page #判断请求的页数是否超过范围

    if page > page_list_aver:
        if last_page > page+page_list_aver:

            page_list=range(page - page_list_aver , page + page_list_aver)
        else:

            page_list=range(last_page - (page_list_num-1), last_page + 1)
    else:
        if last_page > page_list_num:

            page_list = range(page_list_num)
        else:

            page_list = range(last_page + 1)

    return page,last_page,page_list
```
这样不需要提前先查询出所有的数据存入内存，而只需要查询出总共存在多少条数据（注意，这里的查询语句由select `*` 改为select count(`*`)会快很多）。获取到分页函数返回的page后，可以结合sql语句中的limit功能，查询分页要展示的数据内容。
```bash
select * from test limit page*num,num # page为分页返回的显示页码，num是一页显示的数据数量
```
#### session做身份认证
这个功能就是用来验证用户身份的，可配合登录功能，写一个装饰器函数，检查全局是否存在session值。（session值是一个字典格式，在用户登录时生成）
```bash
def session_check(level=2,return_=False):
    '''session_check装饰器函数 针对函数
    @level：可以给用户区分权限
    @return_:检测到不存在session后跳转到不同的页面
    '''
    def dec(func):
        def warp(request,*args,**kwargs):
            if request.session.get('user_id',False) and int(request.session.get('level'))<=level:
                return func(request,*args,**kwargs)
            elif return_:
                return HttpResponse('<head><meta http-equiv="refresh" content="0.0001;url=/login/"></head>')
            else:
                return HttpResponse('<head><meta http-equiv="refresh" content="0.0001;url=/error/"></head>')
        return warp

    return dec
```
使用的话，直接在需要权限控制的函数上添加：
```bash
@session_check(return_=True)
def vul_index(request):
    ''' 漏洞扫描 '''
    pass
```


`暂时就想到了这些，先记这么多吧，等以后遇上了再补充一些，o了`




