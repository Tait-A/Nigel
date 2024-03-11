import RPi.GPIO as GPIO
import time
from adafruit_servokit import ServoKit


kit = ServoKit(channels=16)

kit.servo[0].angle = 180

time.sleep(1)

kit.servo[0].angle = 30

time.sleep(1)

kit.servo[0].angle = 90