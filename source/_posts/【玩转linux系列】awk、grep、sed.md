---
title: 【玩转linux系列】awk、grep、sed
copyright: true
permalink: 1
top: 0
date: 2017-08-12 10:41:19
tags:
- linux
categories: 技术研究
password:
---
<blockquote class="blockquote-center">Learn and live
活着，为了学习
</blockquote>
　　awk、grep、sed是linux操作文本的三大利器，也是必须掌握的linux命令之一。三者的功能都是处理文本，但侧重点各不相同，其中属awk功能最强大，但也最复杂。grep更适合单纯的查找或匹配文本，sed更适合编辑匹配到的文本，awk更适合格式化文本，对文本进行较复杂格式处理。
<!--more-->
以下所有实验输出，均以测试文件test.log内容为基准：
```bash
20170102 admin,password Open
20170801 nmask,nmask close
20180902 nm4k,test filter
```
### awk
AWK是一种处理文本文件的语言，是一个强大的文本分析工具;awk是以列为划分计数的，$0表示所有列，$1表示第一列，$2表示第二列。
#### awk参数
* -F 指定输入文件折分隔符，如-F:
* -v 赋值一个用户定义变量，如-va=1
* -f 从脚本文件中读取awk命令

注：只列举最常用的参数
#### 分隔符
每行按空格分割列，并输出第1、4列
```bash
$ awk '{print $1,$4}' test.log
或者
$ cat test.log | awk '{print $1,$4}'
```
#### 自定义分隔符
使用","进行分割，参数用-F
```bash
awk -F, '{print $1,$2}' test.log
```
使用多个分隔符，先使用空格分割，然后对分割结果再使用","分割
```bash
$ awk -F '[ ,]'  '{print $1,$2,$3}'  test.log  #注意逗号前面有一个空格
```
![](/upload_image/20170812/1.png)
#### 设置变量
设置awk自定义变量，用参数-v
例子：设置变量a为1
![](/upload_image/20170812/2.png)
注意：-v a之间要空格。

字符串拼接：（用""而不是+）
```bash
cat test.txt | awk -v a=\" '{print a""$0""a'
```

#### 逻辑判断
输出第一列为20170801的记录
![](/upload_image/20170812/3.png)

输出第二列不是nmask,nmask的记录
![](/upload_image/20170812/4.png)

#### 内建变量
NR参数：输出行号
![](/upload_image/20170812/5.png)

#### 正则表达式
输出第二列中包含nm开头的所有记录
![](/upload_image/20170812/6.png)
输出包含2017开头的记录
![](/upload_image/20170812/7.png)
注意：这里没有～，因为没有指定是哪一列

忽略大小写{INGORECASE=1}
![](/upload_image/20170812/8.png)
匹配取反 !~
![](/upload_image/20170812/9.png)

#### 内置函数
##### substr字符串截取
截取第一列的第一到第四个字符
![](/upload_image/20170812/10.png)

##### split切分字符串
以逗号分隔第2列的数据，并输出分别输出第2列的内容
![](/upload_image/20170812/11.png)

##### gsub替换
将第2列中的nmask替换成nMask
![](/upload_image/20170812/12.png)

### grep
Linux grep命令用于查找文件里符合条件的字符串。
#### Usage
递归查询
```bash
grep -r nmask /etc/  #查看/etc目录下内容包含nmask的文件 
```
查询取反
```bash
grep -v test  test.log
```

### sed
Linux sed命令是利用script来处理文本文件。
#### 参数
-e 以选项中指定的script来处理输入的文本文件。
-f 以选项中指定的script文件来处理输入的文本文件。
-h 显示帮助。
-n 仅显示script处理后的结果。
-V 显示版本信息。

#### 动作
a ：新增， a 的后面可以接字串，而这些字串会在下一行出现
i ：插入， i 的后面可以接字串，而这些字串会在上一行出现
c ：取代， c 的后面可以接字串，这些字串可以取代 n1,n2 之间的行
d ：删除
s ：取代，通常这个s的动作可以搭配正规表示法！如 s/old/new/g

#### 插入操作
在test.log文件的第4行后插入一行，内容为nmask
```bash
sed -e 4a\nmask test.log
```

#### 删除操作
删除test.log的第2行、第3行数据
```bash
cat test.log | sed '2,3d' 
```
匹配删除，删除行中有nmask字符串的
![](/upload_image/20170812/13.png)

#### 替换操作
```bash
sed 's/要被取代的字串/新的字串/g'
```


### 参考文章
http://www.runoob.com/linux/linux-comm-awk.html
