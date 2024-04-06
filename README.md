# Nigel

This is the Nigel Repository, the pi counterpart of Jenson

Many of the files in this repository rely on pi specific libraries or hardware, and most of the rest are copies from Jenson.

In the src directory:

The Communication directory contains all the code relating to communication with the main system.
The broadcaster is used to send images captured to Jenson.
The mqtt file contains the code used for setting up the broker and a test topic.
The various other files were various attempts at setting communication over the months of this project.

The Models folder contains the Robot model for use of the various parameters.

The Motoring folder contains the code needed to control the robot.
The car_control file contains the controller to convert an action object into movement.
The car_test, motor_test and servo_test files are hardware tests.
The car_test contains a call to the broadcast file, allowing images to be captured at the same time as a
trajectory is executed for localisation.
The Node file contains an attempt to implement a ROS node, before this was found to not be viable.

The Utils folder containts the Action State and Trajectory Object definitions from Jenson.

The Trajectories Folder contains trajectories to be executed by the car, generated and copied across from Jenson.
This has not been included as it is removed by the gitignore on the Pi, however any trajectory converted to JSON
using the Trajectory's write_to_json method will work.
