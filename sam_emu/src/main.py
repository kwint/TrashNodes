import rospy
import numpy

from std_msgs.msg import Bool, Int16, String
from std_srvs.srv import Trigger

def print_data(data):
    print(data.data)

rospy.wait_for_service('requestSeal')
rospy.wait_for_service('requestEject')

rospy.loginfo("SAM connected with module")

requestSeal = rospy.ServiceProxy('requestSeal', Trigger)
requestEject = rospy.ServiceProxy('requestEject', Trigger)
rospy.Subscriber("status", String, print_data)

while not rospy.is_shutdown():
    action = input("requestSeal or requestEject:")
    if action == "requestSeal":
        print(requestSeal)
    if action == "requestEject":
        print(requestEject)
