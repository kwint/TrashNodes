#!/usr/bin/env python
import rospy
import numpy

from std_msgs.msg import Bool, Int16, String
from std_srvs.srv import Trigger, TriggerResponse

def seal(request):
    startSeal()

    #     return TriggerResponse(success=True, message=" ")
    # else:
    #     return TriggerResponse(success=False, message=" ")



def eject(request):
    if True:
        startEject()
    return


def capacity_check_height(data):
    if data.data < 20:
        rospy.loginfo("Full Capacity because of height")
        full()
    else:
        pub_full.publish(False)

    return


def capacity_check_weight(data):
    if data.data > 2000:
        rospy.loginfo("Full Capacity because of weight")
        full()

def full():
    pub_status.publish("Full")
    pub_full.publish(True)


rospy.init_node("trash_master", anonymous=True)

pub_full = rospy.Publisher("Full", Bool, queue_size=1)
pub_status = rospy.Publisher("status", String, queue_size=1)

# rospy.Subscriber("TrashHeight", Int16, capacity_check_height)
rospy.Subscriber("TrashWeight", Int16, capacity_check_weight)

rs = rospy.Service('requestSeal', Trigger, seal)
re = rospy.Service("requestEject", Trigger, eject)

rospy.wait_for_service("startSeal")
rospy.wait_for_service("startEject")

startSeal = rospy.ServiceProxy("startSeal", Trigger)
startEject = rospy.ServiceProxy("startEject", Trigger)
rospy.spin()
