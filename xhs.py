#!/usr/bin/python
# coding=utf-8
import time

from bs4 import BeautifulSoup
import requests
from urllib.error import HTTPError
from urllib.error import URLError
import sys


class Province(object):
    #统计局首页网址
    baseUrl = "https://www.xiaohongshu.com/explore?m_source=baidusem"
    webCharset = "GB2312"
    explainFormat = "html.parser"
    cursor  = ""
    conn  = ""
    id = 0
    session = ""
    regionType = 0
    startTime = 0
    ##设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.36 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'AD_RS_COOKIE=20080919',
        'Host': 'www.stats.gov.cn',
        'Pragma': 'no-cache',
        'Referer': 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/11/01/110105.html',
        'Upgrade-Insecure-Requests': '1'
    }
    def __init__(self):
        print('正在执行，请稍等....')
        print ('当前时间：' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        self.startTime = time.time()
        self.session = requests.Session()
    def openUrl(self,url):
        global html
        newUrl = self.baseUrl+url
        try:
            html = self.session.get(newUrl)
            html.encoding = self.webCharset
            print ("打开网址成功：" + newUrl)
        except HTTPError:
            print('无法打开网页:' + newUrl)
        except ConnectionError:
            print('无法打开网址:' + newUrl)
        return BeautifulSoup(html.text, self.explainFormat)
    ###解析首页
    def firstStep(self,url,parentId = 0):
        time.sleep(0.4)
        bs = self.openUrl(url)
        try:
            provinces = bs
            print(provinces)
        except:
            print(2222)
            return


a = Province().firstStep("")