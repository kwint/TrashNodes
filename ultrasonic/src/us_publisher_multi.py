#!/usr/bin/env python
import rospy

from std_msgs.msg import Int32
from random import randint

import RPi.GPIO as GPIO
import time
import signal
import sys

# use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
pinTrigger_M = 17
pinEcho_M = 20
pinTrigger_L= 27
pinEcho_L = 21
pinTrigger_R = 22
pinEcho_R = 16


def close(signal, frame):
        print("\nTurning off ultrasonic distance detection...\n")
        GPIO.cleanup()
        sys.exit(0)

signal.signal(signal.SIGINT, close)

# set GPIO input and output channels
GPIO.setup(pinTrigger_L, GPIO.OUT)
GPIO.setup(pinEcho_L, GPIO.IN)
GPIO.setup(pinTrigger_M, GPIO.OUT)
GPIO.setup(pinEcho_M, GPIO.IN)
GPIO.setup(pinTrigger_R, GPIO.OUT)
GPIO.setup(pinEcho_R, GPIO.IN)
def ultrasoon():

        while True:
                #Ultrasoon Links
                # set Trigger to HIGH
                GPIO.output(pinTrigger_L, True)
                # set Trigger after 0.01ms to LOW
                time.sleep(0.00001)
                GPIO.output(pinTrigger_L, False)

                startTime_L = time.time()
                stopTime_L = time.time()

                startTime = time.time()
                # save start time
                while 0 == GPIO.input(pinEcho_L):
                        startTime_L= time.time()
                        
                stopTime = time.time()
                # save time of arrival
                while 1 == GPIO.input(pinEcho_L):
                        stopTime_L = time.time()
                #==================================#        
               #Ultrasoon Midden
               # set Trigger to HIGH
                GPIO.output(pinTrigger_M, True)
                # set Trigger after 0.01ms to LOW
                time.sleep(0.00001)
                GPIO.output(pinTrigger_M, False)

                startTime_M = time.time()
                stopTime_M = time.time()

                startTime_M = time.time()
                # save start time
                while 0 == GPIO.input(pinEcho_M):
                        startTime_M = time.time()
                        
                stopTime_M = time.time()
                # save time of arrival
                while 1 == GPIO.input(pinEcho_M):
                        stopTime_M = time.time()
                #==================================#
                #Ultrasoon Midden
               # set Trigger to HIGH
                GPIO.output(pinTrigger_R, True)
                # set Trigger after 0.01ms to LOW
                time.sleep(0.00001)
                GPIO.output(pinTrigger_R, False)

                startTime_R = time.time()
                stopTime_R = time.time()

                startTime_R = time.time()
                # save start time
                while 0 == GPIO.input(pinEcho_R):
                        startTime_R = time.time()
                        
                stopTime_R = time.time()
                # save time of arrival
                while 1 == GPIO.input(pinEcho_R):
                        stopTime_R = time.time()
                #==================================#
                # time difference between start and arrival
                TimeElapsed_L = stopTime_L - startTime_L
                TimeElapsed_M = stopTime_M - startTime_M
                TimeElapsed_R = stopTime_R - startTime_R
                # multiply with the sonic speed (34300 cm/s)
                # and divide by 2, because there and back
                distance_L = (TimeElapsed_L * 34300) / 2
                distance_M = (TimeElapsed_M * 34300) / 2
                distance_R = (TimeElapsed_R * 34300) / 2
                distance_mean = (distance_L+distance_M+distance_R)/3
                print ("Distance Links: %.1f cm; Distance Midden: %.1f cm; Distance Rechts: %.1f cm" % (distance_L, distance_M, distance_R))
                print ("Mean Distance : %.1f cm" % distance_mean)
                return distance_L, distance_M, distance_R, distance_mean

if __name__=='__main__':
    rospy.init_node('ultrasoon_node')
    pub=rospy.Publisher('sensoren', Int32, queue_size=10)
    rate= rospy.Rate(10)

    while not rospy.is_shutdown():
        dist_L,dist_M, dist_R,dist_mean= ultrasoon()
        pub.publish(dist_L )
        pub.publish(dist_M )
        pub.publish(dist_R)
        pub.publish(dist_mean )

rate.sleep()
                                                                        
