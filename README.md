This is Oculus Robot auto move to collection data

How to start
------------
need to replug Arduino to usb port  

#### oepn oculus robot  
  
	# open_interface.sh do:
	# 1. open csi interface
	# 2. open oculus server	
	$ sudo ./open_interface.sh
	
	# start oculus robot
	$ python robot_controller.py [-c][-m] moveTime
	# -c imply whether to collection data
	# -m moveTime imply how many forward time for robot  
	
addition equipment
------------------

Arduino Uno  
Servo  
Ultrasonic sensor  
