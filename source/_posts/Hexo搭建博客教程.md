---
title: Hexo搭建博客教程
date: 2017-03-03 14:47:03
comments: true
tags: 
- hexo
- 博客搭建
categories: 技术研究
password:
copyright: true
top: 0
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
#### 在文章底部增加版权信息
在目录 next/layout/_macro/下添加 my-copyright.swig：
```bash
{% if page.copyright %}
<div class="my_post_copyright">
  <script src="//cdn.bootcss.com/clipboard.js/1.5.10/clipboard.min.js"></script>

  <!-- JS库 sweetalert 可修改路径 -->
  <script type="text/javascript" src="http://jslibs.wuxubj.cn/sweetalert_mini/jquery-1.7.1.min.js"></script>
  <script src="http://jslibs.wuxubj.cn/sweetalert_mini/sweetalert.min.js"></script>
  <link rel="stylesheet" type="text/css" href="http://jslibs.wuxubj.cn/sweetalert_mini/sweetalert.mini.css">
  <p><span>本文标题:</span><a href="{{ url_for(page.path) }}">{{ page.title }}</a></p>
  <p><span>文章作者:</span><a href="/" title="访问 {{ theme.author }} 的个人博客">{{ theme.author }}</a></p>
  <p><span>发布时间:</span>{{ page.date.format("YYYY年MM月DD日 - HH:MM") }}</p>
  <p><span>最后更新:</span>{{ page.updated.format("YYYY年MM月DD日 - HH:MM") }}</p>
  <p><span>原始链接:</span><a href="{{ url_for(page.path) }}" title="{{ page.title }}">{{ page.permalink }}</a>
    <span class="copy-path"  title="点击复制文章链接"><i class="fa fa-clipboard" data-clipboard-text="{{ page.permalink }}"  aria-label="复制成功！"></i></span>
  </p>
  <p><span>许可协议:</span><i class="fa fa-creative-commons"></i> <a rel="license" href="https://creativecommons.org/licenses/by-nc-nd/4.0/" target="_blank" title="Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)">署名-非商业性使用-禁止演绎 4.0 国际</a> 转载请保留原文链接及作者。</p>  
</div>
<script> 
    var clipboard = new Clipboard('.fa-clipboard');
    clipboard.on('success', $(function(){
      $(".fa-clipboard").click(function(){
        swal({   
          title: "",   
          text: '复制成功',   
          html: false,
          timer: 500,   
          showConfirmButton: false
        });
      });
    }));  
</script>
{% endif %}
```
在目录next/source/css/_common/components/post/下添加my-post-copyright.styl：
```bash
.my_post_copyright {
  width: 85%;
  max-width: 45em;
  margin: 2.8em auto 0;
  padding: 0.5em 1.0em;
  border: 1px solid #d3d3d3;
  font-size: 0.93rem;
  line-height: 1.6em;
  word-break: break-all;
  background: rgba(255,255,255,0.4);
}
.my_post_copyright p{margin:0;}
.my_post_copyright span {
  display: inline-block;
  width: 5.2em;
  color: #b5b5b5;
  font-weight: bold;
}
.my_post_copyright .raw {
  margin-left: 1em;
  width: 5em;
}
.my_post_copyright a {
  color: #808080;
  border-bottom:0;
}
.my_post_copyright a:hover {
  color: #a3d2a3;
  text-decoration: underline;
}
.my_post_copyright:hover .fa-clipboard {
  color: #000;
}
.my_post_copyright .post-url:hover {
  font-weight: normal;
}
.my_post_copyright .copy-path {
  margin-left: 1em;
  width: 1em;
  +mobile(){display:none;}
}
.my_post_copyright .copy-path:hover {
  color: #808080;
  cursor: pointer;
}
```
修改next/layout/_macro/post.swig，在代码
```bash
<div>
      {% if not is_index %}
        {% include 'wechat-subscriber.swig' %}
      {% endif %}
</div>
```
之前添加增加如下代码：
```bash
<div>
      {% if not is_index %}
        {% include 'my-copyright.swig' %}
      {% endif %}
</div>
```
修改next/source/css/_common/components/post/post.styl文件，在最后一行增加代码：
```bash
@import "my-post-copyright"
```
如果要在该博文下面增加版权信息的显示，需要在 Markdown 中增加copyright: true的设置，类似：
```bash
---
title: 
date: 
tags: 
categories: 
copyright: true
---
```
#### 自定义hexo new生成md文件的选项
在/scaffolds/post.md文件中添加：
```bash
---
title: {{ title }}
date: {{ date }}
tags:
categories: 
copyright: true
permalink: 01
top: 0
password:
---
```
#### 隐藏网页底部powered By Hexo / 强力驱动
打开themes/next/layout/_partials/footer.swig,使用”<!-- -->”隐藏之间的代码即可，或者直接删除。
```bash
<!--
<div class="powered-by">
  {{ __('footer.powered', '<a class="theme-link" rel="external nofollow" href="https://hexo.io">Hexo</a>') }}
</div>

<div class="theme-info">
  {{ __('footer.theme') }} -
  <a class="theme-link" rel="external nofollow" href="https://github.com/iissnan/hexo-theme-next">
    NexT.{{ theme.scheme }}
  </a>
</div>
-->
```
#### 文章加密访问
打开themes->next->layout->_partials->head.swig文件,在meta标签后面插入这样一段代码：
```bash
<script>
    (function(){
        if('{{ page.password }}'){
            if (prompt('请输入文章密码') !== '{{ page.password }}'){
                alert('密码错误！');
                history.back();
            }
        }
    })();
</script>
```
然后文章中添加：
```bash
password: nmask
```
如果password后面为空，则表示不用密码。

#### 博文置顶
修改 hero-generator-index 插件，把文件：node_modules/hexo-generator-index/lib/generator.js 内的代码替换为：
```bash
'use strict';
var pagination = require('hexo-pagination');
module.exports = function(locals){
  var config = this.config;
  var posts = locals.posts;
    posts.data = posts.data.sort(function(a, b) {
        if(a.top && b.top) { // 两篇文章top都有定义
            if(a.top == b.top) return b.date - a.date; // 若top值一样则按照文章日期降序排
            else return b.top - a.top; // 否则按照top值降序排
        }
        else if(a.top && !b.top) { // 以下是只有一篇文章top有定义，那么将有top的排在前面（这里用异或操作居然不行233）
            return -1;
        }
        else if(!a.top && b.top) {
            return 1;
        }
        else return b.date - a.date; // 都没定义按照文章日期降序排
    });
  var paginationDir = config.pagination_dir || 'page';
  return pagination('', posts, {
    perPage: config.index_generator.per_page,
    layout: ['index', 'archive'],
    format: paginationDir + '/%d/',
    data: {
      __index: true
    }
  });
};
```
在文章中添加 top 值，数值越大文章越靠前，如:
```bash
---
......
copyright: true
top: 100
---
```
默认不设置则为0，数值相同时按时间排序。
#### 添加顶部加载条
打开/themes/next/layout/_partials/head.swig文件，在maximum-scale=1"/>后添加如下代码:
```bash
<script src="//cdn.bootcss.com/pace/1.0.2/pace.min.js"></script>
<link href="//cdn.bootcss.com/pace/1.0.2/themes/pink/pace-theme-flash.css" rel="stylesheet">
```
但是，默认的是粉色的，要改变颜色可以在/themes/next/layout/_partials/head.swig文件中添加如下代码（接在刚才link的后面）
```bash
<style>
    .pace .pace-progress {
        background: #1E92FB; /*进度条颜色*/
        height: 3px;
    }
    .pace .pace-progress-inner {
         box-shadow: 0 0 10px #1E92FB, 0 0 5px     #1E92FB; /*阴影颜色*/
    }
    .pace .pace-activity {
        border-top-color: #1E92FB;    /*上边框颜色*/
        border-left-color: #1E92FB;    /*左边框颜色*/
    }
</style>
```
#### 添加热度
next主题集成leanCloud，打开/themes/next/layout/_macro/post.swig
在"leancloud-visitors-count"></span>标签后面添加<span>℃</span>。
然后打开，/themes/next/languages/zh-Hans.yml，将visitors内容改为*热度*即可。

#### 主页文章添加阴影效果
打开\themes\next\source\css\_custom\custom.styl,向里面加入：
```bash
// 主页文章添加阴影效果
 .post {
   margin-top: 60px;
   margin-bottom: 60px;
   padding: 25px;
   -webkit-box-shadow: 0 0 5px rgba(202, 203, 203, .5);
   -moz-box-shadow: 0 0 5px rgba(202, 203, 204, .5);
  }
```
#### 修改文章底部的那个带#号的标签
修改模板/themes/next/layout/_macro/post.swig，搜索 rel="tag">#，将 # 换成<i class="fa fa-tag"></i>

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
找到文件 themes\next\source\css\\_custom\custom.styl ，添加如下 css 样式：
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
#### 博文压缩
在站点的根目录下执行以下命令：
```bash
$ npm install gulp -g
$ npm install gulp-minify-css gulp-uglify gulp-htmlmin gulp-htmlclean gulp --save
```
在博客根目录下新建 gulpfile.js ，并填入以下内容：
```bash
var gulp = require('gulp');
var minifycss = require('gulp-minify-css');
var uglify = require('gulp-uglify');
var htmlmin = require('gulp-htmlmin');
var htmlclean = require('gulp-htmlclean');
// 压缩 public 目录 css
gulp.task('minify-css', function() {
    return gulp.src('./public/**/*.css')
        .pipe(minifycss())
        .pipe(gulp.dest('./public'));
});
// 压缩 public 目录 html
gulp.task('minify-html', function() {
  return gulp.src('./public/**/*.html')
    .pipe(htmlclean())
    .pipe(htmlmin({
         removeComments: true,
         minifyJS: true,
         minifyCSS: true,
         minifyURLs: true,
    }))
    .pipe(gulp.dest('./public'))
});
// 压缩 public/js 目录 js
gulp.task('minify-js', function() {
    return gulp.src('./public/**/*.js')
        .pipe(uglify())
        .pipe(gulp.dest('./public'));
});
// 执行 gulp 命令时执行的任务
gulp.task('default', [
    'minify-html','minify-css','minify-js'
]);
```
生成博文是执行 hexo g && gulp 就会根据 gulpfile.js 中的配置，对 public 目录中的静态资源文件进行压缩。

#### 搜索功能
安装 hexo-generator-searchdb，在站点的根目录下执行以下命令：
```bash
$ npm install hexo-generator-searchdb --save
```
编辑 站点配置文件，新增以下内容到任意位置：
```bash
search:
  path: search.xml
  field: post
  format: html
  limit: 10000
```
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

来必力评价
优点：界面美观
缺点：不支持数据导入，加载慢

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

#### 多说替换成网易云跟贴
最好的方法就是更新next主题，因为最新版本的主题已经支持这几种评论。
如果不想更新主题，则往下看：

网易云跟贴评价：
性能稳定，功能中规中矩，支持数据导入

首先在 _config.yml 文件中添加如下配置：
```bash
gentie_productKey: #your-gentie-product-key
```
其中 gentie_productKey 即注册网易云跟贴获取到的key。
在 layout/_scripts/third-party/comments/ 目录中添加 gentie.swig，文件内容如下：
```bash
{% if not (theme.duoshuo and theme.duoshuo.shortname) and not theme.duoshuo_shortname and not theme.disqus_shortname and not theme.hypercomments_id %}

  {% if theme.gentie_productKey %}
    {% set gentie_productKey = theme.gentie_productKey %}
    <script>
      var cloudTieConfig = {
        url: document.location.href, 
        sourceId: "",
        productKey: "{{gentie_productKey}}",
        target: "cloud-tie-wrapper"
      };
    </script>
    <script src="https://img1.ws.126.net/f2e/tie/yun/sdk/loader.js"></script>
  {% endif %}

{% endif %}
```
在layout/_scripts/third-party/comments.swig文件中追加：
```bash
{% include './comments/gentie.swig' %}
```
最后，在 layout/_partials/comments.swig 文件中条件最后追加网易云跟帖插件引用的判断逻辑：
```bash
{% elseif theme.gentie_productKey %}
      <div id="cloud-tie-wrapper" class="cloud-tie-wrapper">
      </div>
```
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
　　如果已经出现这个错误，则删除.deploy_git，重新hexo d。

#### （八）hexo s报错
在新版本的mac上，安装运行hexo会报此错误，但不影响使用。
```bash
{ Error: Cannot find module
```
解决方案：
```bash
npm install hexo --no-optional
```
### Local Search错误
　　最近发现Local Search搜索出来的连接有错误，到不是说连接不对，而是当我在/aaa/目录下搜索一个页面时，跳转到了/aaa/正确的连接/，这样明显是正确的，应该是跟目录+跳转的目录。
　　网上搜索了下，没有类似的案例，那么自己动手修改吧，打开node_modules/hexo-generator-searchdb/templates下的xml.ejs文件：
```bash
<url><%- ("../../../../../../../../"+post.path) %></url>
```
说明：将这个文件的两处url都改成这样就可以了。

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

### SEO优化
seo优化对于网站是否能被搜索引擎快速收录有很大帮助，因此适当做一些seo还是有必要的，以下内容参考：https://lancelot_lewis.coding.me/2016/08/16/blog/Hexo-NexT-SEO/
#### 添加sitemap文件
安装以下2个插件，然后重启hexo后，网站根目录（source）下会生成sitemap.xml与baidusitemap.xml文件，搜索引擎在爬取时会参照文件中的url去收录。
```bash
npm install hexo-generator-sitemap --save-dev
hexo d -g
npm install hexo-generator-baidu-sitemap --save-dev
hexo d -g
```
#### 添加robots.txt
新建robots.txt文件，添加以下文件内容，把robots.txt放在hexo站点的source文件下。
```bash
User-agent: * Allow: /
Allow: /archives/
Disallow: /vendors/
Disallow: /js/
Disallow: /css/
Disallow: /fonts/
Disallow: /vendors/
Disallow: /fancybox/

Sitemap: http://thief.one/sitemap.xml
Sitemap: http://thief.one/baidusitemap.xml
```
#### 首页title的优化
更改index.swig文件，文件路径是your-hexo-site\themes\next\layout，将下面代码
```bash
{% block title %}  {{ config.title }}  {% endblock %}
```
改成
```bash
{% block title %}  {{ config.title }} - {{ theme.description }}  {% endblock 
```
观察首页title就是标题+描述了。

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
详细Markdown语法请参考：[MakeDown语法](http://www.appinn.com/markdown/)

### 参考文章
http://www.jianshu.com/p/f054333ac9e6
https://neveryu.github.io/2016/09/30/hexo-next-two/

*提醒：在更新博客内容时，最好先在本地调试完毕后（hexo server），再推送到github上。*
