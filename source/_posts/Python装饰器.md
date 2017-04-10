---
title: Python装饰器
date: 2017-04-07 10:31:53
comments: true
tags: 
- python
- 装饰器
categories: 编程之道
---
<blockquote class="blockquote-center">种一棵树最好的时间是十年前，其次是现在!</blockquote>
　　作为一个脚本小子，平日里写惯了脚本，不太习惯编写项目型的代码。然而报着提升代码质量、提高编码能力的态度，最近开始尝试学习一些编程高级用法，本章用于记录关于python装饰器的一些基础用法，欢迎纠错。
<!--more -->
　　装饰模式有很多经典的使用场景，例如插入日志、性能测试、事务处理等等，有了装饰器，就可以提取大量函数中与本身功能无关的类似代码，从而达到代码重用的目的。简单来说，装饰器的特点就是接收函数作为参数，然后返回函数。

### 入门
```bash
def log(func):
    def wrapper(*args, **kw):
        print 'call %s():' % func.__name__
        return func(*args, **kw)
    return wrapper
@log  #now = log(now)
def now():
    print '2013-12-25'
```
运行：
```bash
>>> now()
call now():
2013-12-25
```
执行流程说明：
>@log相当于now=log(now)，原来的now函数还在，只是现在now变量指向了新函数。因此当我们运行now()时，并不是运行now函数，而是运行log(now)返回的函数，即warpper函数。运行warpper函数后，会输出call....，然后执行func(*args,**kwargs)，而func就是传入的函数now，因此就是执行now函数，即now(*args,*kwargs),输入2013-12-25，从而达到了不必修改now函数，在执行now函数前输出内容。

### 进阶
```bash
#! -*- coding:utf-8 -*-

import functools

def log(*args):
     if len(args)>0:
          text=args[0]
     else:
          text=""
     def a(func):
          @functools.wraps(func)  #run函数属性赋值给b函数，如果不写，则最后run.__name__输出的应该是b，而不是run
          def b(*args,**kwargs):
               print "begin start",text #执行run函数前的输出
               func(*args,**kwargs)
               print "end"              #执行run函数后的输出
          return b
     return a

@log('nmask')  #or @log() 支持不定参数
def run(*args,**kwargs):  ##支持不定参数
     for i in args:
          print i

run(1,2,3)
print run.__name__  #run变量背后的函数名称

```
运行：
```bash
begin start nmask
1
2
3
end
run
```
log函数为装饰器函数，run函数为普通函数。
* @log相当于 run=log(run)
* @log()相当于 run=log()(run)
* @log(“test”)相当于run=log(“test”)(run)

执行流程说明：
>当执行run(1,2,3)函数时，实际先执行了log(’test')函数，返回了a， 然后继续执行a(run)，返回b函数，最后将b复制给run，执行run(1,2,3)，实际是执行b(1,2,3)，先输出begin start，然后执行run(1,2,3)（真正的run函数），输出 1,2,3，最后输出end。


参考：[装饰器|廖雪峰](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001386819879946007bbf6ad052463ab18034f0254bf355000#0) 推荐新手学习！
