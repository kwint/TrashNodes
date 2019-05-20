#!/usr/bin/env python
from upm import pyupm_hx711 as hxlib
import time
import numpy as np
import rospy
from std_msgs.msg import Int16


lc = hxlib.HX711(36, 38)

tare_64 = 8878251.4
tare_32 = 8457386.4

scale_64 = 0.0044286979627989375
scale_32 = 0.0130718954248366

times = 10

rospy.init_node("loadcells", anonymous=True)
pub = rospy.Publisher("TrashWeight", Int16, queue_size=1)
# rate = rospy.Rate(0.25)

def getAvg(lc, tare, scale, times):
    data = np.array([])
    for i in range(0, times):
        data = np.append(data, lc.read())

    # print("data", data)
    data = data.mean()

    # print("mean", data)

    data = data - tare

    weight = data * scale

    return weight




while not rospy.is_shutdown():
    lc.setGain(64)
    # time.sleep(1)
    weight_64 = getAvg(lc, tare_64, scale_64, times)

    lc.setGain(32)
    # time.sleep(1)
    weight_32 = getAvg(lc, tare_32, scale_32, times)

    weight = weight_32 + weight_64

    pub.publish(weight)
    rospy.logdebug(weight)


    # rate.sleep()


#end