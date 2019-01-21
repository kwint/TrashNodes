#!/usr/bin/env python
# import RPi.GPIO as GPIO
from std_srvs.srv import Trigger
import rospy
# PINS = [20]

# GPIO.setmode(GPIO.BCM)

# for pin in PINS:
#     GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

rospy.init_node('lightbridge', anonymous=True)
rospy.wait_for_service("TrownIn")
rolly_update = rospy.ServiceProxy("TrownIn", Trigger)
rate = rospy.Rate(50)

while not rospy.is_shutdown():
    trash = input("Geef getal: ")
    print("komt ie")
    rolly_update()
    rate.sleep()

