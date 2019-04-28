---
title: Python代码加密混淆
copyright: true
permalink: 1
top: 0
date: 2019-03-21 14:27:09
tags:
- python
categories: 编程之道
password:
---
<blockquote class="blockquote-center">我多想再见你
哪怕匆匆一眼就别离</blockquote>
　　python作为一种解释型语言，源代码加密本身比较困难。但有时候我们在发布一款python产品时又必须考虑到代码的加密性，以避免源代码泄露。为此，我查阅了一些资料，研究了几种python代码加密的常见方式，在此记录一下。
<!--more -->
## 源代码加密
### （一）py脚本编译成pyc二进制文件
编译命令：
```bash
python -m py_compile file.py
```
　　pyc文件是一个二进制文件，但是可以被很轻松的被逆向，在线反编译工具：`https://tool.lu/pyc/`。当然也有针对这个问题的解决方案，解决方案是可以通过修改python源代码中的opcode，然后重新编译py代码，可以一定程度上防止被逆向，因为逆向者需要知道被修改的opcode才能还原出来。如果使用私有的Bytecode指令集，那么通常的Python反汇编器和反编译器无法工作在由你私有Python编译器产生的pyc文件上，也相当于保护了你的Python代码。但是这么做的代价是你的Python应用只能在你的私有Python解释器上运行。（实际在发布一款产品时，并不适用）

### （二）py脚本打包成exe文件
　　exe文件针对windows平台使用，一般是使用打包程序（py2exe、PyInstaller等）打包成exe，这些工具用于将一个Python项目打包成单个可执行的文件，方便（在没有Python环境的机器上）使用。但通过压缩包可以方便地得到所有pyc文件或源文件，与C/C++编译生成的可执行文件有本质上的区别，基本上是零保护，所以需要将exe进行加壳操作。

### （三）py脚本编译成c文件（cython）
用cython将核心代码py模块文件转化成.c文件，再用gcc编译成so（unix）文件，或者将其编译成pyd（windows）文件。

编译过程：
1、服务器安装依赖
```bash
pip install python
yum install python-devel gcc
```
2、编写setup.py文件，内容如下：
```bash
from distutils.core import setup
from Cython.Build import cythonize
setup(
    ext_modules = cythonize("test.py",language_level=2)
)

# 批量编译
setup(
    ext_modules = cythonize(["test.py","test2.py".......],language_level=2)
)

```
3、运行以下命令
```bash
python setup.py build_ext —inplace
```
会生成一个test.so，删除其余文件，直接引用test.so即可（跟引用py文件一样）

## 源代码混淆
除了加密以外，还可以对源代码进行混淆，增加源代码的阅读难度。这个有很多第三方库，我列举几个：
https://pypi.org/project/pyminifier/
https://github.com/astrand/pyobfuscate
http://pyob.oxyry.com/

pyminifier库用法：
```bash
pyminifier -O test.py >> test_py.py
pyminifier --replacement-length=1 --obfuscate-builtins --obfuscate-import-methods --obfuscate-variables test.py
```