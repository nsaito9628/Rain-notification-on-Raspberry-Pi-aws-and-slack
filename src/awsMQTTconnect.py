#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import ssl
import time
import datetime 
import subprocess
import paho.mqtt.client as mqtt
import parameters as para


class Com:
    def __init__(self):
        self.client = para.client
        self.cacert = para.CACERT
        self.clientCert = para.CLIENTCERT
        self.clientKey = para.CLIENTKEY
        self.host = para.HOST
        self.port = para.PORT
    

    #Callback function when mqtt connection is successful
    def on_connect(self, client, userdata, flags, respons_code):
        #If the connection cannot be established, reboot after 90 seconds of waiting time for terminal access
        if respons_code != 0:
            print("respons_code:", respons_code, " flags:", flags)
            time.sleep(90)
            subprocess.call(["sudo","reboot"])
        print('Connected')


    #Function to determine the establishment of wifi connection
    def get_ssid(self):
        cmd = 'iwconfig wlan0|grep ESSID'
        r = subprocess.run(cmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)\
            .stdout.decode().rstrip()
        idx = r.find('ESSID:')
        #If the connection cannot be established, reboot after 90 seconds of waiting time for terminal access
        if r[idx + 7:-1] == "ff/an":
            print("ESSID:", r[idx + 7:-1])
            time.sleep(90)
            subprocess.call(["sudo","reboot"])


    #Function that launches an MQTT client and creates an object instance
    def aws_connect(self):
        try:
            # certifications
            self.client.tls_set(
                self.cacert,
                certfile=self.clientCert,
                keyfile=self.clientKey,
                tls_version=ssl.PROTOCOL_TLSv1_2)
            self.client.tls_insecure_set(True)

            # callback
            self.client.on_connect = self.on_connect
            #client.on_disconnect = on_disconnect

            # port, keepalive
            self.client.connect(self.host, self.port, keepalive=60)

            self.client.loop_start()

        except KeyboardInterrupt:
            time.sleep(90)
            subprocess.call(["sudo","reboot"])


class Pub:
    def __init__(self):
        self.client = para.client
        self.topic_lambda = para.TOPIC_LAMBDA
        self.topic_dashboard = para.TOPIC_DASHBOARD
        self.rain_detect = {}
        self.lambda_trigger = {}


    def publish_dashboard(self, sub_t_count,accum_rain):

        t = time.localtime()
        sub_t_sec = str(t.tm_min/10)

        if (sub_t_sec[-1]!='0'): sub_t_count = 1

        if (sub_t_sec[-1]=='0' and sub_t_count!=0):
            self.rain_detect['Timestamp'] = int(time.time())
            self.rain_detect['datetime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')#get datetime to string
            self.rain_detect['rain_drop'] = accum_rain
            print(self.rain_detect)
            self.client.publish(self.topic_dashboard, json.dumps(self.rain_detect, default=self.json_serial))  # publish
            accum_rain = 0
            sub_t_count = 0

        if (sub_t_sec[-1]=='0') and (sub_t_count==0):
            sub_t_count = sub_t_count

        return sub_t_count, accum_rain


    #雨が降り始めたらIoT core -> lambdaにtriggerを入れる
    def publish_lambda(self, rain_count,rain_signal,rain_count_t0):

        dt = datetime.datetime.now() - rain_count_t0
        #print(dt)

        if (rain_signal == 1) and (rain_count == 0) and (dt.total_seconds() > 300):
            self.lambda_trigger['Timestamp'] = int(time.time())
            self.lambda_trigger['datetime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')#get datetime to string
            self.lambda_trigger['trigger'] = 1
            print(self.lambda_trigger)
            self.client.publish(self.topic_lambda, json.dumps(self.lambda_trigger, default=self.json_serial))  # publish
            rain_count = 1
            rain_count_t0 = datetime.datetime.now()

        return rain_count, rain_count_t0


    def json_serial(self, para):
        return para.isoformat()