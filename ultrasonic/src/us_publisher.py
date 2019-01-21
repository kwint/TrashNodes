#!/usr/bin/env python
import rospy

from std_msgs.msg import Int32
from random import randint

import RPi.GPIO as GPIO
import time
import signal
import sys
import time
# use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
#pinTrigger = 17
#pinEcho = 20
pinTrigger = 21
pinEcho = 16

def close(signal, frame):
        print("\nTurning off ultrasonic distance detection...\n")
        GPIO.cleanup()
        sys.exit(0)

signal.signal(signal.SIGINT, close)

# set GPIO input and output channels
GPIO.setup(pinTrigger, GPIO.OUT)
GPIO.setup(pinEcho, GPIO.IN)


def ultrasoon():


        while True:
                # set Trigger to HIGH
                GPIO.output(pinTrigger, True)
                # set Trigger after 0.01ms to LOW
                time.sleep(0.00001)
                GPIO.output(pinTrigger, False)
                lol = 1
                counter = 1
                startTime = time.time()
                while GPIO.input(pinEcho) == 0:
                    startTime = time.time()
                    lol+=1
                    if (lol > 10000):
                        print('ja')
                        break
                    # print("1 keer")

                stopTime = time.time()
                # save time of arrival
                while GPIO.input(pinEcho) == 1:
                        stopTime = time.time()

                print("na time")
                # time difference between start and arrival
                TimeElapsed = stopTime - startTime
                # multiply with the sonic speed (34300 cm/s)
                # and divide by 2, because there and back
                distance = (TimeElapsed * 34300) / 2

                print ("Distance: %.1f cm" % distance)
                return distance

if __name__=='__main__':
    rospy.init_node('ultrasoon_node')
    pub=rospy.Publisher('sensoren', Int32, queue_size=10)
    rate= rospy.Rate(5)

    while not rospy.is_shutdown():
        dist = ultrasoon()
        pub.publish(dist)

rate.sleep()
