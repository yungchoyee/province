#!/usr/bin/python
# coding=utf-8
import time

from bs4 import BeautifulSoup
import requests
from urllib.error import HTTPError
from urllib.error import URLError
import sys
import mysql.connector


class Province(object):
    #统计局首页网址
    baseUrl = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/"
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
        self.conn = mysql.connector.connect(user='root', password='123456', database='test')
        self.cursor = self.conn.cursor()
    def __del__(self):
        self.conn.close()
        print('执行完毕。。。')
        print('执行完毕，共找到' + str(self.id) + '条数据')
        print('开始时间:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.startTime)))
        endTime = time.time()
        print('结束时间:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(endTime)))

        ###插入一条记录到数据库
    def insertMysql(self,data):
        self.cursor.execute('insert into region (region_id,parent_id,region_type,name) values (%s,%s,%s,%s)', data)
        if self.cursor.rowcount > 0:
            print("插入数据库成功,region_id:"+data[0]+",parent_id:"+data[1]+",region_type:"+data[2]+",name:"+data[3])
        else:
            print("插入数据库失败,region_id:" + data[0] + ",parent_id:" + data[1] + ",region_type:" + data[2] + ",name:" + data[3])
        self.conn.commit()

        ###打开网址
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
    ##判断是不是特殊情况
    def isEspecial(self,name):
        return (name == "市辖区" or name == "县")
    ###第五页
    def FifthStep(self, url, parentId=0):
        time.sleep(0.4)
        bs = self.openUrl(url)
        try:
            villages = bs.find("tr", {"class": "villagehead"}).parent.find_all("td")
        except:
            time.sleep(20)
            self.FifthStep(url,parentId)
            return
        regionType = 5
        for key,village in enumerate(villages):
            if (key + 1) %3 == 0 and key > 3:
                villageName = village.get_text()
                self.id += 1
                print (self.id,villageName)
                ##入库操作
                data = [str(self.id), str(parentId), str(regionType), villageName]
                self.insertMysql(data)
    ###第四页
    def FourthStep(self,url,parentId = 0):
        time.sleep(0.4)
        bs = self.openUrl(url)
        try:
            towns = bs.find("tr", {"class": "townhead"}).parent.find_all("a")
        except:
            time.sleep(20)
            self.FourthStep(url,parentId)
            return
        regionType = 4
        for key, town in enumerate(towns):
            if key % 2 == 1:
                self.id += 1
                townName = town.get_text()
                newUrl = "/".join(url.split("/")[:-1])
                newUrl = newUrl + "/"+town['href']
                if self.isEspecial(townName) == False:
                    print(self.id, townName)
                    ##入库操作
                    data = [str(self.id), str(parentId), str(regionType), townName]
                    self.insertMysql(data)
                self.FifthStep(newUrl, self.id)
    ###第三页
    def ThirdStep(self,url,parentId = 0):
        time.sleep(0.4)
        bs = self.openUrl(url)
        try:
            areas = bs.find("tr", {"class": "countyhead"}).parent.find_all("a")
        except:
            time.sleep(20)
            self.ThirdStep(url,parentId)
            return
        regionType = 3
        for key,area in enumerate(areas):
            if key % 2 == 1:
                self.id += 1
                areaName = area.get_text()
                # newUrl = "/".join(url.split("/")[:-1])
                # newUrl = newUrl + "/" + area['href']
                print (self.id, areaName)
                if self.isEspecial(areaName) == False:
                    ##入库操作
                    data = [str(self.id), str(parentId), str(regionType), areaName]
                    self.insertMysql(data)
                # self.FourthStep(newUrl,self.id)
    ##解析次页
    def secondStep(self,url,parentId = 0):
        time.sleep(0.4)
        bs = self.openUrl(url)
        try:
            citys = bs.find("tr",{"class":"cityhead"}).parent.find_all("a")
        except:
            time.sleep(20)
            self.secondStep(url,parentId)
            return
        regionType = 2
        for key,city in enumerate(citys):
            if key %2 == 1:
                cityName = city.get_text()
                newUrl = city['href']
                if self.isEspecial(cityName) == False:
                    self.id += 1
                    print(self.id, cityName)
                    ##入库操作
                    data = [str(self.id), str(parentId), str(regionType), cityName]
                    self.insertMysql(data)
                self.ThirdStep(newUrl,self.id)
    ###解析首页
    def firstStep(self,url,parentId = 0):
        time.sleep(0.4)
        bs = self.openUrl(url)
        try:
            provinces = bs.find("tr",{"class":"provincehead"}).parent.find_all("a")
        except:
            time.sleep(20)
            self.firstStep(url,parentId)
            return
        regionType = 1  #行政级别
        for province in provinces:
            self.id += 1
            provinceName = province.get_text()
            newUrl = province['href']
            data = [str(self.id),str(parentId),str(regionType),provinceName]
            print(self.id, provinceName)
            self.insertMysql(data)
            self.secondStep(newUrl,self.id)
            ##入库操作


a = Province().firstStep("index.html")