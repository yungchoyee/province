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
        self.cursor.execute("SELECT id,live_place FROM x_live_room WHERE province_id = 0 LIMIT 1")
        room = self.cursor.fetchone()

        if len(room) > 0:
            livePlace = room[1].split(" ")
            areaName = livePlace[2]
            self.cursor.execute("SELECT regionid,parentid FROM xcms_region WHERE region_name = %s",[areaName])
            area = self.cursor.fetchone()
            if len(area) > 0:
                area_id = area[0]
                city_id = area[1]
                self.cursor.execute("SELECT parentid,region_name FROM xcms_region WHERE regionid = %s", [str(city_id)])
                province = self.cursor.fetchone()
                province_id =  province[0]
                self.cursor.execute("UPDATE x_live_room SET province_id = %s,city_id = %s,area_id = %s WHERE  id = %s",[province_id,city_id,area_id,room[0]])
                self.conn.commit()
                print("成功，id："+str(room[0])+", live_place:"+room[1]+", province_id:"+str(province_id)+", city_id:"+str(city_id)+", area_id:"+str(area_id))



dbConfig = {
    "host":"81.68.71.30",
    "user":"root",
    "password":"tdsql-jrb88cto",
    "port":3306,
    "database":"shop",
    "charset":"utf8",
    "buffered":True,
}
handleData(dbConfig).updateRoomLivePlaceId()

