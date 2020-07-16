#/usr/bin/python
# -*- coding:utf8 -*

import mysql.connector
import time


class handleData:
    conn = ""
    def __init__(self,dbConfig):
        print('正在执行，请稍等....')
        print('当前时间：' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        self.startTime = time.time()
        self.conn = mysql.connector.connect(user=dbConfig["user"], password=dbConfig["password"], database=dbConfig["shop"])
        self.cursor = self.conn.cursor()
    def __del__(self):
        self.conn.close()

    def updateRoomLivePlaceId(self,roomId):
        self.cursor.execute("")
