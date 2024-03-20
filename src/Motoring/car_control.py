#!/usr/bin/env python
# -*- coding: utf-8 -*-
from motor_utils import CarControl
import sys
import os

# add ../ to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from Models.robot import Robot
from Utils.action import Action
from Utils.trajectory import Trajectory


if __name__ == "__main__":
    car = Robot()
    car_control = CarControl(car)

    trajectory_file = os.path.join(os.path.dirname(__file__), "../control_0.json")

    trajectory = Trajectory.from_json(trajectory_file, car)

    for action in trajectory.actions:
        car_control.process_action(action)
        
    car_control.cleanup()
