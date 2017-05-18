---
title: Hexo搭建博客教程
date: 2017-03-03 14:47:03
comments: true
tags: 
- hexo
- 博客搭建
categories: 技术研究
---
<blockquote class="blockquote-center">所谓博客，都是孤芳自赏
</blockquote>
现在越来越多的人喜欢利用Github搭建静态网站，原因不外乎简单省钱。本人也利用hexo+github搭建了本博客，用于分享一些心得。在此过程中，折腾博客的各种配置以及功能占具了我一部分时间，在此详细记录下我是如何利用hexo+github搭建静态博客以及一些配置相关问题，以免过后遗忘，且当备份之用。
<!-- more -->
### 准备工作

* 下载node.js并安装（官网下载安装），默认会安装npm。
* 下载安装git（官网下载安装）
* 下载安装hexo。方法：打开cmd 运行*npm install -g hexo*（要翻墙） 

### 本地搭建hexo静态博客

* 新建一个文件夹，如MyBlog
* 进入该文件夹内，右击运行git，输入：*hexo init*（生成hexo模板，可能要翻墙）
* 生成完模板，运行*npm install*（目前貌似不用运行这一步）
* 最后运行：*hexo server* （运行程序，访问本地localhost:4000可以看到博客已经搭建成功）

### 将博客与Github关联

* 在Github上创建名字为XXX.github.io的项目，XXX为自己的github用户名。

* 打开本地的MyBlog文件夹项目内的_config.yml配置文件，将其中的type设置为git

```bash
  deploy:
    type: git
    repository: https://github.com/tengzhangchao/tengzhangchao.github.io.git
    branch: master
```

* 运行：*npm install hexo-deployer-git --save*
* 运行：*hexo g*（本地生成静态文件）
* 运行：*hexo d*（将本地静态文件推送至Github）

此时，打开浏览器，访问*http://tengzhangchao.github.io*

### 绑定域名

　　博客已经搭建好，也能通过github的域名访问，但总归还是用自己的域名比较舒服。因为我们需要设置将自己的域名绑定到github这个博客项目上。

* 域名提供商设置

  添加2条A记录：

  @--->192.30.252.154

  @--->192.30.252.153

  添加一条CNAME记录：

  CNAME--->tengzhangchao.github.io

* 博客添加CNAME文件

  配置完域名解析后，进入博客目录，在source目录下新建CNAME文件，写入域名，如：thief.one

* 运行：*hexo g*
* 运行：*hexo d*


### 更新博客内容

　　至此博客已经搭建完毕，域名也已经正常解析，那么剩下的问题就是更新内容了。

#### 更新文章

* 在MyBlog目录下执行：*hexo new "我的第一篇文章"*，会在source->_posts文件夹内生成一个.md文件。
* 编辑该文件（遵循Markdown规则）
* 修改起始字段
  * title    文章的标题  
  * date    创建日期    （文件的创建日期 ）
  * updated    修改日期   （ 文件的修改日期）   
  * comments    是否开启评论    true  
  * tags    标签   
  * categories    分类   
  * permalink    url中的名字（文件名）
* 编写正文内容（MakeDown）
* hexo clean 删除本地静态文件（Public目录），可不执行。
* hexo g 生成本地静态文件（Public目录）
* hexo deploy 将本地静态文件推送至github（hexo d）

#### 添加菜单

进入theme目录，编辑_config_yml文件，找到menu:字段，在该字段下添加一个字段。

```bash
menu:
  home: /
  about: /about
  ......
```

然后找到lanhuages目录，编辑zh-Hans.yml文件：

```bash
menu:
  home: 首页
  about: 关于作者
  ......
```

更新页面显示的中文字符，最后进入theme目录下的Source目录，新增一个about目录，里面写一个index.html文件。


#### 文章内插入图片

在文章中写入:

```bash
![](/upload_image/1.jpg)
```

　　然后进入themes-主题名-source-upload_image目录下(自己创建)，将图片放到这个目录下，就可以了。

说明：当执行hexo g命令时，会自动把图片复制到 public文件的upload_image目录下。


### 个性化设置

#### 基本信息

　　在根目录下的_config.yml文件中，可以修改标题，作者等信息。打开编辑该文件，注意：每一个值的冒号后面都有一个半角空格！

* 未生效的写法：title:nMask的博客
* 能生效的写法：title:[空格]nMask的博客

#### 主题

访问[主题列表](http://www.zhihu.com/question/24422335)，获取主题代码。

进入themes目录，进入以下操作：

* 下载主题 (以next主题为例)
```bash
git clone https://github.com/iissnan/hexo-theme-next.git（主题的地址）
```
* 打开__config.yml文件，将themes修改为next（下载到的主题文件夹的名字）
* hexo g
* hexo d

关于hexo-next主题下的一些个性化配置，参考：[Next主题配置](http://theme-next.iissnan.com/)

### 主题美化

#### 文章中添加居中模块
文章Markdown中填写如下：
````bash
<blockquote class="blockquote-center">优秀的人，不是不合群，而是他们合群的人里面没有你</blockquote>
```
#### 鼠标点击小红心的设置
将 [love.js](https://github.com/Neveryu/Neveryu.github.io/blob/master/js/src/love.js) 文件添加到 \themes\next\source\js\src 文件目录下。
找到 \themes\next\layout\_layout.swing 文件， 在文件的后面，</body> 标签之前 添加以下代码：
```bash
<!-- 页面点击小红心 -->
<script type="text/javascript" src="/js/src/love.js"></script>
```
#### 背景的设置
将 [particle.js](https://github.com/Neveryu/Neveryu.github.io/blob/master/js/src/particle.js) 文件添加到 \themes\next\source\js\src 文件目录下。
找到 \themes\next\layout\_layout.swing 文件， 在文件的后面，</body>标签之前 添加以下代码：
```bash
<!-- 背景动画 -->
<script type="text/javascript" src="/js/src/particle.js"></script>
```
#### 修改文章内链接文本样式
将链接文本设置为蓝色，鼠标划过时文字颜色加深，并显示下划线。
找到文件 themes\next\source\css\_custom\custom.styl ，添加如下 css 样式：
```bash
.post-body p a {
  color: #0593d3;
  border-bottom: none;
  &:hover {
    color: #0477ab;
    text-decoration: underline;
  }
}
```
参考：https://neveryu.github.io/2016/09/30/hexo-next-two/

#### 增加阅读排行统计页面
首先我们可以使用leancloud来统计页面阅读数量，以及储存这些信息，然后通过leancloud提供的api编写js脚本来获取阅读数量信息，并展示在页面上。
首先新建一个page页面，hexo new page "",然后编辑此.md文件，写下：
```bash
<script src="https://cdn1.lncld.net/static/js/av-core-mini-0.6.1.js"></script>

<script>AV.initialize("", "");</script> //需要写上leancloud的key

<script type="text/javascript">
  var time=0
  var title=""
  var url=""
  var query = new AV.Query('Counter');//表名
  query.notEqualTo('id',0); //id不为0的结果
  query.descending('time'); //结果按阅读次数降序排序
  query.limit(20);  //最终只返回10条结果
  query.find().then(function (todo) {
    for (var i=0;i<10;i++){ 
      var result=todo[i].attributes;
      time=result.time;  //阅读次数
      title=result.title; //文章标题
      url=result.url;     //文章url
      var content="<p>"+"<font color='#0477ab'>"+"【阅读次数:"+time+"】"+"<a href='"+"http://thief.one"+url+"'>"+title+"</font>"+"</a>"+"</p>";
      // document.write("<a href='"+"http://thief.one/"+url+"'>"+title+"</a>"+"    Readtimes:"+time+"<br>");
      document.getElementById("heheda").innerHTML+=content
    }
  }, function (error) {
    console.log("error");
  });
</script>
```
最终的效果查看：http://thief.one/count

#### 多说替换成来必力评论
更新于@2017年5月18日
多说已经宣布下线了，因此我找了个来必力评论系统来替换，以下是替换的教程，教程内容来自：https://blog.smoker.cc/web/add-comments-livere-for-hexo-theme-next.html

首先在 _config.yml 文件中添加如下配置：
```bash
livere_uid: your uid
```
其中 livere_uid 即注册来必力获取到的 uid。
在 layout/_scripts/third-party/comments/ 目录中添加 livere.swig，文件内容如下：
```bash
{% if not (theme.duoshuo and theme.duoshuo.shortname) and not theme.duoshuo_shortname and not theme.disqus_shortname and not theme.hypercomments_id and not theme.gentie_productKey %}
  {% if theme.livere_uid %}
    <script type="text/javascript">
      (function(d, s) {
        var j, e = d.getElementsByTagName(s)[0];
        if (typeof LivereTower === 'function') { return; }
        j = d.createElement(s);
        j.src = 'https://cdn-city.livere.com/js/embed.dist.js';
        j.async = true;
        e.parentNode.insertBefore(j, e);
      })(document, 'script');
    </script>
  {% endif %}
{% endif %}
```
优先使用其他评论插件，如果其他评论插件没有开启，且LiveRe评论插件配置开启了，则使用LiveRe。其中脚本代码为上一步管理页面中获取到的。在layout/_scripts/third-party/comments.swig文件中追加：
```bash
{% include './comments/livere.swig' %}
```
引入 LiveRe 评论插件。
最后，在 layout/_partials/comments.swig 文件中条件最后追加LiveRe插件是否引用的判断逻辑：
```bash
{% elseif theme.livere_uid %}
      <div id="lv-container" data-id="city" data-uid="{{ theme.livere_uid }}"></div>
{% endif %}
```
最后打开博客瞧瞧吧！

### 报错解决
#### （一）Deployer not found: git
当编辑__config.yml文件，将type: git设置完成后，运行hexo g 报错：*git not found*
解决方案：可以在MyBlog目录下运行: *npm install hexo-deployer-git --save*。
#### （二）permission denied
当执行: hexo  deploy 报错时，把__config.yml中的github连接形式从ssh改成http。
#### （三）当在themes目录下载主题时，报错。
将该目录只读属性取消。
#### （四）genrnate 报错
检查_config.yml配置中，键值对冒号后面是否已经预留了一个半角空格。
#### （五）ERROR Plugin load failed: hexo-generator-feed
```bash
npm install hexo-generator-feed
npm install hexo-generator-feed --save
```
#### （六）fatal: The remote end hung up unexpectedly
```bash
$ git config https.postBuffer 524288000
$ git config http.postBuffer 524288000
$ git config ssh.postBuffer 524288000
```

#### （七）hero d推送的内容有问题
　　首先检查下.deploy_git文件夹下的.git文件是否存在，此.git文件指定了hexo d时推送public文件夹，而不是所有的内容。如果此.git文件不存在，则会出现推送内容错误。
　　用npm install hexo-deployer-git --save生成的.deploy_git不包含.git文件，因此正确的做法是.deploy_git文件夹也需要备份，然后再用npm install hexo-deployer-git --save更新一下其内容即可。


### 异地同步博客内容
　　现在电脑已经很普及了，因为一般来说我们都是公司一台电脑，家里一台电脑，那么如何将两台电脑上博客的内容同步内，即两台电脑上都可以编辑更新博客？
要解决这个问题，首先我们要清楚我们博客文件的组成：

* node_modules
* public
* scaffolds
* source
* themes
* _config_yml
* db.json
* package.json
* .deploy_git

　　以上为利用hexo生成的博客全部内容，那么当我们执行hexo d时，正真被推送到github上的又有哪些内容呢？
　　我们可以看下github上的tengzhangchao.github.io项目，发现里面只有Public目录下的内容。也就是说，我们博客上呈现的内容，其实就是public下的文件内容。那么这个Pulic目录是怎么生成的呢？
　　一开始hexo init的时候是没有public目录的，而当我们运行hexo g命令时，public目录被生成了，换句话说hexo g命令就是用来生成博客文件的（会根据_config.yml，source目录文件以及themes目录下文件生成）。同样当我们运行hexo clean命令时，public目录被删除了。
　　好了，既然我们知道了决定博客显示内容的只有一个Public目录，而public目录又是可以动态生成的，那么其实我们只要在不同电脑上同步可以生成Public目录的文件即可。

以下文件以及目录是必须要同步的：

* source
* themes
* _config.yml
* db.json
* package.json
* .deploy_git

　　同步的方式有很多种，可以每次更新后都备份到一个地址。我采用github去备份，也就是新建一个项目用来存放以上文件，每次更新后推送到github上，用作备份同步。
　　同步完必须的文件后，怎么再其他电脑上也可以更新博客呢？
　　前提假设我们现在配置了一台新电脑，里面没有安装任何有关博客的东西，那么我们开始吧：

* 下载node.js并安装（官网下载安装），默认会安装npm。
* 下载安装git（官网下载安装）
* 下载安装hexo。方法：打开cmd 运行*npm install -g hexo*（要翻墙） 
* 新建一个文件夹，如MyBlog
* 进入该文件夹内，右击运行git，输入：*hexo init*（生成hexo模板，可能要翻墙)

　　我们重复了一开始搭建博客的步骤，重新生成了一个新的模板，这个模板中包含了hexo生成的一些文件。

* git clone 我们备份的项目，生成一个文件夹，如：MyBlogData
* 将MyBlog里面的node_modules、scaffolds文件夹复制到MyBlogData里面。

　　做完这些，从表面上看，两台电脑上MyBlogData目录下的文件应该都是一样的了。那么我们运行hexo g
hexo d试试，如果会报错，则往下看。

* 这是因为.deploy_git没有同步，在MyBlogData目录内运行:*npm install hexo-deployer-git --save*后再次推送即可

　　总结流程：当我们每次更新MyBlog内容后，先利用hexo将public推送到github，然后再将其余必须同步的文件利用git推送到github。

### MakeDown语法
```bash
[hexo](http://www.baidu.com)  表示超链接
##大标题
###小标题
<!-- more -->
<!-- 标签别名 -->
{% cq %}blah blah blah{% endcq %}
空格  中文全角空格表示
---
文章标题
---
>内容     区块引用
*1
*2
*3
列表
*内容*     表示强调内容
![Alt text](/path/to/img.jpg)  图片
![](/upload_image/20161012/1.png)
```

详细参考：[MakeDown语法](http://www.appinn.com/markdown/)



*提醒：在更新博客内容时，最好先在本地调试完毕后（hexo server），再推送到github上。*