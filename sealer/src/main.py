#!/usr/bin/env python
import rospy
import RPi.GPIO as GPIO  # import GPIO
import time
from std_msgs.msg import Int16, String
from std_srvs.srv import Trigger
GPIO.setmode(GPIO.BCM)

motor_pin_forw = 1
motor_pin_back = 2
uswitch_1_pin = 3
uswitch_2_pin = 4
sealer_pin = 5
cutter_pin = 6

seal_time = 3
cut_time = 2
move_time = 3

rospy.init_node("sealer")
pub_status = rospy.Publisher("status", String, queue_size=1)

GPIO.setup(motor_pin_forw, GPIO.OUT)
GPIO.setup(motor_pin_back, GPIO.OUT)
GPIO.setup(uswitch_1_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(uswitch_2_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

HIGH = GPIO.HIGH
LOW = GPIO.LOW

def seal_cut():
    rospy.loginfo("SEAL: Sealing")

    # Move sealers together
    GPIO.output(motor_pin_forw, HIGH)
    while GPIO.input(uswitch_1_pin) == HIGH and GPIO.input(uswitch_2_pin) == HIGH:
        time.sleep(0.01)
    GPIO.output(motor_pin_forw, LOW)

    # Sealing
    start_time = time.time()
    GPIO.output(sealer_pin, HIGH)
    while time.time() - start_time < seal_time:
        time.sleep(0.01)
    GPIO.output(sealer_pin, LOW)

    # Cutting
    start_time = time.time()
    GPIO.output(cutter_pin, HIGH)
    while time.time() - start_time < cut_time:
        time.sleep(0.01)
    GPIO.output(cutter_pin, LOW)

    # Move sealers away
    start_time = time.time()
    GPIO.output(motor_pin_back, HIGH)
    while time.time() - start_time < move_time:
        time.sleep(0.01)
    GPIO.output(motor_pin_back, LOW)


s = rospy.Service("startSeal", Trigger, seal_cut)
rospy.spin()