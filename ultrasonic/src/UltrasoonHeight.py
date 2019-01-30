#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Range
from std_msgs.msg import Int16

import tf

import array
import numpy as np
import time
import math
import RPi.GPIO as GPIO



# Class Measurement is from the hcsr04 sensor module for python.
class Measurement(object):
    '''Create a measurement using a HC-SR04 Ultrasonic Sensor connected to
    the GPIO pins of a Raspberry Pi.

    Metric values are used by default. For imperial values use
    unit='imperial'
    temperature=<Desired temperature in Fahrenheit>
    '''

    def __init__(self,
                 trig_pin,
                 echo_pin,
                 temperature=20,
                 round_to=1,
                 gpio_mode=GPIO.BCM
                 ):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        self.temperature = temperature
        self.round_to = round_to
        self.gpio_mode = gpio_mode

    def raw_distance(self, sample_size=11, sample_wait=0.1):
        """Return an error corrected unrounded distance, in cm, of an object
        adjusted for temperature in Celcius.  The distance calculated
        is the median value of a sample of `sample_size` readings.


        Speed of readings is a result of two variables.  The sample_size
        per reading and the sample_wait (interval between individual samples).

        Example: To use a sample size of 5 instead of 11 will increase the
        speed of your reading but could increase variance in readings;

        value = sensor.Measurement(trig_pin, echo_pin)
        r = value.raw_distance(sample_size=5)

        Adjusting the interval between individual samples can also
        increase the speed of the reading.  Increasing the speed will also
        increase CPU usage.  Setting it too low will cause errors.  A default
        of sample_wait=0.1 is a good balance between speed and minimizing
        CPU usage.  It is also a safe setting that should not cause errors.

        e.g.

        r = value.raw_distance(sample_wait=0.03)
        """
        speed_of_sound = 331.3 * math.sqrt(1 + (self.temperature / 273.15))
        sample = []
        # setup input/output pins
        GPIO.setwarnings(False)
        GPIO.setmode(self.gpio_mode)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

        for distance_reading in range(sample_size):
            GPIO.output(self.trig_pin, GPIO.LOW)
            rospy.sleep(sample_wait)
            GPIO.output(self.trig_pin, True)
            rospy.sleep(0.00001)
            GPIO.output(self.trig_pin, False)
            echo_status_counter = 1
            while GPIO.input(self.echo_pin) == 0:
                sonar_signal_off = time.time()
                echo_status_counter += 1
                if echo_status_counter > 100000:
                    #print('ja')
                    break
            while GPIO.input(self.echo_pin) == 1:
                sonar_signal_on = time.time()
            time_passed = sonar_signal_on - sonar_signal_off
            distance_cm = time_passed * ((speed_of_sound * 100) / 2)
            # print("distance_cm", distance_cm)
            if 0 < distance_cm and distance_cm < 1100:
                sample.append(distance_cm)
            else:
                sample.append(0)
            # print("sample", sample)
        sorted_sample = sorted(sample)
        new_sorted_sample = filter(lambda a: a != 0, sorted_sample)
        # Only cleanup the pins used to prevent clobbering
        # any others in use by the program
        GPIO.cleanup((self.trig_pin, self.echo_pin))


        return np.average(new_sorted_sample)

    def distance_metric(self, median_reading):
        '''Calculate the rounded metric distance, in cm's, from the sensor
        to an object'''
        return round(median_reading, self.round_to)


# GPIO pins for ultrasonic sensors
sonar_trig = [20, 21]
sonar_echo = [16, 17]

# Start ROS publisher and node
rospy.init_node('sonic', anonymous=True)
pub = rospy.Publisher('TrashHeight', Int16, queue_size=10)
rate = rospy.Rate(100)  # 1hz

# init
num_sensors = len(sonar_trig)
sonic = []
us = []
Total_height = 75 # in cm

# Make sensor objects
for i in range(0, num_sensors):
    sonic.append(Measurement(sonar_trig[i], sonar_echo[i]))

rospy.loginfo(sonic)

# Ros loop
while not rospy.is_shutdown():

    num_readings = 0
    us = []
    for i in range(0, num_sensors):
        try:
            # Read range from ultrasonic sensor, takes the mean of 3 readings
            distance = sonic[i].distance_metric(sonic[i].raw_distance(sample_size=5, sample_wait=0.1))
            print "distance sensor", i + 1, " :", distance
            us.append(distance)
        except SystemError:  # Set distance to 0 so that it gets ignored further on, but direction stays
            rospy.logwarn("No return") # When echo doesn't recive anything
            distance = 0
        except UnboundLocalError:
            rospy.logwarn("local variable 'sonar_signal_on' referenced before assignment") # Happens sometime...
            distance = 0
    average_dist = round(np.average(us), 2)


    if average_dist > 0:
        pub.publish(average_dist)
    else:
        average_dist = 0
        pub.publish(average_dist)
    print "Mean distance:", average_dist
    U_Capacity = round(average_dist / Total_height * 100, 1)  # result is Used Capacity in %
    print "Used Capacity:", 100 - U_Capacity, "%"
    print "=====================================:"

    rate.sleep()

