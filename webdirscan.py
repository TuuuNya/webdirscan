#!/usr/bin/env python
#-*- coding: utf-8 -*-

import re
import argparse
import requests

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
    'Connection': 'Keep-Alive',
    'Cache-Control': 'no-cache',
}

# 字典存入数组
webdict = []

with open(webdic) as infile:
    while True:
        dirdic = infile.readline().strip()
        if(len(dirdic) == 0): break
        webdict.append(website+dirdic)


for url in webdict:
    try:
        respon = requests.get(url, headers=headers,timeout=30)
    except Exception,e:
        print e

    if(respon.status_code == 200):
        print '['+str(respon.status_code)+']' + ":" + url

