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
        self.conn = mysql.connector.connect(**dbConfig)
        self.cursor = self.conn.cursor()
    def __del__(self):
        # self.conn.close()
        pass

    def updateRoomLivePlaceId(self):
        self.cursor.execute("SELECT live_place FROM x_live_room WHERE province_id = 0 LIMIT 1")
        livePlace = self.cursor.fetchone()

        if len(livePlace) > 0:
            livePlace = livePlace[0].split(" ")
            provinceName = livePlace[0]
            cityName = livePlace[1]
            areaName = livePlace[2]
            self.cursor.execute("SELECT regionid,parentid FROM xcms_region WHERE region_name = %s",[areaName])
            area = self.cursor.fetchone()
            if len(area) > 0:
                print(area[0])



dbConfig = {
    "host":"81.68.71.30",
    "user":"root",
    "password":"tdsql-jrb88cto",
    "port":3306,
    "database":"shop",
    "charset":"utf8",
}
handleData(dbConfig).updateRoomLivePlaceId()

