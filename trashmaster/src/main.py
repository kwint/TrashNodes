import rospy
import numpy

from std_msgs.msg import Bool, Int16, String
from std_srvs.srv import Trigger

def seal():
    pass
    return

def eject():
    pass
    return

def capacity_check(data, type):
    if (type == "height" and data.data > 70) or (type == "weight" and data.data > 25):
        print("full")
        pub_full.publish(True)
        pub_status.publish("Full")
    return

def request_in(data):
    if data.data == "seal" and True: # Add seal criteria
        pub_status.publish("Sealing")

    elif data.data == "eject" and True: # Add eject criteria
        pub_status.publish("Ejecting")


rospy.init_node("trash_master", anonymous=True)

pub_full = rospy.Publisher("Full", Bool, queue_size=1)
pub_status = rospy.Publisher("status", String, queue_size=1)

rospy.Subscriber("TrashHeight", Int16, capacity_check, callback_args="height")
rospy.Subscriber("TrashWeight", Int16, capacity_check, callback_args="weight")

rospy.Subscriber("Request", String, request_in)