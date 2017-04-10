---
title: Xss平台搭建小记
date: 2017-03-15 14:18:06
comments: true
tags: 
- xss
- xss平台
categories: web安全
---
<blockquote class="blockquote-center">每天把牢骚拿出来晒晒太阳，心情就不会缺钙</blockquote>

　　之前搭建过很多次xss平台，也用过几套源代码，然而对比之下，还是觉得wuyun的xss.me源码比较好用，即使比较古老了。最近因为工作需要，又准备重新搭建一套xss平台，源码果断选择了xss.me（当然是经过修改之后的），我的源码来之博客:[http://www.bodkin.ren/?p=133](http://www.bodkin.ren/?p=133)，感谢其分享。
<!--more -->
　　Xss平台的搭建过程并不复杂，虽然期间遇到了一些小问题，但也很快解决了，在此记录分享。

### xss源码下载
　　[修改版](https://git.oschina.net/nMask/Resource/raw/master/xss.me.new.zip)
　　[原版](https://git.oschina.net/nMask/Resource/raw/master/xss.me.old.zip)

### Install

　　首先下载xssplatform源码，然后选择一台服务器安装wamp，这里之所以选择wamp来搭建环境，主要是想免去配置apache、mysql的麻烦，因为本文重点还是在于搭建xss平台的过程。（大神可以选择在linux上单独安装配置apache）

　　服务器环境配置好以后，将xss源码放在wamp的www目录下，启动wamp，此时如果wamp运行正常，我们打开localhost/xss/应该可以看到登陆界面了，但此时还不能进行登陆或者注册，还需要进行多项配置。

### apache配置

　　打开wamp\bin\apache\apache2.4.9\conf\httpd.conf，为了后面搭建xss平台不出现错误，我们先将网站目录设置一下：
```bash
将其中的c:/wamp/www/ 改为c:/wamp/www/xss/，重启apache。
```
　　这时打开localhost就可以看到登陆页面了，而不需要访问localhost/xss/路径。当然如果有特殊需要，必须设置二级目录的，那之后的一些路径配置，请都设置成二级目录，即在原来的路径前面加上目录名称，如/xss/index.php等。

### 数据库配置
　　打开localhost/phpmyadmin进入phpmyadmin管理界面，添加一个用户root,123456,为了安全起见，删除其他用户。然后添加一个数据库，名为poppy（具体数据库名称可查看xss.sql文件，里面有写），然后导入xss.sql文件即可。
　　更改oc_module模块域名，进入oc_module表，执行sql语句，改为自己的域名。（影响生成的xss poc）
```bahs
UPDATE oc_module SET code=REPLACE(code,"http://xsser.me","http://xxx.com");
```
### Xss源码配置

apache与数据库配置完以后，还需要配置xss源码。

#### config.php

打开根目录下的config.php文件，主要看以下这些配置。
```bash
/* 数据库连接 */
$config['dbHost']        ='localhost';            //数据库地址
$config['dbUser']        ='root';                //用户
$config['dbPwd']        ='123456';                //密码
$config['database']        ='poppy';            //数据库名
$config['charset']        ='utf8';                //数据库字符集
$config['tbPrefix']        ='oc_';                    //表名前缀
$config['dbType']        ='mysql';                //数据库类型(目前只支持mysql)

/* 注册配置 */
$config['register']        ='invite';                //normal,正常;invite,只允许邀请注册;close,关闭注册功能
$config['mailauth']        =false;                    //注册时是否邮箱验证

/* url配置 */
$config['urlroot']        ='http://localhost';//访问的url起始
```
修改配置如下：

* $config['database']        ='poppy';  #更改，保持跟数据名一致（数据库名字查看.sql文件）
* 数据库账号密码可以选择更改，也可以保持不变。
* $config['register']          ='normal';             # 改为不需要邀请码。
* $config['urlroot']        ='http://localhost'; #改为本地

#### 修改authtest.php

修改根目录下authtest.php文件，改成自己的域名或者ip。
```bash
 else if ((isset($_SERVER['PHP_AUTH_USER'])) && (isset($_SERVER['PHP_AUTH_PW']))){

    /* 变量值存在，检查其是否正确 */

    header("Location: http://xxx.com/index.php?do=api&id={$_GET[id]}&username={$_SERVER[PHP_AUTH_USER]}&password={$_SERVER[PHP_AUTH_PW]}"); 
}
```
　　修改完配置以后，打开localhost，注册一个账号。注册完成后oc_user表中会新增一个记录，手动将adminlevel改为1（即管理员权限，可以有权限下放邀请码）。

完成以上步骤，平台差不多就可以用了，但如果遇到了一些其他问题，请继续往下看。

### Xss_Url 404问题

出现的问题：当访问
```bash
http://xxx.com/y42f59?1489555427
```
等自动生成的xss_poc时，会出现404错误，这是由于url重写没有生效的缘故，主要是因为中间件配置问题。以下就apache与iis中间件，给出解决方案。
#### apache解决方案

首先在网站根目录添加.htaccess文件，文件内容如下：
```bash
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteBase /
RewriteRule ^([0-9a-zA-Z]{6})$ /index.php?do=code&urlKey=$1 [L]
RewriteRule ^do/auth/(\w+?)(/domain/([\w\.]+?))?$  /index.php?do=do&auth=$1&domain=$3 [L]
RewriteRule ^register/(.*?)$ /index.php?do=register&key=$1 [L]
RewriteRule ^register-validate/(.*?)$ /index.php?do=register&act=validate&key=$1 [L]
</IfModule>
```
注意：如果网站需要域名+目录去访问的，如：www.xxx.com/xss/，则在以下代码/index.php前添加/xss/index.php。

然后修改apache配置文件，允许url重写。
```bash
AllowOverride None
```
全部改为
```bash
AllowOverride All
```
这样，apache会根据根目录下的.htaccess文件去匹配url重写规则。

做完以上2条配置后访问类似于此地址，就会显示xss_poc（js）内容了。
```bash
http://xxx.com/y42f59?1489555427
```
写文本时，我是在windows下做的测试，linux下配置方法应当一致。

#### iis解决方案

参考：[http://www.bodkin.ren/?p=133](http://www.bodkin.ren/?p=133)

### 邮件短信设置

* 修改文件\source\function.php 257行,把里面的邮箱账号密码换一下，host改为smtp.xx.com，如：smtp.qq.com
* 飞信短信提醒功能，修改\source\api.php 72行手机号，可能只支持移动手机号。

### 老版本其他问题

*新的源码不需要修改以下参数，老版本可能需要修改*

#### 修改注册页面提交按钮

修改themes\default\templates\register.html内容：
```bash
<input id="btnRegister" type="button" onclick="Register()" value="提交注册" />
```
修改为
```bash
<input id="btnRegister" type="submit" value="提交注册" />
```

#### 邀请码生成

（1）将文件source\user.php第10行和50行的权限控制注释掉
```bash
//if($user->userId<=0) ShowError('未登录或已超时',$url['login'],'重新登录');
//if($user->adminLevel<=0) ShowError('没有操作权限',URL_ROOT.'/index.php?do=user&act=invite');
```
然后访问/index.php?do=user&act=invite即可生成验证码
（2）注册一个用户test，进入数据库，将该用户的adminLevel修改为1，然后去掉（1）中添加到注释；并在第15行case 'invite':处添加权限控制：
```bash
if($user->adminLevel<=0) ShowError('没有操作权限',URL_ROOT.'/index.php');
```
（3）或者开放普通注册权限，修改文件/config.php的第18行
```bash
$config['register']='invite';   //normal,正常;invite,只允许邀请注册;close,关闭注册功能
 ```
#### 删除cookie

　　修改文件themes\default\templates\project_view.html中的Delete()和MultiDelete()函数，将其中post的URL修改为
```bash
'/xss/index.php?do=project&act=delcontent&r='
```
即根据实际的服务器路径，在前面添加'/xss'。
 
#### source\class\user.class.php
```bash
$this->db->Execute("UPDATE ".$this->tbUser." SET loginTime='".time()."'");
修改为
$this->db->Execute("UPDATE ".$this->tbUser." SET loginTime='".time()."' where id={$row['id']}");
```
#### 修改跳转提示时间
文件themes/default/templates/notice.html：
```bash
setTimeout("location.href='{$notice.turnto}'",3000);
修改为
setTimeout("location.href='{$notice.turnto}'",500);
```


本文地址：[http://thief.one/2017/03/15/Xss平台搭建小记/](http://thief.one/2017/03/15/Xss平台搭建小记/)
转载请说明来自：[nMask'Blog](http://thief.one)