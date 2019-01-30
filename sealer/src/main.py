#!/usr/bin/env python
import rospy
import RPi.GPIO as GPIO  # import GPIO
import time
from std_msgs.msg import Int16, String
from std_srvs.srv import Trigger, TriggerResponse
GPIO.setmode(GPIO.BCM)

motor_pin_open = 9 # open
motor_pin_close = 11
uswitch_1_pin = 24
# uswitch_2_pin = 25
sealer_pin = 3
cutter_pin = 22

seal_time = 25
cut_time = 15
move_time = 6

rospy.init_node("sealer")
pub_status = rospy.Publisher("status", String, queue_size=1)

GPIO.setup(motor_pin_open, GPIO.OUT)
GPIO.setup(motor_pin_close, GPIO.OUT)
GPIO.setup(uswitch_1_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(cutter_pin, GPIO.OUT)
GPIO.setup(sealer_pin, GPIO.OUT)

HIGH = GPIO.HIGH
LOW = GPIO.LOW
GPIO.output(motor_pin_open, LOW)
GPIO.output(motor_pin_close, LOW)

def seal_cut(request):
    rospy.loginfo("SEAL: Closing sealer")

    # Move sealers together
    GPIO.output(motor_pin_open, HIGH)
    while not GPIO.input(uswitch_1_pin) == HIGH:
        time.sleep(0.01)
    time.sleep(0.25)
    GPIO.output(motor_pin_open, LOW)

    time.sleep(1)
    # Sealing
    rospy.loginfo("SEAL: Sealing")
    start_time = time.time()
    GPIO.output(sealer_pin, HIGH)
    while time.time() - start_time < seal_time:
        time.sleep(0.01)
    GPIO.output(sealer_pin, LOW)

    # Cutting
    rospy.loginfo("SEAL: Cutting")
    start_time = time.time()
    GPIO.output(cutter_pin, HIGH)
    while time.time() - start_time < cut_time:
        time.sleep(0.01)
    GPIO.output(cutter_pin, LOW)

    # Move sealers away
    start_time = time.time()
    GPIO.output(motor_pin_close, HIGH)
    while time.time() - start_time < move_time:
        time.sleep(0.01)
    GPIO.output(motor_pin_close, LOW)
    rospy.loginfo("SEAL: Sealing done")
    return TriggerResponse(success=True, message=" ")


s = rospy.Service("startSeal", Trigger, seal_cut)
rospy.spin()