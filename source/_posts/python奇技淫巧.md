---
title: python奇技淫巧
date: 2017-04-19 10:41:52
comments: true
top: 0
tags:
- python
- python奇技淫巧
categories: 编程之道
permalink: 01
password:
copyright: true
---
<blockquote class="blockquote-center">叶落下了思念，风摇曳那些岁岁年年</blockquote>
　　本文用作记录，在使用python过程中遇到的一些奇技淫巧，有些代码是本人所写，有些则是python内置函数，有些则取之互联网。在此记录，只为备份以及遗忘时方便查找。
　　本文将会持续更新，内容仅限记录一些常用好用却又永远记不住的代码或者模块。
<!--more -->

### 控制台操作
控制台不闪退
```bash
os.system('pause') 
```
获取控制台大小
```bash
rows, columns = os.popen('stty size', 'r').read().split()
```
#### 输入输出控制
解决输入提示中文乱码问题
```bash
raw_input(unicode('请输入文字','utf-8').encode('gbk'))
```
格式化输出
```bash
print a.prettify()
```
接受多行输入
```bash
text=""
while 1:
    data=raw_input(">>")
    if data.strip()=="stop":
        break
    text+="%s\n" % data
print text
---------------------------
>>1
>>2
>>3
>>stop
1
2
3
```
同行输出
```bash
Print '%s' % a,
Print '%s \r' % a
```
标准输入输出
```bash
sys.stdout.write("input") 标准输入
sys.stdout.flush() 刷新缓冲区
```
print的功能与sys.stdout.write类似，因为2.x中print默认就是将输出指定到标准输出中（sys.stdout)。
#### 颜色控制
控制台颜色控制(适用于windows)
```bash
WConio.textcolor(WConio.YELLOW)
print "yellow"
WConio.textcolor(WConio.BLUE)
print "blue"
```
输出颜色控制(全平台)
```bash
red = '\033[1;31m'
green = '\033[1;32m'
yellow = '\033[1;33m'
white = '\033[1;37m'
reset = '\033[0m’

print red+"color is red"+reset
print green+"color is green"+reset
```
#### 进度条控制
方案一
```bash
from __future__ import division
import sys,time
j = '#'
for i in range(1,61):
    j += '#'
    sys.stdout.write(str(int((i/60)*100))+'%  ||'+j+'->'+"\r")
    sys.stdout.flush()
    time.sleep(0.1)
```
方案二
```bash
import sys
import time
for i in range(1,61):
    sys.stdout.write('#'+'->'+"\b\b")
    sys.stdout.flush()
    time.sleep(0.5)
```
方案三
```bash
from progressbar import *
import time
import os
rows, columns = os.popen('stty size', 'r').read().split() #获取控制台size    
console_width=int(columns)
total = 10
progress = ProgressBar()

def test():
    '''
    进度条函数，记录进度
    '''
    for i in progress(range(total)):
        test2()

def test2():
    '''
    执行函数，输出结果
    '''
    content="nMask'Blog is http://thief.one"
    sys.stdout.write("\r"+content+" "*(console_width-len(content)))
    time.sleep(1)
    sys.stdout.flush()

test()

```
更多高级用法可以使用progressbar模块。
### 系统操作
#### 系统信息
获取python安装路径
```bash
from distutils.sysconfig import get_python_lib
print get_python_lib
```
获取当前python版本
```bash
sys.version_info
sys.version
```
获取当前时间
```bash
c=time.ctime()
#自定义格式输出
ISOTIMEFORMAT=’%Y-%m-%d %X’
time.strftime( ISOTIMEFORMAT, time.localtime() )
```
查看系统环境变量
```bash
os.environ["PATH"] 
```
获取系统磁盘
```bash
os.popen("wmic VOLUME GET Name")
```
获取当前路径(包括当前py文件名)
```bash
os.path.realpath(__file__)
```
当前平台使用的行终止符
```bash
os.linesep
```
获取终端大小
```bash
rows, columns = os.popen('stty size', 'r').read().split()
#python3以后存在可以使用os
os.get_termial_size()
```
#### 退出程序

* return：返回函数的值，并退出函数。
* exit()：直接退出。
* sys.exit(): 引发一个SystemExit异常，若没有捕获错误，则python程序直接退出；捕获异常后，可以做一些额外的清理工作。
* sys.exit(0):为正常退出，其他（1-127）为不正常，可抛异常事情供捕获。（一般用于主线程中退出程序）
* os._exit(0): 直接退出python程序，其后的代码也不会执行。（一般用于线程中退出程序）

### 网络操作
域名解析为ip
```bash
ip= socket.getaddrinfo(domain,'http')[0][4][0]
```
获取服务器版本信息
```bash
sUrl = 'http://www.163.com'
sock = urllib2.urlopen(sUrl)
sock.headers.values()
```
### 文件操作
open函数,使用wb、rb代替w、r
```bash
with open("test.txt","wr") as w:
    w.write("test")
```
这种写法可以兼容python2/3。
输出一个目录下所有文件名称
```bash
def search(paths):
    if os.path.isdir(paths):  #如果是目录
          files=os.listdir(paths)  #列出目录中所有的文件
          for i in files:
               i=os.path.join(paths,i)  #构造文件路径
               search(i)           #递归
          elif os.path.isfile(paths): #如果是文件
               print paths   #输出文件名
```
文件查找
```bash
import glob
print glob.glob(r"E:/*.txt")     #返回的是一个列表
查找文件只用到三个匹配符：”*”, “?”, “[]“
”*”匹配0个或多个字符；
”?”匹配单个字符；
”[]“匹配指定范围内的字符，如：[0-9]匹配数字。
```
查找指定名称的文件夹的路径
```bash
def search(paths,file_name,tag,lists):
    if os.path.isdir(paths):  #如果是目录
        if file_name==tag:    #如果目录名称为tag
            lists.append(paths) #将该路径添加到列表中
        else:                 #如果目录名称不为tag
            try:
                files_list=os.listdir(paths)  #列出目录中所有的文件
                for file_name in files_list:
                    path_new=os.path.join(paths,file_name)  #构造文件路径
                    search(path_new,file_name,tag,lists)    #递归
            except: #遇到特殊目录名时会报错
                pass

    elif os.path.isfile(paths): #如果是文件
        pass

    return lists
```
### 数据操作
判断数据类型
```bash
isinstance("123",(int,long,float,complex)
```
#### 字符串(string)
字符串推导
```bash
a="True"
b=a if a=="True" else "False"
>>>print b
True
```
format方法拼接字符串与变量
```bash
a="{test} abc {test2}".format(test="123",test2="456")
>>>>print a 
123 abc 456
或者：
a="{},{}".format(1,2)
>>>>>print a
1,2
```
去掉小数点后面的数字
```bash
a=1.21311
b=Int(math.floor(a))
```
字符串倒置
```bash
>>> a =  "codementor"
>>> a[::-1]
```
字符串首字母变大写
```bash
info = 'ssfef'
print info.capitalize()
print info.title()
```
返回一个字符串居中，并使用空格填充至长度width的新字符串。
```bash
"center string".center(width) #width设置为控制台宽度，可控制输出的字符串居中。
```
列举所有字母
```bash
print string.ascii_uppercase 所有大写字母
print string. ascii_lowercase 所有小写字母
print string.ascii_letters 所有字母（包括大小写）
```
#### 列表(list)
列表去重
```bash
ids = [1,4,3,3,4,2,3,4,5,6,1]
ids = list(set(ids))
```
判断列表为空
```bash
a=[]
if not a:
```
列表运算
```bash
a=[1,2,3]
b=[3,4,5]
set(a)&set(b) 与
set(a)|set(b) 或
set(a)-set(b) 非
```
单列表元素相加
```bash
a = ["Code", "mentor", "Python", "Developer"]
>>> print " ".join(a)
Code mentor Python Developer
```
多列表元素分别相加
```bash
list1 = ['a', 'b', 'c', 'd']
list2 = ['p', 'q', 'r', 's']
>>> for x, y in zip(list1,list2):  
        print x, y
ap
bq
cr
ds
```
将嵌套列表转换成单一列表
```bash
a = [[1, 2], [3, 4], [5, 6]]
>>> import itertools
>>> list(itertools.chain.from_iterable(a))
[1, 2, 3, 4, 5, 6]
```
列表内元素相加
```bash
a=[1,2,3]（数字）
sum(a)
```
产生a-z的字符串列表
```bash
map(chr,range(97,123))
```
列表复制
```bash
a=[1,2,3]
b=a
当对b进行操作时，会影响a的内容，因为共用一个内存指针，b=a[:] 这样就是单独复制一份了。
```
#### 列表推导
if+else配合列表解析
```bash
[i if i >5 else -i for i in range(10)]
```
多层嵌套列表
```bash
a=[[1,2],[3,4]]
b=[for j in i for i in a]
print b
[1,2,3,4]
```
生成一个生成器，调用next方法，可以减少内存开支。
```bash
a=(i else i+1 for i in b if i==1)
```
#### 字典推导
更换key与value位置
```bash
dict={"a":1,"b":2}
b={value:key for key value in dict.items()}
```
#### 字典操作(dict)
筛选出值重复的key
```bash
list1=self.dict_ip.items()             
        ddict=defaultdict(list)
        for k,v in list1:
            ddict[v].append(k)
        list2=[(i,ddict[i]) for i in ddict if len(ddict[i])>1]
        dict_ns=dict(list2)
```
字典排序（py2）
```bash
file_dict={"a":1,"b":2,"c":3}
file_dict_new=sorted(file_dict.iteritems(), key=operator.itemgetter(1),reverse=True) ##字典排序,reverse=True由高到低，itemgetter(1)表示按值排序，为0表示按key排序。
```
字典值判断
```bash
b={"a":1}
a=b.get("a","")  #如果不存在a，则返回””
c=a if a else 0  #如果存在a，则返回a，不然返回0
```
### 模块操作
导入模块时，设置只允许导入的属性或者方法。
```bash
fb.py:
-----------------------
__all__=["a","b"]
a="123"
c="2345"
def b():
    print “123”
-----------------------
from fb import *
可以导入__all__内定义的变量，a跟b()可以导入，c不行。如果不定义__all__则所有的都可以导入。
```
导入上级目录下的包
```bash
sys.path.append("..")
from spider.spider_ import spider_
```
导入外部目录下的模块
```bash
需要在目标目录下创建__init__.py文件，内容随便。
```
增加模块属性
```bash
有时候源代码中，我们需要写上自己的名字以及版本介绍信息，可以用__name__的方式定义。
a.py:
#! -*- coding:utf-8 -*-
__author__="nMask"
```
然后当我们导入a这个模块的时候，可以输出dir(a)看看
```bash
>>> import p
>>> print dir(p)
['__author__', '__builtins__', '__doc__', '__file__', '__name__', '__package__']
>>> print p.__author__
nmask
```
动态加载一个目录下的所有模块
```bash
目录：
---test
   ----a.py
   ----b.py
---c.py
c.py导入test下面的所有模块：
for path in ["test"]:
    for i in list(set([os.path.splitext(i)[0] for i in os.listdir("./"+path)])):
        if i!="__init__" and i!=".DS_Store": ##排除不必要的文件
            import_string = "import path+"."+i+"
            exec import_string #执行字符串中的内容
```
### 函数操作
#### eval/exec
```bash
def test(content):
    print content

exec(“test(‘abc')”)
```
输出：abc
说明：exec函数没有返回值
```bash
def test(content):
    return content

print eval(“test(‘abc')”)
```
输出：abc
说明：eval函数有返回值
#### 装饰器函数
输出当前时间装饰器
```bash
def current_time(aclass):
    def wrapper():
        print "[Info]NowTimeis:",time.ctime()
        return aclass()
    return wrapper
```
#### itertools迭代器
```bash
p=product(["a","b","c","d"],repeat=2)
----
[("a","a"),("b","b")......]
```
#### reduce函数
函数本次执行的结果传递给下一次。
```bash
def test(a,b):
    return a+b
reduce(test,range(10))
结果：从0+1+2......+9
```
#### enumerate函数
输入列表元素以及序列号
```bash
n=["a","b","c"]
for i,m in enumerate(n):
    print(i,m)
```
#### 函数超时时间设置
@于2017.05.27更新
利用signal设置某个函数执行的超时时间
```bash
import time
import signal
 
def test(i):
    time.sleep(0.999)#模拟超时的情况
    print "%d within time"%(i)
    return i
 
def fuc_time(time_out):
    # 此为函数超时控制，替换下面的test函数为可能出现未知错误死锁的函数
    def handler(signum, frame):
        raise AssertionError
    try:
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(time_out)#time_out为超时时间
        temp = test(1) #函数设置部分，如果未超时则正常返回数据，
        return temp
    except AssertionError:
        print "%d timeout"%(i)# 超时则报错
 
if __name__ == '__main__':
    for i in range(1,10):
        fuc_time(1)
```
#### 函数出错重试
利用retrying模块实现函数报错重试功能
```bash
import random
from retrying import retry

@retry
def have_a_try():
    if random.randint(0, 10) != 5:
        raise Exception('It's not 5!')
    print 'It's 5!'
```
如果我们运行have_a_try函数，那么直到random.randint返回5，它才会执行结束，否则会一直重新执行，关于该模块更多的用法请自行搜索。

### 程序操作
@于2017.05.27更新
#### Ctrl+C退出程序
利用signal实现ctrl+c退出程序。
```bash
import signal
import sys
import time

def handler(signal_num,frame):
    print "\nYou Pressed Ctrl-C."
    sys.exit(signal_num)
signal.signal(signal.SIGINT, handler)

# 正常情况可以开始你自己的程序了。
# 这里为了演示，我们做一个不会卡死机器的循环。
while 1:
    time.sleep(10)
# 当你按下Ctrl-C的时候，应该会输出一段话，并退出.
```
#### 程序自重启
利用os.execl方法实现程序自重启
```bash
import time
import sys
import os

def restart_program():
     python = sys.executable
     print "info:",os.execl(python, python, * sys.argv)
     #os.execl方法会代替自身进程，以达到自重启的目的。

if __name__ == "__main__":
     print 'start...'
     print u"3秒后,程序将结束...".encode("utf8")
     time.sleep(3)
     restart_program()
```

### 时间墙

@2017.04.19创建此文
@2017.04.24增加eval/exec函数
@2017.05.27增加程序操作、函数超时、函数出错重试
@2017.08.24增加format拼接字符串与变量、字符串推导



