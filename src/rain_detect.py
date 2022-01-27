#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import time
import datetime
import parameters as para
from sensing import Sensor 
from awsMQTTconnect import Com, Pub


sensor = Sensor()
com = Com()
pub = Pub()


def loop():
    rain_signal = 0 #Flag that identifies the presence or absence of rainfall by 1/0
    sub_t_count = 1 #Counter for pub every 10 minutes
    rain_count = 0 #A counter that triggers lambda at the start of rainfall
    rain_count_t0 = datetime.datetime(2020, 1, 1) #Initialization of rainfall time counter (dummy value)
    accum_rain = 0 #Accumulation counter for the number of rainfall detections

    while True:
        rain_signal, rain_count, accum_rain = sensor.count_rain(rain_count, accum_rain)
        sub_t_count, accum_rain = pub.publish_dashboard(sub_t_count, accum_rain)
        rain_count, rain_count_t0 = pub.publish_lambda(rain_count, rain_signal, rain_count_t0)
        time.sleep(0.5)


if __name__ == '__main__':
    try:
        time.sleep(90)

        #wifi接続確認とMQTT接続
        com.get_ssid()
        com.aws_connect()

        #メインループ実行
        loop()

    except KeyboardInterrupt:
        sys.exit()
