---
title: 【玩转linux系列】shell编程
copyright: true
permalink: 1
top: 0
date: 2017-08-11 16:38:23
tags:
- linux
- shell
categories: 编程之道
password:
---
<blockquote class="blockquote-center">我猜你可能会问我为什么最近更新得这么勤？
因为我在充电！
</blockquote>
　　如果你去问程序员哪种编程语言最好用，可能会得到很多种答案。但如果问linux下哪种语言使用最方便，shell当之无愧，因为其相当于windows下的bat，可以自动化一些命令操作。当然linux内置安装了很多脚本语言，比如ruby、python等，使用也很方便。作为一名python爱好者，我一般习惯用python去解决问题，但为了能够看懂别人的shell代码，为此也需要学习一些基础的shell语法。
<!-- more -->
### shell变量
#### 定义变量
普通变量：
```bash
a="123"
b="test"
```
只读变量：
```bash
a="123"
readonly a
```
顾名思义，只读变量不能改变内容，否则会报如下错误
```bash
/bin/sh: NAME: This variable is read only.
```
#### 使用变量
```bash
echo {$a} 或者 echo $a
c=$a
```
只有在使用变量时，变量名前需要加$符号,{}可选当然最好使用。
#### 删除变量
```bash
unset a   # 不能删除只读变量
```

### shell数据结构
#### 字符串
```bash
str="123"
str='123'
```
* 单引号里的任何字符都会原样输出，单引号字符串中的变量是无效的
* 单引号字串中不能出现单引号（对单引号使用转义符后也不行）
* 双引号里可以有变量
* 双引号里可以出现转义字符

##### 字符串与字符串变量的拼接
```bash
Str_new="this is "$str""
```
或者
```bash
Str _new="this is {$str}"
```
##### 获取字符串长度
```bash
string="abcd"
echo ${#string} #输出4
```

##### 字符串切片
```bash
string="this is a test"
echo ${string:1:4} # 输出test
```

#### 数组
bash支持一维数组（不支持多维数组），并且没有限定数组的大小。
##### 定义数组
```bash
a=(1 2 3 4)   # 注意是空格隔开而不是逗号
```
或者
```bash
a[0]=1
a[1]=2
a[2]=3
a[3]=4
```
##### 读取数组
```bash
valuen=${array_name[n]} # 读取指定下标的元素
echo ${array_name[@]}  # 读取所有元素
```
##### 数组的长度
取得数组元素的个数
```bash
length=${#array_name[@]}
```
或者
```bash
length=${#array_name[*]}
```
取得数组单个元素的长度
```bash
lengthn=${#array_name[n]}
```

### shell输入输出重定向
#### echo
```bash
换行：echo -e "OK! \n"    #-e 开启转义
不换行：echo -e "OK! \c"   #-e 开启转义 \c 不换行
输出变量名：echo '$a' 输出$a    使用单引号即可
输出命令执行结果：echo `date`   使用反引号
```

#### printf
```bash
printf "%-10s %-8s %-4s\n"
printf "%-10s %-8s %-4.2f\n"
printf "%-10s %-8s %-4.2f\n"
printf "%-10s %-8s %-4.2f\n"
```
%s %c %d %f都是格式替代符%-10s指一个宽度为10个字符（-表示左对齐，没有则表示右对齐），任何字符都会被显示在10个字符宽的字符内，如果不足则自动以空格填充，超过也会将内容全部显示出来。%-4.2f指格式化为小数，其中.2指保留2位小数。

### shell传参
shell代码内容
```bash
#!/bin/bash
echo $0
echo $1
echo $2
```
运行脚本并传参
```bash
./shell.sh a b
```
输出结果
```bash
./shell.sh
a
b
```

#### 特殊参数
* $#    传递到脚本的参数个数
* $*    以一个单字符串显示所有向脚本传递的参数。
如"$*"用「"」括起来的情况、以"$1 $2 … $n"的形式输出所有参数。
* $$    脚本运行的当前进程ID号
* $!    后台运行的最后一个进程的ID号
* $@    与$*相同，但是使用时加引号，并在引号中返回每个参数。
如"$@"用「"」括起来的情况、以"$1" "$2" … "$n" 的形式输出所有参数。
* $-    显示Shell使用的当前选项，与set命令功能相同。
* $?    显示最后命令的退出状态。0表示没有错误，其他任何值表明有错误。

### shell函数
#### 基本格式
```bash
[ function ] funname [()]

{

    action;

    [return int;]

}
```
#### 函数定义
```bash
Test()
{

$a=“123”
return $a

}
```
#### 函数使用并获取返回值
```bash
Test
echo $?    # $?为函数返回值
```
#### 函数传参
```bash
#函数定义
Test()
{
echo $1
echo $2
echo $3
}

#函数使用
Test a b c
```

### shell流程控制

#### if条件语句
##### if-then-else-fi
```bash
if condition
then
    command1 
    command2
    ...
    commandN
else
    command
fi
```
##### if-then-elif-then-else-fi
```bash
if condition1
then
    command1
elif condition2 
then 
    command2
else
    commandN
fi
```

#### for循环语句
```bash
for var in item1 item2 ... itemN
do
    command1
    command2
    ...
    commandN
done
```

#### while循环语句
```bash
int=1
while(( $int<=5 ))
do
        echo $int
        let "int++"
done
```

### shell实战
```bash
#! /bin/bash

#shell综合运用

a=`whoami` #执行命令
b=`date`
c="open"
d=`cat test.log | grep $c`

echo $d
echo "user is $a time is $b"
```

### 参考文章
http://www.runoob.com/linux/linux-shell.html

### 传送门
[【玩转linux系统】Linux内网渗透](https://thief.one/2017/08/09/2/)
[【玩转linux系列】Vim使用](https://thief.one/2017/08/09/1/)
[【玩转linux系列】Linux基础命令](https://thief.one/2017/08/08/1/)

