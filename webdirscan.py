#!/usr/bin/env python
#-*- coding: utf-8 -*-

import re
import argparse
import requests
from termcolor import colored

# 版权区域

mycopyright = '''
*****************************************************

            Web目录扫描工具 - webdirscan.py
            作者：王松_Striker
            邮箱：song@secbox.cn
            团队：安全盒子团队[SecBox.CN]

*****************************************************
'''
print colored(mycopyright,'cyan')

# 命令行传值
parser = argparse.ArgumentParser()
parser.add_argument('website',help="Website for scan, eg: http://www.secbox.cn | www.secbox.cn",type=str)
args = parser.parse_args()

# 字典设置
webdic = 'dict/dict.txt'

# 对输入的网址进行处理
website = args.website
pattern = re.compile(r'^[http\:\/\/|https\:\/\/]')
res = pattern.match(website)

if not(res):
    website = 'http://' + website

# 请求头设置
headers = {
    'Accept': '*/*',
    'Referer': website,
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; ',
    'Cache-Control': 'no-cache',
}

# 字典存入数组
webdict = []

with open(webdic) as infile:
    while True:
        dirdic = infile.readline().strip()
        if(len(dirdic) == 0): break
        webdict.append(website+dirdic)

# 404页面分析,避免有的网站所有页面都返回200的情况
notfoundpage = requests.get(website+'/songgeshigedashuaibi/hello.html',allow_redirects=False)
notfoundpagetext = notfoundpage.text.replace('/songgeshigedashuaibi/hello.html','')

# 遍历扫描过程
for url in webdict:
    try:
        respon = requests.get(url, headers=headers,timeout=30,allow_redirects=False)
    except Exception,e:
        print e

    if(respon.status_code == 200 and respon.text != notfoundpagetext):
        print colored('['+str(respon.status_code)+']','green') + " " + url
