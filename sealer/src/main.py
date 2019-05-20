#!/usr/bin/env python
import rospy
from std_msgs.msg import Int16, String
from std_srvs.srv import Trigger, TriggerResponse

import mraa
import time

HEAT_ON = 0
HEAT_OFF = 1

sealer_pin = 18
cutter_pin = 29

seal_time = 60
cut_time = 15
move_time = 6

rospy.init_node("sealer")

# Export the GPIO pin for use
sealer = mraa.Gpio(sealer_pin)
cutter = mraa.Gpio(cutter_pin)

time.sleep(0.1) # short wait is needed for mraa

# Configure the pin direction and set pin to high directly, otherwise it would warm up
sealer.dir(mraa.DIR_OUT)
sealer.write(HEAT_OFF)
cutter.dir(mraa.DIR_OUT)
cutter.write(HEAT_OFF)

pub_status = rospy.Publisher("status", String, queue_size=1)

rospy.wait_for_service("/seal_act/closeSeal")
rospy.wait_for_service("/seal_act/openSeal")

closeSeal = rospy.ServiceProxy("/seal_act/closeSeal", Trigger)
openSeal = rospy.ServiceProxy("/seal_act/openSeal", Trigger)

def seal_cut(request):
    rospy.loginfo("SEAL: Closing sealer")

    # Move sealers together
    closeSeal()

    time.sleep(1)

    # Sealing
    rospy.loginfo("SEAL: Sealing")
    start_time = time.time()
    sealer.write(HEAT_ON)
    while time.time() - start_time < seal_time:
        time.sleep(0.01)
    sealer.write(HEAT_OFF)

    # Cutting
    rospy.loginfo("SEAL: Cutting")
    start_time = time.time()
    cutter.write(HEAT_ON)
    while time.time() - start_time < cut_time:
        time.sleep(0.01)

    # Move sealers away
    openSeal()

    # shut down heater after opening so plastic doesnt stick
    cutter.write(HEAT_OFF)

    rospy.loginfo("SEAL: Sealing done")
    return TriggerResponse(success=True, message=" ")


s = rospy.Service("startSeal", Trigger, seal_cut)
rospy.spin()

rospy.logwarn("Heat elements will warm up in 10 sec because seal node is terminated")
time.sleep(10)



