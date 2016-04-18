#!/usr/bin/env python
#-*- coding: utf-8 -*-

import re
import sys
import argparse
import requests
import threading
import Queue

# 版权区域

mycopyright = '''
*****************************************************

            ToolName: Webdirscan.py
            Author :  Striker
            Email :   song@secbox.cn
            Team :    SecBox.CN

 Simple Usage: python webdirscan.py -w www.secbox.cn

*****************************************************
'''
print mycopyright

class Dirscan(object):
    def __init__(self, website, dic, threads_num, output):
        print 'Scan starting...'
        self.website = website
        self.dic = dic
        self.threads_num = threads_num
        self.output = website.replace('https://', '').replace('http://', '') + '.txt'
        self._loadDict()
        self._formatWebsite()
        self._loadHeaders()
        self._analysis404()
        self.lock = threading.Lock()

    def _formatWebsite(self):
        pattern = re.compile(r'^[http\:\/\/|https\:\/\/]')
        res = pattern.match(self.website)

        if not res:
            self.website = 'http://' + self.website

    def _analysis404(self):
        notfoundpage = requests.get(self.website + '/songgeshigedashuaibi/hello.html', allow_redirects=False)
        self.notfoundpagetext = notfoundpage.text.replace('/songgeshigedashuaibi/hello.html', '')

    def _loadDict(self):
        self.urllist = Queue.Queue()
        with open(self.dic) as infile:
            for line in infile.readlines():
                if line.find('#') == -1 and line != '':
                    self.urllist.put(line.strip())

    def _loadHeaders(self):
        self.headers = {
            'Accept': '*/*',
            'Referer': self.website,
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; ',
            'Cache-Control': 'no-cache',
        }

    def _scan(self):
        url = self.website + self.urllist.get()
        try:
            respon = requests.get(url, headers=self.headers, timeout=60, allow_redirects=False)
        except Exception, e:
            print e

        if respon.status_code == 200 and respon.text != self.notfoundpagetext:
            print '[' + str(respon.status_code) + ']' + " " + url
            self.lock.acquire()
            with open(self.output, 'a') as infile:
                infile.write(url + '\n')
            self.lock.release()
        self.urllist.task_done()

    def run(self):
        for i in range(self.threads_num):
            t = threading.Thread(target=self._scan, name=str(i))
            t.setDaemon(True)
            t.start()

if __name__ == '__main__':
    # 命令行传值
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--website', help="Website for scan, eg: http://www.secbox.cn | www.secbox.cn", type=str)
    parser.add_argument('-d', '--dict', default="dict/dict.txt", help="Dict for scan, eg: url.txt | ./secbox_url.txt", type=str)
    parser.add_argument('-t', '--threads', dest="threads_num", default=20, help="Threads num for scan eg: 50 | 100", type=int)
    parser.add_argument('-o', '--output', help="Result of the webdirscan output", type=str)
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_usage()
        sys.exit()

    d = Dirscan(args.website, args.dict, args.threads_num, args.output)
    d.run()

    # 判断线程如果全部结束就退出程序
    while True:
        if threading.activeCount() <= 1:
            break

    print 'Scan End!'
