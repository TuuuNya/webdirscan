# 简介

`webdirscan`是一个炒鸡简单的多线程Web目录扫描工具。

# 安装

使用Python语言编写

第三方模块只用了`requests`,所以`clone`以后只需要安装`requests`模块即可。

```
git clone https://github.com/Strikersb/webdirscan.git
pip install requests
```

安装完成。

# 使用方法

```
usage: webdirscan.py [-h] [-d SCANDICT] [-o SCANOUTPUT] [-t THREADNUM]
                     scanSite

positional arguments:
  scanSite              The website to be scanned

optional arguments:
  -h, --help            show this help message and exit
  -d SCANDICT, --dict SCANDICT
                        Dictionary for scanning
  -o SCANOUTPUT, --output SCANOUTPUT
                        Results saved files
  -t THREADNUM, --thread THREADNUM
                        Number of threads running the program
```

# 关于我

 * Author:王松_Striker
 * Team:安全盒子团队
 * QQ:954101430
 * Email:[song@secbox.cn](mailto:song@secbox.cn)
