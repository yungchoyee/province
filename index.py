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
    openUrlFailCount = 0
    errorCount = 0
    startTime = 0
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
        print ("发生错误次数："+str(self.errorCount))

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
        url = self.baseUrl+url
        try:
            html = self.session.get(url)
            html.encoding = self.webCharset
            print ("打开网址成功：" + url)
            self.openUrlFailCount = 0
        except HTTPError:
            print('无法打开网页:' + url)
            self.openUrlFailCount += 1
        except ConnectionError:
            print('无法打开网址:' + url)
            self.openUrlFailCount += 1
        time.sleep(0.3)
        if self.openUrlFailCount < 10 and self.openUrlFailCount > 0:
            self.openUrl(url)
        elif self.openUrlFailCount > 10:
            return False
        else:
            bs = BeautifulSoup(html.text, self.explainFormat)
            return bs
    ##判断是不是特殊情况
    def isEspecial(self,name):
        return (name == "市辖区" or name == "县")
    ###第五页
    def FifthStep(self, url, parentId=0):
        bs = self.openUrl(url)
        if bs == False:
            print ("发生错误")
            self.errorCount += 1
            return
        villages = bs.find("tr", {"class": "villagehead"}).parent.find_all("td")
        regionType = 5
        for key,village in enumerate(villages):
            if (key + 1) %3 == 0 and key > 3:
                villageName = village.get_text()
                self.id += 1
                print (self.id,villageName)
                ##入库操作
                data = [str(self.id), str(parentId), str(regionType), villageName]
                self.insertMysql(data)
                time.sleep(0.3)
    ###第四页
    def FourthStep(self,url,parentId = 0):
        bs = self.openUrl(url)
        if bs == False:
            print ("发生错误")
            self.errorCount += 1
            return
        towns = bs.find("tr", {"class": "townhead"}).parent.find_all("a")
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
                    time.sleep(0.3)
                self.FifthStep(newUrl, self.id)
    ###第三页
    def ThirdStep(self,url,parentId = 0):
        bs = self.openUrl(url)
        if bs == False:
            print ("发生错误")
            self.errorCount += 1
            return
        areas = bs.find("tr", {"class": "countyhead"}).parent.find_all("a")
        regionType = 3
        for key,area in enumerate(areas):
            if key % 2 == 1:
                self.id += 1
                areaName = area.get_text()
                newUrl = "/".join(url.split("/")[:-1])
                newUrl = newUrl + "/" + area['href']
                print (self.id, areaName)
                if self.isEspecial(areaName) == False:
                    ##入库操作
                    data = [str(self.id), str(parentId), str(regionType), areaName]
                    self.insertMysql(data)
                self.FourthStep(newUrl,self.id)
    ##解析次页
    def secondStep(self,url,parentId = 0):
        bs = self.openUrl(url)
        if bs == False:
            print ("发生错误")
            self.errorCount += 1
            return
        citys = bs.find("tr",{"class":"cityhead"}).parent.find_all("a")
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
        bs = self.openUrl(url)
        if bs == False:
            print ("发生错误")
            self.errorCount += 1
            return
        provinces = bs.find("tr",{"class":"provincehead"}).parent.find_all("a")
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