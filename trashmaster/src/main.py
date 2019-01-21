import rospy
import numpy

from std_msgs.msg import Bool, Int16, String
from std_srvs.srv import Trigger


def seal():
    if True:
        startSeal()
    return


def eject():
    if True:
        startEject()
    return


def capacity_check_height(data):
    if data.data > 70:
        rospy.loginfo("Full Capacity because of height")
        full()
    else:
        pub_full.publish(True)

    return


def capacity_check_weight(data):
    if data.data > 25:
        rospy.loginfo("Full Capacity because of weight")
        full()

def full():
    pub_status.publish("Full")
    pub_full.publish(True)

rospy.init_node("trash_master", anonymous=True)

pub_full = rospy.Publisher("Full", Bool, queue_size=1)
pub_status = rospy.Publisher("status", String, queue_size=1)

rospy.Subscriber("TrashHeight", Int16, capacity_check_height, callback_args="height")
rospy.Subscriber("TrashWeight", Int16, capacity_check_weight, callback_args="weight")

rs = rospy.Service('requestSeal', Trigger, seal)
re = rospy.Service("requestEject", Trigger, eject)

rospy.wait_for_service("startSeal")
rospy.wait_for_service("startEject")

startSeal = rospy.ServiceProxy("startSeal", Trigger)
startEject = rospy.ServiceProxy("startEject", Trigger)
