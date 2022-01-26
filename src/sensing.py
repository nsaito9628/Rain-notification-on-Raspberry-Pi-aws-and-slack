#!/usr/bin/python
# -*- coding: utf-8 -*-
#import wiringpi as pi
import RPi.GPIO as GPIO
import time
import parameters as para


class Sensor:
    def __init__(self):
        self.rain_pin = para.RAIN_PIN #ダストセンサー：GPIO 15
        self.sensor_no = para.SENSOR_NO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.rain_pin, GPIO.IN)
    #センサーのHI/LOを1/0で、カウンター積算判定して積算、出力する


    def detect_rain(self):
        sig = 0

        if self.sensor_no == 1:
            if GPIO.input(self.rain_pin) == GPIO.HIGH:
                sig = 0
            else:
                sig = 1
        elif self.sensor_no == 0:
            if GPIO.input(self.rain_pin) == GPIO.HIGH:
                sig = 1
            else:
                sig = 0

        return sig


    def count_rain(self, rain_count, accum_rain):

        sig = self.detect_rain()

        if sig == 1:
            rain_signal = 0
            rain_count = 0
            accum_rain = accum_rain
        elif sig == 0:
            rain_signal = 1
            rain_count = rain_count
            accum_rain += 1
        #print("rain_signal: ", rain_signal, "rain_count: ", rain_count, "accum_rain: ",accum_rain)

        return rain_signal, rain_count, accum_rain
