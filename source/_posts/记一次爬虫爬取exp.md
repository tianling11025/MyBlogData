---
title: 记一次爬虫批量爬取exp
copyright: true
permalink: 1
top: 0
date: 2018-03-27 10:15:36
tags:
- exp
- phantomjs爬虫
categories: 爬虫技术
password:
---
<blockquote class="blockquote-center">磨刀不误砍柴工</blockquote>

　　最近需要收集一些exp，因此逛了逛[exploit-db](https://www.exploit-db.com/)、[国内exp搜索大全](http://expku.com/)、[seebug](https://www.seebug.org/)等几个exp收集的网站。由于需要批量获取漏洞信息以及对应的exp内容，因此心想有必要写一款爬虫去自动化收集漏洞exp。
<!-- more -->
### 选个target
　　前面三个网站都有丰富的exp资源，但是我并不打算从它们身上去爬取，这里介绍另外一个更牛逼的网站：[0day.today](https://cn.0day.today/)（需要翻墙）。选取它的原因是exp更新的更快更丰富，且反爬虫策略做的比较一般。

### 分析URL结构
选好目标后，先尝试分析下网页结构，比如需要判断是动态还是静态页面等特征。此网站算是动态的，其漏洞列表URL结构如下：
* cn.0day.today/webapps/1（web漏洞列表第一页）
* cn.0day.today/webapps/2（web漏洞列表第二页）
* cn.0day.today/remote/1（远程利用漏洞列表第一页）
* cn.0day.today/local/1（本地利用漏洞列表第一页）
* ......

每个漏洞列表页面内有30个漏洞列表，每个漏洞列表对应一个漏洞URL，结构如下：
* cn.0day.today/exploit/30029
* cn.0day.today/exploit/30030

说明：此URL内容便是某个漏洞的exp，粗略算一下，web漏洞有600页，每页30个，总数是18000个漏洞exp。

### 分析网页内容
　　分析完URL结构，大致可以得出爬虫思路：遍历漏洞列表页数获取全部漏洞URL-->爬取漏洞URL获取漏洞exp。
　　那么如何通过爬取漏洞列表页面获取漏洞对应的URL，以及如何爬取漏洞信息页面获取exp？，这里需要分析一下页面结构，可以尝试写正则或者摘取网页元素内容的方式获取目标内容。

#### 获取漏洞URL
页面结构：
![](/upload_image/20180327/3.png)
对于此页面我没有使用正则，而是使用了BeautifulSoup模块来获取网页元素内容，代码如下：
```bash
soup=BeautifulSoup(content,"html.parser")
n=soup.find_all("div",{"class":"ExploitTableContent"})
if n:
    for i in n:
        m=i.find_all("div",{"class":"td allow_tip "})
        for j in m:
            y=j.find_all("a")
            for x in y:
                vul_name=x.text # 漏洞名称
                vul_url=x.attrs.get("href") # 漏洞url
```
#### 获取漏洞EXP
页面结构：
![](/upload_image/20180327/4.png)
对于此页面我也没有使用正则，而是使用了BeautifulSoup模块来获取网页元素内容，代码如下：
```bash
soup=BeautifulSoup(content,"html.parser")
m=soup.find_all("div",{"class":"container"})
n=m[0].find_all("div")
exp_info=""
for i in n:
    exp_info+=i.text+"\n"
```

### 反爬虫策略
我在连续访问n次网站后，发现此站有一些反爬虫的策略。而我必须研究解决它，才能进一步获取exp内容。
#### cdn防ddos策略
　　首先我发现此网站用了cloudflare加速器，且在用户持续访问一段时间后（应该是基于ip+headers认证），会出现防ddos页面。如果此时用普通的爬虫去访问，获取到的页面源码是防ddos的源码，即：
![](/upload_image/20180327/1.png)

#### 解决方案
　　当我们打开浏览器访问漏洞页面时，会在防ddos页面上等待几秒后，自动跳转到目标漏洞页面。基于这一特性，我决定使用无头浏览器去访问，设置等待时间即可。这里我选用phantomjs做此试验，其他headless同理。
```bash
d=webdriver.PhantomJS()
d.get(vul_api)
time.sleep(5) # 等待5s
print d.page_source # 输出源码
```
在访问网页5s后，输出的网页源码，便是目标漏洞exp页面的源码。

#### 用户点击确认
　　在绕过了防ddos策略后，发现网站自身也有一个反爬虫的策略，即需要用户点击确认按钮后，才能继续访问原目标。如果此时用普通的爬虫去访问，获取到的页面源码是用户确认网页的源码，即：
![](/upload_image/20180327/2.png)

#### 解决方案
　　此网页需要用户点击“确定”按钮后，会跳转到目标页面，因此可以使用无头浏览器访问，操作页面元素，即模拟点击确定按钮。
```bash
d=webdriver.PhantomJS()
d.get(vul_api)
time.sleep(5) # 等待5s（绕过防ddos策略）

d.find_element_by_name("agree").click() # 点击确定按钮（绕过用户点击确认策略）
time.sleep(5) # 等待5s
content=d.page_source # 输出网页源码
d.quit()
```

### 总结
　　想要爬取一个网站的内容，必须要分析此网站的URL结构、网页内容、反爬虫策略等。针对此网站而言，复杂点在于如何绕过反爬虫策略，这里用到了无头浏览器去模拟人访问。总之编写爬虫是需要耐心跟细心的，如何一步步去分析整个访问流程，有时候比如何去编程更重要。也许，这就是所谓的：“磨刀不误砍柴工”吧！




