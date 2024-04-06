#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import subprocess

# add ../ to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from Models.robot import Robot
from Utils.action import Action
from Utils.trajectory import Trajectory
from Motoring.car_control import CarControl


def run_trajectory(car, trajectory):

    for action in trajectory.actions:
        car_control.process_action(action)
        car_control.process_action(action)
    car_control.cleanup()


if __name__ == "__main__":
    car = Robot()
    car_control = CarControl(car)

    trajectory_file = os.path.join(os.path.dirname(__file__), "../Trajectories/linear_traj.json")

    trajectory = Trajectory.from_json(trajectory_file, car)

    # start send_video() as a subprocess
    path = os.path.join(os.path.dirname(__file__), "../Communication/")
    process = subprocess.Popen(["python", path + "broadcaster.py"])

    run_trajectory(car, trajectory)
