#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time
import Queue
import argparse
import requests
import threading

class Dirscan(object):

    def __init__(self, scanSite, scanDict, scanOutput,threadNum):
        print 'Dirscan is running!'
        self.scanSite = scanSite if scanSite.find('://') != -1 else 'http://%s' % scanSite
        print 'Scan target:',self.scanSite
        self.scanDict = scanDict
        self.scanOutput = scanSite.rstrip('/').replace('https://', '').replace('http://', '')+'.txt' if scanOutput == 0 else scanOutput
        truncate = open(self.scanOutput,'w')
        truncate.close()
        self.threadNum = threadNum
        self.lock = threading.Lock()
        self._loadHeaders()
        self._loadDict(self.scanDict)
        self._analysis404()
        self.STOP_ME = False

    def _loadDict(self, dict_list):
        self.q = Queue.Queue()
        with open(dict_list) as f:
            for line in f:
                if line[0:1] != '#':
                    self.q.put(line.strip())
        if self.q.qsize() > 0:
            print 'Total Dictionary:',self.q.qsize()
        else:
            print 'Dict is Null ???'
            quit()

    def _loadHeaders(self):
        self.headers = {
            'Accept': '*/*',
            'Referer': 'http://www.baidu.com',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; ',
            'Cache-Control': 'no-cache',
        }
    def _analysis404(self):
        notFoundPage = requests.get(self.scanSite + '/songgeshigedashuaibi/hello.html', allow_redirects=False)
        self.notFoundPageText = notFoundPage.text.replace('/songgeshigedashuaibi/hello.html', '')

    def _writeOutput(self, result):
        self.lock.acquire()
        with open(self.scanOutput, 'a+') as f:
            f.write(result + '\n')
        self.lock.release()

    def _scan(self, url):
        html_result = 0
        try:
            html_result = requests.get(url, headers=self.headers, allow_redirects=False, timeout=60)
        except requests.exceptions.ConnectionError:
            # print 'Request Timeout:%s' % url
            pass
        finally:
            if html_result != 0:
                if html_result.status_code == 200 and html_result.text != self.notFoundPageText:
                    print '[%i]%s' % (html_result.status_code, html_result.url)
                    self._writeOutput('[%i]%s' % (html_result.status_code, html_result.url))


    def run(self):
        while not self.q.empty() and self.STOP_ME == False:
            url = self.scanSite + self.q.get()
            self._scan(url)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('scanSite', help="The website to be scanned", type=str)
    parser.add_argument('-d', '--dict', dest="scanDict", help="Dictionary for scanning", type=str, default="dict/dict.txt")
    parser.add_argument('-o', '--output', dest="scanOutput", help="Results saved files", type=str, default=0)
    parser.add_argument('-t', '--thread', dest="threadNum", help="Number of threads running the program", type=int, default=60)
    args = parser.parse_args()

    scan = Dirscan(args.scanSite, args.scanDict, args.scanOutput, args.threadNum)

    for i in range(args.threadNum):
        t = threading.Thread(target=scan.run)
        t.setDaemon(True)
        t.start()

    while True:
        if threading.activeCount() <= 1 :
            break
        else:
            try:
                time.sleep(0.1)
            except KeyboardInterrupt, e:
                print '\n[WARNING] User aborted, wait all slave threads to exit, current(%i)' % threading.activeCount()
                scan.STOP_ME = True

    print 'Scan end!!!'