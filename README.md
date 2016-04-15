# 简介

Webdirscan.py是一个跨平台的多线程web目录扫描工具。

开发一个简单易用的web目录扫描工具是我很早以前的想法,

网上的确有很多web目录扫描器,但很多是win下的,

最近几年我一直在用ubuntu,想学习linux的知识,

甚至我的笔记本也装成了ubuntu(别问我为啥不用mac,穷!!!)

随后一直没有找到一款比较好用的web目录扫描工具,于是萌生了写这个工具的想法

*目前支持的功能*

 * 目录扫描(废话!)
 * 字典里面可用`# xxxx`来注释,方便字典分类
 * 多线程(可用`-t`参数设置线程,默认`20`线程)
 * 自动保存扫描结果

# 安装

## 1.克隆本项目

`git clone https://github.com/Strikersb/webdirscan.git`

## 2.安装requests模块

使用easy_install

`easy_install requests`

使用pip

`pip install requests`

## 3.安装完成

安装完成。

# 使用方法

直接运行程序会输出usage：

`usage: webdirscan.py [-h] [-w WEBSITE] [-d DICT] [-t THREADS_NUM] [-o OUTPUT]`

其中`-w`是必选参数代表需要扫描的网址,其余均为可选。

比如：

 * `python webdirscan.py -w www.secbox.cn` 扫描`www.secbox.cn`
 * `python webdirscan.py -w www.secbox.cn -t 60`设置`60`线程扫描
 * `python webdirscan.py -w www.secbox.cn -d dict/www.txt`设置使用`dict/www.txt`字典扫描
 * `python webdirscan.py -w www.secbox.cn -o anquanhezi.txt`将结果保存到`anquanhezi.txt`

当然以上参数可以灵活使用。

# 贡献代码/字典

欢迎各位大神贡献代码及字典

请在字典第一行加上注释,描述字典大概都包含什么。

比如：

```
# 常见目录
/index.htm
/index.html
/index.php
/index.asp
/index.acion
# 数据库目录
/data/data.mdb
/database/a.mdb
```

提交代码或字典均可先`fork`然后`pull requests`给我~

看到我会审核然后通过 :)

# 关于我

 * Author:王松_Striker
 * Team:安全盒子团队
 * QQ:954101430
 * Email:[song@secbox.cn](mailto:song@secbox.cn)
