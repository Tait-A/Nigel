#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit
from time import sleep
import sys
import os

# add ../ to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from Models.robot import Robot
from Utils.action import Action


class CarControl(object):
    def __init__(self, car: Robot):

        GPIO.setmode(GPIO.BCM)
        # Pins 18 22 24 GPIO 24 25 8
        Motor1E = 18  #  Enable pin 1 of the controller IC
        Motor1A = 24  #  Input 1 of the controller IC
        Motor1B = 23  #  Input 2 of the controller IC

        GPIO.setup(Motor1A, GPIO.OUT)
        GPIO.setup(Motor1B, GPIO.OUT)
        GPIO.setup(Motor1E, GPIO.OUT)

        self.forwards = GPIO.PWM(Motor1A, 100)  # configuring Enable pin for PWM
        self.reverse = GPIO.PWM(Motor1B, 100)  # configuring Enable pin for PWM

        self.kit = ServoKit(channels=16)

        self.max_mp = 50

        self.car = car
        self.speed = 0
        self.motor_power = 0
        self.steering = self.set_steering(0)

    def set_steering(self, angle):
        def convert_angle(angle):
            # 0 is like -35 180 is like 35
            if angle > 35:
                return 180
            elif angle < -35:
                return 0
            return int((angle + 35) * 18 / 7)

        converted_angle = convert_angle(angle)
        self.kit.servo[0].angle = converted_angle
        return angle

    def set_speed(self, acceleration):

        self.speed = self.mp_to_speed()

        new_speed = self.speed + acceleration

        if new_speed > self.car.max_speed:
            new_speed = self.car.max_speed
            new_mp = min(100, self.max_mp)
        elif new_speed < 0:
            new_speed = 0
            new_mp = 0
        else:
            new_mp = min(self.speed_to_mp(new_speed), self.max_mp)

        self.speed = new_speed
        self.motor_power = new_mp
        self.forwards.ChangeDutyCycle(self.motor_power)

    def mp_to_speed(self, motor_power):
        return float((self.car.max_speed * motor_power) / 100)

    def speed_to_mp(self, speed):
        return float((speed * 100) / self.car.max_speed)

    def process_action(self, action: Action):
        if action.steering is not None:
            self.steering = self.set_steering(action.steering)
        if action.acceleration is not None:
            self.set_speed(action.acceleration)
        sleep(action.timestep)
