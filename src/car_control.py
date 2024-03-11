#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO 
from time import sleep
from adafruit_servokit import ServoKit


kit = ServoKit(channels=16)

GPIO.setmode(GPIO.BCM)
#Pins 18 22 24 GPIO 24 25 8
Motor1E = 18 #  Enable pin 1 of the controller IC
Motor1A = 24 #  Input 1 of the controller IC
Motor1B = 23 #  Input 2 of the controller IC


GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)

reverse=GPIO.PWM(Motor1A,100) # configuring Enable pin for PWM
forward=GPIO.PWM(Motor1B,100) # configuring Enable pin for PWM



