#!/usr/bin/env python
import RPi.GPIO as GPIO
from std_msgs.msg import Bool
import rospy
PINS = [20, 21]

GPIO.setmode(GPIO.BCM)

for pin in PINS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

pub = rospy.Publisher('trashTrownIn', Bool, queue_size=1)
rospy.init_node('lightbridge', anonymous=True)
rate = rospy.Rate(50)

while not rospy.is_shutdown():
    if GPIO.input(PINS[0]) or GPIO.input(PINS[1]):
        detected = True

    else:
        detected = False

    rospy.loginfo(detected)
    pub.publish(detected)
    rate.sleep()


